import streamlit as st
import pandas as pd
import altair as alt

def data_wrangling(df1,df2):
    df1 = df1.loc[:, (df1 != 0).any(axis=0)]
    df2 = df2.loc[:, (df2 != 0).any(axis=0)]
    return df1, df2

def gerando_dataframe(arquivo1,arquivo2):
    gerar_dataframe = st.button("Gerar DF")
    if gerar_dataframe:
        try:
            df1 = pd.read_excel(arquivo1)
            df2 = pd.read_excel(arquivo2)

            df1, df2 = data_wrangling(df1=df1,df2=df2)

            # col1,col2 = st.columns(2)
            # with col1:
            #     st.dataframe(df1)
            # with col2:
            #     st.dataframe(df2)

            return df1, df2
        except ValueError as e:
            st.warning("Adicione o arquivo para gerar o Dataframe")
            st.stop()
    else:
        st.stop()
    
def comparando_valores(df1,df2):
    df_ausentes1 = df1[~df1['LABORATORIO'].isin(df2['LABORATORIO'])]
    df_ausentes2 = df2[~df2['LABORATORIO'].isin(df1['LABORATORIO'])]

    st.subheader("Laboratorios que não se repetiram")
    col1,col2 = st.columns(2)
    with col1:
        st.write("Arquivo 1")
        st.write(df_ausentes2)

    with col2:
        st.write("Arquivo 2")
        st.write(df_ausentes1)

def main():
    st.set_page_config(
    page_title="Comparação de Dados",
    layout="wide",
    initial_sidebar_state=None,
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    st.title("Comparação de Dados")

    col1,col2 = st.columns(2)

    with col1:
        data_1 = st.file_uploader("Arquivo 1")

    with col2:
        data_2 = st.file_uploader("Arquivo 2")

    st.divider()

    dataframe1, dataframe2 = gerando_dataframe(data_1,data_2)

    mesclagem_externa = pd.merge(dataframe1, dataframe2, on='LABORATORIO', how='outer')
    mesclagem_externa = mesclagem_externa.fillna(0)

    dataframe = mesclagem_externa
    lista_colunas = mesclagem_externa.columns.to_list()
    coluna1 =  lista_colunas[1]
    coluna2 =  lista_colunas[2]
    try:
        if lista_colunas > 3:
            mesclagem_externa["Diferença"] = mesclagem_externa[coluna1] - mesclagem_externa[coluna2]
        st.dataframe(mesclagem_externa)
    except:
        st.dataframe(mesclagem_externa)

    comparando_valores(dataframe1,dataframe2)

    try:
        df_plot = dataframe.set_index('LABORATORIO')[[coluna1, coluna2]]
        st.bar_chart(df_plot,stack=False)
    except KeyError:
        df_melted = dataframe.melt(id_vars='LABORATORIO', var_name='MES', value_name='VALOR')

        # Cria gráfico com barras lado a lado
        chart = alt.Chart(df_melted).mark_bar().encode(
            x=alt.X('LABORATORIO:N', title='Laboratório'),
            y=alt.Y('VALOR:Q', title='Valor'),
            color='MES:N',
            column='MES:N' 
        ).properties(
            width=5000,
            height=1000
        ).resolve_scale(
        x='independent'
        )
        st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()


