import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(path):
    return pd.read_csv(path)

def summarize(df):
    print("🔍 Missing Values:")
    print(df.isnull().sum())

    print("\n📈 Feature Distributions:")
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        print(f"\n-- {col} --")
        print(df[col].describe())

def plot_distributions(df, cols=None, cols_per_row=3):
    cols = cols or df.select_dtypes(include=['number']).columns
    total = len(cols)
    rows = (total + cols_per_row - 1) // cols_per_row

    fig, axes = plt.subplots(rows, cols_per_row, figsize=(cols_per_row * 5, rows * 4))
    axes = axes.flatten()

    for i, col in enumerate(cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], bins=30)
        axes[i].set_title(col)
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle("Feature Distributions", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


def plot_correlation(df):
    numeric_df = df.select_dtypes(include=['number'])
    plt.figure(figsize=(12, 10))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title("📊 Feature Correlation Matrix")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    PATH = "../data/final_output_with_elo.csv"  # adjust if needed
    df = load_data(PATH)
    
    summarize(df)
    plot_distributions(df)
    plot_correlation(df)
