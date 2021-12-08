from typing import Optional, Union
import uuid
from contextlib import closing
from logging import Logger
from pathlib import Path

import dramatiq
import pdfkit
from models.convert_request import CONVERT_STATUS, SOURCE_TYPE, ConvertRequestModel
from settings import config

from .db_sync import sync_session

QUEUE_NAME = "convert"


@dramatiq.actor(queue_name=QUEUE_NAME, max_retries=0)
def convert_task(uid: str):
    logger: Logger = convert_task.logger
    with closing(sync_session()) as db_session:
        logger.info(f"{uid}: processing ConvertRequest")
        _cls = ConvertRequestModel
        convert_request: _cls = db_session.query(_cls).get(uid)
        if convert_request is None:
            logger.info(f"{uid}: ConvertRequest not found")
            return

        try:
            convert_request.status = CONVERT_STATUS.failure
            output_dir = Path(config.DOWNLOAD_DIR)
            if convert_request.source_type == SOURCE_TYPE.url:
                target_path = convert_html_to_pdf(
                    source_type=convert_request.source_type,
                    source=convert_request.source,
                    target_dir=output_dir,
                )
                convert_request.status = CONVERT_STATUS.success
                convert_request.target = target_path.name
            elif convert_request.source_type == SOURCE_TYPE.file:
                input_dir = Path(config.UPLOAD_DIR)
                input_filename = convert_request.source
                input_path = input_dir / input_filename
                target_path = convert_html_to_pdf(
                    source_type=convert_request.source_type,
                    source=input_path,
                    target_dir=output_dir,
                )
                convert_request.status = CONVERT_STATUS.success
                convert_request.target = target_path.name
                input_path.unlink()
        finally:
            db_session.commit()


def convert_html_to_pdf(
    source_type: SOURCE_TYPE,
    source: Union[Path, str],
    target_dir: Union[Path, str],
) -> Path:
    """
    Converts the source (URL or path-to-html-file) to pdf and saves it to disk at target_dir.
    Returns Path to target PDF
    """
    target_filename = f"{uuid.uuid4()}.pdf"
    target_path = Path(target_dir) / target_filename
    if source_type == SOURCE_TYPE.url:
        _ = pdfkit.from_url(source, output_path=target_path, verbose=True)
    elif source_type == SOURCE_TYPE.file:
        try:
            # https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2051
            # https://stackoverflow.com/questions/63446380/how-to-ignore-the-error-exit-with-code-1-due-to-network-error-contentnotfounde/67372025#67372025
            _ = pdfkit.from_file(str(source), output_path=target_path, verbose=True)
        except OSError as e:
            if "Done" not in str(e):
                raise e

    return target_path
