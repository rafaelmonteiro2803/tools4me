# Guia Avançado - LinkedIn Data Enrichment Tool

## 📚 Tópicos Avançados

### 1. Customização da Busca

#### Ajustar Scoring

Edite `config/settings.py`:

```python
MATCH_CONFIG = {
    "min_confidence": 0.6,      # Aumenta exigência
    "name_weight": 0.5,         # Prioriza nome
    "company_weight": 0.25,
    "title_weight": 0.25,
}
```

#### Adicionar Regras de Busca

Em `src/services/search_service.py`:

```python
def _build_search_query(self, name: str, company: str = "", title: str = "") -> str:
    # Adicione lógica customizada
    if company and "inc" in company.lower():
        query += " incorporated"
    return query
```

#### Implementar Busca com API Real

```python
from linkedin_api import Linkedin

class LinkedInAPIService:
    def __init__(self, username, password):
        self.linkedin = Linkedin(username, password)
    
    def search_profile(self, name: str) -> Dict:
        results = self.linkedin.search_people(name=name, limit=1)
        return results[0] if results else None
```

### 2. Otimizações de Performance

#### Cache Distribuído com Redis

```python
import redis

class DistributedCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def get(self, key: str):
        return json.loads(self.redis.get(key) or '{}')
    
    def set(self, key: str, value: dict):
        self.redis.setex(key, 3600 * 24, json.dumps(value))
```

#### Processamento em Background com Celery

```python
from celery import Celery

app = Celery('linkedin_enrichment')

@app.task
def enrich_contact_async(contact_id: int):
    processor = DataProcessor()
    # Processar assincrono
    return processor.process_contact(contact_id)
```

#### Pool de Conexões

```python
from concurrent.futures import ThreadPoolExecutor

class OptimizedSearchService(SearchService):
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def search_batch(self, contacts: List[Dict]):
        futures = [
            self.executor.submit(self.search_linkedin_profile, c['nome'])
            for c in contacts
        ]
        return [f.result() for f in futures]
```

### 3. Análise de Dados e Métricas

#### Dashboard de Análise

```python
import matplotlib.pyplot as plt

class AnalyticsDashboard:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def plot_confidence_distribution(self):
        plt.hist(self.df['score_confianca'], bins=20)
        plt.title('Distribuição de Scores')
        plt.show()
    
    def get_success_rate(self) -> float:
        found = len(self.df[self.df['status_busca'] == 'encontrado'])
        return found / len(self.df) * 100
```

#### Exportar Métricas

```python
def export_metrics(df: pd.DataFrame) -> Dict:
    return {
        "total_contacts": len(df),
        "found": len(df[df['status_busca'] == 'encontrado']),
        "avg_confidence": df['score_confianca'].mean(),
        "processing_time": df['processing_time'].sum(),
        "success_rate": (len(df[df['status_busca'] == 'encontrado']) / len(df) * 100),
    }
```

### 4. Validações Avançadas

#### Validação de Email

```python
import re

class EmailValidator:
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def is_valid(email: str) -> bool:
        return bool(EmailValidator.EMAIL_PATTERN.match(email))
    
    @staticmethod
    def suggest_email(name: str, company: str) -> str:
        # Gera email provável
        last_name = name.split()[-1].lower()
        company_domain = company.lower().replace(' ', '')
        return f"{last_name}@{company_domain}.com"
```

#### Validação Geográfica

```python
from geopy.geocoders import Nominatim

class LocationValidator:
    def __init__(self):
        self.geocoder = Nominatim(user_agent="linkedin-enrichment")
    
    def validate_location(self, city: str, country: str) -> bool:
        try:
            location = self.geocoder.geocode(f"{city}, {country}")
            return location is not None
        except:
            return False
```

### 5. Integração com Ferramentas Externas

#### Google Sheets API

```python
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import gspread

def export_to_google_sheets(df: pd.DataFrame, sheet_id: str):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    gc = gspread.authorize(credentials)
    
    sheet = gc.open_by_key(sheet_id).sheet1
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
```

#### Integração com Slack

```python
from slack_sdk import WebClient

def notify_completion(slack_token: str, channel: str, metrics: Dict):
    client = WebClient(token=slack_token)
    
    message = f"""
    LinkedIn Enrichment Completed!
    Total: {metrics['total_contacts']}
    Found: {metrics['found']}
    Success Rate: {metrics['success_rate']:.1f}%
    """
    
    client.chat_postMessage(channel=channel, text=message)
```

#### Integração com HubSpot

