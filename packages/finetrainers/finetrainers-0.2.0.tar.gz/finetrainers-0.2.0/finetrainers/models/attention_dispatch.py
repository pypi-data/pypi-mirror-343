import contextlib
import inspect
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

import torch
from diffusers.utils.import_utils import OptionalDependencyNotAvailable

# Since we will be patching the `scaled_dot_product_attention` function with `attention_dispatch` to take
# control for dispatching to different attention providers, we need to import the original function
# to be able to use it and not go into infinite recursion when the dispatcher calls `scaled_dot_product_attention`.
from torch.nn.functional import scaled_dot_product_attention as native_sdpa

from finetrainers.constants import FINETRAINERS_ATTN_CHECKS, FINETRAINERS_ATTN_PROVIDER
from finetrainers.logging import get_logger
from finetrainers.utils.import_utils import (
    is_flash_attn_available,
    is_flash_attn_version,
    is_sageattention_available,
    is_sageattention_version,
    is_torch_version,
    is_xformers_available,
    is_xformers_version,
)


if is_flash_attn_available():
    if is_flash_attn_version("<", "2.6.3"):
        raise OptionalDependencyNotAvailable(
            "The `flash-attn` library version is too old. Please update it to at least 2.6.3."
        )

    from flash_attn import flash_attn_func, flash_attn_varlen_func
else:
    flash_attn_func = None
    flash_attn_varlen_func = None


if is_sageattention_available():
    if is_sageattention_version("<", "2.1.1"):
        raise OptionalDependencyNotAvailable(
            "The `sageattention` library version is too old. Please update it to at least 2.1.1."
        )

    from sageattention import (
        sageattn,
        sageattn_qk_int8_pv_fp8_cuda,
        sageattn_qk_int8_pv_fp8_cuda_sm90,
        sageattn_qk_int8_pv_fp16_cuda,
        sageattn_qk_int8_pv_fp16_triton,
        sageattn_varlen,
    )
else:
    sageattn = None
    sageattn_qk_int8_pv_fp16_cuda = None
    sageattn_qk_int8_pv_fp16_triton = None
    sageattn_qk_int8_pv_fp8_cuda = None
    sageattn_qk_int8_pv_fp8_cuda_sm90 = None
    sageattn_varlen = None


if is_torch_version(">=", "2.5.0"):
    import torch.nn.attention.flex_attention as flex_attention


if is_xformers_available():
    if is_xformers_version("<", "0.0.29"):
        raise OptionalDependencyNotAvailable(
            "The `xformers` library version is too old. Please update it to at least 0.0.29."
        )

    import xformers.ops as xops
else:
    xops = None


logger = get_logger()

_SAGE_ATTENTION_PV_ACCUM_DTYPE = Literal["fp32", "fp32+fp32"]
_SAGE_ATTENTION_QK_QUANT_GRAN = Literal["per_thread", "per_warp"]
_SAGE_ATTENTION_QUANTIZATION_BACKEND = Literal["cuda", "triton"]


class AttentionProvider(str, Enum):
    # EAGER = "eager"

    # `flash-attn`
    FLASH = "flash"
    FLASH_VARLEN = "flash_varlen"

    # PyTorch native
    FLEX = "flex"
    NATIVE = "native"
    _NATIVE_CUDNN = "_native_cudnn"
    _NATIVE_EFFICIENT = "_native_efficient"
    _NATIVE_FLASH = "_native_flash"
    _NATIVE_MATH = "_native_math"

    # `sageattention`
    SAGE = "sage"
    SAGE_VARLEN = "sage_varlen"
    _SAGE_QK_INT8_PV_FP8_CUDA = "_sage_qk_int8_pv_fp8_cuda"
    _SAGE_QK_INT8_PV_FP8_CUDA_SM90 = "_sage_qk_int8_pv_fp8_cuda_sm90"
    _SAGE_QK_INT8_PV_FP16_CUDA = "_sage_qk_int8_pv_fp16_cuda"
    _SAGE_QK_INT8_PV_FP16_TRITON = "_sage_qk_int8_pv_fp16_triton"
    # TODO: let's not add support for Sparge Attention now because it requires tuning per model
    # We can look into supporting something "autotune"-ing in the future
    # SPARGE = "sparge"

    # `xformers`
    XFORMERS = "xformers"


