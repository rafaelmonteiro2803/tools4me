import time
import random
import requests
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.utils.logger import get_logger
from src.utils.validators import (
    SimilarityValidator,
    LinkedInValidator,
    DataValidator
)
from config.settings import SEARCH_CONFIG, MATCH_CONFIG

logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = SEARCH_CONFIG['timeout']
        self.retry_attempts = SEARCH_CONFIG['retry_attempts']
        self.delay_min = SEARCH_CONFIG['delay_min']
        self.delay_max = SEARCH_CONFIG['delay_max']

    def _apply_delay(self) -> None:
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)

    def _fetch_url(self, url: str, attempts: int = 0) -> Optional[str]:
        if attempts >= self.retry_attempts:
            logger.warning(f"Máximo de tentativas atingido para {url}")
            return None

        try:
            self._apply_delay()
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.debug(f"Tentativa {attempts + 1} falhou para {url}: {e}")
            return self._fetch_url(url, attempts + 1)

    def search_linkedin_profile(
        self,
        name: str,
        company: str = "",
        title: str = "",
    ) -> List[Dict]:
        try:
            query = self._build_search_query(name, company, title)
            logger.info(f"Buscando perfil para: {name}")

            results = self._google_search(query)
            linkedin_results = [r for r in results if 'linkedin.com' in r.get('url', '').lower()]

            return linkedin_results[:5]
        except Exception as e:
            logger.error(f"Erro na busca de perfil para {name}: {e}")
            return []

    def _build_search_query(self, name: str, company: str = "", title: str = "") -> str:
        parts = [f'"{name}"', 'site:linkedin.com/in']

        if company:
            parts.append(company)
        if title:
            parts.append(title)

        return " ".join(parts)

    def _google_search(self, query: str) -> List[Dict]:
        try:
            url = f"https://www.google.com/search?q={query}"
            html = self._fetch_url(url)

            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            results = []

            for g in soup.find_all('div', class_='g')[:10]:
                try:
                    link = g.find('a', href=True)
                    if not link:
                        continue

                    url = link['href']
                    title = link.get_text(strip=True)
                    snippet_elem = g.find('span', class_='VwiC3b')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    if url and 'linkedin.com' in url.lower():
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                        })
                except Exception as e:
                    logger.debug(f"Erro ao parsear resultado: {e}")
                    continue

            return results
        except Exception as e:
            logger.error(f"Erro na busca Google: {e}")
            return []

    def extract_profile_info(self, url: str) -> Optional[Dict]:
        try:
            html = self._fetch_url(url)
            if not html:
                return None

            soup = BeautifulSoup(html, 'html.parser')

            name = self._extract_name(soup)
            company = self._extract_company(soup)
            title = self._extract_title(soup)

            if not name:
                return None

            return {
                'url': url,
                'name': name,
                'company': company,
                'title': title,
                'source': 'linkedin',
            }
        except Exception as e:
            logger.warning(f"Erro ao extrair informações de {url}: {e}")
            return None

    def _extract_name(self, soup: BeautifulSoup) -> str:
        patterns = [
            soup.find('h1'),
            soup.find('meta', {'name': 'description'}),
            soup.find('title'),
        ]

        for elem in patterns:
            if elem:
                text = elem.get_text(strip=True) if elem.name != 'meta' else elem.get('content', '')
                name = text.split('|')[0].strip()
                if name and len(name) > 2:
                    return name

        return ""

    def _extract_company(self, soup: BeautifulSoup) -> str:
        patterns = [
            soup.find('span', class_='text-body-small inline t-black--light'),
            soup.find('div', class_='text-body-medium'),
        ]

        for elem in patterns:
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 2:
                    return text

        return ""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        patterns = [
            soup.find('div', class_='text-body-medium inline t-black--light'),
            soup.find('span', {'data-field': 'title'}),
        ]

        for elem in patterns:
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 2:
                    return text

        return ""

    def validate_profile_match(
        self,
        profile: Dict,
        target_name: str,
        target_company: str = "",
        target_title: str = "",
    ) -> Tuple[bool, float]:
        try:
            name_sim = SimilarityValidator.name_similarity(profile.get('name', ''), target_name)
            company_sim = SimilarityValidator.company_similarity(
                profile.get('company', ''),
                target_company
            )
            title_sim = SimilarityValidator.title_similarity(
                profile.get('title', ''),
                target_title
            )

            score = SimilarityValidator.calculate_confidence_score(
                name_sim,
                company_sim,
                title_sim,
                name_weight=MATCH_CONFIG['name_weight'],
                company_weight=MATCH_CONFIG['company_weight'],
                title_weight=MATCH_CONFIG['title_weight'],
            )

            is_match = score >= MATCH_CONFIG['min_confidence']
            return is_match, score

        except Exception as e:
            logger.error(f"Erro ao validar perfil: {e}")
            return False, 0.0
