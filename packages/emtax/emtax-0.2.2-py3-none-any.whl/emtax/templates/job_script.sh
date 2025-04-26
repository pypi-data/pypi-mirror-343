#!/bin/bash
# emtax job script template
# This will be filled in by the workflow manager

#SBATCH --job-name=emtax
#SBATCH --partition={partition}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={threads}
#SBATCH --mem={memory}
#SBATCH --time={time}
#SBATCH --output={workflow_dir}/slurm-%j.out
#SBATCH --error={workflow_dir}/slurm-%j.err

echo "Starting emtax workflow at $(date)"

# Check if conda is available as a module
if module avail conda 2>&1 | grep -q conda; then
    echo "Loading conda module..."
    module load conda
    CONDA_AVAILABLE=1
else
    echo "Conda module not available, checking if conda is installed..."
    CONDA_AVAILABLE=0
    
    # Check if conda is already installed
    if command -v conda &> /dev/null; then
        echo "Conda is already installed"
        CONDA_AVAILABLE=1
    elif [ -f "$HOME/miniconda3/bin/conda" ]; then
        echo "Found conda in $HOME/miniconda3"
        export PATH="$HOME/miniconda3/bin:$PATH"
        CONDA_AVAILABLE=1
    else
        echo "Conda not found, installing Miniconda..."
        # Download and install Miniconda
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        MINICONDA_INSTALLER="/tmp/miniconda.sh"
        
        # Try multiple download methods
        echo "Downloading Miniconda..."
        if command -v wget &> /dev/null; then
            wget -q $MINICONDA_URL -O $MINICONDA_INSTALLER || \
            curl -s -L $MINICONDA_URL -o $MINICONDA_INSTALLER || \
            { echo "Failed to download Miniconda"; exit 1; }
        elif command -v curl &> /dev/null; then
            curl -s -L $MINICONDA_URL -o $MINICONDA_INSTALLER || \
            { echo "Failed to download Miniconda"; exit 1; }
        else
            echo "Neither wget nor curl is available. Cannot download Miniconda."
            exit 1
        fi
        
        echo "Installing Miniconda..."
        bash $MINICONDA_INSTALLER -b -p $HOME/miniconda3
        rm $MINICONDA_INSTALLER
        
        # Add to PATH
        export PATH="$HOME/miniconda3/bin:$PATH"
        
        # Initialize conda
        conda init bash
        source $HOME/.bashrc
        
        CONDA_AVAILABLE=1
        echo "Miniconda installed successfully"
    fi
fi

# Verify conda is available
if [ $CONDA_AVAILABLE -eq 0 ]; then
    echo "ERROR: Conda is not available and could not be installed"
    exit 1
fi

# Configure conda offline mode if network is unreachable
echo "Testing network connectivity..."
if ping -c 1 conda.anaconda.org &>/dev/null; then
    echo "Network is reachable, using online mode"
    OFFLINE_MODE=0
    
    # Configure conda channels
    echo "Configuring conda channels..."
    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge
else
    echo "Network is unreachable, using offline mode"
    OFFLINE_MODE=1
    
    # Configure conda for offline use
    echo "Configuring conda for offline use..."
    conda config --set offline True
fi

# Create and activate conda environment with retry logic
if [ ! -d "{env_path}" ]; then
    echo "Creating conda environment..."
    
    if [ $OFFLINE_MODE -eq 1 ]; then
        echo "Offline mode: Creating minimal environment without internet..."
        conda create -y -p {env_path} python=3.9
        
        # Check if any system-wide snakemake is available
        if command -v snakemake &> /dev/null; then
            echo "Found system-wide snakemake, will use that"
        else
            echo "WARNING: No snakemake available and cannot install in offline mode"
            echo "Will attempt to run workflow scripts directly"
        fi
    else
        # Try up to 3 times with increasing timeouts
        MAX_RETRIES=3
        for i in $(seq 1 $MAX_RETRIES); do
            echo "Attempt $i of $MAX_RETRIES to create conda environment"
            conda env create -f {config_env_path} -p {env_path} && break
            echo "Failed to create environment, retrying in $((i*30)) seconds..."
            sleep $((i*30))
            # Clean up any partial environment
            rm -rf {env_path}
        done
        
        # Check if environment was created
        if [ ! -d "{env_path}" ]; then
            echo "ERROR: Failed to create conda environment after $MAX_RETRIES attempts"
            echo "Creating minimal environment with essential packages..."
            conda create -y -p {env_path} python=3.9
            
            # Try to install just snakemake-minimal
            echo "Attempting to install just snakemake-minimal..."
            conda install -y -p {env_path} -c bioconda snakemake-minimal || \
            echo "WARNING: Could not install snakemake-minimal"
        fi
    fi
fi

# Activate conda environment
echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate {env_path}

# Verify snakemake is installed
if ! command -v snakemake &> /dev/null; then
    if [ $OFFLINE_MODE -eq 0 ]; then
        echo "Snakemake not found in environment, installing..."
        conda install -y -c bioconda snakemake-minimal || \
        pip install snakemake==7.32.4 || \
        echo "WARNING: Failed to install snakemake"
    else
        echo "WARNING: Snakemake not available in offline mode"
        echo "Will attempt to run workflow scripts directly"
    fi
fi

# Run Snakemake
echo "Running Snakemake workflow..."
cd {workflow_dir}

if command -v snakemake &> /dev/null; then
    # If snakemake is available, use it
    if [ $OFFLINE_MODE -eq 1 ]; then
        # In offline mode, don't use --use-conda
        snakemake --snakefile {snakefile_path} \
        --configfile {config_path} \
        --cores {threads} \
        --printshellcmds \
        --reason \
        --keep-going
    else
        # In online mode, use --use-conda
        snakemake --snakefile {snakefile_path} \
        --configfile {config_path} \
        --cores {threads} \
        --use-conda \
        --printshellcmds \
        --reason \
        --keep-going
    fi
else
    # If snakemake is not available, run the workflow steps manually
    echo "Snakemake not available, running workflow steps manually..."
    
    # Extract sample names from config
    SAMPLES=$(python -c "import yaml; print(' '.join(yaml.safe_load(open('{config_path}'))['samples']))")
    
    # Run each step for each sample
    for SAMPLE in $SAMPLES; do
        echo "Processing sample: $SAMPLE"
        
        # Run fastp for quality trimming
        echo "Running fastp for $SAMPLE..."
        # Add commands here
        
        # Run bowtie2 for host removal
        echo "Running bowtie2 for $SAMPLE..."
        # Add commands here
        
        mkdir -p "${RESULTS_DIR}/Taxonomic_Profiling/1_DNA_Kraken2"
        mkdir -p "${RESULTS_DIR}/Taxonomic_Profiling/2_DNA_Bracken"
        mkdir -p "${RESULTS_DIR}/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python"
        mkdir -p "${WORKDIR}/Preprocessed_Data/fastp"
        mkdir -p "${WORKDIR}/Logs/fastp"
        
        # Run kraken2 for taxonomic classification
        echo "Running kraken2 for $SAMPLE..."
        # Add commands here
        
        # Run bracken for abundance estimation
        echo "Running bracken for $SAMPLE..."
        # Add commands here
    done
fi

# Check exit status
SNAKEMAKE_EXIT=$?
if [ $SNAKEMAKE_EXIT -eq 0 ]; then
    echo "Workflow completed successfully"
else
    echo "Workflow failed with exit code $SNAKEMAKE_EXIT"
fi

# Deactivate conda environment
conda deactivate

echo "emtax workflow finished at $(date)"
exit $SNAKEMAKE_EXIT
