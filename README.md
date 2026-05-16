# LinkedIn Data Enrichment Tool

Uma aplicação web moderna em Python que enriquece automaticamente planilhas de contatos profissionais através de busca e extração de dados do LinkedIn.

## 🎯 Funcionalidades

- ✅ Upload de planilhas (Excel .xlsx ou CSV)
- ✅ Busca inteligente de perfis do LinkedIn
- ✅ Extração automática de empresa e cargo
- ✅ Score de confiança baseado em similaridade
- ✅ Cache local para otimizar performance
- ✅ Interface gráfica moderna e responsiva
- ✅ Processamento assíncrono sem travamento
- ✅ Logs detalhados em tempo real
- ✅ Exportação de resultados enriquecidos

## 📋 Requisitos

- Python 3.11+
- pip (gerenciador de pacotes)
- ~500MB de espaço livre em disco

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd tools4me
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Iniciar a aplicação

```bash
python app.py
```

A interface gráfica abrirá em uma nova janela.

### Fluxo de utilização

1. **Carregar Arquivo**
   - Clique em "Selecionar Arquivo"
   - Escolha um arquivo CSV ou Excel
   - Visualize os dados no preview

2. **Configurar Parâmetros** (opcional)
   - Ajuste número de threads
   - Configure timeouts
   - Defina delays entre requisições

3. **Iniciar Enriquecimento**
   - Clique em "▶ Iniciar Busca"
   - Acompanhe o progresso em tempo real
   - Os logs mostram cada ação realizada

4. **Exportar Resultados**
   - Clique em "💾 Exportar"
   - Escolha o local e formato de saída
   - Arquivo será gerado com colunas adicionais

## 📊 Estrutura de Entrada

A planilha de entrada deve conter as seguintes colunas:

| Coluna | Obrigatório | Descrição |
|--------|-------------|-----------|
| nome | ✅ | Nome completo da pessoa |
| empresa | ❌ | Empresa atual ou última empresa |
| cargo | ❌ | Cargo atual ou último cargo |
| linkedin | ❌ | URL do LinkedIn (se já conhecida) |

### Exemplo de entrada (CSV)

```csv
nome,empresa,cargo,linkedin
João Silva,Google,Engenheiro de Software,
Maria Santos,Meta,Gerente de Produto,https://linkedin.com/in/maria-santos
Pedro Costa,Amazon,Arquiteto de Solução,
```

## 📤 Estrutura de Saída

A planilha exportada contém as colunas originais + colunas enriquecidas:

| Coluna | Descrição |
|--------|-----------|
| linkedin_encontrado | URL do perfil do LinkedIn |
| empresa_atual | Empresa extraída do perfil |
| cargo_atual | Cargo extraído do perfil |
| score_confianca | Score de 0-1 indicando precisão do match |
| status_busca | Status da busca (encontrado, nao_encontrado, erro, etc) |
| observacoes | Observações adicionais sobre o processamento |

### Exemplo de saída

```csv
nome,empresa,cargo,linkedin,linkedin_encontrado,empresa_atual,cargo_atual,score_confianca,status_busca,observacoes
João Silva,Google,Engenheiro,,,,,0.0,nao_encontrado,Nenhum perfil encontrado
Maria Santos,Meta,Gerente,https://linkedin.com/in/maria-santos,https://linkedin.com/in/maria-santos,Meta,Gerente de Produto,1.0,encontrado,
```

## ⚙️ Configurações

### Parâmetros de busca

```python
SEARCH_CONFIG = {
    "max_threads": 5,              # Número máximo de threads paralelos
    "timeout": 10,                 # Timeout em segundos
    "retry_attempts": 3,           # Tentativas de busca
    "delay_min": 1,                # Delay mínimo entre requisições
    "delay_max": 3,                # Delay máximo entre requisições
    "rate_limit_requests": 50,     # Requisições por janela
    "rate_limit_window": 60,       # Janela em segundos
}
```

### Scoring de confiança

```python
MATCH_CONFIG = {
    "min_confidence": 0.5,         # Score mínimo para considerar match
    "name_weight": 0.4,            # Peso do nome no score
    "company_weight": 0.35,        # Peso da empresa no score
    "title_weight": 0.25,          # Peso do cargo no score
}
```

