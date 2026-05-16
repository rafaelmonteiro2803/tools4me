# 🚀 Quick Start Guide

Comece em 5 minutos!

## 1️⃣ Instalação (2 minutos)

```bash
# Clone ou navegue até o projeto
cd tools4me

# Crie ambiente virtual (Python 3.11+)
python -m venv venv

# Ative (Windows)
venv\Scripts\activate

# Ative (Linux/Mac)
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

## 2️⃣ Prepare seu arquivo (1 minuto)

**Opção A: Use o exemplo**
```bash
# Já temos um arquivo de exemplo em examples/sample_input.csv
```

**Opção B: Crie seu próprio**

Crie um arquivo `contacts.csv`:
```csv
nome,empresa,cargo,linkedin
João Silva,Google,Engenheiro,
Maria Santos,Meta,Gerente,https://linkedin.com/in/maria-santos
Pedro Costa,Amazon,Arquiteto,
```

## 3️⃣ Execute a aplicação (1 minuto)

```bash
python app.py
```

A interface gráfica abrirá automaticamente.

## 4️⃣ Use a interface (1 minuto)

1. **Selecionar Arquivo**
   - Clique em "Selecionar Arquivo"
   - Escolha seu `contacts.csv`
   - Veja o preview dos dados

2. **Iniciar Busca**
   - Clique em "▶ Iniciar Busca"
   - Acompanhe o progresso
   - Espere conclusão

3. **Exportar Resultados**
   - Clique em "💾 Exportar"
   - Escolha local para salvar
   - Arquivo pronto para usar!

## 📊 Resultado Esperado

Seu arquivo enriquecido terá:

```csv
nome,empresa,cargo,linkedin,linkedin_encontrado,empresa_atual,cargo_atual,score_confianca,status_busca,observacoes
João Silva,Google,Engenheiro,,https://linkedin.com/in/joao-silva,Google,Senior Software Engineer,0.92,encontrado,
Maria Santos,Meta,Gerente,https://linkedin.com/in/maria-santos,https://linkedin.com/in/maria-santos,Meta,Product Manager,1.0,encontrado,
Pedro Costa,Amazon,Arquiteto,,https://linkedin.com/in/pedro-costa,Amazon Web Services,Solutions Architect,0.85,encontrado,
```

## ✅ Checklist

- [ ] Python 3.11+ instalado
- [ ] Dependências instaladas
- [ ] Arquivo de entrada pronto (CSV ou Excel)
- [ ] Arquivo contém coluna "nome"
- [ ] Aplicação rodando sem erros

## 🎯 Próximos Passos

### Otimizar Performance
```python
# Em config/settings.py, ajuste:
SEARCH_CONFIG = {
    "max_threads": 10,        # Aumente para mais threads
    "timeout": 15,            # Aumente se tiver conexão lenta
    "delay_min": 0.5,         # Reduza delays
    "delay_max": 1.5,
}
```

### Melhorar Precisão
```python
MATCH_CONFIG = {
    "min_confidence": 0.7,    # Exija scores mais altos
    "name_weight": 0.5,       # Priorize nome
}
```

### Integrar com Ferramentas
- [ ] Exportar para Google Sheets
- [ ] Sincronizar com HubSpot
- [ ] Enviar para Slack
- [ ] Importar de Salesforce

## 📚 Documentação

- **README.md**: Documentação completa
- **DEPLOYMENT.md**: Como fazer deploy
- **ARCHITECTURE.md**: Design do sistema
- **ADVANCED_GUIDE.md**: Tópicos avançados

## 🐛 Solução Rápida de Problemas

**Erro: "ModuleNotFoundError: customtkinter"**
```bash
pip install customtkinter
```

**Erro: "No column named 'nome'"**
```
Certifique-se que seu arquivo tem a coluna "nome"
(case-sensitive, sem acentos extras)
```

**Aplicação lenta**
```
1. Reduza max_threads em config/settings.py
2. Aumente delays entre requisições
3. Verifique sua internet
```

**Arquivo não abre**
```
1. Verifique extensão (.csv ou .xlsx)
2. Converta para UTF-8 se necessário
3. Remova caracteres especiais dos nomes
```

## 💡 Dicas

1. **Primeiro teste**: Use o arquivo de exemplo
2. **Com muitos contatos**: Processe em lotes de 100
3. **Para produção**: Habilite cache para reutilizar resultados
4. **Performance**: Aumente threads gradualmente

## 📞 Suporte Rápido

```bash
# Testar instalação
python test_setup.py

# Ver logs
tail -f logs/app.log

# Limpar cache
rm data/search_cache.json
```

## 🎓 Exemplo Completo

```bash
# 1. Prepare ambiente
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Teste instalação
python test_setup.py

# 3. Inicie aplicação
python app.py

# 4. Na GUI:
#    - Selecione examples/sample_input.csv
#    - Clique "▶ Iniciar Busca"
#    - Espere 2-5 minutos
#    - Clique "💾 Exportar"
#    - Abra arquivo gerado

# 5. Veja resultados em data/enriquecido.xlsx
```

## 🔒 Segurança

- ✅ Sem necessidade de login
- ✅ Sem armazenamento de credenciais
- ✅ Cache local (não envia dados)
- ✅ HTTPS por padrão

## 📈 Dados Esperados

| Métrica | Valor |
|---------|-------|
| Tempo por contato | 30-60s |
| Taxa de sucesso | 60-80% |
| Score médio | 0.65-0.75 |
| Memória usada | 50-100MB |

---

**Dúvidas?** Veja a [documentação completa](README.md)

**Pronto para começar!** 🎉