```python
from hubspot.crm.contacts import ApiClient

def sync_to_hubspot(df: pd.DataFrame, api_key: str):
    client = ApiClient(api_key=api_key)
    
    for _, row in df.iterrows():
        contact = {
            "properties": {
                "firstname": row['nome'].split()[0],
                "lastname": row['nome'].split()[-1],
                "linkedinbio": row['linkedin_encontrado'],
                "jobtitle": row['cargo_atual'],
                "company": row['empresa_atual'],
            }
        }
        client.create_contact(contact)
```

### 6. Tratamento Avançado de Erros

#### Retry com Backoff Exponencial

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def fetch_with_retry(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response
```

#### Circuit Breaker

```python
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def search_linkedin(name: str):
    # Se falhar 5 vezes em 60s, para de tentar
    return SearchService().search_linkedin_profile(name)
```

### 7. Testes Automatizados

#### Unit Tests

```python
import unittest
from src.utils.validators import SimilarityValidator

class TestSimilarity(unittest.TestCase):
    def test_name_similarity(self):
        result = SimilarityValidator.name_similarity("John Silva", "João Silva")
        self.assertGreater(result, 0.7)
    
    def test_string_similarity(self):
        result = SimilarityValidator.string_similarity("google", "Google Inc")
        self.assertGreater(result, 0.5)

if __name__ == '__main__':
    unittest.main()
```

#### Integration Tests

```python
def test_full_enrichment_flow():
    processor = DataProcessor()
    df = processor.load_spreadsheet('examples/sample_input.csv')
    
    enriched = processor.enrich_contacts(df)
    
    assert len(enriched) > 0
    assert 'linkedin_encontrado' in enriched.columns
    assert enriched['score_confianca'].max() > 0
```

### 8. Logging Avançado

#### Correlação de Requisições

```python
import uuid

class RequestLogger:
    def __init__(self):
        self.request_id = str(uuid.uuid4())
        self.logger = get_logger(__name__)
    
    def log(self, message: str):
        self.logger.info(f"[{self.request_id}] {message}")
```

#### Logging Estruturado

```python
import json

class StructuredLogger:
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def log_event(self, event_name: str, **kwargs):
        log_data = {
            "event": event_name,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.logger.info(json.dumps(log_data))
```

### 9. Configuração Dinâmica

#### Arquivo de Configuração YAML

```yaml
# config.yaml
app:
  title: "LinkedIn Enrichment"
  version: "1.0.0"

search:
  max_threads: 5
  timeout: 10
  retry_attempts: 3

matching:
  min_confidence: 0.5
  weights:
    name: 0.4
    company: 0.35
    title: 0.25
```

#### Carregador de Configuração

```python
import yaml

class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
```

### 10. Otimização de Memória

#### Processamento em Chunks

```python
def process_large_file(file_path: str, chunk_size: int = 100):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield processor.enrich_contacts(chunk)
```

#### Limpeza de Memória

```python
import gc

def cleanup_memory():
    gc.collect()
    logger.info(f"Memória liberada")

# Use em intervalos
import atexit
atexit.register(cleanup_memory)
```

## 🎯 Melhores Práticas

### 1. Code Organization
- Use type hints em todas as funções
- Separar lógica de negócio de interface
- Usar padrões de design (Factory, Strategy)

### 2. Performance
- Cache agressivo para buscas repetidas
- Processamento paralelo onde possível
- Monitorar uso de memória

### 3. Segurança
- Validar entrada do usuário
- Usar variáveis de ambiente para senhas
- Implementar rate limiting
- Log de atividades suspeitas

### 4. Manutenibilidade
- Documentar funções complexas
- Manter testes atualizados
- Usar versionamento semântico
- Fazer code reviews

### 5. Escalabilidade
- Design para processar em batch
- Implementar fila de tarefas
- Cache distribuído
- Múltiplas instâncias

## 📊 Monitoramento de Produção

### Métricas Importantes

```python
class ProductionMonitor:
    def __init__(self):
        self.metrics = {
            "requests_per_minute": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "cache_hit_rate": 0,
        }
    
    def report(self) -> Dict:
        return self.metrics
```

### Alertas

- Taxa de erro > 5%
- Tempo de resposta > 30s
- Cache > 1GB
- Memória > 80%

## 🔧 Troubleshooting Avançado

### Profile de Código

```python
import cProfile

def profile_enrichment():
    profiler = cProfile.Profile()
    profiler.enable()
    
    processor = DataProcessor()
    processor.enrich_contacts(df)
    
    profiler.disable()
    profiler.print_stats(sort='cumulative')
```

### Debug Mode

```python
# Ativa debug detalhado
import logging
logging.basicConfig(level=logging.DEBUG)

# No código
if DEBUG:
    logger.debug(f"Variable state: {variable}")
```

---

**Versão**: 1.0.0  
**Última atualização**: 2024
