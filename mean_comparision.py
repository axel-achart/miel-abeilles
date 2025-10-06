import os
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Optional: Use scienceplots for better visuals (pip install scienceplots)
try:
    import seaborn as sns
    import scienceplots
    plt.style.use(["science", "grid", "high-vis", "no-latex"])
    sns.set_context("paper", font_scale=1.15)
except ImportError:
    print("scienceplots/seaborn not found, using default matplotlib style.")

def process_mutation_rate_directory(rate_dir_path, output_dir):
    """
    Process all CSV files in a mutation rate directory and calculate mean and std by generation.
    """
    rate_name = rate_dir_path.name
    csv_files = list(rate_dir_path.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {rate_name}")
        return None

    print(f"\nProcessing {rate_name}: {len(csv_files)} CSV files")
    all_dataframes = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, delimiter=';')
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            all_dataframes.append(df)
        except Exception as e:
            print(f"  Warning: Could not read {csv_file}: {e}")
            continue

    if not all_dataframes:
        print(f"  No valid CSV files found in {rate_name}")
        return None

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    mean_by_generation = combined_df.groupby('generation').agg({
        'best_distance': 'mean',
        'best_fitness': 'mean',
        'average_fitness': 'mean'
    }).reset_index()
    std_by_generation = combined_df.groupby('generation').agg({
        'best_distance': 'std',
        'best_fitness': 'std',
        'average_fitness': 'std'
    }).reset_index()
    std_columns = {col: f"{col}_std" for col in std_by_generation.columns if col != 'generation'}
    std_by_generation = std_by_generation.rename(columns=std_columns)
    result_df = mean_by_generation.merge(std_by_generation, on='generation')
    output_file = Path(output_dir) / f"{rate_name}_mean.csv"
    result_df.to_csv(output_file, index=False)
    print(f"  Processed {len(all_dataframes)} files")
    print(f"  Generations: {result_df['generation'].min()} to {result_df['generation'].max()}")
    print(f"  Saved to: {output_file}")
    return result_df

def main():
    # MODIFY THESE PATHS FOR YOUR DATA:
    data_path = Path("data")  # Your base data directory
    output_dir = Path("output_means")  # Where to save mean CSV files
    output_dir.mkdir(exist_ok=True)
    processed_results = {}

    if data_path.exists():
        rate_directories = [d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('mutation_rate_')]
        rate_directories.sort()
        print(f"Found {len(rate_directories)} mutation rate directories:")
        for rate_dir in rate_directories:
            print(f"  {rate_dir.name}")
        for rate_dir in rate_directories:
            result_df = process_mutation_rate_directory(rate_dir, output_dir)
            if result_df is not None:
                processed_results[rate_dir.name] = result_df
        print(f"\n=== PROCESSING COMPLETE ===")
        print(f"Successfully processed {len(processed_results)} mutation rates")
        print(f"Mean CSV files saved to {output_dir}/ directory")
        if processed_results:
            create_comparison_plots(processed_results, output_dir)
    else:
        print(f"Data directory {data_path} not found!")
        print("Please ensure your data is organized as: data/rate_X.X/resultsXXX.csv")

def create_comparison_plots(processed_results, output_dir):
    print(f"\nCreating comparative visualizations...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    # Plot 1: Best Distance
    ax = axes[0, 0]
    for i, (rate_name, df) in enumerate(sorted(processed_results.items())):
        color = colors[i % len(colors)]
        ax.plot(df['generation'], df['best_distance'], label=rate_name.replace('_', ' '), color=color, linewidth=2)
        if 'best_distance_std' in df.columns:
            ax.fill_between(df['generation'], df['best_distance'] - df['best_distance_std'],
                            df['best_distance'] + df['best_distance_std'], alpha=0.2, color=color)
    ax.set_title('Best Distance Over Generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Best Distance')
    ax.legend()
    # Plot 2: Best Fitness
    ax = axes[0, 1]
    for i, (rate_name, df) in enumerate(sorted(processed_results.items())):
        color = colors[i % len(colors)]
        ax.plot(df['generation'], df['best_fitness'], label=rate_name.replace('_', ' '), color=color, linewidth=2)
        if 'best_fitness_std' in df.columns:
            ax.fill_between(df['generation'], df['best_fitness'] - df['best_fitness_std'],
                            df['best_fitness'] + df['best_fitness_std'], alpha=0.2, color=color)
    ax.set_title('Best Fitness Over Generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Best Fitness')
    ax.legend()
    # Plot 3: Average Fitness
    ax = axes[1, 0]
    for i, (rate_name, df) in enumerate(sorted(processed_results.items())):
        color = colors[i % len(colors)]
        ax.plot(df['generation'], df['average_fitness'], label=rate_name.replace('_', ' '), color=color, linewidth=2)
        if 'average_fitness_std' in df.columns:
            ax.fill_between(df['generation'], df['average_fitness'] - df['average_fitness_std'],
                            df['average_fitness'] + df['average_fitness_std'], alpha=0.2, color=color)
    ax.set_title('Average Fitness Over Generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Average Fitness')
    ax.legend()
    # Plot 4: Final performance comparison
    ax = axes[1, 1]
    final_metrics = {}
    for rate_name, df in sorted(processed_results.items()):
        final_10 = df.tail(10)
        final_metrics[rate_name] = {
            'best_distance': final_10['best_distance'].mean(),
            'best_fitness': final_10['best_fitness'].mean(),
            'average_fitness': final_10['average_fitness'].mean()
        }
    rates = list(final_metrics.keys())
    x_pos = np.arange(len(rates))
    width = 0.25
    ax.bar(x_pos - width, [final_metrics[r]['best_distance'] for r in rates], width, label='Best Distance', alpha=0.8, color=colors[0])
    ax.bar(x_pos, [final_metrics[r]['best_fitness'] for r in rates], width, label='Best Fitness', alpha=0.8, color=colors[1])
    ax.bar(x_pos + width, [final_metrics[r]['average_fitness'] for r in rates], width, label='Average Fitness', alpha=0.8, color=colors[2])
    ax.set_title('Final Performance (Last 10 Generations Average)')
    ax.set_xlabel('Mutation Rate')
    ax.set_ylabel('Value')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([r.replace('_', ' ') for r in rates], rotation=45, ha='right')
    ax.legend()
    plt.suptitle('Evolutionary Algorithm Performance by Mutation Rate', fontsize=16, fontweight='bold')
    plot_file = output_dir / 'mutation_rate_comparison.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Comparison plot saved to: {plot_file}")

if __name__ == "__main__":
    main()
