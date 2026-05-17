#!/usr/bin/env python3
"""
Wrapper para compatibilidade com Render.
O Render procura por 'app:app' por padrão.
Este arquivo apenas importa e expõe a aplicação Flask de app_api.
"""
from app_api import app

if __name__ == "__main__":
    app.run()
