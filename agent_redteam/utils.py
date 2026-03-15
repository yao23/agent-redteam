from pathlib import Path
import tempfile
import shutil


def make_temp_dir(prefix: str = "agent_redteam_") -> Path:
    return Path(tempfile.mkdtemp(prefix=prefix))


def cleanup_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
