import click
from skvai.core import CSVData
from skvai.tasks.regression import regress
from skvai.tasks.classification import Task  # Importing the Task class for classification
from skvai.tasks.clustering import cluster

@click.group()
def cli():
    """SKVAI CLI: Run classification, regression, or clustering."""
    pass

@cli.command()
@click.option("--input", prompt="Path to input CSV", help="Path to input CSV file.")
@click.option("--target", prompt="Target column", help="Name of the target column.")
@click.option("--model", default="LinearRegression", help="Regression model to use.")
@click.option("--output", default="metrics,plot", help="Output options (comma-separated).")
def regression(input, target, model, output):
    """Run regression analysis."""
    data = CSVData.from_csv(input, target)
    result = regress(data, model, output.split(","))
    click.echo(result)

@cli.command()
@click.option("--input", prompt="Path to input CSV", help="Path to input CSV file.")
@click.option("--target", prompt="Target column", help="Name of the target column.")
@click.option("--model", default="RandomForestClassifier", help="Classification model to use.")
@click.option("--output", default="metrics,plot", help="Output options (comma-separated).")
def classification(input, target, model, output):
    """Run classification analysis."""
    # Create an instance of the Task class for classification
    task = Task()
    
    # Set the target column
    task.set_target(target)
    
    # Load the data
    task.load_data(input)
    
    # Train the model and output results
    task.train_and_output(format=output)

    click.echo(f"Classification task completed. Output: {output}")

@cli.command()
@click.option("--input", prompt="Path to input CSV", help="Path to input CSV file.")
@click.option("--model", default="KMeans", help="Clustering model to use.")
@click.option("--clusters", default=3, help="Number of clusters for KMeans (ignored for DBSCAN).")
@click.option("--output", default="plot", help="Output options (comma-separated).")
def clustering(input, model, clusters, output):
    """Run clustering analysis."""
    data = CSVData.from_csv(input)
    result = cluster(
    data=data,
    model=model,
    n_clusters=clusters,
    output=output.split(",")
)

    click.echo(result)
