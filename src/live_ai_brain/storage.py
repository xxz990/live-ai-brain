from __future__ import annotations

import json
from pathlib import Path

from live_ai_brain.models import ExecutionTask


class JsonStore:
    def __init__(self, root: Path | str = "data") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def tasks_path(self) -> Path:
        return self.root / "execution_tasks.json"

    def save_tasks(self, tasks: list[ExecutionTask]) -> None:
        payload = [task.to_dict() for task in tasks]
        self.tasks_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_tasks(self) -> list[ExecutionTask]:
        if not self.tasks_path.exists():
            return []
        payload = json.loads(self.tasks_path.read_text(encoding="utf-8"))
        return [ExecutionTask.from_dict(item) for item in payload]
