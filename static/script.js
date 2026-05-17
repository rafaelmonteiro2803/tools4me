// API Configuration
const API_BASE = window.location.origin;
let selectedFile = null;
let isProcessing = false;
let enrichedData = null;

// DOM Elements - will be initialized on DOMContentLoaded
let fileInput, fileLabel, fileName, startBtn, stopBtn, downloadBtn, clearBtn;
let previewSection, progressSection, logsSection, resultsSection;
let progressFill, progressPercent, statusText, logsContent;
let toast;

function initializeDOMElements() {
    fileInput = document.getElementById('fileInput');
    fileLabel = document.querySelector('.file-label');
    fileName = document.getElementById('fileName');
    startBtn = document.getElementById('startBtn');
    stopBtn = document.getElementById('stopBtn');
    downloadBtn = document.getElementById('downloadBtn');
    clearBtn = document.getElementById('clearBtn');

    previewSection = document.getElementById('previewSection');
    progressSection = document.getElementById('progressSection');
    logsSection = document.getElementById('logsSection');
    resultsSection = document.getElementById('resultsSection');

    progressFill = document.getElementById('progressFill');
    progressPercent = document.getElementById('progressPercent');
    statusText = document.getElementById('statusText');
    logsContent = document.getElementById('logsContent');

    toast = document.getElementById('toast');

    // Attach event listeners
    fileInput.addEventListener('change', handleFileSelect);
    startBtn.addEventListener('click', startProcessing);
    stopBtn.addEventListener('click', () => {
        isProcessing = false;
        addLog('⏹ Processamento interrompido');
        stopBtn.disabled = true;
        startBtn.disabled = false;
    });
    downloadBtn.addEventListener('click', downloadResults);
    clearBtn.addEventListener('click', clearCache);

    console.log('✓ Elementos DOM inicializados');
    console.log('✓ startBtn:', startBtn);
}

function parseCSVLine(line) {
    const result = [];
    let current = '';
    let insideQuotes = false;

    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        if (char === '"') {
            insideQuotes = !insideQuotes;
        } else if (char === ',' && !insideQuotes) {
            result.push(current.trim().replace(/^"|"$/g, ''));
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current.trim().replace(/^"|"$/g, ''));
    return result;
}

function readCSV(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const text = e.target.result;
                const lines = text.split('\n').filter(l => l.trim());
                if (lines.length < 1) {
                    resolve([]);
                    return;
                }

                const headers = parseCSVLine(lines[0]).map(h => h.toLowerCase());
                const data = lines.slice(1).map(line => {
                    const values = parseCSVLine(line);
                    const obj = {};
                    headers.forEach((h, i) => {
                        obj[h] = values[i] ? values[i] : '';
                    });
                    return obj;
                });

                resolve(data);
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
        reader.readAsText(file);
    });
}

function readXLSX(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheet = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheet];
                const jsonData = XLSX.utils.sheet_to_json(worksheet);

                const normalized = jsonData.map(row => {
                    const obj = {};
                    Object.keys(row).forEach(key => {
                        obj[key.toLowerCase()] = String(row[key] || '');
                    });
                    return obj;
                });

                resolve(normalized);
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
        reader.readAsArrayBuffer(file);
    });
}

async function handleFileSelect(e) {
    selectedFile = e.target.files[0];
    if (!selectedFile) return;

    // Validate file
    const validTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    if (!validTypes.includes(selectedFile.type) && !selectedFile.name.endsWith('.csv') && !selectedFile.name.endsWith('.xlsx')) {
        showToast('❌ Arquivo inválido. Use CSV ou XLSX', 'error');
        selectedFile = null;
        return;
    }

    fileName.textContent = `✓ Arquivo: ${selectedFile.name}`;

    // Enable button regardless of preview result
    startBtn.disabled = false;
    startBtn.removeAttribute('disabled');
    console.log('✓ Arquivo selecionado, botão habilitado:', selectedFile.name);

    // Show preview
    await showPreview();
}

