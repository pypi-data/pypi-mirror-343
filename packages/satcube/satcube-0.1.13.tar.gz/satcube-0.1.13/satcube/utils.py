from __future__ import annotations

import gc
from typing import Any, Optional

import torch


def _reset_gpu() -> None:
    """Release CUDA memory and reset allocation statistics.

    Calling this on a system without a CUDA device is a no-op.
    """
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()


class DeviceManager:
    """Hold a compiled mlstac model and move it between devices on demand."""

    def __init__(self, experiment: Any, init_device: str = "cpu") -> None:
        """
        Parameters
        ----------
        experiment
            An mlstac experiment exposing ``compiled_model``.
        init_device
            Device where the model is first compiled, e.g. ``"cpu"`` or
            ``"cuda:0"``.
        """
        self._experiment: Any = experiment
        self.device: Optional[str] = None
        self.model: Optional[torch.nn.Module] = None
        self.switch(init_device)

    def switch(self, new_device: str) -> torch.nn.Module:
        """Return a model compiled for *new_device*, recompiling if needed.

        Parameters
        ----------
        new_device
            Target device identifier.

        Returns
        -------
        torch.nn.Module
            The model resident on *new_device*.

        Raises
        ------
        AssertionError
            If *new_device* requests CUDA but no GPU is available.
        """
        if new_device == self.device:
            return self.model  # type: ignore[return-value]

        if self.model is not None:
            del self.model
        gc.collect()

        if self.device == "cuda":
            _reset_gpu()

        if new_device == "cuda":
            assert torch.cuda.is_available(), "CUDA device not detected"

        print(f"→ Compiling model on {new_device} …")
        self.model = self._experiment.compiled_model(device=new_device, mode="max")
        self.device = new_device
        return self.model
