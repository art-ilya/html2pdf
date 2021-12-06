import tempfile
import uuid
from asyncio import BaseEventLoop
from pathlib import Path

from fastapi import UploadFile
from html2pdf.helpers.storage import LocalFileStorage


def test_save_file(local_storage: LocalFileStorage):
    base_path = local_storage.base_path
    uniq_filename = str(uuid.uuid4())
    b_content = b"Hello world!"
    with tempfile.TemporaryFile() as fp:
        fp.write(b_content)
        fp.seek(0)
        local_storage.save_file(fp, uniq_filename)

    saved_file = Path(base_path / uniq_filename)
    assert saved_file.exists() == True
    assert saved_file.read_bytes() == b_content


# TODO: по-хорошему надо такое проверять с pytest-asyncio
def test_save_file_async(event_loop: BaseEventLoop, local_storage: LocalFileStorage):
    base_path = local_storage.base_path
    uniq_filename = str(uuid.uuid4())
    b_content = b"Hello world!"
    with tempfile.TemporaryFile() as fp:
        fp.write(b_content)
        fp.seek(0)
        file = UploadFile(
            filename="test.file", file=fp, content_type="application/octet-stream"
        )
        event_loop.run_until_complete(
            local_storage.save_file_async(file, uniq_filename)
        )

    saved_file = Path(base_path / uniq_filename)
    assert saved_file.exists() == True
    assert saved_file.read_bytes() == b_content
