import dramatiq
from dramatiq.brokers.redis import RedisBroker
from settings import config

redis_broker = RedisBroker(url=config.MESSAGE_BROKER_URI)
dramatiq.set_broker(redis_broker)

from .convert import convert_task
