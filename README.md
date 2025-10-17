  # 🚚 VTEX Freight Calculator

  ![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
  ![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)
  ![VTEX](https://img.shields.io/badge/VTEX-API-orange.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
  ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

  > **Simulador de Frete VTEX** - Aplicação desktop para simular custos de frete e consultar estoque em múltiplas lojas VTEX simultaneamente com interface moderna e processamento paralelo.

  ## 📋 Índice

  - [🎯 Sobre o Projeto](#-sobre-o-projeto)
  - [✨ Funcionalidades](#-funcionalidades)
  - [🖥️ Interface](#️-interface)
  - [📦 Instalação](#-instalação)
  - [🚀 Como Usar](#-como-usar)
  - [⚙️ Configuração](#️-configuração)
  - [🔧 Gerando o Executável](#-gerando-o-executável)
  - [📋 Requisitos](#-requisitos)
  - [🏗️ Arquitetura](#️-arquitetura)
  - [🤝 Contribuição](#-contribuição)
  - [📄 Licença](#-licença)

  ## 🎯 Sobre o Projeto

  O **VTEX Freight Calculator** é uma aplicação desktop desenvolvida em Python com PySide6 que permite simular custos de frete e consultar estoque em múltiplas lojas VTEX simultaneamente. A aplicação utiliza processamento paralelo com threads para otimizar as consultas à API VTEX e oferece uma interface moderna e intuitiva para análise de dados de logística.

  ### 🎨 Características Técnicas
  - **Interface Moderna**: PySide6 com design responsivo e cores personalizáveis
  - **Processamento Paralelo**: Threads assíncronas para consultas simultâneas à API
  - **Sistema de Configuração**: Gerenciamento persistente de configurações por empresa
  - **Tela de Splash**: Animação de carregamento com progresso
  - **Executável Autocontido**: Build modular com PyInstaller

  ## ✨ Funcionalidades

  ### 🏆 **Ranking de Lojas**
  - Exibe ranking das melhores lojas baseado em custo e prazo
  - Filtros por tipo de entrega (normal, retirada)
  - Ordenação automática por melhor custo-benefício
  - Destaque visual para top 3 posições
  - Informações de estoque e transportadoras

  ### 📊 **Análise Detalhada**
  - Visão detalhada de cada loja selecionada
  - Comparação de opções de frete (entregas normais e retirada)
  - Cálculo de prazos de entrega com datas estimadas
  - Formatação de valores em moeda brasileira
  - Informações de transportadoras e modalidades

  ### 📍 **Pontos de Retirada**
  - Lista de pontos de retirada disponíveis por loja
  - Endereços formatados e organizados
  - Informações de distância e disponibilidade
  - Tabela organizada com preços e prazos

  ### ❌ **Lojas Sem Entrega**
  - Identificação de lojas sem opções de entrega
  - Informações de estoque disponível
  - Filtro por lojas nacionais
  - Diferenciação entre estoque zerado e fora do range de CEP

  ### 📦 **Consulta de Estoque**
  - Consulta simultânea em múltiplas lojas
  - Visualização de estoque total e principal (1_1)
  - Interface dedicada para análise de inventário
  - Destaque visual para estoque baixo/zerado

  ### 📄 **Exportação JSON**
  - Exportação completa dos dados em formato JSON
  - Estrutura organizada para análise posterior
  - Botão para copiar JSON para área de transferência
  - Compatível com ferramentas de análise de dados

  ### ⚙️ **Sistema de Configuração**
  - Configuração personalizada por empresa
  - Gerenciamento de lojas e filiais com importação/exportação Excel
  - Sistema de cores personalizável
  - Tokens de autenticação VTEX
  - Configurações de performance (workers, timeout)

  ## 🖥️ Interface

  A aplicação possui uma interface moderna dividida em:

  - **Painel Esquerdo**: Entrada de dados (CEP, SKU, seleção de lojas)
  - **Painel Direito**: Resultados organizados em abas
  - **Barra de Status**: Informações de progresso e status
  - **Sistema de Abas**: Organização clara das funcionalidades
  - **Tela de Splash**: Animação de carregamento com progresso

  ### Componentes da Interface
  - **InputPanel**: Painel de entrada com validação de CEP e SKU
  - **HeaderWidget**: Cabeçalho personalizado com nome da empresa
  - **StatusBarWidget**: Barra de status com mensagens coloridas
  - **SplashScreen**: Tela de carregamento com animação

  ## 📦 Instalação

  ### Pré-requisitos
  - Python 3.8 ou superior
  - Windows 10/11
  - Conexão com internet
  - Conta VTEX com API habilitada
  - App Key e App Token da VTEX com permissões adequadas

  ### Instalação Manual

  1. **Clone o repositório:**
  ```bash
  git clone https://github.com/seu-usuario/vtex-freight-calculator.git
  cd vtex-freight-calculator
  ```

  2. **Instale as dependências:**
  ```bash
  pip install -r requirements.txt
  ```

  3. **Execute a aplicação:**
  ```bash
  python main.py
  ```

  ### Instalação via Executável

  1. **Baixe o executável:**
    - `SimuladorFrete2025_Modular.exe`

  2. **Execute o arquivo:**
    - Duplo clique no executável
    - A aplicação será executada automaticamente
    - As configurações são salvas na pasta do usuário: `C:\Users\[Usuário]\VTEX_Freight_Calculator\`


  ## 🚀 Como Usar

  ### 1. **Configuração Inicial**
  - Abra a aplicação
  - Vá para a aba "⚙️ Configurações"
  - Clique em "🔧 Configurar Empresa"
  - Configure sua empresa e lojas (veja seção [⚙️ Configuração](#️-configuração) para detalhes)

  ### 2. **Simulação de Frete**
  - **Digite o CEP** de destino (formato: 00000-000)
  - **Selecione o SKU** do produto (histórico automático)
  - **Escolha as lojas** para simular (filtro disponível)
  - **Clique em "▶ SIMULAR FRETE"**

  ### 3. **Análise dos Resultados**
  - **🏆 Ranking**: Melhores opções de frete ordenadas
  - **📊 Detalhada**: Análise por loja com seletor
  - **📍 Retirada**: Pontos de retirada organizados
  - **❌ Sem Entrega**: Lojas sem opções com filtro
  - **📦 Estoque**: Consulta de inventário
  - **📄 JSON**: Dados completos para exportação

  ### 4. **Consulta de Estoque**
  - Vá para a aba "📦 Estoque"
  - Digite o SKU do produto
  - Clique em "CONSULTAR ESTOQUE"
  - Visualize o estoque por loja com destaque visual

  ## ⚙️ Configuração

  ### Configuração da Empresa

  #### **Informações da Empresa**
  - **Nome da empresa**: Nome que aparecerá no cabeçalho da aplicação
  - **App Key**: Chave de aplicação da VTEX (obtida no Admin da VTEX)
  - **App Token**: Token de autenticação da VTEX (obtido no Admin da VTEX)

  > ⚠️ **PERMISSÕES NECESSÁRIAS**: O App Token deve ter acesso a:
  > - **Conta Principal**: Para consultas gerais e medição de SLAs
  > - **Todas as Lojas**: Para consultar estoque e simular frete
  > - **APIs de Logística**: Para simulação de frete e consulta de estoque

  #### **Lojas e Filiais**
  - **Adicionar/remover lojas**: Gerenciar lista de lojas
  - **ID da Loja**: Deve ser exatamente igual ao ID no Gerenciador de Marketplace da VTEX
  - **Tipo de Entrega**: Nacional (todo Brasil) ou Local (regional)
  - **Propriedade**: Franquia ou Própria
  - **Conta Principal**: ⭐ **CRÍTICO** - Apenas uma loja pode ser principal
  - **Importar/exportar Excel**: Gerenciar lojas em massa

  #### **Configurações de Performance**
  - **Número máximo de workers**: Threads paralelas (padrão: 20)
  - **Timeout de requisições**: Tempo limite por requisição (padrão: 10s)
  - **SKU padrão**: SKU inicial para simulação
  - **Histórico de SKUs recentes**: Quantos SKUs lembrar (padrão: 5)

  > 🔧 **CONFIGURAÇÕES OTIMIZADAS**: As configurações padrão são otimizadas para performance e estabilidade. Não é necessário alterar a menos que tenha necessidades específicas.

  ### Fluxo de Configuração

  #### **1. Configuração Inicial**
  1. Abra a aplicação
  2. Vá para a aba "⚙️ Configurações"
  3. Clique em "🔧 Configurar Empresa"
  4. Preencha as informações da empresa
  5. Configure as lojas
  6. Salve as configurações
  7. Feche e reabra a aplicação para aplicar as mudanças

  #### **2. Configuração de Lojas**
  1. **Adicionar Loja**: Clique em "Adicionar Loja"
  2. **ID da Loja**: Use exatamente o mesmo ID do Gerenciador de Marketplace da VTEX
  3. **Nome**: Nome descritivo para identificação
  4. **Tipo**: Nacional (todo Brasil) ou Local (regional)
  5. **Propriedade**: Franquia ou Própria
  6. **Conta Principal**: ⭐ Marque apenas UMA loja como principal

  #### **3. Importação em Massa**
  - Use "📊 Exportar Excel" para criar template
  - Preencha o Excel com suas lojas
  - Use "📥 Importar Excel" para importar todas as lojas

  ### 🎯 Importância da Loja Principal

  A **loja principal** é fundamental para o funcionamento da aplicação:

  #### **Funções da Loja Principal**
  - **Centro de Distribuição**: Serve como referência para medição de SLAs
  - **Medição de Performance**: Compara performance das outras lojas
  - **Configuração Automática**: A aplicação identifica automaticamente qual é a principal
  - **Apenas Uma**: Só pode haver uma loja marcada como principal

  #### **Como Configurar**
  1. **Adicione todas as lojas** primeiro
  2. **Marque apenas UMA** como "Conta Principal"
  3. **Salve as configurações**
  4. **Reinicie a aplicação** para aplicar as mudanças

  > ⚠️ **ATENÇÃO**: Se não configurar uma loja principal, a aplicação não conseguirá medir os SLAs das outras lojas corretamente.

  ### Estrutura de Configuração

  ```json
  {
    "empresa": {
      "nome": "Sua Empresa",
      "conta_principal": "sua-empresa",
      "app_key": "sua-app-key",
      "app_token": "seu-app-token"
    },
    "lojas": [
      {
        "id": "loja-id",
        "nome": "Nome da Loja",
        "tipo": "Nacional",
        "nacional": true,
        "propriedade": "Própria",
        "conta_principal": false
      }
    ],
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
  ```

  ## 🔧 Gerando o Executável

  ### Método Automático (Recomendado)

  1. **Execute o script de build:**
  ```bash
  python build_encrypted.py
  ```

  2. **O script irá:**
    - Verificar dependências automaticamente
    - Instalar PyInstaller se necessário
    - Criar o executável modular autocontido
    - Limpar arquivos temporários
    - Gerar `SimuladorFrete2025_Modular.exe`

  ### Método Manual

  1. **Instale o PyInstaller:**
  ```bash
  pip install pyinstaller
  ```

  2. **Execute o comando:**
  ```bash
  pyinstaller --onefile --windowed --name=SimuladorFrete2025 --icon=entrega-rapida.ico main.py
  ```

  ### Características do Executável

  - **Modular**: Todos os módulos integrados
  - **Autocontido**: Não precisa de instalação Python
  - **Portável**: Pode ser copiado para qualquer lugar
  - **Configurável**: Sistema de configuração integrado
  - **Persistente**: Configurações salvas na pasta do usuário
  - **Seguro**: Configurações isoladas por usuário

  ### Localização das Configurações

  - **Executável**: `C:\Users\[Usuário]\VTEX_Freight_Calculator\empresa_config.json`
  - **Script Python**: `empresa_config.json` (na pasta do projeto)
  - **Backup**: Configurações são salvas automaticamente
  - **Portabilidade**: Cada usuário tem suas próprias configurações

  ## 📋 Requisitos

  ### Sistema
  - **OS**: Windows 10/11
  - **RAM**: 4GB mínimo, 8GB recomendado
  - **Espaço**: 100MB para instalação
  - **Internet**: Conexão estável

  ### Dependências Python
  ```
  PySide6>=6.0.0
  requests>=2.25.0
  pyinstaller>=4.0
  openpyxl>=3.0.0
  ```

  ### API VTEX
  - Conta VTEX ativa
  - App Key e App Token válidos
  - Permissões de API habilitadas

  ## 🏗️ Arquitetura

  ### Estrutura do Projeto

  ```
  simulador-de-frete/
  ├── main.py                 # Classe principal FreteSimulator
  ├── config_manager.py       # Gerenciador de configurações persistente
  ├── config_ui.py           # Interface de configuração com Excel
  ├── ui_components.py       # Componentes de UI (InputPanel, Header, Status)
  ├── utils.py               # Funções utilitárias (validação, formatação)
  ├── threads.py             # Threads de processamento paralelo
  ├── splash_screen.py       # Tela de splash com animação
  ├── build_encrypted.py     # Script de build modular
  ├── tabs/                  # Módulos de abas
  │   ├── __init__.py
  │   ├── ranking_tab.py     # Aba de ranking com tabela
  │   ├── resumo_tab.py      # Aba de resumo detalhado
  │   ├── retirada_tab.py    # Aba de pontos de retirada
  │   ├── estoque_tab.py     # Aba de consulta de estoque
  │   ├── sem_entrega_tab.py # Aba de lojas sem entrega
  │   └── json_tab.py        # Aba de exportação JSON
  ├── entrega-rapida.ico     # Ícone da aplicação
  ├── VTEX_Logo.svg.png      # Logo VTEX
  └── README.md
  ```

  ### Componentes Principais

  - **FreteSimulator**: Classe principal da aplicação
  - **ConfigManager**: Gerenciamento de configurações com persistência
  - **InputPanel**: Painel de entrada de dados com validação
  - **StatusBarWidget**: Barra de status com mensagens coloridas
  - **SimulacaoThread**: Thread para processamento paralelo de simulação
  - **EstoqueThread**: Thread para consulta paralela de estoque

  ### Fluxo de Dados

  1. **Entrada**: CEP, SKU, lojas selecionadas
  2. **Validação**: Validação de CEP e SKU
  3. **Processamento**: Threads assíncronas para API VTEX
  4. **Análise**: Cálculo de custos, prazos e estoque
  5. **Exibição**: Resultados organizados em abas
  6. **Persistência**: Configurações salvas automaticamente

  ### APIs Utilizadas

  - **Simulação de Frete**: `/api/checkout/pub/orderForms/simulation`
  - **Políticas de Envio**: `/api/logistics/pvt/shipping-policies`
  - **Consulta de Estoque**: `/api/logistics/pvt/inventory/skus/{sku}`

