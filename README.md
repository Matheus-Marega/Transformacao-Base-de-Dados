
# 📊 Comparador de Dados Tabulares com Streamlit

Uma ferramenta interativa desenvolvida em **Python + Streamlit** para **comparação e visualização de dados tabulares** provenientes de dashboards corporativos. Ideal para cenários onde arquivos gerados em diferentes períodos não oferecem meios visuais ou estruturados de comparação direta.

## 🔍 Motivação

No dia a dia do trabalho, muitos dashboards geram arquivos apenas com **dados brutos em formato tabular**, dificultando a comparação entre dois períodos ou a análise visual dos resultados. Este projeto foi criado para resolver esse problema, permitindo:

* Upload de dois arquivos `.xlsx`
* Limpeza e tratamento automático dos dados
* Identificação de diferenças entre os arquivos
* Geração de gráficos comparativos interativos
* Uso flexível: **visualização única** ou **comparação entre períodos**

---

## 🚀 Funcionalidades

* 📁 Upload de dois arquivos Excel
* 🧹 Limpeza automática: remoção de colunas com apenas zeros
* 🔍 Identificação de laboratórios ausentes em um dos períodos
* 📊 Geração de dataframe unificado com cálculo da diferença entre colunas
* 📈 Gráfico interativo (Streamlit ou Altair) com comparação visual por laboratório
* 🔄 Comportamento dinâmico: a aplicação se adapta mesmo que apenas um dos arquivos tenha dados relevantes

---

## 🖼️ Exemplo de Visualização

Exemplo de gráfico gerado:

![Exemplo de Gráfico Comparativo](https://via.placeholder.com/800x400?text=Grafico+de+Comparacao)

---

## 🛠️ Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [Pandas](https://pandas.pydata.org/)
* [Streamlit](https://streamlit.io/)
* [Altair](https://altair-viz.github.io/)

---

## ▶️ Como Executar o Projeto

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repo.git
   cd nome-do-repo
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o app:

   ```bash
   streamlit run app.py
   ```

4. Faça o upload de dois arquivos `.xlsx` com uma coluna chamada `LABORATORIO` e colunas de valores numéricos.

---

## 📂 Estrutura Esperada dos Arquivos

| LABORATORIO | VALOR\_MES1 |
| ----------- | ----------- |
| LAB A       | 100         |
| LAB B       | 200         |

---

## ⚠️ Observações

* Os arquivos precisam conter a coluna `LABORATORIO` como chave de comparação.
* A ferramenta identifica automaticamente colunas com apenas zeros e as remove.
* Em caso de erro de leitura ou arquivos inválidos, uma mensagem de aviso é exibida.
