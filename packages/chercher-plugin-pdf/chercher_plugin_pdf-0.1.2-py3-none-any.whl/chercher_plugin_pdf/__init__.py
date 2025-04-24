import hashlib
from pathlib import Path
from typing import Generator
import pymupdf
from chercher import Document, hookimpl

pymupdf.JM_mupdf_show_errors = 0


@hookimpl
def ingest(uri: str) -> Generator[Document, None, None]:
    path = Path(uri).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".pdf":
        return

    doc = pymupdf.open(uri)

    file_bytes = doc.tobytes(no_new_id=True)
    digest = hashlib.sha256(file_bytes)

    body = ""
    for page in doc:
        body += page.get_text()

    yield Document(
        uri=uri,
        body=body,
        hash=digest.hexdigest(),
        metadata={},
    )
