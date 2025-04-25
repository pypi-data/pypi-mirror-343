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
    try:
        resource_path = f"data/{experiment}"
        files = pkg_resources.resource_listdir("krithik_dclab", resource_path)
        java_files = [f for f in files if f.endswith(".java")]
        return java_files
    except Exception as e:
        click.echo(f"Error accessing resource path: {str(e)}")
        return []

def read_java_file(experiment, filename):
    try:
        resource_path = f"data/{experiment}/{filename}"
        return pkg_resources.resource_string("krithik_dclab", resource_path).decode("utf-8")
    except Exception as e:
        click.echo(f"Error reading file {filename}: {str(e)}")
        return None

def download_file(content, filename, out_dir):
    try:
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        click.echo(f"Saved: {filepath}")
    except Exception as e:
        click.echo(f"Failed to save {filename}: {str(e)}")

@click.command()
@click.argument("experiment", required=False)
@click.option("--download", is_flag=True, help="Download .java files instead of just displaying.")
@click.option("--outdir", default="downloaded_java_files", help="Directory to save downloaded files.")
def print_java_files(experiment, download, outdir):
    if not experiment:
        click.echo("Available experiments:")
        for folder_name, display_name in EXPERIMENTS.items():
            click.echo(f"  - {display_name} (use: {folder_name})")
        click.echo("\nRun 'dclab-print <experiment>' to print or download .java files.")
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
            if download:
                download_file(content, filename, os.path.join(outdir, experiment))
            else:
                click.echo(f"\n--- {filename} ---")
                click.echo(content)
        else:
            click.echo(f"\n--- {filename} ---")
            click.echo("Error: Could not read file.")
