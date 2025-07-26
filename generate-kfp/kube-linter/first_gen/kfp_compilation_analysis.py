import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_clean_data(file_path):
    """Load the CSV data and clean it"""
    df = pd.read_csv(file_path)
    
    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    
    # Extract error types from the Status column
    df['Error_Type'] = df['Status'].apply(extract_error_type)
    
    # Extract repository/author information
    df['Repository'] = df['File'].apply(extract_repository)
    
    # Extract file extension
    df['File_Extension'] = df['File'].apply(lambda x: x.split('.')[-1] if '.' in x else 'unknown')
    
    return df

def extract_error_type(status_text):
    """Extract the main error type from status text"""
    if pd.isna(status_text) or status_text.strip() == '':
        return 'Unknown'
    
    # Remove the ❌ symbol and extract the error type
    clean_text = status_text.replace('❌', '').strip()
    
    # Extract the error type (first word before colon)
    if ':' in clean_text:
        error_type = clean_text.split(':')[0].strip()
        return error_type
    else:
        return 'Unknown'

def extract_repository(file_path):
    """Extract repository/author name from file path"""
    parts = file_path.split('__')
    if len(parts) > 1:
        return parts[0]
    else:
        # If no __ separator, try to extract from beginning
        return file_path.split('/')[0] if '/' in file_path else 'unknown'

def analyze_error_patterns(df):
    """Analyze common error patterns"""
    error_patterns = []
    
    for status in df['Status']:
        if pd.notna(status):
            # Extract specific import errors
            if 'ImportError' in status:
                if 'cannot import name' in status:
                    match = re.search(r"cannot import name '(\w+)'", status)
                    if match:
                        error_patterns.append(f"Missing import: {match.group(1)}")
                else:
                    error_patterns.append("ImportError (other)")
            elif 'ModuleNotFoundError' in status:
                match = re.search(r"No module named '(\w+)'", status)
                if match:
                    error_patterns.append(f"Missing module: {match.group(1)}")
            elif 'NameError' in status:
                match = re.search(r"name '(\w+)' is not defined", status)
                if match:
                    error_patterns.append(f"Undefined name: {match.group(1)}")
            elif 'TypeError' in status:
                error_patterns.append("TypeError")
            elif 'AttributeError' in status:
                error_patterns.append("AttributeError")
            else:
                error_patterns.append("Other")
    
    return Counter(error_patterns)

