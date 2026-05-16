import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
from typing import Optional, List, Dict
from CTkMessagebox import CTkMessagebox

from src.utils.logger import get_logger
from src.services.data_processor import DataProcessor
from config.settings import APP_CONFIG, DATA_DIR

logger = get_logger(__name__)

class LinkedInEnrichmentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_CONFIG['title'])
        self.geometry(APP_CONFIG['geometry'])
        self.resizable(APP_CONFIG['resizable'], APP_CONFIG['resizable'])

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.processor = DataProcessor()
        self.current_data: Optional[List[Dict]] = None
        self.processing_thread: Optional[threading.Thread] = None

        self._setup_ui()
        self._center_window()

    def _center_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_main_content()
        self._create_footer()

    def _create_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="#1e1e1e")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="🔗 LinkedIn Data Enrichment Tool",
            font=("Helvetica", 24, "bold"),
            text_color="#00d9ff",
        )
        title.grid(row=0, column=0, sticky="w", pady=(10, 5))

        subtitle = ctk.CTkLabel(
            header,
            text="Enriqueça seus contatos com dados do LinkedIn automaticamente",
            font=("Helvetica", 12),
            text_color="#a0a0a0",
        )
        subtitle.grid(row=1, column=0, sticky="w")

    def _create_main_content(self) -> None:
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        self._create_file_section(main_frame)
        self._create_config_section(main_frame)
        self._create_preview_section(main_frame)
        self._create_action_section(main_frame)

    def _create_file_section(self, parent) -> None:
        file_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        file_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            file_frame,
            text="📁 Arquivo de Entrada",
            font=("Helvetica", 12, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.file_path_var = ctk.StringVar(value="Nenhum arquivo selecionado")
        file_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.file_path_var,
            font=("Helvetica", 10),
            text_color="#00d9ff",
        )
        file_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        ctk.CTkButton(
            file_frame,
            text="Selecionar Arquivo",
            command=self._select_file,
            fg_color="#00d9ff",
            text_color="#000000",
            hover_color="#00a8cc",
        ).grid(row=0, column=2, padx=10, pady=10)

    def _create_config_section(self, parent) -> None:
        config_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        config_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            config_frame,
            text="⚙️ Configurações",
            font=("Helvetica", 12, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        config_frame.grid_columnconfigure(0, weight=1)
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(2, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(config_frame, text="Threads:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.threads_var = ctk.StringVar(value="5")
        ctk.CTkEntry(
            config_frame,
            textvariable=self.threads_var,
            width=60,
        ).grid(row=1, column=0, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(config_frame, text="Timeout (s):").grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.timeout_var = ctk.StringVar(value="10")
        ctk.CTkEntry(
            config_frame,
            textvariable=self.timeout_var,
            width=60,
        ).grid(row=1, column=1, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(config_frame, text="Min Delay (s):").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.delay_min_var = ctk.StringVar(value="1")
        ctk.CTkEntry(
            config_frame,
            textvariable=self.delay_min_var,
            width=60,
        ).grid(row=1, column=2, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(config_frame, text="Max Delay (s):").grid(row=1, column=3, sticky="w", padx=10, pady=5)
        self.delay_max_var = ctk.StringVar(value="3")
        ctk.CTkEntry(
            config_frame,
            textvariable=self.delay_max_var,
            width=60,
        ).grid(row=1, column=3, sticky="e", padx=10, pady=5)

    def _create_preview_section(self, parent) -> None:
        preview_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            preview_frame,
            text="📊 Preview dos Dados",
            font=("Helvetica", 12, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            height=200,
            fg_color="#1e1e1e",
            text_color="#ffffff",
        )
        self.preview_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.preview_text.configure(state="disabled")

        self.log_text = ctk.CTkTextbox(
            preview_frame,
            height=150,
            fg_color="#1e1e1e",
            text_color="#00d9ff",
        )
        self.log_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.log_text.configure(state="disabled")

    def _create_action_section(self, parent) -> None:
        action_frame = ctk.CTkFrame(parent)
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)

        button_frame = ctk.CTkFrame(action_frame)
        button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ Iniciar Busca",
            command=self._start_enrichment,
            fg_color="#00d9ff",
            text_color="#000000",
            hover_color="#00a8cc",
            width=150,
        )
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹ Parar",
            command=self._stop_enrichment,
            fg_color="#ff6b6b",
            text_color="#ffffff",
            hover_color="#ee5a5a",
            width=150,
            state="disabled",
        )
        self.stop_button.pack(side="left", padx=5)

        self.export_button = ctk.CTkButton(
            button_frame,
            text="💾 Exportar",
            command=self._export_results,
            fg_color="#51cf66",
            text_color="#000000",
            hover_color="#40c057",
            width=150,
            state="disabled",
        )
        self.export_button.pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🔄 Limpar Cache",
            command=self._clear_cache,
            fg_color="#ffd43b",
            text_color="#000000",
            hover_color="#f9ca24",
            width=150,
        ).pack(side="left", padx=5)

        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            action_frame,
            variable=self.progress_var,
            fg_color="#2b2b2b",
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(
            action_frame,
            text="Pronto para processar",
            font=("Helvetica", 10),
            text_color="#a0a0a0",
        )
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    def _create_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="#1e1e1e")
        footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        footer.grid_columnconfigure(0, weight=1)

        cache_stats = self.processor.cache.get_stats()
        footer_text = f"Cache: {cache_stats['total_cached']} itens | Tamanho: {cache_stats['file_size_kb']:.1f} KB"

        ctk.CTkLabel(
            footer,
            text=footer_text,
            font=("Helvetica", 9),
            text_color="#696969",
        ).pack(pady=5)

    def _select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            initialdir=DATA_DIR,
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        self.current_data = self.processor.load_spreadsheet(file_path)

        if self.current_data is not None:
            self.file_path_var.set(f"Carregado: {Path(file_path).name}")
            self._update_preview()
            self._log("✓ Arquivo carregado com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível carregar o arquivo")

    def _update_preview(self) -> None:
        if self.current_data is None:
            return

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        info = f"Total de contatos: {len(self.current_data)}\n"
        info += f"Colunas: {', '.join(self.current_data[0].keys()) if self.current_data else 'N/A'}\n\n"
        info += "Primeiras 5 linhas:\n"
        for idx, row in enumerate(self.current_data[:5]):
            info += f"\nLinha {idx + 1}:\n"
            for key, value in row.items():
                info += f"  {key}: {value}\n"

        self.preview_text.insert("1.0", info)
        self.preview_text.configure(state="disabled")

    def _log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update()

    def _start_enrichment(self) -> None:
        if self.current_data is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo primeiro")
            return

        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("Aviso", "Processamento já em andamento")
            return

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.export_button.configure(state="disabled")
        self.progress_var.set(0)

        self._log("▶ Iniciando enriquecimento de dados...")

        self.processing_thread = threading.Thread(target=self._process_data, daemon=True)
        self.processing_thread.start()

    def _process_data(self) -> None:
        try:
            self.current_data = self.processor.enrich_contacts(
                self.current_data,
                progress_callback=lambda p: self._update_progress(p),
                status_callback=lambda s: self._log(s),
            )

            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.export_button.configure(state="normal")

            self._log("✓ Enriquecimento concluído!")
            self._log(f"Resumo: {len(self.current_data)} contatos processados")

        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            self._log(f"✗ Erro: {str(e)}")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def _update_progress(self, percentage: float) -> None:
        self.progress_var.set(percentage / 100)
        self.status_label.configure(text=f"Progresso: {percentage:.1f}%")
        self.update()

    def _stop_enrichment(self) -> None:
        self.processor.stop_processing()
        self._log("⏹ Processamento interrompido")
        self.stop_button.configure(state="disabled")
        self.start_button.configure(state="normal")

    def _export_results(self) -> None:
        if self.current_data is None:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar")
            return

        file_path = filedialog.asksaveasfilename(
            initialdir=DATA_DIR,
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")],
        )

        if not file_path:
            return

        success = self.processor.export_spreadsheet(self.current_data, file_path)

        if success:
            messagebox.showinfo("Sucesso", f"Arquivo exportado: {Path(file_path).name}")
            self._log(f"✓ Exportado para: {Path(file_path).name}")
        else:
            messagebox.showerror("Erro", "Não foi possível exportar o arquivo")

    def _clear_cache(self) -> None:
        if messagebox.askyesno("Confirmação", "Limpar todo o cache local?"):
            self.processor.cache.clear()
            self._log("🗑 Cache limpo")
            messagebox.showinfo("Sucesso", "Cache limpo com sucesso")

    def run(self) -> None:
        self.mainloop()
