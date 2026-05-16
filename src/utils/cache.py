import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LocalCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "search_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Erro ao carregar cache: {e}")
        return {}

    def _save_cache(self) -> None:
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {e}")

    def _generate_key(self, name: str, company: str = "", title: str = "") -> str:
        data = f"{name.lower().strip()}|{company.lower().strip()}|{title.lower().strip()}"
        return hashlib.md5(data.encode()).hexdigest()

    def get(self, name: str, company: str = "", title: str = "") -> Optional[Dict]:
        key = self._generate_key(name, company, title)
        return self.cache.get(key)

    def set(self, name: str, data: Dict, company: str = "", title: str = "") -> None:
        key = self._generate_key(name, company, title)
        self.cache[key] = data
        self._save_cache()
        logger.debug(f"Cache atualizado para {name}")

    def clear(self) -> None:
        self.cache = {}
        self._save_cache()
        logger.info("Cache limpo")

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_cached": len(self.cache),
            "file_size_kb": self.cache_file.stat().st_size / 1024 if self.cache_file.exists() else 0,
        }
