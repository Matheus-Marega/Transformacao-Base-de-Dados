# Análise de Volume de Exames Integrados

Esta ferramenta Streamlit automatiza a análise de dados de volume de exames integrados, eliminando a necessidade de ajustes manuais em planilhas Excel exportadas do WeKnow BI.

## Funcionalidades

- **Upload de Arquivos**: Carregue facilmente dois arquivos Excel (mês anterior e mês atual).
- **Limpeza de Dados**: Remove automaticamente colunas com valores zero.
- **Cálculo de Métricas**: Calcula o total de exames integrados para cada período e a diferença entre eles.
- **Variação Percentual**: Exibe a variação percentual do volume de exames em relação ao mês anterior.
- **Análise de Queda de Volume**: Identifica laboratórios com queda no volume e classifica a situação (Normal, Verificar, Crítico).
- **Visualização de Dados**: Gera gráficos de barras para comparar o volume de exames entre os meses.
- **Identificação de Laboratórios Ausentes**: Mostra laboratórios presentes em um arquivo, mas ausentes no outro.

## Estrutura do Projeto

```
.
├── src/
│   ├── core/
│   │   └── data_processing.py  # Funções de processamento e cálculo de dados
│   └── ui/
│       └── app.py              # Lógica da interface do usuário Streamlit
├── data/
│   ├── TotalJulho.xlsx         # Exemplo de arquivo de dados
│   └── TotalJunho.xlsx         # Exemplo de arquivo de dados
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
└── todo.md                     # Tarefas de desenvolvimento (para uso interno)
```

## Como Rodar a Aplicação

Siga os passos abaixo para configurar e executar a aplicação localmente:

1.  **Clone o Repositório (se aplicável)**:
    ```bash
    git clone [<URL_DO_SEU_REPOSITORIO>](https://github.com/Matheus-Marega/Transformacao-Base-de-Dados.git)
    cd analise_volumetria
    ```

2.  **Instale as Dependências**:
    Certifique-se de ter o Python instalado (versão 3.7+ recomendada). Em seguida, instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a Aplicação Streamlit**:
    Navegue até o diretório `src/ui` e execute o arquivo `app.py`:
    ```bash
    cd src/ui
    streamlit run app.py
    ```

    Isso abrirá a aplicação no seu navegador padrão. Se não abrir automaticamente, copie o URL fornecido no terminal (geralmente `http://localhost:8501`).

## Uso da Aplicação

1.  **Upload dos Arquivos**: Na interface da aplicação, faça o upload do "Arquivo do Mês Anterior" e do "Arquivo do Mês Atual" (arquivos `.xlsx`).
2.  **Processar Dados**: Clique no botão "Processar Dados".
3.  **Visualizar Resultados**: A aplicação exibirá as métricas, tabelas de comparação, laboratórios com queda de volume e gráficos de volume.


