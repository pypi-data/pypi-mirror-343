# EM-TAX

A Python package for running taxonomic profiling workflows on HPC systems with conda environment support.

## Overview

EM-TAX simplifies the process of running taxonomic profiling workflows on High-Performance Computing (HPC) systems. It automates the following tasks:

- Connecting to HPC systems using SSH
- Uploading raw sequencing data
- Downloading and setting up reference databases
- Configuring and submitting Snakemake workflows with conda environment support
- Monitoring job progress and checking job status
- Retrieving results and abundance matrices

## Installation

```bash
pip install emtax
```

## Prerequisites

- SSH access to an HPC system
- Python 3.9 or higher
- Conda or Mamba installed on the HPC system (for environment activation)

## Conda Environment Setup

TaxoPipe requires a conda environment on the HPC system. While TaxoPipe can automatically generate the environment file, you may want to manually create it before running the workflow:

1. Create a file named `environment.yaml` with the following content (do NOT run these lines as commands!):

> **Tip:** Save the following block as `environment.yaml` and create the environment with:
> ```bash
> conda env create -f environment.yaml
> ```

```yaml
name: emtax_env
channels:
  - bioconda
  - conda-forge
  - defaults
dependencies:
  - python=3.9.19
  - snakemake-minimal=7.32.4
  - kraken2=2.1.3
  - bracken=2.8
  - krona=2.7.1
  - fastp=0.23.4
  - bowtie2=2.5.2
  - samtools=1.18
  - pandas=2.1.1
  - numpy=1.23.5
  - biopython=1.81
  - scikit-bio=0.5.8
  - pip=23.3.1
  - pip:

```

2. Create the conda environment on the HPC system:

```bash
# SSH into your HPC system
ssh username@hpc.example.edu

# Navigate to your working directory
cd /path/to/your/project

# Create the conda environment from the YAML file
conda env create -f environment.yaml

# Activate the environment
conda activate emtax_env
```

3. Once the environment is created, you can submit your TaxoPipe job using the `--conda-env` option to specify the environment name:

```bash
emtax hpc \
  -r /path/to/sample1_L001_R1.fastq.gz \
  [...other options...] \
  --conda-env emtax_env
```

## Usage

### Basic Commands

#### Submit a job

##### For paired-end data:

```bash
emtax hpc \
  -r /path/to/sample1_L001_R1.fastq.gz \
  -r /path/to/sample1_L001_R2.fastq.gz \
  -r /path/to/sample1_L002_R1.fastq.gz \
  -r /path/to/sample1_L002_R2.fastq.gz \
  -o /path/on/hpc/output \
  --kraken-db /path/on/hpc/kraken2_db \
  --corn-db /path/on/hpc/corn_db \
  --host hpc.example.edu \
  --username myuser \
  --password-auth
```

##### For single-end data:

```bash
emtax hpc \
  -r /path/to/sample1.fastq.gz \
  -r /path/to/sample2.fastq.gz \
  -o /path/on/hpc/output \
  --kraken-db /path/on/hpc/kraken2_db \
  --corn-db /path/on/hpc/corn_db \
  --host hpc.example.edu \
  --username myuser \
  --password-auth
```

Example with real paths:

```bash
emtax hpc \
  -r /Users/username/Downloads/S1_L001_R1.fastq.gz \
  -r /Users/username/Downloads/S1_L001_R2.fastq.gz \
  -r /Users/username/Downloads/S1_L002_R1.fastq.gz \
  -r /Users/username/Downloads/S1_L002_R2.fastq.gz \
  -o /home/username/toxotest/output \
  --kraken-db /home/username/toxotest/Kraken2_DB \
  --corn-db /home/username/toxotest/Zm-B73-REFERENCE-NAM-5.0 \
  --host hpcr8o2rnp.uta.edu \
  --username username \
  --password-auth
```

#### Check job status

```bash
emtax status 12345 --host hpc.example.edu --username myuser --password-auth
```

Example with real job ID:

```bash
emtax status 23104 --host hpcr8o2rnp.uta.edu --username username --password-auth
```

#### Download results

```bash
emtax download \
  --output-dir /path/on/hpc/output \
  --local-dir ./results \
  --host hpc.example.edu \
  --username myuser
```

#### Download abundance matrix

To download just the abundance matrix file (the final result of the workflow):

```bash
emtax get-abundance \
  --output-dir /path/on/hpc/output \
  --local-dir ./results \
  --host hpc.example.edu \
  --username myuser \
  --password-auth
```

You can also wait for a specific job to complete before downloading:

```bash
emtax get-abundance \
  --output-dir /path/on/hpc/output \
  --local-dir ./results \
  --host hpc.example.edu \
  --username myuser \
  --password-auth \
  --job-id 23110
```

### Command Options

#### HPC Command Options