class _AttentionProviderRegistry:
    _providers = {}
    _constraints = {}
    _supported_arg_names = {}
    _active_provider = AttentionProvider(FINETRAINERS_ATTN_PROVIDER)
    _checks_enabled = FINETRAINERS_ATTN_CHECKS

    @classmethod
    def register(cls, provider: AttentionProvider, constraints: Optional[List[Callable]] = None):
        logger.debug(f"Registering attention provider: {provider}")

        def decorator(func):
            cls._providers[provider] = func
            cls._constraints[provider] = constraints or []
            cls._supported_arg_names[provider] = set(inspect.signature(func).parameters.keys())
            return func

        return decorator

    @classmethod
    def get_active_provider(cls):
        return cls._active_provider, cls._providers[cls._active_provider]

    @classmethod
    def list_providers(cls):
        return list(cls._providers.keys())


@contextlib.contextmanager
def attention_provider(provider: AttentionProvider = AttentionProvider.NATIVE):
    """Context manager to set the active attention provider."""
    if provider not in _AttentionProviderRegistry._providers:
        raise ValueError(f"Provider {provider} is not registered.")

    old_provider = _AttentionProviderRegistry._active_provider
    _AttentionProviderRegistry._active_provider = provider

    try:
        yield
    finally:
        _AttentionProviderRegistry._active_provider = old_provider


def attention_dispatch(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
    attention_kwargs: Optional[Dict[str, Any]] = None,
) -> torch.Tensor:
    attention_kwargs = attention_kwargs or {}
    provider_name, provider_fn = _AttentionProviderRegistry.get_active_provider()
    kwargs = {
        "query": query,
        "key": key,
        "value": value,
        "attn_mask": attn_mask,
        "dropout_p": dropout_p,
        "is_causal": is_causal,
        "scale": scale,
        "enable_gqa": enable_gqa,
        **attention_kwargs,
    }

    if _AttentionProviderRegistry._checks_enabled:
        removed_kwargs = set(kwargs) - set(_AttentionProviderRegistry._supported_arg_names[provider_name])
        if removed_kwargs:
            log_freq = 512
            msg = (
                f"Removing unsupported arguments for attention provider {provider_name}: {removed_kwargs}. This "
                f"message will be logged every {log_freq} calls."
            )
            logger.log_freq("WARNING", "REMOVING_ATTN_UNSUPPORTED_KWARGS", msg, log_freq)
        for check in _AttentionProviderRegistry._constraints.get(provider_name):
            check(**kwargs)

    kwargs = {k: v for k, v in kwargs.items() if k in _AttentionProviderRegistry._supported_arg_names[provider_name]}
    return provider_fn(**kwargs)


def _check_attn_mask_is_none(attn_mask: Optional[torch.Tensor], **kwargs) -> None:
    if attn_mask is not None:
        raise ValueError("Attention mask must be None for this provider.")


def _check_attn_mask_or_causal(attn_mask: Optional[torch.Tensor], is_causal: bool, **kwargs) -> None:
    if attn_mask is not None and is_causal:
        raise ValueError("`is_causal` cannot be True when `attn_mask` is not None.")


def _check_device(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, **kwargs) -> None:
    if query.device != key.device or query.device != value.device:
        raise ValueError("Query, key, and value must be on the same device.")
    if query.dtype != key.dtype or query.dtype != value.dtype:
        raise ValueError("Query, key, and value must have the same dtype.")


def _check_device_cuda(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, **kwargs) -> None:
    _check_device(query, key, value)
    if query.device.type != "cuda":
        raise ValueError("Query, key, and value must be on a CUDA device.")


def _check_device_cuda_atleast_smXY(major: int, minor: int) -> Callable:
    def check_device_cuda(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, **kwargs) -> None:
        _check_device_cuda(query, key, value)
        if torch.cuda.get_device_capability(query.device) < (major, minor):
            raise ValueError(
                f"Query, key, and value must be on a CUDA device with compute capability >= {major}.{minor}."
            )

    return check_device_cuda


def _check_qkv_dtype_match(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, **kwargs) -> None:
    if query.dtype != key.dtype:
        raise ValueError("Query and key must have the same dtype.")
    if query.dtype != value.dtype:
        raise ValueError("Query and value must have the same dtype.")


