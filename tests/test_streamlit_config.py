from pathlib import Path
import tomllib


def test_streamlit_allows_large_recording_uploads():
    config_path = Path(".streamlit") / "config.toml"
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))

    assert config["server"]["maxUploadSize"] >= 2048
