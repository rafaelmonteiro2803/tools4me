# Arquitetura - LinkedIn Data Enrichment Tool

## 🏗️ Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    GUI Layer (CustomTkinter)                 │
│              main_window.py - Interface Responsiva            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Application Layer                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          DataProcessor - Orquestração                │   │
│  │  - Load/Save planilhas                              │   │
│  │  - Coordenar buscas                                 │   │
│  │  - Gerenciar processamento                          │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Service Layer                                 │
│  ┌────────────────────┐  ┌──────────────────────────────┐   │
│  │  SearchService     │  │     Cache Management         │   │
│  │  - Web Search      │  │  - LocalCache                │   │
│  │  - Profile Extract │  │  - Deduplication             │   │
│  │  - Validation      │  │  - Performance Optimization  │   │
│  └────────────────────┘  └──────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Utility/Support Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │  Logger      │  │  Validators  │  │  Cache Engine  │    │
│  │  - Logging   │  │  - Similarity│  │  - JSON Store  │    │
│  │  - Tracking  │  │  - LinkedIn  │  │  - Hash Index  │    │
│  │  - Audit     │  │  - Data      │  │  - Expiration  │    │
│  └──────────────┘  └──────────────┘  └────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│           External Services & Libraries                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │  Requests    │  │  BeautifulSoup│ │  Pandas        │    │
│  │  - HTTP      │  │  - HTML Parse │ │  - DataFrame   │    │
│  │  - Retry     │  │  - Scraping   │ │  - Export      │    │
│  │  - Rate Limit│  │               │ │  - Import      │    │
│  └──────────────┘  └──────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Estrutura de Pastas

```
tools4me/
├── app.py                          # Entry point
├── requirements.txt                # Dependências
├── config/
│   ├── __init__.py
│   └── settings.py                # Configurações centralizadas
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Inicialização
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   └── main_window.py         # Interface Tkinter
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search_service.py      # Serviço de busca web
│   │   └── data_processor.py      # Processador de dados
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py              # Sistema de logging
│       ├── cache.py               # Cache local
│       └── validators.py          # Validadores
│
├── data/                           # Arquivos de dados
├── logs/                           # Logs de execução
├── examples/
│   ├── sample_input.csv           # Entrada de exemplo
│   └── sample_output.csv          # Saída esperada
│
├── README.md                       # Documentação principal
├── DEPLOYMENT.md                   # Guia de deployment
├── ARCHITECTURE.md                 # Este arquivo
├── ADVANCED_GUIDE.md               # Tópicos avançados
└── .gitignore
```

## 🔄 Fluxo de Dados

### 1. Carregamento de Arquivo

```
[Usuário Seleciona Arquivo]
         │
         ▼
    [main_window.py::_select_file()]
         │
         ▼
    [DataProcessor::load_spreadsheet()]
         │
    ┌────┴─────────────────────┐
    │                           │
    ▼                           ▼
[CSV]                      [XLSX]
    │                           │
    └────┬─────────────────────┘
         │
         ▼
[Pandas DataFrame]
         │
         ▼
[Normalizar Colunas]
         │
         ▼
[Cache Preview]
```

### 2. Enriquecimento de Dados

```
[Iniciar Busca]
       │
       ▼
[DataProcessor::enrich_contacts()]
       │
       ├─► [Verificar Cache] ──┐
       │                       │
       │       ┌───────────────┘
       │       ▼ (encontrado)
       │   [Retornar Cached]
       │
       ├─► (não encontrado)
       │   [SearchService::search_linkedin_profile()]
       │   │
       │   ├─► [Validar URL Existente]
       │   │   │
       │   │   ▼
       │   │ [extract_profile_info()]
       │   │
       │   └─► [Buscar por Nome+Empresa]
       │       │
       │       ▼
       │   [_google_search()]
       │       │
       │       ▼
       │   [Parsear Resultados]
       │       │
       │       ▼
       │   [extract_profile_info() para cada]
       │       │
       │       ▼
       │   [SimilarityValidator::calculate_confidence_score()]
       │       │
       │       ▼
       │   [Selecionar Melhor Match]
       │
       ▼
[Salvar no Cache]
       │
       ▼
[Atualizar DataFrame]
       │
       ▼
[Próximo Contato]
```

