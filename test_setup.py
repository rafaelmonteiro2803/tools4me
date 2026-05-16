#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    print("✓ Testando importações...")
    try:
        import customtkinter
        print("  ✓ customtkinter")
        import pandas
        print("  ✓ pandas")
        import requests
        print("  ✓ requests")
        from bs4 import BeautifulSoup
        print("  ✓ beautifulsoup4")
        from config.settings import APP_CONFIG, SEARCH_CONFIG
        print("  ✓ config.settings")
        from src.utils.logger import get_logger
        print("  ✓ logger")
        from src.utils.cache import LocalCache
        print("  ✓ cache")
        from src.utils.validators import SimilarityValidator
        print("  ✓ validators")
        from src.services.search_service import SearchService
        print("  ✓ search_service")
        from src.services.data_processor import DataProcessor
        print("  ✓ data_processor")
        from src.gui.main_window import LinkedInEnrichmentApp
        print("  ✓ main_window")
        return True
    except ImportError as e:
        print(f"  ✗ Erro: {e}")
        return False

def test_structure():
    print("\n✓ Testando estrutura de pastas...")
    required_dirs = ["data", "logs", "examples", "src", "config"]
    for dir_name in required_dirs:
        path = Path(__file__).parent / dir_name
        if path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ não encontrado")
            return False
    return True

def test_config():
    print("\n✓ Testando configurações...")
    try:
        from config.settings import APP_CONFIG, SEARCH_CONFIG, MATCH_CONFIG
        print(f"  ✓ App: {APP_CONFIG['title']}")
        print(f"  ✓ Search threads: {SEARCH_CONFIG['max_threads']}")
        print(f"  ✓ Min confidence: {MATCH_CONFIG['min_confidence']}")
        return True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False

def main():
    print("=" * 60)
    print("LinkedIn Data Enrichment Tool - Test Setup")
    print("=" * 60)

    results = [
        test_imports(),
        test_structure(),
        test_config(),
    ]

    print("\n" + "=" * 60)
    if all(results):
        print("✓ Todas as verificações passaram!")
        print("✓ Você pode executar: python app.py")
        return 0
    else:
        print("✗ Algumas verificações falharam")
        print("✗ Instale as dependências: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
