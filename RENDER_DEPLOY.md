# 🚀 Guia: Deploy no Render (Passo a Passo)

## ⚠️ Nota Importante

A aplicação com GUI CustomTkinter **não funciona bem em servidores headless** (sem tela).

Oferecemos **2 opções de deploy no Render:**

1. **API REST** (Recomendado) ← Use isso
2. **CLI Backend** (Sem interface)

---

## ✅ Opção 1: Deploy com API REST (Recomendado)

### Passo 1: Preparar o Repositório

Sua branch já está pronta! Certifique-se que tem:

```bash
✓ app_api.py           # API Flask
✓ requirements.txt     # Com Flask + Gunicorn
✓ Dockerfile           # Para containerização
✓ render.yaml          # Config do Render
```

### Passo 2: Push do Código para GitHub

```bash
# Certifique-se que está na branch correta
git branch

# Se não estiver:
git checkout claude/web-data-enrichment-app-IboxF

# Push (se ainda não fez)
git push origin claude/web-data-enrichment-app-IboxF
```

### Passo 3: Acessar Render.com

1. Vá para https://render.com
2. Faça login (ou crie conta grátis)
3. Clique em **"New +"** (canto superior direito)
4. Selecione **"Web Service"**

### Passo 4: Conectar Repositório GitHub

```
┌─────────────────────────────────────┐
│ Conectar Repositório                │
├─────────────────────────────────────┤
│ Clique em "Connect GitHub account"  │
│                                     │
│ Selecione: tools4me                 │
│ Branch: claude/web-data-enrichment  │
│          -app-IboxF                 │
└─────────────────────────────────────┘
```

### Passo 5: Configurar o Serviço

Preencha com esses valores:

```
Name:                    linkedin-enrichment-api
Environment:             Docker
Region:                  Oregon (usa-west)

Build Command:          (deixe em branco, usa Dockerfile)
Start Command:          (deixe em branco, usa Dockerfile)

Plan:                   Free (ou Starter+ se quer mais poder)

⭐ Important:
  Auto-Deploy:          ✓ Enabled
  Persistent Disk:      ✓ Yes
    Mount Path:         /app/data
    Size:               1 GB
```

### Passo 6: Variáveis de Ambiente

Clique em "Environment" e adicione:

```
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO
DEBUG=False
```

### Passo 7: Deploy

1. Clique em **"Create Web Service"**
2. Aguarde (5-15 minutos)
3. Você verá um link como: `https://linkedin-enrichment-api.onrender.com`

---

## 🧪 Testar a API após Deploy

### Health Check

```bash
curl https://linkedin-enrichment-api.onrender.com/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "cache_stats": {
    "total_cached": 0,
    "file_size_kb": 0
  }
}
```

### Enriquecer Arquivo

```bash
curl -X POST https://linkedin-enrichment-api.onrender.com/enrich \
  -F "file=@seu_arquivo.csv"
```

Resposta:
```json
{
  "status": "success",
  "total": 10,
  "found": 7,
  "success_rate": "70.0%",
  "output_file": "enriched_seu_arquivo.csv"
}
```

---

## 📊 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Info da API |
| `GET` | `/health` | Status |
| `POST` | `/enrich` | Enriquecer planilha |
| `GET` | `/cache/stats` | Stats do cache |
| `POST` | `/cache/clear` | Limpar cache |

---

## 💾 Fazer Upload de Arquivo

### Opção 1: cURL (terminal)

```bash
curl -X POST https://seu-url.onrender.com/enrich \
  -F "file=@contacts.csv"
```

### Opção 2: Python

```python
import requests

url = "https://seu-url.onrender.com/enrich"
files = {'file': open('contacts.csv', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### Opção 3: JavaScript/Frontend

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://seu-url.onrender.com/enrich', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🔗 Integrar com Interface Web

Você pode criar uma interface web simples para fazer upload:

```html
<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Enrichment</title>
</head>
<body>
    <h1>📊 LinkedIn Data Enrichment</h1>
    
    <input type="file" id="file" accept=".csv,.xlsx">
    <button onclick="enrichFile()">Enriquecer</button>
    
    <div id="result"></div>
    
    <script>
    const API_URL = 'https://linkedin-enrichment-api.onrender.com';
    
    async function enrichFile() {
        const file = document.getElementById('file').files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(API_URL + '/enrich', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        document.getElementById('result').innerHTML = 
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }
    </script>
</body>
</html>
```

---

## 🐛 Troubleshooting

### Build failed
```
Solução: Certifique-se que requirements.txt tem Flask e Gunicorn
pip install -r requirements.txt
```

### Application crashed
```
Solução: Verifique logs em Render dashboard
Clique no serviço → Logs → veja os erros
```

### Disco cheio
```
Solução: Limpar cache
curl -X POST https://seu-url.onrender.com/cache/clear
```

### App muito lenta
```
Solução: Upgrade para plano pago
Ou otimize config/settings.py:
  - Reduza max_threads de 5 para 3
  - Aumente delays de 1-3 para 2-5
```

---

## 📈 Monitorar em Produção

### Ver Logs
```bash
# No dashboard do Render, clique em seu serviço
# Vá até "Logs"
# Verá logs em tempo real
```

### Métricas
```bash
# Clique em seu serviço → Metrics
# Veja CPU, memória, requests
```

### Cache Status
```bash
curl https://seu-url.onrender.com/cache/stats
```

---

## 🔄 Deploy Automático

Render faz **deploy automático** a cada push na branch:

```bash
# Faça uma mudança local
git add .
git commit -m "fix: melhoria"
git push origin claude/web-data-enrichment-app-IboxF

# Render automaticamente fará novo deploy! 🚀
```

---

## 💰 Custos

| Plano | CPU | RAM | Preço |
|-------|-----|-----|-------|
| **Free** | Compartilhado | 512MB | Grátis* |
| **Starter** | 0.5 | 512MB | $7/mês |
| **Standard** | 1 | 2GB | $25/mês |

*Free: Cold starts (demora iniciar após inatividade)

**Recomendação**: Use Free para testar, passe para Starter se usar em produção.

---

## ✅ Checklist Pré-Deploy

- [ ] Branch atualizada com código
- [ ] `app_api.py` criado
- [ ] `requirements.txt` tem Flask + Gunicorn
- [ ] `Dockerfile` presente
- [ ] `render.yaml` presente
- [ ] Repositório public (ou você autorizar)
- [ ] Conta Render criada

---

## 📚 Próximos Passos

1. **Deploy feito?** Teste: `curl https://seu-url.onrender.com/health`

2. **Criar interface web?** Use exemplo HTML acima

3. **Integrar com CRM?** Use endpoints da API

4. **Quer GUI local?** Use `python app.py` no seu computador

---

## 🎯 Resumo Rápido

```bash
# 1. Se não fez push ainda:
git push origin claude/web-data-enrichment-app-IboxF

# 2. No Render:
#    - New Web Service
#    - Connect GitHub
#    - Select tools4me repo
#    - Select branch
#    - Configure (veja Passo 5)
#    - Deploy

# 3. Teste (esperando 5-15 min)
curl https://seu-url.onrender.com/health

# 4. Pronto! Use a API!
```

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Suporte**: Veja README.md e FAQ.md
