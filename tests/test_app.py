from pathlib import Path

from live_ai_brain import app


class FakeUpload:
    def __init__(self, name: str, content: bytes = b"demo") -> None:
        self.name = name
        self._content = content

    def getbuffer(self) -> bytes:
        return self._content


def test_save_uploaded_file_sanitizes_name_and_stays_inside_upload_dir(
    tmp_path: Path, monkeypatch
):
    upload_dir = tmp_path / "data" / "uploads"
    monkeypatch.setattr(app, "UPLOAD_DIR", upload_dir)

    saved_path = app._save_uploaded_file(FakeUpload("../bad folder/report #1.csv"))

    assert saved_path.parent == upload_dir
    assert saved_path.read_bytes() == b"demo"
    assert saved_path.name.endswith(".csv")
    assert saved_path.name != "report #1.csv"
    assert "bad" not in saved_path.parts
    assert all(char.isalnum() or char in "._-" for char in saved_path.name)
