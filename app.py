import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # <-- Ajoute cette ligne avant d'importer pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request
import io
import base64

app = Flask(__name__)

DATA_ROOT = "data"

def list_mutation_folders():
    folders = [f for f in os.listdir(DATA_ROOT) if os.path.isdir(os.path.join(DATA_ROOT, f))]
    print("Dossiers trouvés :", folders)
    return folders


def list_csv_files(mutation_folder):
    folder_path = os.path.join(DATA_ROOT, mutation_folder)
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    print(f"Fichiers CSV dans {mutation_folder} :", files)
    return files


def load_results(mutation_folder, csv_file):
    path = os.path.join(DATA_ROOT, mutation_folder, csv_file)
    df = pd.read_csv(path, sep=';')
    return df

def describe_results(df):
    desc = df.describe()
    return desc

def plot_evolution(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['Generation'], df['Best Distance'], label='Best Distance')
    plt.plot(df['Generation'], df['Average Fitness'], label='Average Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.legend()
    plt.title('Evolution des scores')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_comparison(all_results):
    plt.figure(figsize=(10,5))
    for label, df in all_results.items():
        plt.plot(df['Generation'], df['Best Distance'], label=f'{label}')
    plt.xlabel('Generation')
    plt.ylabel('Best Distance')
    plt.legend()
    plt.title('Comparaison convergence (Best Distance)')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    mutation_folders = list_mutation_folders()
    return render_template('index.html', mutation_folders=mutation_folders)

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    mutation_folders = list_mutation_folders()
    if not mutation_folders:
        return "Aucun dossier de mutation trouvé.", 404

    # Récupérer le dossier sélectionné (POST ou GET)
    selected_folder = request.form.get('mutation_folder')
    if not selected_folder:
        # Si pas de POST, prendre le premier dossier par défaut
        selected_folder = request.args.get('mutation_folder', mutation_folders[0])

    csv_files = list_csv_files(selected_folder)
    if not csv_files:
        return f"Aucun fichier CSV trouvé dans le dossier {selected_folder}.", 404

    # Récupérer le CSV sélectionné
    selected_csv = request.form.get('csv_file')

    # Si dossier changé ou pas de csv sélectionné, prendre le premier CSV du dossier
    if (not selected_csv) or (request.method == 'POST' and 'mutation_folder' in request.form and request.form['mutation_folder'] != request.form.get('prev_folder')):
        selected_csv = csv_files[0]

    df = load_results(selected_folder, selected_csv)
    desc = describe_results(df).to_html(classes='table table-striped')
    plot_url = plot_evolution(df)

    return render_template('explore.html',
                           mutation_folders=mutation_folders,
                           selected_folder=selected_folder,
                           csv_files=csv_files,
                           selected_csv=selected_csv,
                           desc=desc,
                           plot_url=plot_url)


@app.route('/compare')
def compare():
    mutation_folders = list_mutation_folders()
    all_results = {}
    for folder in mutation_folders:
        csv_files = list_csv_files(folder)
        if csv_files:
            df = load_results(folder, csv_files[0])
            all_results[folder] = df
    plot_url = plot_comparison(all_results)  # Le graphique reste inchangé

    stats = {folder: df.iloc[-1][['Best Distance', 'Average Fitness']].to_dict() for folder, df in all_results.items()}

    # Récupérer les paramètres GET pour tri
    sort_by = request.args.get('sort_by', 'Best Distance')
    order = request.args.get('order', 'asc')

    if sort_by not in ['Best Distance', 'Average Fitness']:
        sort_by = 'Best Distance'
    if order not in ['asc', 'desc']:
        order = 'asc'

    reverse = (order == 'desc')
    sorted_stats = dict(sorted(stats.items(), key=lambda item: item[1][sort_by], reverse=reverse))

    return render_template('compare.html', plot_url=plot_url, stats=sorted_stats, sort_by=sort_by, order=order)

if __name__ == '__main__':
    app.run(debug=True)
