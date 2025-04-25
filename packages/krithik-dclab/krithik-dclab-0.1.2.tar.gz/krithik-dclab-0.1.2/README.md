# DCLab

A Python package to print Java source code from Distributed Computing Lab (DC_lab) experiments.

## Installation

Install the package using pip:

### For Windows
```bash
pip install krithik-dclab
```

### For Ubuntu
```bash
sudo pip install krithik-dclab
```

## Usage

After installation, use the `dclab-print` command to print the contents of `.java` files for a specific experiment.

### List Available Experiments

```bash
dclab-print
```

### Print Java Files for an Experiment

```bash
dclab-print exp1
```

This will print the contents of all `.java` files in the `exp1` folder (e.g., `LoadBalancers.java`).

### Downloading files

Downloading in the same directory

```bash
dclab-print exp1 —download
```

Downloading in your own directory

```bash
dclab-print exp1 —outdir <directory_name/path>
```

## Experiments

The package includes the following experiments:
- exp1: LoadBalancing
- exp2: Multithreading
- exp3: RPC
- exp4: BullyElection
- exp5: GroupCommunication
- exp6: ChandyHaasMisra
- exp7: IPC
- exp8: MutualExclusion
- exp9: BerkleyClockSync
- lab_assign_exp1: LoadBalancing
- lab_assign_exp3: RPC
- lab_assign_exp4: RingElection
- lab_assign_exp6: PathPushing

## Requirements

- Python 3.6 or higher
- `click` library (installed automatically)

## License

MIT License