#!/usr/bin/env python3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.data_processor import DataProcessor
from src.utils.logger import get_logger
from config.settings import DATA_DIR

logger = get_logger(__name__)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = DATA_DIR

processor = DataProcessor()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'cache_stats': processor.cache.get_stats(),
    })

@app.route('/enrich', methods=['POST'])
def enrich():
    """Enriquecer planilha"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Arquivo não fornecido'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400

        filename = secure_filename(file.filename)
        file_path = app.config['UPLOAD_FOLDER'] / filename
        file.save(file_path)

        logger.info(f"Processando arquivo: {filename}")

        df = processor.load_spreadsheet(str(file_path))
        if df is None:
            return jsonify({'error': 'Erro ao carregar arquivo'}), 400

        df_enriched = processor.enrich_contacts(df)

        output_path = app.config['UPLOAD_FOLDER'] / f"enriched_{filename}"
        success = processor.export_spreadsheet(df_enriched, str(output_path))

        if not success:
            return jsonify({'error': 'Erro ao exportar resultado'}), 500

        return jsonify({
            'status': 'success',
            'total': len(df_enriched),
            'found': len(df_enriched[df_enriched['status_busca'] == 'encontrado']),
            'success_rate': f"{len(df_enriched[df_enriched['status_busca'] == 'encontrado']) / len(df_enriched) * 100:.1f}%",
            'output_file': output_path.name,
        })

    except Exception as e:
        logger.error(f"Erro no enriquecimento: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Estatísticas do cache"""
    return jsonify(processor.cache.get_stats())

@app.route('/cache/clear', methods=['POST'])
def cache_clear():
    """Limpar cache"""
    processor.cache.clear()
    return jsonify({'status': 'cache cleared'})

@app.route('/', methods=['GET'])
def index():
    """Landing page"""
    return jsonify({
        'name': 'LinkedIn Data Enrichment API',
        'version': '1.0.0',
        'endpoints': {
            'POST /enrich': 'Enriquecer planilha (file: arquivo CSV/XLSX)',
            'GET /health': 'Health check',
            'GET /cache/stats': 'Estatísticas do cache',
            'POST /cache/clear': 'Limpar cache',
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