def create_visualizations(df):
    """Create comprehensive visualizations"""
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Error Types Distribution
    plt.subplot(3, 3, 1)
    error_counts = df['Error_Type'].value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(error_counts)))
    bars = plt.bar(range(len(error_counts)), error_counts.values, color=colors)
    plt.xticks(range(len(error_counts)), error_counts.index, rotation=45, ha='right')
    plt.title('Distribution of Error Types', fontsize=14, fontweight='bold')
    plt.ylabel('Count')
    
    # Add value labels on bars
    for bar, value in zip(bars, error_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(value), ha='center', va='bottom', fontweight='bold')
    
    # 2. Top Repositories with Most Errors
    plt.subplot(3, 3, 2)
    top_repos = df['Repository'].value_counts().head(10)
    bars = plt.barh(range(len(top_repos)), top_repos.values, color='coral')
    plt.yticks(range(len(top_repos)), top_repos.index)
    plt.title('Top 10 Repositories with Most Errors', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Errors')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_repos.values)):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                str(value), ha='left', va='center', fontweight='bold')
    
    # 3. Error Types Pie Chart
    plt.subplot(3, 3, 3)
    error_counts_top = df['Error_Type'].value_counts().head(8)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6', '#c4e17f']
    wedges, texts, autotexts = plt.pie(error_counts_top.values, labels=error_counts_top.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Error Types Distribution (Pie Chart)', fontsize=14, fontweight='bold')
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    # 4. Analyze specific error patterns
    plt.subplot(3, 3, 4)
    error_patterns = analyze_error_patterns(df)
    top_patterns = dict(error_patterns.most_common(10))
    
    bars = plt.bar(range(len(top_patterns)), list(top_patterns.values()), color='lightgreen')
    plt.xticks(range(len(top_patterns)), list(top_patterns.keys()), rotation=45, ha='right')
    plt.title('Top 10 Specific Error Patterns', fontsize=14, fontweight='bold')
    plt.ylabel('Count')
    
    # Add value labels
    for bar, value in zip(bars, top_patterns.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(value), ha='center', va='bottom', fontweight='bold')
    
    # 5. Import Errors Analysis
    plt.subplot(3, 3, 5)
    import_errors = [status for status in df['Status'] if pd.notna(status) and 'ImportError' in status]
    import_modules = []
    for error in import_errors:
        if 'cannot import name' in error:
            match = re.search(r"cannot import name '(\w+)'", error)
            if match:
                import_modules.append(match.group(1))
    
    if import_modules:
        module_counts = Counter(import_modules).most_common(10)
        bars = plt.bar(range(len(module_counts)), [count for _, count in module_counts], color='orange')
        plt.xticks(range(len(module_counts)), [module for module, _ in module_counts], rotation=45, ha='right')
        plt.title('Most Common Missing Imports', fontsize=14, fontweight='bold')
        plt.ylabel('Count')
        
        # Add value labels
        for bar, (_, count) in zip(bars, module_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom', fontweight='bold')
    
    # 6. Module Not Found Errors
    plt.subplot(3, 3, 6)
    module_errors = [status for status in df['Status'] if pd.notna(status) and 'ModuleNotFoundError' in status]
    missing_modules = []
    for error in module_errors:
        match = re.search(r"No module named '(\w+)'", error)
        if match:
            missing_modules.append(match.group(1))
    
    if missing_modules:
        missing_counts = Counter(missing_modules).most_common(8)
        bars = plt.bar(range(len(missing_counts)), [count for _, count in missing_counts], color='red', alpha=0.7)
        plt.xticks(range(len(missing_counts)), [module for module, _ in missing_counts], rotation=45, ha='right')
        plt.title('Most Common Missing Modules', fontsize=14, fontweight='bold')
        plt.ylabel('Count')
        
        # Add value labels
        for bar, (_, count) in zip(bars, missing_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom', fontweight='bold')
    
    # 7. Repository Success Rate (if we had successful compilations)
    plt.subplot(3, 3, 7)
    repo_error_counts = df.groupby('Repository').size().sort_values(ascending=False).head(15)
    bars = plt.bar(range(len(repo_error_counts)), repo_error_counts.values, color='purple', alpha=0.7)
    plt.xticks(range(len(repo_error_counts)), repo_error_counts.index, rotation=45, ha='right')
    plt.title('Error Count by Repository (Top 15)', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Errors')
    
    # Add value labels
    for bar, value in zip(bars, repo_error_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(value), ha='center', va='bottom', fontweight='bold')
    
    # 8. Error Type by Repository (Heatmap for top repos and errors)
    plt.subplot(3, 3, 8)
    top_repos_list = df['Repository'].value_counts().head(10).index
    top_errors_list = df['Error_Type'].value_counts().head(6).index
    
    # Create crosstab
    heatmap_data = pd.crosstab(df[df['Repository'].isin(top_repos_list)]['Repository'], 
                              df[df['Repository'].isin(top_repos_list)]['Error_Type'])
    heatmap_data = heatmap_data.reindex(columns=top_errors_list, fill_value=0)
    
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Count'})
    plt.title('Error Types by Repository (Heatmap)', fontsize=14, fontweight='bold')
    plt.ylabel('Repository')
    plt.xlabel('Error Type')
    
    # 9. Summary Statistics
    plt.subplot(3, 3, 9)
    plt.axis('off')
    
    # Calculate summary statistics
    total_errors = len(df)
    unique_repos = df['Repository'].nunique()
    unique_error_types = df['Error_Type'].nunique()
    most_common_error = df['Error_Type'].value_counts().index[0]
    most_problematic_repo = df['Repository'].value_counts().index[0]
    
    summary_text = f"""
    SUMMARY STATISTICS
    
    Total Compilation Errors: {total_errors}
    Unique Repositories: {unique_repos}
    Unique Error Types: {unique_error_types}
    
    Most Common Error: {most_common_error}
    ({df['Error_Type'].value_counts().iloc[0]} occurrences)
    
    Most Problematic Repository: {most_problematic_repo}
    ({df['Repository'].value_counts().iloc[0]} errors)
    
    Top 3 Error Types:
    1. {df['Error_Type'].value_counts().index[0]} ({df['Error_Type'].value_counts().iloc[0]})
    2. {df['Error_Type'].value_counts().index[1]} ({df['Error_Type'].value_counts().iloc[1]})
    3. {df['Error_Type'].value_counts().index[2]} ({df['Error_Type'].value_counts().iloc[2]})
    """
    
    plt.text(0.1, 0.9, summary_text, transform=plt.gca().transAxes, fontsize=12, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('kfp_compilation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_detailed_analysis(df):
    """Print detailed analysis results"""
    print("="*80)
    print("KUBEFLOW PIPELINES COMPILATION REPORT ANALYSIS")
    print("="*80)
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   • Total files analyzed: {len(df)}")
    print(f"   • Unique repositories: {df['Repository'].nunique()}")
    print(f"   • Unique error types: {df['Error_Type'].nunique()}")
    
    print(f"\n🔥 TOP ERROR TYPES:")
    error_counts = df['Error_Type'].value_counts()
    for i, (error, count) in enumerate(error_counts.head(5).items(), 1):
        percentage = (count / len(df)) * 100
        print(f"   {i}. {error}: {count} ({percentage:.1f}%)")
    
    print(f"\n🏗️ MOST PROBLEMATIC REPOSITORIES:")
    repo_counts = df['Repository'].value_counts()
    for i, (repo, count) in enumerate(repo_counts.head(5).items(), 1):
        print(f"   {i}. {repo}: {count} errors")
    
    print(f"\n📦 MISSING MODULES ANALYSIS:")
    module_errors = [status for status in df['Status'] if pd.notna(status) and 'ModuleNotFoundError' in status]
    missing_modules = []
    for error in module_errors:
        match = re.search(r"No module named '(\w+)'", error)
        if match:
            missing_modules.append(match.group(1))
    
    if missing_modules:
        module_counts = Counter(missing_modules).most_common(5)
        for i, (module, count) in enumerate(module_counts, 1):
            print(f"   {i}. {module}: {count} times")
    
    print(f"\n📥 IMPORT ISSUES ANALYSIS:")
    import_errors = [status for status in df['Status'] if pd.notna(status) and 'ImportError' in status]
    import_modules = []
    for error in import_errors:
        if 'cannot import name' in error:
            match = re.search(r"cannot import name '(\w+)'", error)
            if match:
                import_modules.append(match.group(1))
    
    if import_modules:
        import_counts = Counter(import_modules).most_common(5)
        for i, (module, count) in enumerate(import_counts, 1):
            print(f"   {i}. {module}: {count} times")

def main():
    """Main analysis function"""
    # Load the data
    print("Loading and analyzing KFP compilation report...")
    
    # Read the data directly from the file
    df = load_and_clean_data('kfp_compilation_report.csv')
    
    # Print detailed analysis
    print_detailed_analysis(df)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_visualizations(df)
    
    print("\nAnalysis complete! Check 'kfp_compilation_analysis.png' for detailed charts.")

if __name__ == "__main__":
    main()
