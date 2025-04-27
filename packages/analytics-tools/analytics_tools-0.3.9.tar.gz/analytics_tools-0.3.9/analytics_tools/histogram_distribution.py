import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

def histogram_distribution(df):
    # Select only numeric columns for distribution analysis
    numeric_df = df.select_dtypes(include=['number'])
    
    num_cols = len(numeric_df.columns)
    num_rows = (num_cols + 2) // 3  # Calculate the number of rows needed
    fig, axes = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))
    axes = axes.flatten()  # Flatten the axes array for easier iteration


    for i, col in enumerate(numeric_df.columns):
        sns.histplot(numeric_df[col], kde=True, ax=axes[i], color='#ff4800')
        axes[i].set_title(f'Histograma de {col}')

        # Calculate skewness and kurtosis
        sk = skew(numeric_df[col])
        kurt = kurtosis(numeric_df[col])

        # Determine the distribution shape based on skewness and kurtosis
        if abs(sk) < 0.5 and abs(kurt) < 0.5:
            distribution_shape = "Aproximadamente Simétrica e Mesocúrtica"
            hypotheses = [
                "- Distribuição dos dados é aproximadamente normal;",
                "- A concentração de dados em torno da média é típica;",
                "- Os dados seguem um padrão estável ou esperado;"
            ]
        elif sk > 0.5:
            distribution_shape = "Assimétrica Positiva"
            hypotheses = [
                "- Presença de valores extremos altos (outliers);",
                "- A média é maior que a mediana e a moda;",
                "- Existe crescimento exponencial ou acúmulo progressivo;"
            ]
        elif sk < -0.5:
            distribution_shape = "Assimétrica Negativa"
            hypotheses = [
                "- Pode haver uma pequena quantidade de observações com valores muito abaixo da média, influenciando a distribuição;",
                "- A maior parte da população tem desempenho bom/alto;"
            ]
        elif kurt > 0.5:
            distribution_shape = "Leptocúrtica"
            hypotheses = [
                "- Existência de valores extremos (outliers) com maior frequência;",
                "- Os dados têm maior concentração em torno da média;",
                "- Os dados podem não seguir uma distribuição normal, afetando testes estatísticos baseados nessa suposição;"
            ]
        else:
            distribution_shape = "Platicúrtica"
            hypotheses = [
                "- Os dados têm menor frequência de valores extremos;",
                "- A variabilidade está mais distribuída entre valores médios;"
            ]

        # Display distribution shape and hypotheses
        axes[i].text(0.5, -0.2, f'Formato da Distribuição: {distribution_shape}', transform=axes[i].transAxes, ha='center')
        for j, hypothesis in enumerate(hypotheses):
            axes[i].text(0.5, -0.3 - j * 0.1, hypothesis, transform=axes[i].transAxes, ha='center', fontsize=10) # Updated for better readability
    
    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()
    return fig, axes