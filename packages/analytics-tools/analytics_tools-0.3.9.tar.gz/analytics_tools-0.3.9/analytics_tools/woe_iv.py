import pandas as pd
import numpy as np
from IPython.display import display_html

def woe_iv_each_feature(df, feature, target):
    lst = []
    for val in df[feature].unique():
        lst.append({
            'Category': val,
            'All': df[df[feature] == val].count()[feature],
            'Good': df[(df[feature] == val) & (df[target] == 0)].count()[feature],
            'Bad': df[(df[feature] == val) & (df[target] == 1)].count()[feature]
        })

    dset = pd.DataFrame(lst)
    dset['Share'] = dset['All'] / dset['All'].sum()
    dset['Bad Rate'] = (dset['Bad'] / dset['All']) * 100
    dset['Good Rate'] = (dset['Good'] / dset['All']) * 100
    dset['Distribution Bad'] = (dset['Bad'] / dset['Bad'].sum()) * 100
    dset['Distribution Good'] = (dset['Good'] / dset['Good'].sum()) * 100
    dset['WoE'] = np.log(dset['Distribution Good'] / dset['Distribution Bad'])
    dset['IV'] = (dset['Distribution Good'] - dset['Distribution Bad']) * dset['WoE']
    dset = dset.replace([np.inf, -np.inf], 0)
    dset['IV'] = dset['IV'].sum()

    dset['Bad Rate'] = dset['Bad Rate'].apply(lambda x: f'{x:.2f}%')
    dset['Good Rate'] = dset['Good Rate'].apply(lambda x: f'{x:.2f}%')
    dset['Distribution Bad'] = dset['Distribution Bad'].apply(lambda x: f'{x:.2f}%')
    dset['Distribution Good'] = dset['Distribution Good'].apply(lambda x: f'{x:.2f}%')

    return dset[['Category', 'All', 'Good', 'Bad', 'Good Rate', 'Bad Rate', 'Distribution Good', 'Distribution Bad', 'WoE', 'IV']]

def woe_iv(df, features, target):
    result_html = ""
    for feature in features:
        woe_iv_df = woe_iv_each_feature(df, feature, target)
        woe_iv_df['Feature'] = feature
        woe_iv_df = woe_iv_df[['Feature', 'Category', 'All', 'Good', 'Bad', 'Good Rate', 'Bad Rate', 'Distribution Good', 'Distribution Bad', 'WoE', 'IV']]
        woe_iv_df = woe_iv_df.sort_values(by='WoE', ascending=False)
        
        def color_woe(val):
            color = 'background: linear-gradient(90deg, transparent {0}%, lightgreen {0}%, lightgreen {1}%, transparent {1}%)'.format(50, 50 + int(val * 50)) if val > 0 else 'background: linear-gradient(90deg, transparent {0}%, lightcoral {0}%, lightcoral {1}%, transparent {1}%)'.format(50 + int(val * 50), 50)
            return color

        woe_iv_df['WoE'] = woe_iv_df['WoE'].apply(lambda x: f'<div style="width: 150px; {color_woe(x)}">{x:.4f}</div>')
        result_html += woe_iv_df.to_html(escape=False, index=False, justify='center', border=0, classes='dataframe table text-center', table_id='woe_iv_table') + "<br>"

    display_html(f'<div style="width: 100%;">{result_html}</div>', raw=True)