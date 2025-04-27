import seaborn as sns
import matplotlib.pyplot as plt

def bivariate_analysis(df, target):
    
    columns = df.columns.to_list()
    
    # Number of subplots
    num_plots = len(columns)

    # Create subplots
    fig, axes = plt.subplots(nrows=num_plots, ncols=2, figsize=(15, 5 * num_plots))

    # Flatten the axes array
    axes = axes.reshape(num_plots, 2)

    # Plot each categorical column
    for i, col in enumerate(columns):
        if df[col].nunique() > 0:
            total = len(df[col])
            total_target = len(df[df[target] == 1][col])

            # Get unique values and their order
            unique_vals = df[col].value_counts().index
            
            # Countplot
            sns.countplot(x=col, data=df, ax=axes[i, 0], order=unique_vals)
            for p in axes[i, 0].patches:
                percentage = '{:.1f}%'.format(100 * p.get_height() / total)
                x = p.get_x() + p.get_width() / 2 - 0.05
                y = p.get_height()
                axes[i, 0].annotate(percentage, (x, y), ha='center', fontsize=9)
            axes[i, 0].set_title(f'Count', fontsize=9)
            axes[i, 0].set_xlabel(col, fontsize=9)
            axes[i, 0].set_ylabel('Amount', fontsize=9)
            axes[i, 0].tick_params(axis='x', labelrotation=45, labelsize=7)
            
            # Countplot with respect to 'target' where target = 1
            sns.countplot(x=col, data=df[df[target] == 1], ax=axes[i, 1], order=unique_vals)
            for p in axes[i, 1].patches:
                percentage = '{:.1f}%'.format(100 * p.get_height() / total_target)
                x = p.get_x() + p.get_width() / 2 - 0.05
                y = p.get_height()
                axes[i, 1].annotate(percentage, (x, y), ha='center', fontsize=9)
            axes[i, 1].set_title(f'{col} (target = 1)', fontsize=9)
            axes[i, 1].set_xlabel(col, fontsize=9)
            axes[i, 1].set_ylabel('Amount', fontsize=9)
            axes[i, 1].tick_params(axis='x', labelrotation=45, labelsize=7)
        else:
            axes[i, 0].remove()
            axes[i, 1].remove()

    plt.tight_layout()
    plt.show()