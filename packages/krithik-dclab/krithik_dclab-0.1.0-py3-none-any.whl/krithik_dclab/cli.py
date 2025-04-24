import click
import pkg_resources
import os

EXPERIMENTS = {
    "exp1_LoadBalancing": "LoadBalancing",
    "exp2_Multithreading": "Multithreading",
    "exp3_RPC": "RPC",
    "exp4_BullyElection": "BullyElection",
    "exp5_GroupCommunication": "GroupCommunication",
    "exp6_ChandyHaasMisra": "ChandyHaasMisra",
    "exp7_IPC": "IPC",
    "exp8_MutualExclusion": "MutualExclusion",
    "exp9_BerkleyClockSync": "BerkleyClockSync",
    "lab_assign_exp1_LoadBalancing": "LoadBalancing (Lab Assignment)",
    "lab_assign_exp3_RPC": "RPC (Lab Assignment)",
    "lab_assign_exp4_RingElection": "RingElection",
    "lab_assign_exp6_PathPushing": "PathPushing"
}

def get_java_files(experiment):
    """Get list of .java files for the given experiment."""
    try:
        resource_path = f"data/{experiment}"
        click.echo(f"DEBUG: Looking for files in resource path: {resource_path}")
        files = pkg_resources.resource_listdir("krithik_dclab", resource_path)
        java_files = [f for f in files if f.endswith(".java")]
        click.echo(f"DEBUG: Found files: {files}")
        click.echo(f"DEBUG: Java files: {java_files}")
        return java_files
    except Exception as e:
        click.echo(f"DEBUG: Error accessing resource path: {str(e)}")
        return []

def read_java_file(experiment, filename):
    """Read the contents of a .java file."""
    try:
        resource_path = f"data/{experiment}/{filename}"
        return pkg_resources.resource_string("krithik_dclab", resource_path).decode("utf-8")
    except Exception as e:
        click.echo(f"DEBUG: Error reading file {filename}: {str(e)}")
        return None

@click.command()
@click.argument("experiment", required=False)
def print_java_files(experiment):
    """Print the contents of .java files for the specified DC_lab experiment.

    If no experiment is provided, list available experiments.
    Example: dclab-print exp1_LoadBalancing
    """
    if not experiment:
        click.echo("Available experiments:")
        for folder_name, display_name in EXPERIMENTS.items():
            click.echo(f"  - {display_name} (use: {folder_name})")
        click.echo("\nRun 'dclab-print <experiment>' to print .java files for an experiment.")
        return

    if experiment not in EXPERIMENTS:
        click.echo(f"Error: Experiment '{experiment}' not found.")
        click.echo("Available experiments:")
        for folder_name, display_name in EXPERIMENTS.items():
            click.echo(f"  - {display_name} (use: {folder_name})")
        return

    java_files = get_java_files(experiment)
    if not java_files:
        click.echo(f"No .java files found for experiment '{EXPERIMENTS[experiment]}'.")
        return

    click.echo(f"\nJava files for experiment '{EXPERIMENTS[experiment]}':")
    for filename in java_files:
        content = read_java_file(experiment, filename)
        if content:
            click.echo(f"\n--- {filename} ---")
            click.echo(content)
        else:
            click.echo(f"\n--- {filename} ---")
            click.echo("Error: Could not read file.")