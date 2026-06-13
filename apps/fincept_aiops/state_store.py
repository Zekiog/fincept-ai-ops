import json
import os
import tempfile
from pathlib import Path
from typing import Any


class StateStore:
    """File-backed key/value state with atomic writes (temp + os.replace)."""

    def __init__(self, base: str | None = None):
        self.base = Path(base or os.getenv("STATE_PATH", "./data/state"))
        self.base.mkdir(parents=True, exist_ok=True)

    def save(self, key: str, data: Any) -> None:
        target = self.base / f"{key}.json"
        payload = json.dumps(data, indent=2, ensure_ascii=False)
        # Atomic write: temp file in same dir, fsync, then os.replace.
        # os.replace is atomic on POSIX and Windows; concurrent readers never
        # observe a half-written file.
        fd, tmp_path = tempfile.mkstemp(prefix=f".{key}.", suffix=".tmp", dir=str(self.base))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(payload)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, target)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    def load(self, key: str) -> Any:
        p = self.base / f"{key}.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def exists(self, key: str) -> bool:
        return (self.base / f"{key}.json").exists()

    def delete(self, key: str) -> None:
        p = self.base / f"{key}.json"
        if p.exists():
            p.unlink()
