import hashlib
from pathlib import Path
from typing import Generator
import frontmatter
from chercher import Document, hookimpl


@hookimpl
def ingest(uri: str) -> Generator[Document, None, None]:
    path = Path(uri).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".md":
        return

    with path.open("rb") as f:
        digest = hashlib.file_digest(f, "sha256")
        post = frontmatter.loads(f.read().decode("utf-8"))

    yield Document(
        uri=path.as_uri(),
        title=path.stem,
        body=post.content,
        hash=digest.hexdigest(),
        metadata=post.metadata,
    )
