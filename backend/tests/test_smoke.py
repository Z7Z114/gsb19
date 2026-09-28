"""冒烟测试：只覆盖顺利路径（离线 mock 分支）。

在初始快照上必须全绿——缺陷不在这些顺利路径上，而在 README「行为规格」覆盖的边界语义里。
"""
import os
import sys

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import main  # noqa: E402

client = TestClient(main.app, raise_server_exceptions=False)

WAV_BYTES = b"RIFF" + b"\x00" * 512


def _upload(filename="fieldwork.wav", dialect="闽南语", region="福建省泉州市"):
    resp = client.post(
        "/api/audio/upload",
        files={"file": (filename, WAV_BYTES, "audio/wav")},
        data={"dialect": dialect, "region": region},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def _process(session_id):
    resp = client.post("/api/processing/start", json={"session_id": session_id})
    assert resp.status_code == 200, resp.text
    status = client.get("/api/processing/status/{}".format(session_id))
    assert status.status_code == 200, status.text
    body = status.json()
    assert body["status"] == "completed", body
    assert body["progress"] == 100
    return body


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_upload_returns_session():
    body = _upload()
    assert body["session_id"]
    assert body["file_size"] == len(WAV_BYTES)
    assert body["filename"] == "fieldwork.wav"


def test_pipeline_completes_and_lists_speakers():
    session_id = _upload()["session_id"]
    _process(session_id)

    resp = client.get("/api/speakers/{}".format(session_id))
    assert resp.status_code == 200, resp.text
    speakers = resp.json()
    assert speakers, "离线 mock 分支也应产出说话人"
    for speaker in speakers:
        assert speaker["name"]
        assert speaker["role"] in ("informant", "researcher")
        assert speaker["pyannote_label"]


def test_discussion_roundtrip():
    session_id = _upload()["session_id"]
    payload = {
        "session_id": session_id,
        "user_id": "u1",
        "user_name": "研究员甲",
        "user_role": "researcher",
        "content": "第三段的体标记需要复核",
        "segment_ref": None,
        "annotations": [],
    }
    posted = client.post("/api/discussion/{}".format(session_id), json=payload)
    assert posted.status_code == 200, posted.text
    assert posted.json()["content"] == payload["content"]

    listed = client.get("/api/discussion/{}".format(session_id))
    assert listed.status_code == 200, listed.text
    assert len(listed.json()) == 1


def test_report_generate_and_markdown_export():
    session_id = _upload()["session_id"]
    _process(session_id)

    resp = client.post("/api/report/generate", json={"session_id": session_id})
    assert resp.status_code == 200, resp.text
    report = resp.json()
    assert report["summary"]
    assert report["endangerment"] is not None
    assert report["transcription_count"] > 0

    markdown = client.get("/api/report/{}/markdown".format(report["id"]))
    assert markdown.status_code == 200, markdown.text
    assert "方言特征报告" in markdown.text
    assert "语料统计" in markdown.text


def test_unknown_resources_return_404():
    assert client.get("/api/audio/stream/does-not-exist").status_code == 404
    assert client.get("/api/processing/status/does-not-exist").status_code == 404
    assert client.post("/api/processing/start", json={"session_id": "does-not-exist"}).status_code == 404
    assert client.get("/api/speakers/does-not-exist").status_code == 200
