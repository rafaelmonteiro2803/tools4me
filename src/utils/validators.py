import re
from difflib import SequenceMatcher
from typing import Tuple, Dict
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SimilarityValidator:
    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def string_similarity(a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        a = SimilarityValidator.normalize(a)
        b = SimilarityValidator.normalize(b)
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def name_similarity(profile_name: str, target_name: str) -> float:
        if not profile_name or not target_name:
            return 0.0

        profile_parts = set(profile_name.lower().split())
        target_parts = set(target_name.lower().split())

        if not profile_parts or not target_parts:
            return 0.0

        intersection = len(profile_parts & target_parts)
        union = len(profile_parts | target_parts)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def company_similarity(profile_company: str, target_company: str) -> float:
        if not profile_company or not target_company:
            return 0.0
        return SimilarityValidator.string_similarity(profile_company, target_company)

    @staticmethod
    def title_similarity(profile_title: str, target_title: str) -> float:
        if not profile_title or not target_title:
            return 0.0
        return SimilarityValidator.string_similarity(profile_title, target_title)

    @staticmethod
    def calculate_confidence_score(
        name_sim: float,
        company_sim: float,
        title_sim: float,
        name_weight: float = 0.4,
        company_weight: float = 0.35,
        title_weight: float = 0.25,
    ) -> float:
        score = (
            name_sim * name_weight +
            company_sim * company_weight +
            title_sim * title_weight
        )
        return min(max(score, 0.0), 1.0)


class LinkedInValidator:
    LINKEDIN_URL_PATTERN = re.compile(
        r'linkedin\.com/(in|company)/([a-z0-9\-]+)',
        re.IGNORECASE
    )

    @staticmethod
    def is_valid_linkedin_url(url: str) -> bool:
        if not url:
            return False
        return bool(LinkedInValidator.LINKEDIN_URL_PATTERN.search(str(url)))

    @staticmethod
    def extract_linkedin_id(url: str) -> str:
        if not url:
            return ""
        match = LinkedInValidator.LINKEDIN_URL_PATTERN.search(str(url))
        return match.group(2) if match else ""

    @staticmethod
    def normalize_linkedin_url(url: str) -> str:
        if not url:
            return ""
        url = url.strip().rstrip('/')
        if not url.startswith('http'):
            url = f"https://{url}"
        return url


class DataValidator:
    @staticmethod
    def validate_row(row: Dict) -> Tuple[bool, str]:
        required_fields = ['nome']
        missing = [f for f in required_fields if not row.get(f) or str(row.get(f)).strip() == '']

        if missing:
            return False, f"Campos obrigatórios faltando: {', '.join(missing)}"

        return True, ""

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        return str(text).strip()
