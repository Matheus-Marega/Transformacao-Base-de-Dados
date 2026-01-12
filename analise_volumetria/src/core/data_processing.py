import pandas as pd
from typing import Tuple, Union

def clean_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Remove colunas com todos os valores zero de ambos os dataframes."""
    df1 = df1.loc[:, (df1 != 0).any(axis=0)]
    df2 = df2.loc[:, (df2 != 0).any(axis=0)]
    return df1, df2

def get_negative_volume_laboratories(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna um dataframe com laboratórios que tiveram volume negativo."""
    df_negativos = df[df['Diferença'] < 0].copy()
    df_resultado = df_negativos[['LABORATORIO', 'Diferença']].copy()
    df_resultado.rename(columns={'Diferença': 'VOLUME'}, inplace=True)
    return df_resultado

def classify_volume_situation(value: Union[int, float]) -> str:
    """Classifica a situação do volume (Normal, Verificar, Crítico) com base no valor absoluto."""
    abs_value = abs(value)
    if abs_value < 1000:
        return "Normal"
    elif abs_value < 3000:
        return "Verificar"
    else:
        return "Crítico"

def calculate_percentage_variation(previous_month_value: Union[int, float], current_month_value: Union[int, float]) -> str:
    """Calcula a variação percentual entre o valor do mês anterior e o mês atual."""
    if current_month_value == 0:
        return "N/A"
    formula = ((previous_month_value - current_month_value) / current_month_value) * 100
    formula = round(formula, 1)
    return f"{formula}%"


def calculate_total_volumes_and_difference(merged_df: pd.DataFrame, col1_name: str, col2_name: str) -> Tuple[str, str, str]:
    """Calcula o total de exames integrados para dois períodos e a diferença entre eles."""
    total_exams_col1 = int(merged_df[col1_name].sum())
    total_exams_col2 = int(merged_df[col2_name].sum())

    total_exams_col1_str = format(total_exams_col1, ",").replace(",", ".")
    total_exams_col2_str = format(total_exams_col2, ",").replace(",", ".")

    difference_exams = total_exams_col2 - total_exams_col1
    difference_exams_str = format(difference_exams, ",").replace(",", ".")

    return total_exams_col1_str, total_exams_col2_str, difference_exams_str

def calculate_total_volume(monthly_summary_df: pd.DataFrame) -> str:
    total_volume = monthly_summary_df["Total de Exames"].sum()
    total_volume_int = int(total_volume)
    formatted_volume = "{:,}".format(total_volume_int).replace(",", ".")
    return formatted_volume




def load_and_process_multi_month_data(file: pd.DataFrame) -> pd.DataFrame:
    """Carrega e processa um dataframe com dados de múltiplos meses."""
    # Assumimos que a primeira coluna é 'LABORATORIO' e as demais são os meses
    # Se o formato for diferente, esta função precisará ser ajustada.
    df = file.copy()
    # Remove colunas com todos os valores zero
    df = df.loc[:, (df != 0).any(axis=0)]
    return df

def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Gera um resumo mensal do volume total de exames."""
    # Assume que a primeira coluna é 'LABORATORIO' e as demais são os meses
    monthly_summary = df.drop(columns="LABORATORIO").sum().reset_index()
    monthly_summary.columns = ["Mês", "Total de Exames"]

    # Defina a ordem correta dos meses
    ordem_dos_meses = [
        "JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
    ]

    #Converta a coluna "Mês" para um tipo categórico com a ordem definida
    monthly_summary["Mês"] = pd.Categorical(
        monthly_summary["Mês"],
        categories=ordem_dos_meses,
        ordered=True
    )

    # 3. Ordene o DataFrame com base nessa nova ordem (garantia extra)
    monthly_summary = monthly_summary.sort_values("Mês")
    return monthly_summary

def get_top_n_laboratories_by_month(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Retorna os top N laboratórios por volume para cada mês."""
    df_melted = df.melt(id_vars=["LABORATORIO"], var_name="Mês", value_name="Volume")
    top_n_labs = df_melted.groupby("Mês").apply(lambda x: x.nlargest(n, "Volume")).reset_index(drop=True)
    return top_n_labs


def get_highest_integration_volume(dataframe_current_month: pd.DataFrame) -> Tuple[str, Union[int, float]]:
    """Identifica o laboratório com o maior volume de integração."""
    volume_columns = dataframe_current_month.select_dtypes(include=["number"]).columns
    if not volume_columns.empty:
        volume_col = volume_columns[0]
        max_volume_row = dataframe_current_month.loc[dataframe_current_month[volume_col].idxmax()]
        laboratorio = max_volume_row["LABORATORIO"]
        volume = max_volume_row[volume_col]
        return str(laboratorio), float(volume)
    return "N/A", 0


