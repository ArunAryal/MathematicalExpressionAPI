import logging
import shutil
import os
from pathlib import Path

import kagglehub
from app.core.config import settings

logger = logging.getLogger(__name__)

KAGGLE_MODEL_HANDLE = "binitawasthi/hmer/pyTorch/default"


def ensure_model(model_path: str) -> None:
    """Check if *model_path* exists; if not, download it from Kaggle.

    The downloaded artefact directory is scanned for the first ``*.pt`` file,
    which is then copied to *model_path*.

    Args:
        model_path: Relative or absolute path where the model file should live
                    (e.g. ``"models/hmer.pt"``).
    """
    target = Path(model_path)

    if target.exists():
        logger.info("Model already present at '%s' — skipping download.", target)
        return

    # Make sure the parent directory exists
    target.parent.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Model not found at '%s'. Downloading from Kaggle (%s) …",
        target,
        KAGGLE_MODEL_HANDLE,
    )

    # Export credentials if provided in configuration
    if getattr(settings, "KAGGLE_USERNAME", "") and getattr(settings, "KAGGLE_KEY", ""):
        os.environ["KAGGLE_USERNAME"] = settings.KAGGLE_USERNAME
        os.environ["KAGGLE_KEY"] = settings.KAGGLE_KEY

    # kagglehub.model_download returns the local path to the downloaded files
    download_dir = Path(kagglehub.model_download(KAGGLE_MODEL_HANDLE))
    logger.info("Kaggle download directory: %s", download_dir)

    # Find the .pt file inside the downloaded directory (recursively)
    pt_files = list(download_dir.rglob("*.pt"))
    if not pt_files:
        raise FileNotFoundError(
            f"No '.pt' file found inside the downloaded Kaggle artefact at "
            f"'{download_dir}'. Contents: {list(download_dir.rglob('*'))}"
        )

    src = pt_files[0]
    if len(pt_files) > 1:
        logger.warning(
            "Multiple .pt files found; using the first one: %s", src
        )

    shutil.copy2(src, target)
    logger.info("Model saved to '%s'.", target)
