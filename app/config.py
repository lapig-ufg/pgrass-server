from dynaconf import Dynaconf
from loguru import logger

logger.add('../logs/serve.log')

settings = Dynaconf(
    envvar_prefix='PGRASS',
    settings_files=['settings.toml', '.secrets.toml','/data/settings.toml'],
    environments=True,
    load_dotenv=True,
)
