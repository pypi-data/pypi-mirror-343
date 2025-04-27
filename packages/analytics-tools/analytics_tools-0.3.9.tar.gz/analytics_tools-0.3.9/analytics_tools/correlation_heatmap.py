import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def correlation_heatmap(df, min_correlation=None):
    """
    Gera um heatmap de correlação das variáveis do DataFrame, com opções de personalização.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        min_correlation (float, optional): Valor mínimo absoluto de correlação a ser exibido. 
                                            Se None, exibe todas as correlações. Defaults to None.
    """

    # Criação de dummies para variáveis categóricas
    df = pd.get_dummies(df, drop_first=True)  

    # Seleciona o método de correlação apropriado
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) == len(df.columns):
      correlation_method = 'pearson'
      correlation_description = "O método de Pearson foi selecionado pois todas as colunas do DataFrame são numéricas."

    elif all(df[col].isin([0,1]).all() for col in df.select_dtypes(include=np.number).columns):
      correlation_method = 'kendall'
      correlation_description = "O método de Kendall foi selecionado pois o dataframe parece conter apenas variáveis binárias."

    else:
      correlation_method = 'spearman'
      correlation_description = "O método de Spearman foi selecionado pois há pelo menos uma coluna não binária."

    # Calcula a matriz de correlação
    correlation_matrix = df.corr(method=correlation_method)

    # Aplica o filtro de correlação mínima (se especificado)
    if min_correlation is not None:
        correlation_matrix = correlation_matrix[
            abs(correlation_matrix) >= min_correlation
        ]

    # Plota o heatmap
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", mask=mask)
    plt.title(f"Heatmap de Correlação ({correlation_method.capitalize()})")
    plt.show()


    # Descrição do método utilizado
    print("\n")
    print(correlation_description)
