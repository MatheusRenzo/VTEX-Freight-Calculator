"""
VTEX Freight Calculator - Arquivo Principal
"""
import sys
import time
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidgetItem, QDialog
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from PySide6.QtCore import Qt

# Importar módulos locais
from config_manager import ConfigManager
from utils import *
from ui_components import InputPanel, HeaderWidget, StatusBarWidget
from tabs.ranking_tab import RankingTab
from tabs.resumo_tab import ResumoTab
from tabs.retirada_tab import RetiradaTab
from tabs.estoque_tab import EstoqueTab
from tabs.sem_entrega_tab import SemEntregaTab
from tabs.json_tab import JsonTab
from threads import SimulacaoThread, EstoqueThread
from splash_screen import SplashScreen
from config_ui import ConfigDialog


class FreteSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inicializar gerenciador de configurações
        self.config_manager = ConfigManager()
        
        # Carregar configurações
        self.load_config()
        
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QIcon("entrega-rapida.ico"))
        self.resize(1200, 800)
        
        # Variáveis
        self.skus_recentes = [self.sku_default]
        
        self.init_ui()
    
    def load_config(self):
        """Carrega configurações da empresa"""
        # Carregar informações da empresa
        empresa = self.config_manager.get_empresa_info()
        self.window_title = f"{empresa.get('nome', 'VTEX Freight Calculator')} - VTEX Freight Calculator"
        
        # Carregar tokens da configuração
        self.APP_KEY = empresa.get('app_key', '')
        self.APP_TOKEN = empresa.get('app_token', '')
        # Removido user_token - não é mais necessário
        
        # Carregar lojas
        self.lojas_completas = self.config_manager.get_lojas_ids()
        self.lojas_nacionais = self.config_manager.get_lojas_nacionais()
        self.codigos_filiais = self.config_manager.get_codigos_filiais()
        
        # Carregar configurações gerais
        config = self.config_manager.get_configuracoes()
        self.sku_default = config.get('sku_padrao', '149718')
        self.max_workers = config.get('max_workers', 20)
        
        # Carregar cores
        cores = self.config_manager.get_cores()
        self.COR_PRIMARIA = cores.get('primaria', '#000000')
        self.COR_SECUNDARIA = cores.get('secundaria', '#FFFFFF')
        self.COR_DESTAQUE = cores.get('destaque', '#000000')
        self.COR_FUNDO = cores.get('fundo', '#F0F0F0')
        self.COR_TEXTO = cores.get('texto', '#333333')
        self.COR_BORDA = cores.get('borda', '#CCCCCC')
        self.COR_DESTAQUE2 = cores.get('destaque2', '#239623')
    
    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-color: {self.COR_FUNDO};")
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Definir cores
        cores = {
            'primaria': self.COR_PRIMARIA,
            'secundaria': self.COR_SECUNDARIA,
            'destaque': self.COR_DESTAQUE,
            'fundo': self.COR_FUNDO,
            'texto': self.COR_TEXTO,
            'borda': self.COR_BORDA,
            'destaque2': self.COR_DESTAQUE2
        }
        
        # Cabeçalho
        empresa_nome = self.config_manager.get_empresa_info().get('nome', 'Sua Empresa')
        self.header = HeaderWidget(cores, empresa_nome)
        main_layout.addWidget(self.header)
        
        # Container principal com splitter
        from PySide6.QtWidgets import QSplitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter, 1)
        
        # Painel esquerdo (entrada de dados)
        self.input_panel = InputPanel(self, cores)
        main_splitter.addWidget(self.input_panel)
        
        # Painel direito (resultados)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 0, 5, 5)
        
        # Barra de status
        self.status_bar = StatusBarWidget(cores)
        
        # Área de resultados
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Arial", 10))
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.COR_BORDA};
                background: {self.COR_SECUNDARIA};
            }}
            QTabBar::tab {{
                background: {self.COR_FUNDO};
                border: 1px solid {self.COR_BORDA};
                padding: 8px;
                color: {self.COR_TEXTO};
            }}
            QTabBar::tab:selected {{
                background: {self.COR_SECUNDARIA};
                border-bottom-color: {self.COR_SECUNDARIA};
            }}
        """)
        right_layout.addWidget(self.tab_widget, 1)
        right_layout.addWidget(self.status_bar)
        
        # Criar abas
        self.ranking_tab = RankingTab(self)
        self.tab_widget.addTab(self.ranking_tab, "🏆 Ranking")
        
        self.resumo_tab = ResumoTab(self)
        self.tab_widget.addTab(self.resumo_tab, "📊 Detalhada")
        
        self.sem_entrega_tab = SemEntregaTab(self)
        self.tab_widget.addTab(self.sem_entrega_tab, "❌ Sem Entrega")
        
        self.retirada_tab = RetiradaTab(self)
        self.tab_widget.addTab(self.retirada_tab, "📍 Retirada")
        
        self.estoque_tab = EstoqueTab(self)
        self.tab_widget.addTab(self.estoque_tab, "📦 Estoque")
        
        self.json_tab = JsonTab(self)
        self.tab_widget.addTab(self.json_tab, "📄 JSON")
        
        # Aba de configuração
        self.config_tab = self.create_config_tab()
        self.tab_widget.addTab(self.config_tab, "⚙️ Configurações")
        
        # Adicionar ícones personalizados nas abas
        self.adicionar_icones_abas()
        
        # Adicionar painéis ao splitter
        main_splitter.addWidget(self.input_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([300, 700])
        
        # Popular lista de lojas após criar o input_panel
        self.popular_lista_lojas()
        
        # Menu removido - configurações estão na aba
    
    def create_config_tab(self):
        """Cria aba de configuração integrada com design profissional"""
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QGroupBox, QFrame, QScrollArea
        
        # Widget principal com scroll
        scroll_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(scroll_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header elegante
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.COR_PRIMARIA}, stop:1 {self.COR_DESTAQUE});
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        # Título principal
        title = QLabel("⚙️ Configurações da Empresa")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            padding: 10px;
            background-color: transparent;
        """)
        header_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Gerencie as configurações da sua empresa VTEX")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            padding: 5px;
            background-color: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Botões de ação com design moderno
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COR_SECUNDARIA};
                border: 1px solid {self.COR_BORDA};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(15)
        
        # Botão principal
        self.config_btn = QPushButton("🔧 Configurar Empresa")
        self.config_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.config_btn.setMinimumHeight(50)
        self.config_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.COR_DESTAQUE}, stop:1 {self.COR_DESTAQUE2});
                color: white;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 12pt;
                border: none;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.COR_DESTAQUE2}, stop:1 {self.COR_DESTAQUE});
            }}
            QPushButton:pressed {{
                background-color: {self.COR_DESTAQUE2};
            }}
        """)
        self.config_btn.clicked.connect(self.abrir_configuracao)
        
        buttons_layout.addWidget(self.config_btn)
        
        layout.addWidget(buttons_frame)
        
        # Seção de informações com design moderno
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COR_SECUNDARIA};
                border: 1px solid {self.COR_BORDA};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        # Título da seção
        info_title = QLabel("📋 Status da Configuração")
        info_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info_title.setStyleSheet(f"""
            color: {self.COR_TEXTO};
            padding: 10px 0;
            background-color: transparent;
        """)
        info_layout.addWidget(info_title)
        
        # Grid de informações
        empresa = self.config_manager.get_empresa_info()
        lojas = self.config_manager.get_lojas()
        
        # Criar cards para cada informação
        self.criar_info_cards(info_layout, empresa, lojas)
        
        layout.addWidget(info_frame)
        layout.addStretch()
        
        # Retornar scroll area
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        config_widget = QWidget()
        config_widget.setLayout(main_layout)
        return config_widget
    
    def criar_info_cards(self, layout, empresa, lojas):
        """Cria cards informativos com design moderno"""
        from PySide6.QtWidgets import QGridLayout, QFrame, QLabel
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Card 1: Empresa
        empresa_card = self.criar_info_card(
            "🏢 Empresa",
            empresa.get('nome', 'Não configurado'),
            "Nome da empresa configurado" if empresa.get('nome') else "Nome não configurado"
        )
        grid_layout.addWidget(empresa_card, 0, 0)
        
        # Card 2: Conta Principal
        conta_card = self.criar_info_card(
            "🔑 Conta Principal",
            empresa.get('conta_principal', 'Não configurado'),
            "Conta principal definida" if empresa.get('conta_principal') else "Conta principal não definida"
        )
        grid_layout.addWidget(conta_card, 0, 1)
        
        # Card 3: Total de Lojas
        lojas_card = self.criar_info_card(
            "🏪 Total de Lojas",
            str(len(lojas)),
            f"{len(lojas)} loja(s) configurada(s)"
        )
        grid_layout.addWidget(lojas_card, 1, 0)
        
        # Card 4: Status dos Tokens
        token_status = "✅ Configurado" if empresa.get('app_key') and empresa.get('app_token') else "❌ Não configurado"
        token_card = self.criar_info_card(
            "🔐 Tokens VTEX",
            token_status,
            "App Key e App Token configurados" if empresa.get('app_key') and empresa.get('app_token') else "Tokens não configurados"
        )
        grid_layout.addWidget(token_card, 1, 1)
        
        layout.addLayout(grid_layout)
    
    def criar_info_card(self, titulo, valor, descricao):
        """Cria um card informativo individual"""
        from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
        
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COR_FUNDO};
                border: 1px solid {self.COR_BORDA};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        titulo_label.setStyleSheet(f"color: {self.COR_TEXTO};")
        layout.addWidget(titulo_label)
        
        # Valor
        valor_label = QLabel(valor)
        valor_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        valor_label.setStyleSheet(f"color: {self.COR_DESTAQUE};")
        layout.addWidget(valor_label)
        
        # Descrição
        desc_label = QLabel(descricao)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet(f"color: {self.COR_TEXTO}; opacity: 0.8;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return card
    
    def abrir_configuracao(self):
        """Abre dialog de configuração"""
        dialog = ConfigDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            # Recarregar configurações
            self.load_config()
            
            # Atualizar título da janela
            empresa_nome = self.config_manager.get_empresa_info().get('nome', 'Sua Empresa')
            self.setWindowTitle(f"{empresa_nome} - VTEX Freight Calculator")
            
            # Atualizar header
            if hasattr(self, 'header'):
                self.header.setText(f"{empresa_nome} - VTEX Freight Calculator")
            
            # Recarregar lista de lojas
            self.popular_lista_lojas()
            
            # Atualizar informações na aba de configuração
            self.atualizar_info_config()
            
            self.atualizar_status("Configurações atualizadas!", "green")
    
    
    def adicionar_icones_abas(self):
        """Adiciona ícones personalizados nas abas"""
        try:
            # Criar ícones personalizados para cada aba
            icones_abas = [
                self.criar_icone_ranking(),      # 0: Ranking
                self.criar_icone_detalhada(),    # 1: Detalhada
                self.criar_icone_sem_entrega(),  # 2: Sem Entrega
                self.criar_icone_retirada(),     # 3: Retirada
                self.criar_icone_estoque(),      # 4: Estoque
                self.criar_icone_json(),         # 5: JSON
                self.criar_icone_config()        # 6: Configurações
            ]
            
            # Aplicar ícones nas abas
            for i, icone in enumerate(icones_abas):
                if i < self.tab_widget.count():
                    self.tab_widget.setTabIcon(i, icone)
                    
        except Exception as e:
            print(f"Erro ao adicionar ícones: {e}")
    
    def criar_icone_ranking(self):
        """Cria ícone para aba de ranking"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_detalhada(self):
        """Cria ícone para aba detalhada"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_sem_entrega(self):
        """Cria ícone para aba sem entrega"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_retirada(self):
        """Cria ícone para aba retirada"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_estoque(self):
        """Cria ícone para aba estoque"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_json(self):
        """Cria ícone para aba JSON"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def criar_icone_config(self):
        """Cria ícone para aba configurações"""
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    
    
    
    
    def aplicar_cores_dinamicamente(self):
        """Aplica as cores dinamicamente aos componentes"""
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                background-color: {self.COR_PRIMARIA};
                color: {self.COR_SECUNDARIA};
                padding: 15px;
                border-radius: 8px;
            """)
        
        if hasattr(self, 'status_bar'):
            self.status_bar.setStyleSheet(f"""
                background-color: {self.COR_SECUNDARIA};
                color: {self.COR_TEXTO};
                padding: 8px;
                border-top: 1px solid {self.COR_BORDA};
            """)
        
        # Aplicar cores aos painéis de input
        if hasattr(self, 'input_panel'):
            self.input_panel.aplicar_cores_dinamicamente({
                'primaria': self.COR_PRIMARIA,
                'secundaria': self.COR_SECUNDARIA,
                'destaque': self.COR_DESTAQUE,
                'fundo': self.COR_FUNDO,
                'texto': self.COR_TEXTO,
                'borda': self.COR_BORDA
            })
    
    def atualizar_info_config(self):
        """Atualiza as informações exibidas na aba de configuração"""
        if hasattr(self, 'info_label'):
            empresa = self.config_manager.get_empresa_info()
            lojas = self.config_manager.get_lojas()
            
            info_text = f"""
            <b>Empresa:</b> {empresa.get('nome', 'Não configurado')}<br>
            <b>Conta Principal:</b> {empresa.get('conta_principal', 'Não configurado')}<br>
            <b>Total de Lojas:</b> {len(lojas)}<br>
            <b>App Key:</b> {'✅ Configurado' if empresa.get('app_key') else '❌ Não configurado'}<br>
            <b>App Token:</b> {'✅ Configurado' if empresa.get('app_token') else '❌ Não configurado'}<br>
            """
            self.info_label.setText(info_text)
    
    
    def recreate_ui(self):
        """Recria a interface com as novas configurações"""
        # Limpar interface atual
        self.centralWidget().deleteLater()
        
        # Recriar interface
        self.init_ui()
        
        # Aplicar cores dinamicamente
        self.aplicar_cores_dinamicamente()
    
    def popular_lista_lojas(self):
        if hasattr(self, 'input_panel') and hasattr(self.input_panel, 'lojas_list'):
            self.input_panel.lojas_list.clear()
            for loja in self.lojas_completas:
                # Extrair código da loja (últimos 6 caracteres)
                codigo = loja[-6:]
                codigo2 = loja[-10:]

                # Verificar se o código existe no dicionário
                nome_filial = self.codigos_filiais.get(codigo, f"seller: ({codigo2})")
                
                # Formatar texto: "CÓDIGO - FILIAL"
                texto_item = f"{codigo2} - {nome_filial}"
                
                item = QListWidgetItem(texto_item)
                item.setData(Qt.UserRole, loja)  # Armazenar nome original
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.input_panel.lojas_list.addItem(item)
    
    def formatar_nome_loja(self, loja_id):
        """Formata o ID da loja para um nome amigável usando o dicionário"""
        return self.config_manager.formatar_nome_loja(loja_id)
    
    def determinar_tipo_loja(self, loja_id):
        """Determina se a loja é Nacional ou Local baseado no dicionário"""
        return self.config_manager.determinar_tipo_loja(loja_id)
    
    def filtrar_lojas(self, texto):
        texto = texto.lower()
        for i in range(self.input_panel.lojas_list.count()):
            item = self.input_panel.lojas_list.item(i)
            loja = item.text().lower()
            
            # Verificar se o texto é "nacional" para mostrar apenas lojas nacionais
            if texto == "nacional":
                # Obter o ID da loja do item
                loja_id = item.data(Qt.UserRole)
                # Verificar se é uma loja nacional
                codigo = loja_id[-6:]  # Últimos 6 caracteres
                codigo2 = loja_id[-10:]  # Últimos 10 caracteres
                
                # Verificar se está na lista de lojas nacionais
                is_nacional = (codigo in self.lojas_nacionais or 
                              codigo2 in self.lojas_nacionais or 
                              loja_id in self.lojas_nacionais)
                
                item.setHidden(not is_nacional)
            else:
                # Filtro normal por texto
                item.setHidden(texto not in loja)
    
    def selecionar_todas(self):
        for i in range(self.input_panel.lojas_list.count()):
            item = self.input_panel.lojas_list.item(i)
            if not item.isHidden():
                item.setCheckState(Qt.Checked)
    
    def desselecionar_todas(self):
        for i in range(self.input_panel.lojas_list.count()):
            item = self.input_panel.lojas_list.item(i)
            if not item.isHidden():
                item.setCheckState(Qt.Unchecked)
    
    def get_lojas_selecionadas(self):
        lojas = []
        for i in range(self.input_panel.lojas_list.count()):
            item = self.input_panel.lojas_list.item(i)
            if item.checkState() == Qt.Checked and not item.isHidden():
                # Recuperar nome original da loja
                loja_original = item.data(Qt.UserRole)
                lojas.append(loja_original)
        return lojas
    
    def iniciar_simulacao_thread(self):
        lojas_selecionadas = self.get_lojas_selecionadas()
        if not lojas_selecionadas:
            self.mostrar_erro("Selecione pelo menos uma loja para simular!")
            return
        
        if not validar_cep(self.input_panel.cep_input.text()):
            self.mostrar_erro("Formato de CEP inválido! Use 00000-000")
            return
        
        # Obter SKU do campo de entrada
        sku = self.input_panel.sku_combo.currentText().strip()
        if not sku:
            self.mostrar_erro("O SKU não pode estar vazio!")
            return
        
        # Atualizar histórico de SKUs
        self.atualizar_historico_skus(sku)
        
        # Obter conta principal da configuração
        conta_principal = self.config_manager.get_empresa_info().get('conta_principal', 'trackfield')
        
        self.simulacao_thread = SimulacaoThread(
            self.input_panel.cep_input.text(),
            lojas_selecionadas,
            sku,
            self.APP_KEY,
            self.APP_TOKEN,
            conta_principal,
            self.max_workers
        )
        
        self.simulacao_thread.result_signal.connect(self.mostrar_resultados)
        self.simulacao_thread.error_signal.connect(self.mostrar_erro)
        self.simulacao_thread.status_signal.connect(self.atualizar_status)
        self.simulacao_thread.progress_signal.connect(self.atualizar_progresso)
        
        self.input_panel.simular_btn.setEnabled(False)
        self.input_panel.limpar_btn.setEnabled(False)
        self.input_panel.simular_btn.setText("PROCESSANDO...")
        self.simulacao_thread.start()
    
    def atualizar_historico_skus(self, novo_sku):
        """Atualiza o histórico de SKUs mantendo os mais recentes"""
        # Adiciona novo SKU se não existir
        if novo_sku not in self.skus_recentes:
            self.skus_recentes.insert(0, novo_sku)
            
            # Mantém apenas os mais recentes
            max_skus = self.config_manager.get_configuracoes().get('max_skus_recentes', 5)
            if len(self.skus_recentes) > max_skus:
                self.skus_recentes = self.skus_recentes[:max_skus]
            
            # Atualiza o combobox
            self.input_panel.sku_combo.clear()
            self.input_panel.sku_combo.addItems(self.skus_recentes)
            self.input_panel.sku_combo.setCurrentText(novo_sku)
            
            # Atualiza também o combo de estoque
            self.estoque_tab.estoque_sku_input.clear()
            self.estoque_tab.estoque_sku_input.addItems(self.skus_recentes)
            self.estoque_tab.estoque_sku_input.setCurrentText(novo_sku)

    def atualizar_status(self, mensagem, cor="black"):
        self.status_bar.showMessage(mensagem)
        if cor == "red":
            self.status_bar.setStyleSheet(f"background-color: {self.COR_SECUNDARIA}; color: #e74c3c;")
        elif cor == "green":
            self.status_bar.setStyleSheet(f"background-color: {self.COR_SECUNDARIA}; color: #27ae60;")
        else:
            self.status_bar.setStyleSheet(f"background-color: {self.COR_SECUNDARIA}; color: {self.COR_TEXTO};")
    
    def atualizar_progresso(self, atual, total):
        self.status_bar.showMessage(f"Processando: {atual}/{total} lojas...")
    
    def limpar_resultados(self):
        # Limpa conteúdo das abas
        self.ranking_tab.ranking_layout.clear()
        self.resumo_tab.resumo_layout.clear()
        self.retirada_tab.retirada_layout.clear()
        self.sem_entrega_tab.sem_entrega_layout.clear()
        
        # Limpa JSON
        self.json_tab.json_edit.clear()
        self.resumo_tab.loja_selector.clear()
        self.atualizar_status("Resultados limpos", "green")
    
    def calcular_prazo_entrega(self, shipping_estimate):
        return calcular_prazo_entrega(shipping_estimate)
    
    def formatar_moeda(self, valor):
        return formatar_moeda(valor)
    
    def parse_prazo_para_dias(self, prazo_str):
        return parse_prazo_para_dias(prazo_str)
    
    def calcular_estoque_total(self, inventory_data):
        return calcular_estoque_total(inventory_data)
    
    def mostrar_resultados(self, resultados):
        # Salva JSON formatado
        formatted_json = json.dumps(resultados, indent=2, ensure_ascii=False)
        self.json_tab.json_edit.setPlainText(formatted_json)
        
        # Armazena resultados para acesso posterior
        self.resultados_completos = resultados
        
        # Preenche o seletor de lojas com nomes formatados
        self.resumo_tab.loja_selector.clear()
        lojas_com_entrega = [loja for loja, data in resultados.items() 
                             if loja_tem_qualquer_entrega(data.get('simulation', {}))]
        
        for loja in lojas_com_entrega:
            nome_formatado = self.formatar_nome_loja(loja)
            self.resumo_tab.loja_selector.addItem(nome_formatado, loja)
        
        try:
            # Exibir informações formatadas nas abas
            self.atualizar_status("Exibindo ranking...", "black")
            self.ranking_tab.exibir_ranking(resultados)
            
            self.atualizar_status("Exibindo pontos de retirada...", "black")
            self.retirada_tab.exibir_pontos_retirada(resultados)
            
            # Exibir lojas sem entrega
            self.atualizar_status("Exibindo lojas sem entrega...", "black")
            self.exibir_lojas_sem_entrega(resultados)
            
            # Seleciona a primeira loja na visão detalhada
            if self.resumo_tab.loja_selector.count() > 0:
                self.resumo_tab.loja_selector.setCurrentIndex(0)
                self.atualizar_resumo(0)
            
            # Atualiza UI
            self.input_panel.simular_btn.setEnabled(True)
            self.input_panel.limpar_btn.setEnabled(True)
            self.input_panel.simular_btn.setText("▶ SIMULAR FRETE")
            self.atualizar_status(f"Simulação concluída para {len(resultados)} lojas!", "green")
            
        except Exception as e:
            # Em caso de erro, reabilitar botões e mostrar erro
            self.input_panel.simular_btn.setEnabled(True)
            self.input_panel.limpar_btn.setEnabled(True)
            self.input_panel.simular_btn.setText("▶ SIMULAR FRETE")
            self.atualizar_status(f"Erro ao exibir resultados: {str(e)}", "red")
            print(f"Erro na exibição: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def exibir_lojas_sem_entrega(self, resultados):
        """Exibe as lojas sem entrega disponível"""
        lojas_sem_entrega = []
        
        for loja, data in resultados.items():
            simulation = data.get('simulation', {})
            inventory = data.get('inventory', {})
            
            # Verificar se a loja tem entrega
            tem_entrega = loja_tem_qualquer_entrega(simulation)
            
            if not tem_entrega:
                # Calcular estoque total
                estoque_total = self.calcular_estoque_total(inventory)
                lojas_sem_entrega.append((loja, estoque_total))
        
        # Popular a aba sem entrega
        self.sem_entrega_tab.popular_aba_sem_entrega(lojas_sem_entrega)
    
    def atualizar_resumo(self, index):
        # Limpa o conteúdo atual
        for i in reversed(range(self.resumo_tab.resumo_layout.count())): 
            widget = self.resumo_tab.resumo_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Obtém a loja selecionada (ID)
        loja_selecionada = self.resumo_tab.loja_selector.currentData()
        
        if loja_selecionada and loja_selecionada in self.resultados_completos:
            data = self.resultados_completos[loja_selecionada]
            self.resumo_tab.exibir_resumo_para_loja(loja_selecionada, data)

    def mostrar_erro(self, mensagem):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Erro", mensagem)
        self.input_panel.simular_btn.setEnabled(True)
        self.input_panel.limpar_btn.setEnabled(True)
        self.input_panel.simular_btn.setText("▶ SIMULAR FRETE")
        self.estoque_tab.consultar_estoque_btn.setEnabled(True)
        self.estoque_tab.consultar_estoque_btn.setText("CONSULTAR ESTOQUE")
        self.atualizar_status(mensagem, "red")
    
    def iniciar_consulta_estoque(self):
        sku = self.estoque_tab.estoque_sku_input.currentText().strip()
        if not sku:
            self.mostrar_erro("O SKU não pode estar vazio!")
            return
        
        # Atualizar histórico de SKUs
        self.atualizar_historico_skus(sku)
        
        # Obter conta principal da configuração
        conta_principal = self.config_manager.get_empresa_info().get('conta_principal', 'trackfield')
        
        self.estoque_thread = EstoqueThread(
            sku,
            self.lojas_completas,
            self.APP_KEY,
            self.APP_TOKEN,
            conta_principal,
            self.max_workers
        )
        
        self.estoque_tab.consultar_estoque_btn.setEnabled(False)
        self.estoque_thread.result_signal.connect(self.estoque_tab.mostrar_resultados_estoque)
        self.estoque_thread.error_signal.connect(self.mostrar_erro)
        self.estoque_thread.status_signal.connect(self.atualizar_status)
        self.estoque_thread.progress_signal.connect(self.atualizar_progresso_estoque)
        
        self.estoque_tab.consultar_estoque_btn.setText("PROCESSANDO...")
        self.estoque_thread.start()
    
    def atualizar_progresso_estoque(self, atual, total):
        self.status_bar.showMessage(f"Consultando estoque: {atual}/{total} lojas...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Define estilo geral
    app.setStyle("Fusion")
    palette = app.palette()
    
    # Configuração de cores para tema da empresa
    palette.setColor(QPalette.Window, QColor("#F0F0F0"))
    palette.setColor(QPalette.WindowText, QColor("#000000"))
    palette.setColor(QPalette.Base, QColor("#FFFFFF"))
    palette.setColor(QPalette.AlternateBase, QColor("#F5F5F5"))
    palette.setColor(QPalette.ToolTipBase, QColor("#FFFFFF"))
    palette.setColor(QPalette.ToolTipText, QColor("#000000"))
    palette.setColor(QPalette.Text, QColor("#000000"))
    palette.setColor(QPalette.Button, QColor("#E0E0E0"))
    palette.setColor(QPalette.ButtonText, QColor("#000000"))
    palette.setColor(QPalette.BrightText, QColor("#239623"))
    palette.setColor(QPalette.Highlight, QColor("#239623"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    
    app.setPalette(palette)
    
    # Mostrar splash screen
    splash = SplashScreen()
    splash.set_message("Inicializando aplicação...")
    splash.show()
    app.processEvents()

    # Criar janela principal
    window = FreteSimulator()

    # Simular carregamento com animação de progresso
    start_time = time.time()
    while time.time() - start_time < 3:
        elapsed = (time.time() - start_time) / 3
        splash.set_progress(int(elapsed * 100))
        app.processEvents()
        time.sleep(0.01)

    # Esconder splash e mostrar app
    splash.close()
    window.show()

    sys.exit(app.exec())