- `-r, --raw-files`: Raw FASTQ files to process (use multiple -r flags for multiple files)
- `-o, --output-dir`: Output directory on the HPC system
- `--kraken-db`: Path to Kraken2 database on the HPC system
- `--corn-db`: Path to corn genome database for host removal
- `--host`: HPC hostname (default: uses SSH config)
- `--username`: HPC username (default: uses SSH config)
- `--identity-file`: Path to SSH identity file/private key (e.g., ~/.ssh/id_rsa_toxolib)
- `--password-auth`: Use password authentication instead of SSH keys
- `--partition`: HPC partition/queue to use (default: normal)
- `--threads`: Number of threads to request (default: 16)
- `--memory`: Memory to request (default: 200GB)
- `--time`: Time limit for the job (default: 48:00:00)
- `--conda-env`: Specify a custom conda environment name (default: emtax_env)
- `--no-download-db`: Skip downloading reference databases
- `--no-upload-data`: Skip uploading raw data files (use if files are already on HPC)
- `--dry-run`: Show what would be done without actually connecting to HPC
- `--help`: Show help message

#### Status Command Options

- `job_id`: The SLURM job ID to check (required)
- `--host`: HPC hostname
- `--username`: HPC username
- `--identity-file`: Path to SSH identity file (private key)
- `--password-auth`: Use password authentication instead of key-based

#### Download Command Options

- `--output-dir`: HPC output directory path (required)
- `--local-dir`: Local directory to save downloaded files (default: current directory)
- `--host`: HPC hostname
- `--username`: HPC username
- `--identity-file`: Path to SSH identity file (private key)
- `--password-auth`: Use password authentication instead of key-based
- `--file-pattern`: File pattern to download (default: *.csv)

#### Get-Abundance Command Options

- `--output-dir`: HPC output directory path (required)
- `--local-dir`: Local directory to save the abundance matrix file (default: current directory)
- `--host`: HPC hostname
- `--username`: HPC username
- `--identity-file`: Path to SSH identity file (private key)
- `--password-auth`: Use password authentication instead of key-based
- `--job-id`: Job ID to check before downloading (will wait for job completion)

## Reference Databases

TaxoPipe can automatically download and set up the required reference databases:

- **Kraken2 Database**: Standard microbial database for taxonomic classification
  - Source: https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz

- **Corn Genome Database**: Used for host removal
  - Source: https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip

### Manual Database Setup

If you prefer to manually download and set up the reference databases:

1. **Download and prepare the Kraken2 database**:

```bash
# On your local machine
# Download the Kraken2 database
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20230605.tar.gz

# Extract the database
mkdir -p k2_standard
tar -xzvf k2_standard_20230605.tar.gz -C k2_standard
```

2. **Download and prepare the Corn database**:

```bash
# On your local machine
# Download the Corn database
wget https://genome-idx.s3.amazonaws.com/bt/Zm-B73-REFERENCE-NAM-5.0.zip

# Extract the database
unzip Zm-B73-REFERENCE-NAM-5.0.zip
```

3. **Transfer databases to HPC**:

```bash
# First, create the destination directories on HPC
ssh username@hpc.example.edu "mkdir -p /path/on/hpc/Kraken2_DB"
ssh username@hpc.example.edu "mkdir -p /path/on/hpc/Zm-B73-REFERENCE-NAM-5.0"
```

**Option A: Using scp (simple but may fail with large directories)**
```bash
# Transfer Kraken2 database
scp -r k2_standard/* username@hpc.example.edu:/path/on/hpc/Kraken2_DB/

# Transfer Corn database
scp -r Zm-B73-REFERENCE-NAM-5.0/* username@hpc.example.edu:/path/on/hpc/Zm-B73-REFERENCE-NAM-5.0/
```

**Option B: Using rsync (recommended for large transfers)**
```bash
# Transfer Kraken2 database
rsync -avz k2_standard/ username@hpc.example.edu:/path/on/hpc/Kraken2_DB/

# Transfer Corn database
rsync -avz Zm-B73-REFERENCE-NAM-5.0/ username@hpc.example.edu:/path/on/hpc/Zm-B73-REFERENCE-NAM-5.0/
```

**Option C: Using tar+ssh (for troubleshooting transfer issues)**
```bash
# For Kraken2 database
tar -czf - k2_standard | ssh username@hpc.example.edu "tar -xzf - -C /path/on/hpc && mv /path/on/hpc/k2_standard/* /path/on/hpc/Kraken2_DB/ && rmdir /path/on/hpc/k2_standard"

# For Corn database
tar -czf - Zm-B73-REFERENCE-NAM-5.0 | ssh username@hpc.example.edu "tar -xzf - -C /path/on/hpc && mv /path/on/hpc/Zm-B73-REFERENCE-NAM-5.0/* /path/on/hpc/Zm-B73-REFERENCE-NAM-5.0/ && rmdir /path/on/hpc/Zm-B73-REFERENCE-NAM-5.0"
```

**Troubleshooting Transfer Issues**:

If you encounter "path canonicalization failed" or other transfer errors:

1. Verify the destination directory exists:
   ```bash
   ssh username@hpc.example.edu "ls -la /path/on/hpc/"
   ```

2. Check permissions:
   ```bash
   ssh username@hpc.example.edu "ls -la /path/on/hpc/ | grep Kraken2_DB"
   ssh username@hpc.example.edu "ls -la /path/on/hpc/ | grep Zm-B73"
   ```