def _check_qkv_dtype_bf16_or_fp16(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, **kwargs) -> None:
    _check_qkv_dtype_match(query, key, value)
    if query.dtype not in (torch.bfloat16, torch.float16):
        raise ValueError("Query, key, and value must be either bfloat16 or float16.")


def _check_shape(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    **kwargs,
) -> None:
    if query.shape[-1] != key.shape[-1]:
        raise ValueError("Query and key must have the same last dimension.")
    if query.shape[-2] != value.shape[-2]:
        raise ValueError("Query and value must have the same second to last dimension.")
    if attn_mask is not None and attn_mask.shape[-1] != key.shape[-2]:
        raise ValueError("Attention mask must match the key's second to last dimension.")


def _prepare_for_flash_attn_or_sage_varlen(
    batch_size: int,
    seq_len_q: int,
    seq_len_kv: int,
    attn_mask: Optional[torch.Tensor] = None,
    device: Optional[torch.device] = None,
) -> None:
    seqlens_q = torch.full((batch_size,), seq_len_q, dtype=torch.int32, device=device)
    if attn_mask is None:
        seqlens_k = torch.full((batch_size,), seq_len_kv, dtype=torch.int32, device=device)
    else:
        seqlens_k = attn_mask.sum(dim=1, dtype=torch.int32)
    cu_seqlens_q = torch.zeros(batch_size + 1, dtype=torch.int32, device=device)
    cu_seqlens_k = torch.zeros(batch_size + 1, dtype=torch.int32, device=device)
    cu_seqlens_q[1:] = torch.cumsum(seqlens_q, dim=0)
    cu_seqlens_k[1:] = torch.cumsum(seqlens_k, dim=0)
    max_seqlen_q = seqlens_q.max().item()
    max_seqlen_k = seqlens_k.max().item()
    return (seqlens_q, seqlens_k), (cu_seqlens_q, cu_seqlens_k), (max_seqlen_q, max_seqlen_k)


def _normalize_attn_mask(attn_mask: torch.Tensor, batch_size: int, seq_len_k: int) -> torch.Tensor:
    """
    Normalize an attention mask to shape [batch_size, seq_len_k] (bool) suitable for inferring seqlens_k in
    FlashAttention/Sage varlen.

    Supports 1D to 4D shapes and common broadcasting patterns.
    """
    if attn_mask.dtype != torch.bool:
        raise ValueError(f"Attention mask must be of type bool, got {attn_mask.dtype}.")

    if attn_mask.ndim == 1:
        # [seq_len_k] -> broadcast across batch
        attn_mask = attn_mask.unsqueeze(0).expand(batch_size, seq_len_k)

    elif attn_mask.ndim == 2:
        # [batch_size, seq_len_k]. Maybe broadcast across batch
        if attn_mask.size(0) not in [1, batch_size]:
            raise ValueError(
                f"attn_mask.shape[0] ({attn_mask.shape[0]}) must be 1 or {batch_size} for 2D attention mask."
            )
        attn_mask = attn_mask.expand(batch_size, seq_len_k)

    elif attn_mask.ndim == 3:
        # [batch_size, seq_len_q, seq_len_k] -> reduce over query dimension
        if attn_mask.size(0) not in [1, batch_size]:
            raise ValueError(
                f"attn_mask.shape[0] ({attn_mask.shape[0]}) must be 1 or {batch_size} for 3D attention mask."
            )
        attn_mask = attn_mask.any(dim=1)
        attn_mask = attn_mask.expand(batch_size, seq_len_k)

    elif attn_mask.ndim == 4:
        # [batch_size, num_heads, seq_len_q, seq_len_k] or broadcastable versions
        if attn_mask.size(0) not in [1, batch_size]:
            raise ValueError(
                f"attn_mask.shape[0] ({attn_mask.shape[0]}) must be 1 or {batch_size} for 4D attention mask."
            )
        attn_mask = attn_mask.expand(batch_size, -1, -1, seq_len_k)  # [B, H, Q, K]
        attn_mask = attn_mask.any(dim=(1, 2))  # [B, K]

    else:
        raise ValueError(f"Unsupported attention mask shape: {attn_mask.shape}")

    if attn_mask.shape != (batch_size, seq_len_k):
        raise ValueError(
            f"Normalized attention mask shape mismatch: got {attn_mask.shape}, expected ({batch_size}, {seq_len_k})"
        )

    return attn_mask


