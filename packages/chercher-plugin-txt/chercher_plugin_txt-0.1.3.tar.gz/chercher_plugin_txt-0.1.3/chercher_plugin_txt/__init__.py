import hashlib
from pathlib import Path
from typing import Generator
from chercher import Document, hookimpl


@hookimpl()
def ingest(uri: str) -> Generator[Document, None, None]:
    path = Path(uri).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".txt":
        return

    with path.open("rb") as f:
        content = f.read()
        digest = hashlib.file_digest(f, "sha256")

    yield Document(
        uri=path.as_uri(),
        title=path.stem,
        body=content.decode("utf-8"),
        hash=digest.hexdigest(),
        metadata={},
    )
