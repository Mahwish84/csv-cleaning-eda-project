import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a nice visual style for the charts
sns.set_theme(style="whitegrid")

def run_eda(file_path):
    print(f"📊 Starting EDA on '{file_path}'...\n")
    
    # 1. Load the clean data
    df = pd.read_csv(file_path)
    
    # 2. Basic Structure
    print("--- 1. DATASET OVERVIEW ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print("\nData Types:")
    print(df.dtypes)
    
    # 3. Missing Values
    print("\n--- 2. MISSING VALUES ---")
    missing = df.isnull().sum()
    print(missing[missing > 0] if not missing.empty else "No missing values!")
    
    # 4. Summary Statistics (Numbers)
    print("\n--- 3. SUMMARY STATISTICS (NUMBERS) ---")
    print(df[['age', 'salary']].describe().round(2))
    
    # 5. Summary Statistics (Categories)
    print("\n--- 4. SUMMARY STATISTICS (TEXT) ---")
    print("Top Countries:")
    print(df['country'].value_counts().head())
    print("\nMost Common Job/Notes:")
    print(df['notes'].value_counts().head(3))

    # ==========================================
    # VISUALIZATIONS
    # ==========================================
    print("\n🎨 Generating charts... (Close the chart window to see the next one)")
    
    # Chart 1: Salary Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['salary'].dropna(), bins=10, kde=True, color='blue')
    plt.title('Distribution of Salaries')
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Employees')
    plt.show()

    # Chart 2: Average Salary by Country
    plt.figure(figsize=(8, 5))
    avg_salary_country = df.groupby('country')['salary'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_salary_country.index, y=avg_salary_country.values, palette='viridis')
    plt.title('Average Salary by Country')
    plt.xlabel('Country')
    plt.ylabel('Average Salary ($)')
    plt.show()

    # Chart 3: Age vs Salary (Scatter Plot)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='age', y='salary', hue='country', s=100)
    plt.title('Age vs Salary by Country')
    plt.xlabel('Age')
    plt.ylabel('Salary ($)')
    plt.show()

if __name__ == "__main__":
    # Make sure this matches the name of the file your cleaning script produced
    run_eda('clean_data.csv') 