async function showPreview() {
    try {
        // Read CSV/XLSX file
        let data = [];
        if (selectedFile.name.endsWith('.csv')) {
            data = await readCSV(selectedFile);
        } else {
            data = await readXLSX(selectedFile);
        }

        if (!data || data.length === 0) {
            showToast('⚠️ Arquivo carregado, mas vazio ou sem dados', 'warning');
            return;
        }

        // Update preview
        document.getElementById('totalContacts').textContent = data.length;
        const columns = Object.keys(data[0]).length;
        document.getElementById('totalColumns').textContent = columns;

        // Create table
        const tableHead = document.getElementById('tableHead');
        const tableBody = document.getElementById('tableBody');
        tableHead.innerHTML = '';
        tableBody.innerHTML = '';

        // Header
        const headerRow = document.createElement('tr');
        Object.keys(data[0]).forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

        // First 5 rows
        data.slice(0, 5).forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell || '-';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });

        previewSection.style.display = 'block';
        showToast('✓ Arquivo carregado com sucesso', 'success');
    } catch (error) {
        showToast(`⚠️ Arquivo selecionado, mas preview indisponível: ${error.message}`, 'warning');
    }
}

// Start Processing
async function startProcessing() {
    if (!selectedFile) {
        showToast('❌ Selecione um arquivo', 'error');
        return;
    }

    isProcessing = true;
    startBtn.disabled = true;
    startBtn.style.display = 'none';
    stopBtn.disabled = false;
    stopBtn.style.display = 'inline-block';

    progressSection.style.display = 'block';
    logsSection.style.display = 'block';
    logsContent.innerHTML = '';

    addLog('▶ Iniciando enriquecimento de dados...');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch(`${API_BASE}/enrich`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.status === 'success') {
            addLog('✓ Enriquecimento concluído com sucesso!');
            addLog(`  Total: ${result.total}`);
            addLog(`  Encontrados: ${result.found}`);
            addLog(`  Taxa de sucesso: ${result.success_rate}`);
            addLog(`  Arquivo: ${result.output_file}`);

            enrichedData = result;
            showResults(result);
            downloadBtn.style.display = 'inline-block';
        } else {
            throw new Error(result.error || 'Erro desconhecido');
        }
    } catch (error) {
        addLog(`✗ Erro: ${error.message}`);
        showToast(`❌ Erro ao processar: ${error.message}`, 'error');
    } finally {
        isProcessing = false;
        startBtn.disabled = false;
        startBtn.style.display = 'inline-block';
        stopBtn.disabled = true;
        stopBtn.style.display = 'none';
    }

    updateProgress(100);
}

// Show Results
function showResults(result) {
    document.getElementById('resultTotal').textContent = result.total;
    document.getElementById('resultFound').textContent = result.found;
    document.getElementById('resultRate').textContent = result.success_rate;
    document.getElementById('resultFile').textContent = result.output_file;

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Download Results
async function downloadResults() {
    if (!enrichedData) return;

    try {
        const response = await fetch(`${API_BASE}/download/${enrichedData.output_file}`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = enrichedData.output_file;
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('✓ Download iniciado', 'success');
        } else {
            showToast('❌ Erro ao baixar arquivo', 'error');
        }
    } catch (error) {
        showToast(`❌ Erro: ${error.message}`, 'error');
    }
}

// Clear Cache
async function clearCache() {
    if (!confirm('Tem certeza que deseja limpar o cache?')) return;

    try {
        const response = await fetch(`${API_BASE}/cache/clear`, {
            method: 'POST'
        });

        if (response.ok) {
            showToast('✓ Cache limpo com sucesso', 'success');
            updateCacheStats();
        } else {
            showToast('❌ Erro ao limpar cache', 'error');
        }
    } catch (error) {
        showToast(`❌ Erro: ${error.message}`, 'error');
    }
}

// Update Progress
function updateProgress(percent) {
    progressFill.style.width = percent + '%';
    progressPercent.textContent = Math.round(percent) + '%';
    statusText.textContent = `Processando... ${Math.round(percent)}%`;
}

// Add Log Entry
function addLog(message) {
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logsContent.appendChild(entry);
    logsContent.scrollTop = logsContent.scrollHeight;
}

// Show Toast Notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Update Cache Stats
async function updateCacheStats() {
    try {
        const response = await fetch(`${API_BASE}/cache/stats`);
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('cacheItems').textContent = stats.total_cached;
            document.getElementById('cacheSize').textContent = stats.file_size_kb.toFixed(1);
        }
    } catch (error) {
        console.error('Erro ao atualizar cache stats:', error);
    }
}

// Health Check
async function healthCheck() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('✓ API rodando:', data);
            updateCacheStats();
        }
    } catch (error) {
        console.error('API não está acessível');
    }
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ DOM Carregado');

    // Initialize DOM elements and attach listeners
    initializeDOMElements();

    // Check health and cache
    healthCheck();
    updateCacheStats();
});
