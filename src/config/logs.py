import logging
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"

os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = LOGS_DIR / "api.log"

logging.basicConfig(
    filename=str(LOG_FILE_PATH),  
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("uvicorn")


def registrar_log(mensagem: str, nivel: str = "info"):
    """Registra logs utilizando o logger configurado.

    Args:
        mensagem: O texto a ser registrado no log
        nivel: O nível do log ('info', 'warning', 'error', 'debug')
    """
    if nivel == "info":
        logger.info(mensagem)
    elif nivel == "warning":
        logger.warning(mensagem)
    elif nivel == "error":
        logger.error(mensagem)
    elif nivel == "debug":
        logger.debug(mensagem)
