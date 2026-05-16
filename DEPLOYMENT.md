# Guia de Deployment

## 🚀 Deployment no Render

### Pré-requisitos

- Conta no [Render.com](https://render.com)
- Repositório GitHub com o código

### Passos

1. **Conecte seu repositório ao Render**
   - Acesse https://render.com
   - Clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório GitHub

2. **Configure o serviço**
   - **Name**: `linkedin-enrichment-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (ou pago conforme necessário)

3. **Configure variáveis de ambiente**
   - `PYTHONUNBUFFERED=1`
   - `LOG_LEVEL=INFO`

4. **Configure disco persistente** (para cache)
   - Clique em "Environment"
   - Adicione um disco
   - Mount Path: `/app/data`
   - Size: 1 GB

5. **Deploy**
   - Clique em "Deploy"
   - Aguarde construção (5-10 minutos)

### URL de acesso

Após o deploy, sua aplicação estará em:
```
https://linkedin-enrichment-app.onrender.com
```

## 🐳 Deployment com Docker

### Build local

```bash
docker build -t linkedin-enrichment .
docker run -p 8000:8000 linkedin-enrichment
```

### Publicar no Docker Hub

```bash
docker login
docker tag linkedin-enrichment seuusuario/linkedin-enrichment:latest
docker push seuusuario/linkedin-enrichment:latest
```

### Deploy no Docker Compose

```yaml
version: '3.8'
services:
  app:
    image: linkedin-enrichment:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      LOG_LEVEL: INFO
      PYTHONUNBUFFERED: 1
```

```bash
docker-compose up -d
```

## ☁️ Deployment no Heroku

### Pré-requisitos

```bash
# Instale Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login
```

### Deploy

```bash
# Crie aplicação Heroku
heroku create linkedin-enrichment

# Configure buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku claude/web-data-enrichment-app-IboxF:main

# Veja logs
heroku logs --tail
```

## 🏃 Deployment Local com Systemd (Linux/Mac)

### Crie um serviço systemd

```ini
# /etc/systemd/system/linkedin-enrichment.service

[Unit]
Description=LinkedIn Enrichment Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/linkedin-enrichment
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/linkedin-enrichment/venv/bin/python /opt/linkedin-enrichment/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Ative o serviço

```bash
sudo systemctl daemon-reload
sudo systemctl enable linkedin-enrichment
sudo systemctl start linkedin-enrichment
sudo systemctl status linkedin-enrichment
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Render
      env:
        RENDER_DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK }}
      run: |
        curl $RENDER_DEPLOY_HOOK
```

## 📊 Monitoramento em Produção

### Logs

```bash
# Seguir logs em tempo real
tail -f logs/app.log | grep ERROR

# Analisar performance
grep "Enriquecimento concluído" logs/app.log
```

### Health Check

```bash
curl https://linkedin-enrichment-app.onrender.com/health
```

### Métricas

Monitore:
- Tempo de processamento
- Taxa de sucesso nas buscas
- Tamanho do cache
- Uso de memória

## 🔐 Segurança em Produção

1. **Variáveis de Ambiente**
   ```bash
   # Use .env.local (não commitar)
   LOG_LEVEL=WARNING
   DEBUG=False
   ```

2. **Acesso SSH**
   - Configure chaves SSH para clone de repositório

3. **Rate Limiting**
   - Ajuste delays conforme necessário
   - Monitore para bloqueios

4. **Backup do Cache**
   ```bash
   # Backup automático
   0 2 * * * cp /app/data/search_cache.json /backups/cache-$(date +%Y%m%d).json
   ```

## 🆘 Troubleshooting de Deployment

### Erro: "ModuleNotFoundError"

```bash
# Reforce instalação de dependências
pip install -r requirements.txt --upgrade
```

### Erro: "Port already in use"

```bash
# Mude a porta
PORT=8001 python app.py
```

### Erro: "No space left on device"

```bash
# Limpe cache
rm data/search_cache.json
```

### Aplicação lenta em produção

1. Aumentar timeouts
2. Reduzir concorrência
3. Implementar caching mais agressivo

## 📈 Escalabilidade

Para lidar com muitos usuários:

1. **Aumente recursos**
   - CPU: de 0.1 para 0.5-1.0
   - RAM: de 512MB para 2-4GB

2. **Implemente fila de processamento**
   - Use Celery + Redis
   - Processar em background

3. **Distribua cache**
   - Use Redis para cache compartilhado
   - CloudFlare para CDN

## 📝 Checklist pré-Deploy

- [ ] Todas as dependências em requirements.txt
- [ ] Variáveis de ambiente configuradas
- [ ] Logs em nível apropriado
- [ ] Cache configurado para persistência
- [ ] Erro handling robusto
- [ ] Timeouts configurados
- [ ] Tests passando
- [ ] README atualizado
- [ ] Dockerfile funcional
- [ ] Dados sensíveis não no código

## 🔄 Atualizações em Produção

```bash
# Faça pull da nova versão
git pull origin main

# Instale dependências atualizadas
pip install -r requirements.txt

# Reinicie o serviço
sudo systemctl restart linkedin-enrichment

# Verifique logs
tail -f logs/app.log
```

## 📞 Suporte de Deployment

Para problemas específicos de plataforma:

- **Render**: https://render.com/docs
- **Heroku**: https://devcenter.heroku.com
- **Docker**: https://docs.docker.com
- **Systemd**: https://systemd.io

---

**Última atualização**: 2024
