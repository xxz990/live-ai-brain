from pathlib import Path

from live_ai_brain.models import ExecutionTask, TaskStatus
from live_ai_brain.storage import JsonStore


def test_json_store_round_trips_execution_tasks(tmp_path: Path):
    store = JsonStore(tmp_path)
    task = ExecutionTask(
        id="task-1",
        session_id="session-1",
        owner_role="主播",
        title="改开场痛点话术",
        detail="把文言文痛点前置到前 20 秒。",
        status=TaskStatus.ADOPTED,
    )

    store.save_tasks([task])
    loaded = store.load_tasks()

    assert loaded == [task]
