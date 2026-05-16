import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Callable
from threading import Lock
from src.utils.logger import get_logger
from src.utils.cache import LocalCache
from src.utils.validators import LinkedInValidator, DataValidator
from src.services.search_service import SearchService
from config.settings import DATA_DIR

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.cache = LocalCache(DATA_DIR)
        self.search_service = SearchService()
        self.lock = Lock()
        self.is_running = False

    def load_spreadsheet(self, file_path: str) -> Optional[pd.DataFrame]:
        try:
            file_path = Path(file_path)

            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                logger.error(f"Formato não suportado: {file_path.suffix}")
                return None

            df.columns = [col.lower().strip() for col in df.columns]
            logger.info(f"Planilha carregada: {len(df)} linhas")
            return df

        except Exception as e:
            logger.error(f"Erro ao carregar planilha: {e}")
            return None

    def enrich_contacts(
        self,
        df: pd.DataFrame,
        progress_callback: Optional[Callable] = None,
        status_callback: Optional[Callable] = None,
    ) -> pd.DataFrame:
        try:
            self.is_running = True
            output_columns = [
                'linkedin_encontrado',
                'empresa_atual',
                'cargo_atual',
                'score_confianca',
                'status_busca',
                'observacoes',
            ]

            for col in output_columns:
                if col not in df.columns:
                    df[col] = ""

            total = len(df)

            for idx, row in df.iterrows():
                if not self.is_running:
                    logger.info("Processamento interrompido pelo usuário")
                    break

                try:
                    result = self._process_contact(row)
                    for key, value in result.items():
                        df.at[idx, key] = value

                    if status_callback:
                        status_callback(f"Processado: {row.get('nome', 'N/A')}")

                except Exception as e:
                    logger.error(f"Erro ao processar contato {idx}: {e}")
                    df.at[idx, 'status_busca'] = 'erro'
                    df.at[idx, 'observacoes'] = str(e)

                finally:
                    if progress_callback:
                        progress_callback((idx + 1) / total * 100)

            self.is_running = False
            logger.info("Enriquecimento concluído")
            return df

        except Exception as e:
            logger.error(f"Erro no enriquecimento: {e}")
            self.is_running = False
            return df

    def _process_contact(self, row: Dict) -> Dict:
        result = {
            'linkedin_encontrado': '',
            'empresa_atual': '',
            'cargo_atual': '',
            'score_confianca': 0.0,
            'status_busca': 'pendente',
            'observacoes': '',
        }

        is_valid, error_msg = DataValidator.validate_row(row)
        if not is_valid:
            result['status_busca'] = 'erro'
            result['observacoes'] = error_msg
            return result

        nome = DataValidator.clean_text(row.get('nome', ''))
        empresa = DataValidator.clean_text(row.get('empresa', ''))
        cargo = DataValidator.clean_text(row.get('cargo', ''))
        linkedin_url = DataValidator.clean_text(row.get('linkedin', ''))

        if linkedin_url and LinkedInValidator.is_valid_linkedin_url(linkedin_url):
            return self._process_existing_linkedin(linkedin_url, nome, result)

        return self._search_linkedin_profile(nome, empresa, cargo, result)

    def _process_existing_linkedin(
        self,
        url: str,
        name: str,
        result: Dict,
    ) -> Dict:
        try:
            url = LinkedInValidator.normalize_linkedin_url(url)
            cached = self.cache.get(name)

            if cached and cached.get('url') == url:
                return {**result, **cached}

            profile = self.search_service.extract_profile_info(url)

            if profile:
                self.cache.set(name, {
                    'linkedin_encontrado': url,
                    'empresa_atual': profile.get('company', ''),
                    'cargo_atual': profile.get('title', ''),
                    'status_busca': 'encontrado',
                })

                return {
                    **result,
                    'linkedin_encontrado': url,
                    'empresa_atual': profile.get('company', ''),
                    'cargo_atual': profile.get('title', ''),
                    'score_confianca': 1.0,
                    'status_busca': 'encontrado',
                }
            else:
                return {
                    **result,
                    'linkedin_encontrado': url,
                    'status_busca': 'url_invalida',
                    'observacoes': 'URL não retornou informações válidas',
                }

        except Exception as e:
            logger.error(f"Erro ao processar LinkedIn existente: {e}")
            return {
                **result,
                'status_busca': 'erro',
                'observacoes': str(e),
            }

    def _search_linkedin_profile(
        self,
        nome: str,
        empresa: str,
        cargo: str,
        result: Dict,
    ) -> Dict:
        try:
            cached = self.cache.get(nome, empresa, cargo)
            if cached:
                logger.debug(f"Usando cache para {nome}")
                return {**result, **cached}

            search_results = self.search_service.search_linkedin_profile(nome, empresa, cargo)

            if not search_results:
                return {
                    **result,
                    'status_busca': 'nao_encontrado',
                    'observacoes': 'Nenhum perfil encontrado',
                }

            best_match = None
            best_score = 0.0

            for search_result in search_results:
                profile = self.search_service.extract_profile_info(search_result['url'])
                if not profile:
                    continue

                is_match, score = self.search_service.validate_profile_match(
                    profile,
                    nome,
                    empresa,
                    cargo,
                )

                if score > best_score:
                    best_score = score
                    best_match = (profile, score)

            if best_match:
                profile, score = best_match
                cached_data = {
                    'linkedin_encontrado': profile['url'],
                    'empresa_atual': profile.get('company', ''),
                    'cargo_atual': profile.get('title', ''),
                    'score_confianca': round(score, 3),
                    'status_busca': 'encontrado' if score >= 0.5 else 'duvidoso',
                }

                self.cache.set(nome, cached_data, empresa, cargo)
                return {**result, **cached_data}

            return {
                **result,
                'status_busca': 'nao_encontrado',
                'observacoes': 'Nenhum perfil com score suficiente',
            }

        except Exception as e:
            logger.error(f"Erro na busca de perfil para {nome}: {e}")
            return {
                **result,
                'status_busca': 'erro',
                'observacoes': str(e),
            }

    def stop_processing(self) -> None:
        self.is_running = False
        logger.info("Parada de processamento solicitada")

    def export_spreadsheet(self, df: pd.DataFrame, output_path: str) -> bool:
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if output_path.suffix.lower() == '.csv':
                df.to_csv(output_path, index=False, encoding='utf-8')
            else:
                df.to_excel(output_path, index=False, engine='openpyxl')

            logger.info(f"Planilha exportada: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao exportar planilha: {e}")
            return False