## 📁 Estrutura do Projeto

```
tools4me/
├── app.py                          # Ponto de entrada
├── requirements.txt                # Dependências
├── README.md                       # Este arquivo
├── config/
│   └── settings.py                # Configurações da aplicação
├── src/
│   ├── main.py                    # Inicialização
│   ├── gui/
│   │   └── main_window.py         # Interface gráfica
│   ├── services/
│   │   ├── search_service.py      # Serviço de busca web
│   │   └── data_processor.py      # Processamento de dados
│   └── utils/
│       ├── logger.py              # Sistema de logging
│       ├── cache.py               # Cache local
│       └── validators.py          # Validadores e similaridade
├── data/                           # Pasta para planilhas
├── logs/                           # Logs de execução
└── examples/
    └── sample_input.csv           # Exemplo de entrada
```

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Arquivo não carrega
- Verifique se o arquivo é válido (CSV ou XLSX)
- Certifique-se que contém a coluna "nome"
- Tente converter para UTF-8 se houver problemas com encoding

### Busca muito lenta
- Aumente o delay entre requisições
- Reduza o número de threads
- Verifique sua conexão de internet

### Cache ocupando muito espaço
- Clique em "🗑 Limpar Cache" na interface
- Ou delete manualmente: `data/search_cache.json`

## 📊 Logs

Os logs são salvos em `logs/app.log` e também exibidos na interface.

Níveis de log:
- **INFO**: Informações importantes
- **DEBUG**: Detalhes técnicos
- **ERROR**: Erros durante processamento
- **CRITICAL**: Erros críticos da aplicação

## 🔒 Segurança

- Sem necessidade de autenticação no LinkedIn
- Sem armazenamento de credenciais
- Busca baseada em mecanismo de pesquisa público
- Cache local (não envia dados para nuvem)
- Não coleta dados pessoais além do necessário

## 🚀 Performance

- **Cache local**: Reduz tempo em buscas repetidas
- **Threading assíncrono**: Não trava a interface
- **Rate limiting**: Evita bloqueios por excesso de requisições
- **Delays randômicos**: Simula comportamento humano

Tempo estimado:
- 50 contatos: 5-10 minutos
- 100 contatos: 10-20 minutos
- 500 contatos: 50-100 minutos

## 📈 Métricas

A aplicação gera métricas úteis:
- Total de contatos processados
- Taxa de sucesso
- Score médio de confiança
- Tempo total de processamento
- Tamanho do cache local

## 🔄 Atualizações Futuras

- [ ] Integração com API real do LinkedIn
- [ ] Suporte a múltiplas planilhas em batch
- [ ] Dashboard com gráficos de análise
- [ ] Exportação para Google Sheets
- [ ] Validação de emails
- [ ] Busca por telefone
- [ ] Interface web (Streamlit)
- [ ] Docker para deployment

## 📝 Licença

Este projeto é fornecido como-está para fins educacionais e corporativos.

## 👨‍💻 Autor

Desenvolvido como uma solução profissional de enriquecimento de dados.

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique os logs em `logs/app.log`
2. Consulte o README
3. Abra uma issue no repositório

## 📚 Exemplos de Uso

### Exemplo 1: Enriquecer lista de contatos Google

```bash
# 1. Exporte contatos do Google como CSV
# 2. Coloque em data/contacts.csv
# 3. Execute: python app.py
# 4. Clique "Selecionar Arquivo" → escolha contacts.csv
# 5. Clique "▶ Iniciar Busca"
# 6. Espere conclusão
# 7. Clique "💾 Exportar" → salve como contacts_enriquecidos.xlsx
```

### Exemplo 2: Validar dados de CRM

```bash
# Mesmo fluxo, mas use dados de CRM como entrada
# Score de confiança ajudará a validar dados duplicados
```

## ⚠️ Aviso Legal

- Respeite os Termos de Serviço do LinkedIn
- Use apenas para fins legítimos
- Não use para spam ou atividades ilegais
- Sempre obtenha consentimento dos contatos

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Python**: 3.11+
