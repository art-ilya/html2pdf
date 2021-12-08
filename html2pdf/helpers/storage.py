import shutil
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Optional, Union

import aiofiles
from fastapi import UploadFile


class FileStorage(ABC):
    @abstractmethod
    def save_file(self, in_file: IO, uniq_filename: Optional[str] = None):
        """Saves file synchronously"""


class FileStorageAsync(ABC):
    @abstractmethod
    def save_file_async(self, in_file: IO, uniq_filename: Optional[str] = None):
        """Saves file asynchronously"""


class LocalFileStorage(FileStorage, FileStorageAsync):

    CHUNK_SIZE = 16 * 1024

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        self.base_path: Path = self._init_base_path(Path(base_path or "./"))

    def _init_base_path(self, base_path: Path) -> Path:
        base_path.mkdir(parents=True, exist_ok=True)
        return base_path

    def save_file(self, in_file: IO, uniq_filename: Optional[str] = None) -> Path:
        try:
            uniq_filename: str = uniq_filename or uuid.uuid4()
            dest: Path = self.base_path / uniq_filename
            with dest.open("wb") as buffer:
                shutil.copyfileobj(in_file, buffer, length=self.CHUNK_SIZE)
            return dest
        finally:
            in_file.close()

    async def save_file_async(
        self, in_file: UploadFile, uniq_filename: Optional[str] = None
    ) -> Path:
        try:
            uniq_filename: str = uniq_filename or uuid.uuid4()
            dest: Path = self.base_path / uniq_filename
            async with aiofiles.open(dest.as_posix(), "wb") as out_file:
                while True:
                    chunk = await in_file.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    await out_file.write(chunk)
                return dest
        finally:
            await in_file.close()
