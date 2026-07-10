# """
# visualization.py — Visualization Module (Hour 11-14)

# TODO (Hour 11-14):
# - bar_chart(df, column, save_path=None)
# - line_chart(df, x, y, save_path=None)
# - histogram(df, column, bins=20, save_path=None)
# - scatter_plot(df, x, y, save_path=None)
# - pie_chart(df, column, save_path=None)
# - save_all_charts(df, output_dir)   # batch-generate standard chart set
# """

import matplotlib.pyplot as plt

def bar_chart(df,x,y, save_path = None):
    fig, ax = plt.subplots()
    ax.plot(kind='bar')
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'{x} vs {y}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()

def line_chart(df,x,y,save_path = None):
    fig, ax = plt.subplots()
    ax.plot(df[f], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'{x} vs {y}')
    plt.tight_layout()
    if save_path:
            plt.savefig(save_path)
    else:
            plt.show()
    plt.close()

def histogram(df,column , bins=20, save_path = None):
     fig, ax = plt.subplots()
     ax.hist(df[column], bins = bins)
     ax.set_xlabel(column)
     ax.set_ylabel('Frequecy')
     ax.set_title(f'distributin of {column}')
     plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()

def Scatter_plot(df,x,y, save_path = None):
    fig, ax = plt.subplots()
    ax.scatter(df[x],df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'Scatter plot {x} vs {y}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()