### 3. Exportação de Resultados

```
[Usuário Clica Exportar]
         │
         ▼
[main_window.py::_export_results()]
         │
         ▼
[DataProcessor::export_spreadsheet()]
         │
    ┌────┴──────────────────────┐
    │                           │
    ▼                           ▼
[CSV]                      [XLSX]
    │                           │
    │       [openpyxl]          │
    │                           │
    └────┬──────────────────────┘
         │
         ▼
[Arquivo Salvo]
         │
         ▼
[Notificação ao Usuário]
```

## 🧩 Componentes Detalhados

### GUI Layer (main_window.py)

**Responsabilidades:**
- Renderizar interface de usuário
- Capturar entrada do usuário
- Exibir progresso e logs
- Coordenar callbacks

**Classes principais:**
- `LinkedInEnrichmentApp`: Janela principal com CustomTkinter

**Método chave:**
- `_setup_ui()`: Inicializa layout
- `_start_enrichment()`: Inicia processamento em thread
- `_log()`: Exibe mensagens em tempo real

### Application Layer (data_processor.py)

**Responsabilidades:**
- Orquestrar fluxo de processamento
- Gerenciar cache
- Controlar threading

**Classes principais:**
- `DataProcessor`: Orquestrador principal

**Métodos chave:**
```python
load_spreadsheet()          # Carrega arquivo
enrich_contacts()           # Loop principal de enriquecimento
_process_contact()          # Processa um contato
export_spreadsheet()        # Salva resultado
```

### Service Layer (search_service.py)

**Responsabilidades:**
- Buscar perfis no LinkedIn
- Extrair informações
- Validar matches

**Classes principais:**
- `SearchService`: Gerencia buscas web

**Métodos chave:**
```python
search_linkedin_profile()   # Busca principal
_google_search()            # Busca Google
extract_profile_info()      # Extrai dados
validate_profile_match()    # Valida similaridade
```

### Utility Layer (validators.py, cache.py, logger.py)

**SimilarityValidator:**
- `string_similarity()`: Compara strings
- `name_similarity()`: Compara nomes (Jaccard)
- `calculate_confidence_score()`: Score ponderado

**LocalCache:**
- `get()`: Recupera do cache
- `set()`: Armazena no cache
- `_generate_key()`: Cria chave hash

**Logger:**
- Configuração centralizada
- Múltiplos handlers (console, arquivo)

## 🔐 Padrões de Design

### 1. Singleton Pattern
- `Logger`: Uma única instância por módulo
- `LocalCache`: Uma instância por aplicação

### 2. Factory Pattern
- `SearchService`: Cria instâncias de Session
- `DataProcessor`: Cria instâncias de Cache

### 3. Strategy Pattern
- `SimilarityValidator`: Diferentes estratégias de validação
- Plugável para novas estratégias

### 4. Observer Pattern
- `progress_callback`: GUI observa progresso
- `status_callback`: Logs observam status

## 📊 Fluxo de Processamento Detalhado

### Processamento de Um Contato

```python
Contact = {
    'nome': 'João Silva',
    'empresa': 'Google',
    'cargo': 'Engenheiro',
    'linkedin': ''
}

# 1. Validação
if not validate_row(Contact):
    return error_result

# 2. Verificar Cache
cached = cache.get('João Silva', 'Google', 'Engenheiro')
if cached:
    return cached

# 3. Decidir Estratégia
if Contact['linkedin']:
    # Cenário 1: URL existente
    return process_existing_linkedin(url)
else:
    # Cenário 2: Buscar por nome
    return search_linkedin_profile(name, company, title)

# 4. Buscar
results = google_search("João Silva Google site:linkedin.com/in")

# 5. Extrair e Validar
for result in results:
    profile = extract_profile_info(result['url'])
    score = validate_profile_match(profile, name, company, title)
    
    if score > best_score:
        best_match = (profile, score)

# 6. Salvar no Cache
if best_match:
    cache.set(name, best_match_data)

# 7. Retornar Resultado
return {
    'linkedin_encontrado': url,
    'empresa_atual': company,
    'cargo_atual': title,
    'score_confianca': score,
    'status_busca': 'encontrado',
}
```

