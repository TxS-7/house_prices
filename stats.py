#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt


def create_graph(df, feature, cont=False):
    print "\n[*] Creating plot for: " + feature
    if not cont:
        fig, axes = plt.subplots(2, 1, sharex=True)
        avg_price = df[[feature, 'SalePrice']].groupby(feature).mean()
        avg_price.plot.bar(ax=axes[0], title=feature, legend=False, color=(0, 0.5, 0.5))
        df[feature].value_counts().sort_index().plot.bar(ax=axes[1])
        axes[0].set_ylabel("SalePrice")
        fig.savefig("output/" + feature + ".png")
    else:
        df[[feature, 'SalePrice']].plot.scatter(x=feature, y="SalePrice", title=feature, legend=False)
        plt.savefig("output/" + feature + ".png")

    plt.close()


def run():
    df = pd.read_csv("train.csv")

    df.info()
    print df.describe()


    # Create continuous features correlation graph with the most correlated features with SalePrice
    corr = df.corr().abs()
    plt.figure(figsize=(20, 20))
    plot = plt.matshow(corr, fignum=1)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation="vertical");
    plt.yticks(range(len(corr.columns)), corr.columns);
    fig = plot.get_figure()
    fig.savefig("output/heatmap.png")


    # Create heatmap of important features only
    high_corr_features = [feat for feat in corr.columns if corr[feat]['SalePrice'] > 0.6]
    high_corr_df = df[high_corr_features]
    high_corr = high_corr_df.corr().abs()
    plot = plt.matshow(high_corr)
    plt.colorbar()
    plt.xticks(range(len(high_corr.columns)), high_corr.columns, rotation="vertical");
    plt.yticks(range(len(high_corr.columns)), high_corr.columns);
    fig = plot.get_figure()
    fig.savefig("output/heatmap_correlated.png")

    print "[+] Columns with high correlation with SalePrice:"
    print "\n".join(high_corr_features)


    # Remove columns that have high correlation with other columns (excluding SalePrice) since they will not add new information
    best_features = high_corr_features
    best_features.remove("1stFlrSF")
    best_features.remove("GarageArea")
    print "[+] Best continuous features after removing correlated features:"
    print "\n".join(best_features)


    pd.plotting.scatter_matrix(high_corr_df[best_features], c=high_corr_df['SalePrice'], figsize=(15, 15), marker='o')
    plt.savefig("output/scatter_matrix.png")



    # Create a graph for price column
    plt.figure()
    plot = df['SalePrice'].plot.hist(title="Sale price distribution")
    df['SalePrice'].plot.kde(ax=plot, secondary_y=True, linewidth=2)
    fig = plot.get_figure()
    fig.savefig("output/sale_price.png")



    # Create average sale price and value count plots for the best features
    create_graph(df, "OverallQual")
    create_graph(df, "TotalBsmtSF", cont=True)
    create_graph(df, "GrLivArea", cont=True)
    create_graph(df, "GarageCars")

    # Create average sale price and value count plots for some categorical features
    create_graph(df, "MSSubClass")
    create_graph(df, "Utilities")
    create_graph(df, "Neighborhood")
    create_graph(df, "Condition1")
    create_graph(df, "Condition2")
    create_graph(df, "HouseStyle")
    create_graph(df, "YearBuilt")
    create_graph(df, "YearRemodAdd")
    create_graph(df, "ExterQual")
    create_graph(df, "ExterCond")
    df['BsmtQual'].fillna(df['BsmtQual'].value_counts().idxmax(), inplace=True)
    df['BsmtCond'].fillna(df['BsmtCond'].value_counts().idxmax(), inplace=True)
    create_graph(df, "BsmtQual")
    create_graph(df, "BsmtCond")
    create_graph(df, "KitchenQual")
    create_graph(df, "SaleType")
    create_graph(df, "SaleCondition")

    #plt.show()

if __name__ == "__main__":
    run()
