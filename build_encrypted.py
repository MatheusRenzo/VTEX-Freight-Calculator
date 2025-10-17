"""
Script para criar executável modular do VTEX Freight Calculator
Este script cria um executável autocontido com todos os módulos integrados
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_encrypted_executable():
    """Cria o executável modular autocontido"""
    
    print("🔐 Iniciando criação do executável modular...")
    
    # Verificar se os arquivos necessários existem
    required_files = [
        'main.py',                    # Arquivo principal
        'config_manager.py',          # Gerenciador de configurações
        'config_ui.py',              # Interface de configuração
        'ui_components.py',          # Componentes de UI
        'utils.py',                  # Utilitários
        'threads.py',                # Threads de processamento
        'splash_screen.py',          # Tela de splash
        'entrega-rapida.ico',        # Ícone
        'VTEX_Logo.svg.png',         # Logo da splash screen
        'tabs/__init__.py',          # Módulo de abas
        'tabs/ranking_tab.py',       # Aba de ranking
        'tabs/resumo_tab.py',        # Aba de resumo
        'tabs/retirada_tab.py',      # Aba de retirada
        'tabs/estoque_tab.py',       # Aba de estoque
        'tabs/sem_entrega_tab.py',   # Aba sem entrega
        'tabs/json_tab.py'           # Aba JSON
    ]
    
    # Arquivos opcionais (podem não existir ainda)
    optional_files = [
        'empresa_config.json'        # Configuração da empresa (criada depois)
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos necessários não encontrados:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # Verificar arquivos opcionais
    missing_optional = []
    for file in optional_files:
        if not os.path.exists(file):
            missing_optional.append(file)
    
    if missing_optional:
        print("⚠️  Arquivos opcionais não encontrados (serão criados automaticamente):")
        for file in missing_optional:
            print(f"   - {file}")
        print("   (Estes arquivos serão criados quando o executável for executado pela primeira vez)")
    
    # Comando PyInstaller com proteções
    cmd = [
        'pyinstaller',
        '--onefile',                    # Arquivo único
        '--windowed',                   # Sem console
        '--name=SimuladorFrete2025',    # Nome do executável
        '--icon=entrega-rapida.ico',    # Ícone
        
        # Incluir arquivos de dados
        '--add-data=entrega-rapida.ico;.',   # Ícone
        '--add-data=VTEX_Logo.svg.png;.',   # Logo da splash screen
    ]
    
    # Incluir JSON padrão para configuração inicial
    if os.path.exists('empresa_config.json'):
        cmd.append('--add-data=empresa_config.json;empresa_config.json')
        print("✅ Incluindo empresa_config.json como configuração inicial")
    else:
        print("ℹ️  Nenhum JSON encontrado - criando configuração padrão")
        # Criar um JSON padrão temporário para incluir no executável
        default_config = {
            "empresa": {
                "nome": "Sua Empresa",
                "conta_principal": "sua-empresa",
                "app_key": "",
                "app_token": ""
            },
            "lojas": [],
            "configuracoes": {
                "sku_padrao": "149718",
                "max_skus_recentes": 5,
                "max_workers": 20,
                "timeout_requests": 10
            },
            "cores": {
                "primaria": "#E91E63",
                "secundaria": "#FFFFFF",
                "destaque": "#E91E63",
                "fundo": "#FFFFFF",
                "texto": "#333333",
                "borda": "#F5F5F5",
                "destaque2": "#C2185B"
            }
        }
        
        # Criar arquivo temporário
        import json
        with open('empresa_config_temp.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        cmd.append('--add-data=empresa_config_temp.json;empresa_config.json')
        print("✅ Criando empresa_config.json padrão para configuração inicial")
    
    # Continuar com o resto do comando
    cmd.extend([
        # Incluir módulos Python
        '--add-data=config_manager.py;.',
        '--add-data=config_ui.py;.',
        '--add-data=ui_components.py;.',
        '--add-data=utils.py;.',
        '--add-data=threads.py;.',
        '--add-data=splash_screen.py;.',
        
        # Incluir pasta tabs
        '--add-data=tabs;tabs',
        
        # Importações ocultas necessárias
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=threading',
        '--hidden-import=queue',
        '--hidden-import=time',
        '--hidden-import=sys',
        '--hidden-import=os',
        '--hidden-import=pathlib',
        
        # Módulos locais
        '--hidden-import=config_manager',
        '--hidden-import=config_ui',
        '--hidden-import=ui_components',
        '--hidden-import=utils',
        '--hidden-import=threads',
        '--hidden-import=splash_screen',
        '--hidden-import=tabs.ranking_tab',
        '--hidden-import=tabs.resumo_tab',
        '--hidden-import=tabs.retirada_tab',
        '--hidden-import=tabs.estoque_tab',
        '--hidden-import=tabs.sem_entrega_tab',
        '--hidden-import=tabs.json_tab',
        
        '--clean',                      # Limpar cache
        '--noconfirm',                  # Não confirmar sobrescrita
        'main.py'                       # Arquivo principal
    ])
    
    print("📦 Executando PyInstaller...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyInstaller executado com sucesso!")
        
        # Verificar se o executável foi criado
        exe_path = Path('dist/SimuladorFrete2025.exe')
        if exe_path.exists():
            print(f"✅ Executável criado: {exe_path}")
            
            # Mover para o diretório principal
            final_path = Path('SimuladorFrete2025_Modular.exe')
            shutil.move(str(exe_path), str(final_path))
            print(f"✅ Executável movido para: {final_path}")
            
            # Limpar arquivos temporários
            cleanup_files = ['build', 'dist', 'SimuladorFrete2025.spec', 'empresa_config_temp.json']
            for item in cleanup_files:
                if os.path.exists(item):
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
            print("🧹 Arquivos temporários removidos")
            
            return True
        else:
            print("❌ Executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        print(f"Saída de erro: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_requirements():
    """Cria arquivo requirements.txt com todas as dependências"""
    requirements = [
        'PySide6>=6.0.0',
        'requests>=2.25.0',
        'pyinstaller>=4.0'
    ]
    
    with open('requirements_build.txt', 'w') as f:
        for req in requirements:
            f.write(req + '\n')
    
    print("📋 Arquivo requirements_build.txt criado")

def install_dependencies():
    """Instala as dependências necessárias"""
    print("📥 Instalando dependências...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_build.txt'], 
                      check=True)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 VTEX Freight Calculator - Build Modular")
    print("=" * 50)
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        if not install_dependencies():
            return False
    
    # Criar executável
    if create_encrypted_executable():
        print("\n🎉 SUCESSO! Executável modular criado!")
        print("📁 Arquivo: SimuladorFrete2025_Modular.exe")
        print("🔐 O executável contém:")
        print("   - Todos os módulos Python integrados")
        print("   - Interface de configuração integrada")
        print("   - Sistema de abas modular")
        print("   - Funciona sozinho sem dependências externas")
        print("\n📋 Sobre o sistema de configuração:")
        print("   - O empresa_config.json fica EMBARCADO como configuração inicial")
        print("   - As configurações personalizadas são salvas na pasta do usuário")
        print("   - Pasta: C:\\Users\\[Usuário]\\VTEX_Freight_Calculator\\")
        print("   - Use a aba 'Configurações' para personalizar sua empresa")
        print("   - As configurações ficam salvas no sistema da pessoa")
        print("   - Executável portável - pode ser copiado para qualquer lugar")
        print("   - Cada usuário tem suas próprias configurações")

        return True
    else:
        print("\n❌ Falha na criação do executável")
        return False

if __name__ == "__main__":
    main()
