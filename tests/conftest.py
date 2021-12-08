import asyncio
import logging
import os
import shutil
import sys
from os.path import abspath, dirname, join
from pathlib import Path

import pytest

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(join(root_dir, 'html2pdf'))

from html2pdf.helpers.storage import LocalFileStorage

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
default_logger = logging.getLogger(__name__)


@pytest.fixture()
def tmp_dir():
    tmp_dir = Path(root_dir) / Path("TMP_DIR")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    yield tmp_dir
    shutil.rmtree(tmp_dir)


@pytest.fixture()
def local_storage(tmp_dir):
    yield LocalFileStorage(base_path=tmp_dir)



@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
