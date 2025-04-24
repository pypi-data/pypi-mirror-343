from chercher_plugin_md import ingest
from chercher import Document

CONTENT = """
---
title: TDD
---

# TDD
And how to do it in production.
"""


def test_valid_file(tmp_path):
    p = tmp_path / "test.md"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = ingest(uri=uri)
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.uri == uri
        assert doc.body == CONTENT
        assert isinstance(doc.metadata, dict)
        assert doc.metadata["title"] == "TDD"
        assert doc.hash is not None


def test_invalid_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = ingest(uri=uri)
    assert list(documents) == []


def test_missing_file(tmp_path):
    p = tmp_path / "missingno.md"
    documents = ingest(uri=p.as_uri())
    assert list(documents) == []


def test_invalid_uri():
    uri = "https://blog/post.md"
    documents = ingest(uri=uri)
    assert list(documents) == []
