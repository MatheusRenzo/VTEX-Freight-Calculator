"""
Configurações e constantes do VTEX Freight Calculator
"""

# Cores do tema VTEX (Branco com detalhes rosa)
COR_PRIMARIA = "#E91E63"       # Rosa VTEX
COR_SECUNDARIA = "#FFFFFF"     # Branco
COR_DESTAQUE = "#E91E63"       # Rosa VTEX (vibrante)
COR_FUNDO = "#FFFFFF"          # Branco (base VTEX)
COR_TEXTO = "#333333"          # Cinza escuro
COR_BORDA = "#E0E0E0"          # Cinza claro
COR_DESTAQUE2 = "#C2185B"      # Rosa escuro (para destaques)

# Configurações da aplicação
SKU_DEFAULT = "149718"
MAX_SKUS_RECENTES = 5
MAX_WORKERS = 20

# Lista completa de lojas
LOJAS_COMPLETAS = [
    "trackfield",
    "trackfieldtfsp000066"
]

# Dicionário de lojas nacionais
LOJAS_NACIONAIS = {
    "000066": "Nacional",
    "kfield": "Nacional-CD"
}

# Dicionário de códigos e filiais
CODIGOS_FILIAIS = {
    "000066": "Cristiano Viana",
    "kfield": "TF Log (cd)"
}

# Configurações da janela
WINDOW_SIZE = (1200, 800)
WINDOW_ICON = "entrega-rapida.ico"
