#!/usr/bin/env python3
"""
Script de Instalação - VTEX Freight Calculator
Este script instala automaticamente todas as dependências necessárias
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_requirements():
    """Instala as dependências do requirements.txt"""
    print("📦 Instalando dependências...")
    
    try:
        # Verificar se requirements.txt existe
        if not os.path.exists('requirements.txt'):
            print("❌ Arquivo requirements.txt não encontrado!")
            return False
        
        # Instalar dependências
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print(f"Saída de erro: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_config_example():
    """Cria arquivo de configuração de exemplo se não existir"""
    if not os.path.exists('empresa_config.json'):
        if os.path.exists('empresa_config_exemplo.json'):
            import shutil
            shutil.copy('empresa_config_exemplo.json', 'empresa_config.json')
            print("✅ Arquivo de configuração de exemplo criado")
        else:
            print("⚠️  Arquivo de configuração de exemplo não encontrado")

def test_installation():
    """Testa se a instalação foi bem-sucedida"""
    print("🧪 Testando instalação...")
    
    try:
        # Testar importações principais
        import PySide6
        print("✅ PySide6 importado com sucesso")
        
        import requests
        print("✅ Requests importado com sucesso")
        
        # Testar se os módulos locais existem
        required_modules = [
            'main.py',
            'config_manager.py',
            'ui_components.py',
            'utils.py',
            'threads.py'
        ]
        
        missing_modules = []
        for module in required_modules:
            if not os.path.exists(module):
                missing_modules.append(module)
        
        if missing_modules:
            print(f"❌ Módulos não encontrados: {missing_modules}")
            return False
        
        print("✅ Todos os módulos encontrados")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar dependências: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal de instalação"""
    print("🚀 VTEX Freight Calculator - Instalação")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        return False
    
    # Instalar dependências
    if not install_requirements():
        return False
    
    # Criar configuração de exemplo
    create_config_example()
    
    # Testar instalação
    if not test_installation():
        return False
    
    print("\n🎉 Instalação concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure sua empresa na aba 'Configurações'")
    print("2. Adicione suas lojas VTEX")
    print("3. Configure seus tokens de API")
    print("4. Execute: python main.py")
    print("\n📖 Para mais informações, consulte o README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Instalação falhou!")
        sys.exit(1)
    else:
        print("\n✅ Instalação bem-sucedida!")
        sys.exit(0)