## 🔗 Integração de Componentes

### MainWindow → DataProcessor

```python
# Callback de progresso
def update_progress(percentage):
    self.progress_var.set(percentage / 100)

processor.enrich_contacts(
    df,
    progress_callback=update_progress,
    status_callback=self._log,
)
```

### DataProcessor → SearchService

```python
# Dentro de _process_contact()
search_results = self.search_service.search_linkedin_profile(
    nome, empresa, cargo
)

# Validar resultado
is_match, score = self.search_service.validate_profile_match(
    profile, nome, empresa, cargo
)
```

### DataProcessor → LocalCache

```python
# Verificar cache
cached = self.cache.get(nome, empresa, cargo)

# Armazenar resultado
self.cache.set(nome, result_data, empresa, cargo)
```

## 🚀 Threading Model

```
┌─────────────────────────────────────┐
│    Main Thread (GUI)                 │
│ - Renderiza UI                       │
│ - Captura eventos                    │
│ - Exibe logs                         │
└────────────┬────────────────────────┘
             │
             │ Thread.start()
             │
             ▼
┌────────────────────────────────────┐
│  Worker Thread (Processamento)      │
│ - enrich_contacts()                 │
│ - SearchService.search()            │
│ - Cache.set()                       │
│                                     │
│ Callbacks:                          │
│ - progress_callback()               │
│ - status_callback()                 │
└────────────┬────────────────────────┘
             │
             │ queue.put(update)
             │
             ▼
┌────────────────────────────────────┐
│  Main Thread (Recebe atualizações)  │
│ - Update progress bar               │
│ - Log message                       │
│ - UI refresh                        │
└────────────────────────────────────┘
```

## 📈 Escalabilidade

### Atual (Single Thread)
- ~1-2 contatos por minuto
- Limitado por rate limiting

### Otimizada (Multi Thread)
- 5 threads = ~5-10 contatos/minuto
- Limitado por cache

### Escalada (Com Fila)
- Celery + Redis
- Múltiplas workers
- 100+ contatos/minuto

## 🔍 Pontos de Extensão

### 1. Novos Serviços de Busca
```python
class LinkedInAPIService(SearchService):
    def search_linkedin_profile(self, name: str):
        # Usar API oficial ao invés de scraping
        pass
```

### 2. Novos Validadores
```python
class AdvancedValidator:
    def validate_with_email(self, profile, email):
        # Validar usando email também
        pass
```

### 3. Novos Formatos de Entrada
```python
class JSONDataProcessor(DataProcessor):
    def load_spreadsheet(self, file_path):
        # Suportar JSON
        pass
```

### 4. Novos Destinos de Exportação
```python
def export_to_google_sheets(df):
    # Exportar para Google Sheets
    pass

def export_to_hubspot(df):
    # Sincronizar com HubSpot
    pass
```

## 📊 Métricas Chave

**Performance:**
- Tempo por contato: ~30-60 segundos
- Taxa de sucesso: ~60-80%
- Score médio: ~0.65-0.75

**Recursos:**
- Memória: ~50-100 MB
- Disco: ~10-50 MB (cache)
- Banda: ~1-2 KB por requisição

**Confiabilidade:**
- Uptime: 99%+ com retry
- Taxa de erro: <5%
- Completude: >95%

## 🔄 Ciclo de Vida

```
[App Iniciada]
    │
    ▼
[Cache Carregado]
    │
    ▼
[GUI Renderizada]
    │
    ├─► [Usuário Interage] ────┐
    │                          │
    │   ┌──────────────────────┘
    │   │
    │   ▼
    │ [Arquivo Carregado]
    │   │
    │   ▼
    │ [Processamento Iniciado]
    │   │
    │   ├─► [Contato Processado]
    │   │
    │   └─► [Loop até fim]
    │
    │   ▼
    │ [Resultado Exportado]
    │
    ▼
[App Fechada]
    │
    ▼
[Cache Salvo]
```

---

**Versão**: 1.0.0  
**Padrão**: Clean Architecture + Layered Architecture  
**Última atualização**: 2024
