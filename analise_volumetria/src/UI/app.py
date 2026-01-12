import streamlit as st
import pandas as pd
from typing import Optional, Tuple
import sys
import os
from dotenv import load_dotenv

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_processing import (
    clean_dataframes,
    get_negative_volume_laboratories,
    classify_volume_situation,
    calculate_percentage_variation,
    calculate_total_volumes_and_difference,
    calculate_total_volume,
    load_and_process_multi_month_data,
    get_monthly_summary,
    get_top_n_laboratories_by_month
)

def load_dataframes_from_excel(file1: Optional[st.runtime.uploaded_file_manager.UploadedFile], 
                               file2: Optional[st.runtime.uploaded_file_manager.UploadedFile]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega dataframes a partir de arquivos Excel enviados pelo usuário."""
    if file1 is None or file2 is None:
        st.warning("Por favor, adicione ambos os arquivos para gerar o DataFrame")
        st.stop()
    
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        return df1, df2
    except Exception as e:
        st.error(f"Erro ao carregar os arquivos: {str(e)}")
        st.stop()

def display_missing_laboratories(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """Exibe laboratórios que não se repetem entre os dois dataframes."""
    df_missing_in_df2 = df1[~df1["LABORATORIO"].isin(df2["LABORATORIO"])]
    df_missing_in_df1 = df2[~df2["LABORATORIO"].isin(df1["LABORATORIO"])]

    st.subheader("Laboratórios que não se repetiram")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Arquivo 1")
        st.write(df_missing_in_df2)

    with col2:
        st.write("Arquivo 2")
        st.write(df_missing_in_df1)

def display_volume_metrics(merged_df: pd.DataFrame, col1_name: str, col2_name: str) -> None:
    """Exibe métricas de volume em containers organizados."""
    previous_month, current_month, difference = calculate_total_volumes_and_difference(
        merged_df, col1_name, col2_name
    )
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        container1 = st.container(border=True)
        container1.metric(label=f"Total exames {col1_name}", value=previous_month)
    
    with col2:
        container2 = st.container(border=True)
        container2.metric(label=f"Total exames {col2_name}", value=current_month)
    
    with col3:
        container3 = st.container(border=True)
        container3.metric(
            label=f"Diferença de Exames integrados {col1_name} x {col2_name}", 
            value=difference
        )
    
    with col4:
        # Para calcular a variação, precisamos dos valores numéricos
        prev_value = merged_df[col1_name].sum()
        curr_value = merged_df[col2_name].sum()
        variation = calculate_percentage_variation(curr_value,prev_value)
        container4 = st.container(border=True)
        container4.metric(
            value=variation, 
            label=f"Variação ao mês anterior {col2_name}"
        )

def display_negative_volume_analysis(merged_df: pd.DataFrame) -> None:
    """Exibe análise de laboratórios com queda no volume."""
    df_negative_volume = get_negative_volume_laboratories(merged_df)
    df_negative_volume["SITUACAO"] = df_negative_volume["VOLUME"].apply(classify_volume_situation)
    
    st.subheader("Laboratórios com queda no Volume")
    st.dataframe(df_negative_volume)
    
    # Métricas de situação
    situation_metrics = df_negative_volume["SITUACAO"].value_counts()
    columns = st.columns(len(situation_metrics))

    for col, (situation, count) in zip(columns, situation_metrics.items()):
        col.metric(label=situation, value=int(count))

def display_volume_charts(dataframe: pd.DataFrame, columns_list: list) -> None:
    """Exibe gráficos de volume dos dados."""
    try:
        if len(columns_list) == 3:  # LABORATORIO + 2 colunas de dados
            st.subheader("Volume dos Números")
            col1_name = columns_list[1]
            col2_name = columns_list[2]
            df_plot = dataframe.set_index("LABORATORIO")[[col1_name, col2_name]]
            st.bar_chart(df_plot, stack=False)
        else:
            st.subheader("Volume dos Números")
            df_melted = dataframe.melt(id_vars="LABORATORIO", var_name="MES", value_name="VALOR")
            months = df_melted["MES"].unique()

            for month in months:
                df_month = df_melted[df_melted["MES"] == month]
                df_month = df_month.set_index("LABORATORIO")

                st.markdown(f"### Mês: {month}")
                st.bar_chart(df_month["VALOR"])
    except Exception as e:
        st.error(f"Não foi possível gerar os gráficos: {str(e)}")


def run_app() -> None:
    """Função principal que executa a aplicação Streamlit."""
    st.set_page_config(
        page_title="Análise de Volume de Exames Integrados",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://www.extremelycoolapp.com/help",
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "Aplicação desenvolvida pelo time de Integrações Serviços Proprios.\n Para mais duvidas, entrar em contato com Matheus Pansani Marega."
        }
    )

    load_dotenv()
    st.logo(
        image=os.getenv("LOGO_URL_LARGE"),
        size="large"
    )

    st.title("Análise de Volume de Exames Integrados")
    st.markdown("""
    Esta ferramenta automatiza a análise de dados exportados do WeKnow BI, 
    eliminando a necessidade de ajustes manuais no Excel.
    """)

    tab1, tab2 = st.tabs(["Comparação Mensal", "Análise Multi-Meses"])

    with tab1:
        st.header("Comparação de Volume entre Dois Meses")
        # Upload de arquivos
        col1, col2 = st.columns(2)

        with col1:
            file1 = st.file_uploader("Arquivo do Mês Anterior", type=["xlsx"], key="file1_tab1")

        with col2:
            file2 = st.file_uploader("Arquivo do Mês Atual", type=["xlsx"], key="file2_tab1")

        # Botão para processar dados
        if st.button("Processar Dados (Comparação Mensal)", type="primary", key="process_button_tab1"):
            if file1 is not None and file2 is not None:
                # Carregamento e limpeza dos dados
                dataframe1, dataframe2 = load_dataframes_from_excel(file1, file2)
                dataframe1, dataframe2 = clean_dataframes(dataframe1, dataframe2)
                
                st.divider()

                # Mesclagem dos dados
                merged_df = pd.merge(dataframe1, dataframe2, on="LABORATORIO", how="outer")
                merged_df = merged_df.fillna(0)

                columns_list = merged_df.columns.to_list()
                
                try:
                    if len(columns_list) == 3:  # LABORATORIO + 2 colunas de dados
                        col1_name = columns_list[1]
                        col2_name = columns_list[2]

                        # Exibir métricas de volume
                        display_volume_metrics(merged_df, col1_name, col2_name)

                        st.header("Comparação dos Meses")
                        merged_df["Diferença"] = merged_df[col2_name] - merged_df[col1_name]
                        
                        # Layout de duas colunas para dados e análise
                        left_col, right_col = st.columns(2)
                        
                        with left_col:
                            st.dataframe(merged_df, width=1200)
                        
                        with right_col:
                            display_negative_volume_analysis(merged_df)

                    else:
                        # Caso com múltiplas colunas (se o usuário carregar um arquivo com mais de 2 meses aqui)
                        st.dataframe(merged_df)
                        display_missing_laboratories(dataframe1, dataframe2)

                except Exception as e:
                    st.error(f"Erro no processamento dos dados: {str(e)}")
                    st.dataframe(merged_df)
                    display_missing_laboratories(dataframe1, dataframe2)

                st.divider()

                # Exibir gráficos
                display_volume_charts(merged_df, columns_list)

            else:
                st.warning("Por favor, faça upload de ambos os arquivos antes de processar.")

    with tab2:
        st.header("Análise de Volume Multi-Meses")
        multi_month_file = st.file_uploader("Arquivo com Dados de Todos os Meses", type=["xlsx"], key="multi_month_file_tab2")

        if st.button("Processar Dados (Multi-Meses)", type="primary", key="process_button_tab2"):
            if multi_month_file is not None:
                try:
                    df_multi_month = pd.read_excel(multi_month_file)
                    processed_df_multi_month = load_and_process_multi_month_data(df_multi_month)
                    
                    st.subheader("Dados Processados")
                    st.dataframe(processed_df_multi_month)

                    st.divider()

                    st.subheader("Resumo Mensal de Exames")
                    monthly_summary_df = get_monthly_summary(processed_df_multi_month)
                    st.dataframe(monthly_summary_df)
                    st.line_chart(
                        data=monthly_summary_df.set_index("Mês"),
                        x_label= "Mêses",
                        y_label="Volume de Exames",)
                    
                    total_volume = calculate_total_volume(monthly_summary_df)
                    st.metric(label="Total de Exames",value=total_volume)

                    st.divider()

                    st.subheader("Top 5 Laboratórios por Mês")
                    top_labs_df = get_top_n_laboratories_by_month(processed_df_multi_month, n=5)
                    st.dataframe(top_labs_df)

                except Exception as e:
                    st.error(f"Erro ao processar o arquivo multi-meses: {str(e)}")
            else:
                st.warning("Por favor, faça upload do arquivo multi-meses antes de processar.")

if __name__ == "__main__":
    run_app()

