"""Predict cloud masks for Sentinel-2 GeoTIFFs with the SEN2CloudEnsemble model.

The callable :pyfunc:`cloud_masking` accepts **either** a single ``.tif`` file  
or a directory tree; in both cases it writes a masked copy of every image (and,
optionally, the binary mask) to *output*.

Example
-------
>>> from satcube.cloud_detection import cloud_masking
>>> cloud_masking("~/s2/input", "~/s2/output", device="cuda")
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import List

import mlstac
import numpy as np
import rasterio as rio
import torch

from satcube.utils import DeviceManager, _reset_gpu
import warnings, re


warnings.filterwarnings(
    "ignore",
    message=re.escape("The secret `HF_TOKEN` does not exist in your Colab secrets."),
    category=UserWarning,
    module="huggingface_hub.utils._auth",
)

def cloud_masking(
    input: str | Path,              # noqa: A002 (shadowing built-in is OK here)
    output: str | Path,
    *,
    tile: int = 512,
    pad: int = 64,
    save_mask: bool = False,
    device: str = "cpu",
    max_pix_cpu: float = 7.0e7
) -> List[Path]:
    """Write cloud-masked Sentinel-2 images.

    Parameters
    ----------
    input
        Path to a single ``.tif`` file **or** a directory containing them.
    output
        Destination directory (created if missing).
    tile, pad
        Tile size and padding (pixels) when tiling is required.
    save_mask
        If *True*, store the binary mask alongside the masked image.
    device
        Torch device for inference, e.g. ``"cpu"`` or ``"cuda:0"``.
    max_pix_cpu
        Tile images larger than this when running on CPU.

    Returns
    ------
    list[pathlib.Path]
        Paths to the generated masked images.
    """
    t_start = time.perf_counter()

    src = Path(input).expanduser().resolve()
    dst_dir = Path(output).expanduser().resolve()
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Collect files to process -------------------------------------------------
    tif_paths: list[Path]
    if src.is_dir():
        tif_paths = [p for p in src.rglob("*.tif")]
    elif src.is_file() and src.suffix.lower() == ".tif":
        tif_paths = [src]
        src = src.parent  # for relative-path bookkeeping below
    else:
        raise ValueError(f"Input must be a .tif or directory, got: {src}")

    if not tif_paths:
        print(f"[cloud_masking] No .tif files found in {src}")
        return []
    
    dir = Path("SEN2CloudEnsemble")

    if not dir.exists():

        mlstac.download(
            file = "https://huggingface.co/tacofoundation/CloudSEN12-models/resolve/main/SEN2CloudEnsemble/mlm.json",
            output_dir = "SEN2CloudEnsemble",
        )

    experiment = mlstac.load(dir.as_posix())

    dm = DeviceManager(experiment, init_device=device)

    masked_paths: list[Path] = []

    # -------------------------------------------------------------------------
    for idx, tif_path in enumerate(tif_paths, 1):
        rel = tif_path.relative_to(src)
        out_dir = dst_dir / rel.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        mask_path = out_dir / f"{tif_path.stem}_cloudmask.tif"
        masked_path = out_dir / f"{tif_path.stem}_masked.tif"

        with rio.open(tif_path) as src_img:
            profile = src_img.profile
            h, w = src_img.height, src_img.width

        mask_prof = profile.copy()
        mask_prof.update(driver="GTiff", count=1, dtype="uint8", nodata=255)

        do_tiling = (dm.device == "cuda") or (h * w > max_pix_cpu)
        full_mask = np.full((h, w), 255, np.uint8)

        t0 = time.perf_counter()

        # ----------------------- inference -----------------------------------
        if not do_tiling:  # full frame
            with rio.open(tif_path) as src_img, torch.inference_mode():
                img = src_img.read().astype(np.float32) / 1e4
                h32, w32 = (h + 31) // 32 * 32, (w + 31) // 32 * 32
                pad_b, pad_r = h32 - h, w32 - w
                tensor = torch.from_numpy(img).unsqueeze(0)
                if pad_b or pad_r:
                    tensor = torch.nn.functional.pad(tensor, (0, pad_r, 0, pad_b))
                mask = dm.model(tensor.to(dm.device)).squeeze(0)
                full_mask[:] = mask[..., :h, :w].cpu().numpy().astype(np.uint8)
        else:  # tiled
            with rio.open(tif_path) as src_img, torch.inference_mode():
                for y0 in range(0, h, tile):
                    for x0 in range(0, w, tile):
                        y0r, x0r = max(0, y0 - pad), max(0, x0 - pad)
                        y1r, x1r = min(h, y0 + tile + pad), min(w, x0 + tile + pad)
                        win = rio.windows.Window(x0r, y0r, x1r - x0r, y1r - y0r)

                        patch = src_img.read(window=win).astype(np.float32) / 1e4
                        tensor = torch.from_numpy(patch).unsqueeze(0).to(dm.device)
                        mask = dm.model(tensor).squeeze(0).cpu().numpy().astype(np.uint8)

                        y_in0 = pad if y0r else 0
                        x_in0 = pad if x0r else 0
                        y_in1 = mask.shape[0] - (pad if y1r < h else 0)
                        x_in1 = mask.shape[1] - (pad if x1r < w else 0)
                        core = mask[y_in0:y_in1, x_in0:x_in1]
                        full_mask[y0 : y0 + core.shape[0], x0 : x0 + core.shape[1]] = core

        # ----------------------- output --------------------------------------
        if save_mask:
            with rio.open(mask_path, "w", **mask_prof) as dst:
                dst.write(full_mask, 1)

        with rio.open(tif_path) as src_img:
            data = src_img.read()
            img_prof = src_img.profile.copy()

        masked = data.copy()
        masked[:, full_mask != 0] = 65535
        img_prof.update(dtype="uint16", nodata=65535)

        with rio.open(masked_path, "w", **img_prof) as dst:
            dst.write(masked)

        masked_paths.append(masked_path)
        dt = time.perf_counter() - t0
        print(f"[{idx}/{len(tif_paths)}] {rel} → done in {dt:.1f}s")

    if dm.device == "cuda":
        _reset_gpu()

    total_time = time.perf_counter() - t_start
    print(f"Processed {len(masked_paths)} image(s) in {total_time:.1f}s.")
    return masked_paths
