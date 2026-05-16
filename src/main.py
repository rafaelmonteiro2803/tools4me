import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.main_window import LinkedInEnrichmentApp
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        logger.info("Iniciando aplicação LinkedIn Data Enrichment Tool")
        app = LinkedInEnrichmentApp()
        app.run()
    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar aplicação: {e}")
        raise

if __name__ == "__main__":
    main()
