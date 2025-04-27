import pandas as pd

def score_analysis(df, feature, target):
    
    df_distribuicao = df[df[feature] == 1]
    
    # Ensure the 'score' column is numeric
    df_distribuicao['score'] = pd.to_numeric(df_distribuicao['score'], errors='coerce')
    
    # Create score bins
    df_distribuicao['Faixas Score'] = pd.qcut(df_distribuicao['score'], q=20, duplicates='drop')
    
    # Calculate Quantidade and Target
    score_table = df_distribuicao.groupby('Faixas Score').agg(
        Quantidade=('pedido_id', 'size'),
        Target=(target, 'sum')
    ).reset_index()
    
    # Calculate % Alcance and % Target
    total_records = df_distribuicao.shape[0]
    total_target = df_distribuicao[target].sum()
    score_table['% Alcance'] = ((score_table['Quantidade'] / total_records) * 100).round(3)
    score_table['% Target'] = ((score_table['Target'] / total_target) * 100).round(3)
    
    # Calculate % Alcance Acumulado and % Target Acumulado
    score_table['% Alcance Acumulado'] = score_table['% Alcance'].cumsum().round(3)
    score_table['% Target Acumulado'] = score_table['% Target'].cumsum().round(3)
    score_table = score_table.round(3)
    score_table_styled = score_table.style.set_properties(**{'font-size': '10pt', 'padding': '5px', 'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt')]}]).bar(subset=['% Alcance'], color='lightgreen').bar(subset=['% Target'], color='lightcoral').bar(subset=['% Alcance Acumulado'], color='lightblue').bar(subset=['% Target Acumulado'], color='lightpink').set_table_styles([{'selector': 'th', 'props': [('min-width', '100px')]}]).hide(axis='index')

    
    return score_table_styled