3. Try transferring files individually:
   ```bash
   # For Corn database
   for file in Zm-B73-REFERENCE-NAM-5.0/*.bt2; do
     scp "$file" username@hpc.example.edu:/path/on/hpc/Zm-B73-REFERENCE-NAM-5.0/
   done
   ```

3. **Transfer your sequencing data**:

```bash
# On your local machine
# Create a directory for your data on HPC
ssh username@hpc.example.edu "mkdir -p /path/on/hpc/output/Raw_Data"

# Transfer your FASTQ files
scp /path/to/local/sample_L001_R1.fastq.gz username@hpc.example.edu:/path/on/hpc/output/Raw_Data/
scp /path/to/local/sample_L001_R2.fastq.gz username@hpc.example.edu:/path/on/hpc/output/Raw_Data/
# Repeat for all your FASTQ files
```

4. **Run TaxoPipe with the `--no-upload-data` flag**:

```bash
emtax hpc \
  -r /path/to/sample1_L001_R1.fastq.gz \
  -r /path/to/sample1_L001_R2.fastq.gz \
  -o /path/on/hpc/output \
  --kraken-db /path/on/hpc/Kraken2_DB \
  --corn-db /path/on/hpc/Zm-B73-REFERENCE-NAM-5.0 \
  --host hpc.example.edu \
  --username myuser \
  --password-auth \
  --no-upload-data
```

## Output Structure

```
output/
├── Raw_Data/                  # Raw input files
├── workflow/                  # Workflow files and scripts
│   ├── Snakefile              # Snakemake workflow definition
│   ├── config.yaml            # Workflow configuration
│   ├── environment.yaml       # Conda environment definition
│   ├── scripts/               # Helper scripts
│   │   └── create_abundance_matrix.py  # Script for abundance matrix creation
│   ├── submit_job.sh          # Job submission script
│   ├── emtax_[job_id].out  # SLURM output log file
│   └── emtax_[job_id].err  # SLURM error log file

## Job Log Files

TaxoPipe generates log files for each job submission. These log files contain important information about the job execution, including any errors or warnings.

### Log File Locations

The log files are created in the workflow directory with the following naming pattern:

- **Output log**: `[output_dir]/workflow/emtax_[job_id].out`
- **Error log**: `[output_dir]/workflow/emtax_[job_id].err`

For example, if your output directory is `/home/username/toxotest/output` and your job ID is `23109`, the log files would be located at:

```
/home/username/toxotest/output/workflow/emtax_23109.out
/home/username/toxotest/output/workflow/emtax_23109.err
```

### Viewing Log Files

You can view the log files using the following commands:

```bash
# SSH into your HPC system
ssh username@hpc.example.edu

# View the output log
cat /path/to/output/workflow/emtax_[job_id].out

# View the error log
cat /path/to/output/workflow/emtax_[job_id].err

# Or use 'tail' to follow the logs in real-time
tail -f /path/to/output/workflow/emtax_[job_id].out
```
```text
Results/
└── Taxonomic_Profiling/
    ├── 1_DNA_Kraken2/                   # Kraken2 classification results
    ├── 2_DNA_Bracken/                   # Bracken abundance estimation
    ├── 3_DNA_Krona/                     # Krona input files
    ├── 4_DNA_Krona_HTML/                # Krona visualizations
    └── 5_DNA_Relative_Abundance_Matrix_Python/  # Abundance matrices
```
```

## Flexible Input File Support

EM-TAX now supports multiple input file formats and automatically detects the file type:

### Supported Input Formats

1. **Multi-lane paired-end files**: Files with lane information (e.g., `S1_L001_R1.fastq.gz`, `S1_L001_R2.fastq.gz`)
2. **Lane-combined paired-end files**: Files without lane information (e.g., `S1_R1.fastq.gz`, `S1_R2.fastq.gz`)
3. **Single-end files**: Files without pair information (e.g., `S1.fastq.gz`)

The workflow automatically detects the file format and processes accordingly:
- For multi-lane files, it combines the lanes for each sample
- For lane-combined files, it uses them directly
- For single-end files, it processes them in single-end mode without creating unnecessary empty R2 files

### Important Notes for Single-End Data

- When using true single-end data, provide files with the naming pattern `SampleName.fastq.gz` (without R1/R2 designation)
- Do not concatenate paired-end files (R1+R2) to create a single-end file, as this will lead to suboptimal results
- All tools in the workflow (fastp, bowtie2, kraken2) will automatically run in the appropriate mode based on the input file type

## Workflow Features

- **Automatic Authentication**: Multiple authentication methods with fallback options
- **Network Resilience**: Handles network connectivity issues and provides offline mode support
- **Conda Environment Support**: Automatically activates conda environments on the HPC system
- **Flexible Environment Management**: Creates minimal conda environments with retry logic
- **Progress Tracking**: Detailed logging and progress bars for file transfers
- **Job Status Checking**: Monitors job status and provides detailed information
- **Result Retrieval**: Downloads abundance matrices and other result files
- **Raw Data Management**: Efficiently uploads raw data with duplicate detection
- **Flexible Input Support**: Automatically detects and processes single-end and paired-end files

## License

MIT License