from settings import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Make separate sync_session for dramatiq workers because there is no async support
sync_engine = create_engine(
    config.DATABASE_SYNC_URI,
    connect_args={"check_same_thread": False},
    echo=config.DEBUG,
)
sync_session = sessionmaker(
    sync_engine,
    autocommit=False,
    autoflush=False,
)