def _flex_attention_causal_mask_mod(batch_idx, head_idx, q_idx, kv_idx):
    return q_idx >= kv_idx


@_AttentionProviderRegistry.register(
    AttentionProvider.FLASH,
    constraints=[_check_attn_mask_is_none, _check_device, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _flash_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    dropout_p: float = 0.0,
    scale: Optional[float] = None,
    is_causal: bool = False,
    window_size: Tuple[int, int] = (-1, -1),
    softcap: float = 0.0,
    alibi_slopes: Optional[torch.Tensor] = None,
    deterministic: bool = False,
    return_attn_probs: bool = False,
    attn_mask: Optional[torch.Tensor] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    if enable_gqa:
        # TODO
        pass

    query, key, value = (x.permute(0, 2, 1, 3) for x in (query, key, value))

    out = flash_attn_func(
        q=query,
        k=key,
        v=value,
        dropout_p=dropout_p,
        softmax_scale=scale,
        causal=is_causal,
        window_size=window_size,
        softcap=softcap,
        alibi_slopes=alibi_slopes,
        deterministic=deterministic,
        return_attn_probs=return_attn_probs,
    )
    out = out.permute(0, 2, 1, 3)
    return out


@_AttentionProviderRegistry.register(
    AttentionProvider.FLASH_VARLEN,
    constraints=[_check_device, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _flash_varlen_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    cu_seqlens_q: Optional[torch.Tensor] = None,
    cu_seqlens_k: Optional[torch.Tensor] = None,
    max_seqlen_q: Optional[int] = None,
    max_seqlen_k: Optional[int] = None,
    dropout_p: float = 0.0,
    scale: Optional[float] = None,
    is_causal: bool = False,
    window_size: Tuple[int, int] = (-1, -1),
    softcap: float = 0.0,
    alibi_slopes: Optional[torch.Tensor] = None,
    deterministic: bool = False,
    return_attn_probs: bool = False,
    attn_mask: Optional[torch.Tensor] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    batch_size, _, seq_len_q, _ = query.shape
    _, _, seq_len_kv, _ = key.shape

    if attn_mask is not None:
        attn_mask = _normalize_attn_mask(attn_mask, batch_size, seq_len_kv)

    if enable_gqa:
        # TODO
        pass

    if any(x is None for x in (cu_seqlens_q, cu_seqlens_k, max_seqlen_q, max_seqlen_k)):
        (_, seqlens_k), (cu_seqlens_q, cu_seqlens_k), (max_seqlen_q, max_seqlen_k) = (
            _prepare_for_flash_attn_or_sage_varlen(
                batch_size, seq_len_q, seq_len_kv, attn_mask=attn_mask, device=query.device
            )
        )
    else:
        seqlens_k = torch.full((batch_size,), max_seqlen_k, dtype=torch.int32, device=query.device)
        cu_seqlens_q = cu_seqlens_q.to(dtype=torch.int32, device=query.device)
        cu_seqlens_k = cu_seqlens_k.to(dtype=torch.int32, device=query.device)

    query, key, value = (x.permute(0, 2, 1, 3) for x in (query, key, value))

    key_valid, value_valid = [], []
    for b in range(batch_size):
        valid_len = seqlens_k[b]
        key_valid.append(key[b, :valid_len])
        value_valid.append(value[b, :valid_len])

    query_packed = query.flatten(0, 1)
    key_packed = torch.cat(key_valid, dim=0)
    value_packed = torch.cat(value_valid, dim=0)

    out = flash_attn_varlen_func(
        q=query_packed,
        k=key_packed,
        v=value_packed,
        cu_seqlens_q=cu_seqlens_q,
        cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max_seqlen_q,
        max_seqlen_k=max_seqlen_k,
        dropout_p=dropout_p,
        softmax_scale=scale,
        causal=is_causal,
        window_size=window_size,
        softcap=softcap,
        alibi_slopes=alibi_slopes,
        deterministic=deterministic,
        return_attn_probs=return_attn_probs,
    )
    out = out.unflatten(0, (batch_size, -1)).permute(0, 2, 1, 3)  # .contiguous()

    return out


@_AttentionProviderRegistry.register(
    AttentionProvider.FLEX,
    constraints=[_check_attn_mask_or_causal, _check_device, _check_shape],
)
def _native_flex_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[Union[torch.Tensor, "flex_attention.BlockMask"]] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
    return_lse: bool = False,
    kernel_options: Optional[Dict[str, Any]] = None,
) -> torch.Tensor:
    # TODO: should we LRU cache the block mask creation?
    score_mod = None
    block_mask = None
    batch_size, num_heads, seq_len_q, _ = query.shape
    _, _, seq_len_kv, _ = key.shape

    if attn_mask is None or isinstance(attn_mask, flex_attention.BlockMask):
        block_mask = attn_mask
    elif is_causal:
        block_mask = flex_attention.create_block_mask(
            _flex_attention_causal_mask_mod, None, None, seq_len_q, seq_len_kv, query.device
        )
    elif torch.is_tensor(attn_mask):
        if attn_mask.ndim == 2:
            attn_mask = attn_mask.view(attn_mask.size(0), 1, attn_mask.size(1), 1)

        attn_mask = attn_mask.expand(batch_size, num_heads, seq_len_q, seq_len_kv)

        if attn_mask.dtype == torch.bool:
            # TODO: this probably does not work but verify!
            def mask_mod(batch_idx, head_idx, q_idx, kv_idx):
                return attn_mask[batch_idx, head_idx, q_idx, kv_idx]

            block_mask = flex_attention.create_block_mask(
                mask_mod, batch_size, None, seq_len_q, seq_len_kv, query.device
            )
        else:

            def score_mod(score, batch_idx, head_idx, q_idx, kv_idx):
                return score + attn_mask[batch_idx, head_idx, q_idx, kv_idx]
    else:
        raise ValueError("Attention mask must be either None, a BlockMask, or a 2D/4D tensor.")

    return flex_attention.flex_attention(
        query=query,
        key=key,
        value=value,
        score_mod=score_mod,
        block_mask=block_mask,
        scale=scale,
        enable_gqa=enable_gqa,
        return_lse=return_lse,
        kernel_options=None,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider.NATIVE,
    constraints=[_check_device, _check_shape],
)
def _native_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    return native_sdpa(
        query=query,
        key=key,
        value=value,
        attn_mask=attn_mask,
        dropout_p=dropout_p,
        is_causal=is_causal,
        scale=scale,
        enable_gqa=enable_gqa,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider._NATIVE_CUDNN,
    constraints=[_check_device, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _native_cudnn_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    with torch.nn.attention.sdpa_kernel(torch.nn.attention.SDPBackend.CUDNN_ATTENTION):
        return native_sdpa(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
            enable_gqa=enable_gqa,
        )


@_AttentionProviderRegistry.register(
    AttentionProvider._NATIVE_EFFICIENT,
    constraints=[_check_device, _check_shape],
)
def _native_efficient_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    with torch.nn.attention.sdpa_kernel(torch.nn.attention.SDPBackend.EFFICIENT_ATTENTION):
        return native_sdpa(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
            enable_gqa=enable_gqa,
        )


@_AttentionProviderRegistry.register(
    AttentionProvider._NATIVE_FLASH,
    constraints=[_check_attn_mask_is_none, _check_device, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _native_flash_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    with torch.nn.attention.sdpa_kernel(torch.nn.attention.SDPBackend.FLASH_ATTENTION):
        return native_sdpa(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
            enable_gqa=enable_gqa,
        )


@_AttentionProviderRegistry.register(
    AttentionProvider._NATIVE_MATH,
    constraints=[_check_device, _check_shape],
)
def _native_math_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    with torch.nn.attention.sdpa_kernel(torch.nn.attention.SDPBackend.MATH):
        return native_sdpa(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
            enable_gqa=enable_gqa,
        )


@_AttentionProviderRegistry.register(
    AttentionProvider.SAGE,
    constraints=[_check_device_cuda, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _sage_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    is_causal: bool = False,
    scale: Optional[float] = None,
    return_lse: bool = False,
) -> torch.Tensor:
    return sageattn(
        q=query,
        k=key,
        v=value,
        tensor_layout="HND",
        is_causal=is_causal,
        sm_scale=scale,
        return_lse=return_lse,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider.SAGE_VARLEN,
    constraints=[_check_device_cuda, _check_qkv_dtype_bf16_or_fp16, _check_shape],
)
def _sage_varlen_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    cu_seqlens_q: Optional[torch.Tensor] = None,
    cu_seqlens_k: Optional[torch.Tensor] = None,
    max_seqlen_q: Optional[int] = None,
    max_seqlen_k: Optional[int] = None,
    is_causal: bool = False,
    scale: Optional[float] = None,
    smooth_k: bool = True,
    attn_mask: Optional[torch.Tensor] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    batch_size, _, seq_len_q, _ = query.shape
    _, _, seq_len_kv, _ = key.shape

    if attn_mask is not None:
        attn_mask = _normalize_attn_mask(attn_mask, batch_size, seq_len_kv)

    if enable_gqa:
        # TODO
        pass

    if any(x is None for x in (cu_seqlens_q, cu_seqlens_k, max_seqlen_q, max_seqlen_k)):
        (_, seqlens_k), (cu_seqlens_q, cu_seqlens_k), (max_seqlen_q, max_seqlen_k) = (
            _prepare_for_flash_attn_or_sage_varlen(
                batch_size, seq_len_q, seq_len_kv, attn_mask=attn_mask, device=query.device
            )
        )
    else:
        seqlens_k = torch.full((batch_size,), max_seqlen_k, dtype=torch.int32, device=query.device)
        cu_seqlens_q = cu_seqlens_q.to(dtype=torch.int32, device=query.device)
        cu_seqlens_k = cu_seqlens_k.to(dtype=torch.int32, device=query.device)

    query, key, value = (x.permute(0, 2, 1, 3) for x in (query, key, value))

    key_valid, value_valid = [], []
    for b in range(batch_size):
        valid_len = seqlens_k[b]
        key_valid.append(key[b, :valid_len])
        value_valid.append(value[b, :valid_len])

    query_packed = query.flatten(0, 1)
    key_packed = torch.cat(key_valid, dim=0)
    value_packed = torch.cat(value_valid, dim=0)

    out = sageattn_varlen(
        q=query_packed,
        k=key_packed,
        v=value_packed,
        cu_seqlens_q=cu_seqlens_q,
        cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max_seqlen_q,
        max_seqlen_k=max_seqlen_k,
        is_causal=is_causal,
        sm_scale=scale,
        smooth_k=smooth_k,
    )
    out = out.unflatten(0, (batch_size, -1)).permute(0, 2, 1, 3)  # .contiguous()

    return out


@_AttentionProviderRegistry.register(
    AttentionProvider._SAGE_QK_INT8_PV_FP8_CUDA,
    constraints=[_check_device_cuda_atleast_smXY(9, 0), _check_shape],
)
def _sage_qk_int8_pv_fp8_cuda_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    is_causal: bool = False,
    scale: Optional[float] = None,
    qk_quant_gran: _SAGE_ATTENTION_QK_QUANT_GRAN = "per_thread",
    pv_accum_dtype: _SAGE_ATTENTION_PV_ACCUM_DTYPE = "fp32+fp32",
    smooth_k: bool = True,
    smooth_v: bool = False,
    return_lse: bool = False,
) -> torch.Tensor:
    return sageattn_qk_int8_pv_fp8_cuda(
        q=query,
        k=key,
        v=value,
        tensor_layout="HND",
        is_causal=is_causal,
        qk_quant_gran=qk_quant_gran,
        sm_scale=scale,
        pv_accum_dtype=pv_accum_dtype,
        smooth_k=smooth_k,
        smooth_v=smooth_v,
        return_lse=return_lse,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider._SAGE_QK_INT8_PV_FP8_CUDA_SM90,
    constraints=[_check_device_cuda_atleast_smXY(9, 0), _check_shape],
)
def _sage_qk_int8_pv_fp8_cuda_sm90_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    is_causal: bool = False,
    scale: Optional[float] = None,
    qk_quant_gran: _SAGE_ATTENTION_QK_QUANT_GRAN = "per_thread",
    pv_accum_dtype: _SAGE_ATTENTION_PV_ACCUM_DTYPE = "fp32+fp32",
    smooth_k: bool = True,
    return_lse: bool = False,
) -> torch.Tensor:
    return sageattn_qk_int8_pv_fp8_cuda_sm90(
        q=query,
        k=key,
        v=value,
        tensor_layout="HND",
        is_causal=is_causal,
        qk_quant_gran=qk_quant_gran,
        sm_scale=scale,
        pv_accum_dtype=pv_accum_dtype,
        smooth_k=smooth_k,
        return_lse=return_lse,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider._SAGE_QK_INT8_PV_FP16_CUDA,
    constraints=[_check_device_cuda_atleast_smXY(8, 0), _check_shape],
)
def _sage_qk_int8_pv_fp16_cuda_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    is_causal: bool = False,
    scale: Optional[float] = None,
    qk_quant_gran: _SAGE_ATTENTION_QK_QUANT_GRAN = "per_thread",
    pv_accum_dtype: _SAGE_ATTENTION_PV_ACCUM_DTYPE = "fp32+fp32",
    smooth_k: bool = True,
    smooth_v: bool = False,
    return_lse: bool = False,
) -> torch.Tensor:
    return sageattn_qk_int8_pv_fp16_cuda(
        q=query,
        k=key,
        v=value,
        tensor_layout="HND",
        is_causal=is_causal,
        qk_quant_gran=qk_quant_gran,
        sm_scale=scale,
        pv_accum_dtype=pv_accum_dtype,
        smooth_k=smooth_k,
        smooth_v=smooth_v,
        return_lse=return_lse,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider._SAGE_QK_INT8_PV_FP16_TRITON,
    constraints=[_check_device_cuda_atleast_smXY(8, 0), _check_shape],
)
def _sage_qk_int8_pv_fp16_triton_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    is_causal: bool = False,
    scale: Optional[float] = None,
    quantization_backend: _SAGE_ATTENTION_QUANTIZATION_BACKEND = "triton",
    smooth_k: bool = True,
    return_lse: bool = False,
) -> torch.Tensor:
    return sageattn_qk_int8_pv_fp16_triton(
        q=query,
        k=key,
        v=value,
        tensor_layout="HND",
        quantization_backend=quantization_backend,
        is_causal=is_causal,
        sm_scale=scale,
        smooth_k=smooth_k,
        return_lse=return_lse,
    )


@_AttentionProviderRegistry.register(
    AttentionProvider.XFORMERS,
    constraints=[_check_attn_mask_or_causal, _check_device, _check_shape],
)
def _xformers_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    scale: Optional[float] = None,
    enable_gqa: bool = False,
) -> torch.Tensor:
    batch_size, num_heads_q, seq_len_q, _ = query.shape
    _, num_heads_kv, seq_len_kv, _ = key.shape

    # TODO: check if `contiguous` is really needed since it may cause unnecessary slowdowns
    if is_causal:
        attn_mask = xops.LowerTriangularMask()
    elif attn_mask is not None:
        if attn_mask.ndim == 2:
            attn_mask = attn_mask.view(attn_mask.size(0), 1, attn_mask.size(1), 1)
        elif attn_mask.ndim != 4:
            raise ValueError("Only 2D and 4D attention masks are supported for xformers attention.")
        attn_mask = attn_mask.expand(batch_size, num_heads_q, seq_len_q, seq_len_kv).type_as(query)

    # QKV need to be in [batch, seq_len, num_heads, head_dim] format for xformers
    # query, key, value = (x.permute(0, 2, 1, 3).contiguous() for x in (query, key, value))
    query, key, value = (x.permute(0, 2, 1, 3) for x in (query, key, value))

    if enable_gqa:
        if num_heads_q % num_heads_kv != 0:
            raise ValueError("Number of heads in query must be divisible by number of heads in key/value.")
        num_heads_per_group = num_heads_q // num_heads_kv
        query = query.unflatten(2, (num_heads_kv, -1))
        key = key.unflatten(2, (num_heads_kv, -1)).expand(-1, -1, -1, num_heads_per_group, -1)
        value = value.unflatten(2, (num_heads_kv, -1)).expand(-1, -1, -1, num_heads_per_group, -1)

    out = xops.memory_efficient_attention(query, key, value, attn_mask, dropout_p, scale)
    if enable_gqa:
        out = out.flatten(2, 3)

    out = out.permute(0, 2, 1, 3)  # .contiguous()
    return out
