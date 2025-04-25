#!/usr/bin/env python3
"""
Workflow utility module for emtax
"""
import os
import sys
import logging
import tempfile
import yaml
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class SnakemakeWorkflow:
    """Snakemake workflow manager for emtax."""

    def __init__(self, ssh, config):
        """
        Initialize Snakemake workflow manager.

        Args:
            ssh (SSHClient): SSH client for HPC connection
            config (Config): emtax configuration
        """
        self.ssh = ssh
        self.config = config
        self.workflow_dir = os.path.join(self.config.output_dir, "workflow")
        self.snakefile_path = os.path.join(self.workflow_dir, "Snakefile")
        self.config_path = os.path.join(self.workflow_dir, "config.yaml")
        self.env_path = os.path.join(self.workflow_dir, "environment.yaml")
        self.script_path = os.path.join(
            self.workflow_dir, "scripts", "create_abundance_matrix.py"
        )

        # Create workflow directory
        self._create_workflow_dir()

    def _create_workflow_dir(self):
        """Create workflow directory on HPC or reuse existing one."""
        # Check if workflow directory already exists
        stdout, _, _ = self.ssh.execute_command(
            f"test -d {self.workflow_dir} && echo 'exists'"
        )
        if "exists" in stdout:
            logger.info(
                f"Workflow directory already exists at {self.workflow_dir}, using existing directory"
            )
        else:
            logger.info(f"Creating new workflow directory at {self.workflow_dir}")
            cmd = f"mkdir -p {self.workflow_dir}/scripts"
            self.ssh.execute_command(cmd)

        # Create Raw_Data directory
        raw_data_dir = os.path.join(self.config.output_dir, "Raw_Data")
        self.ssh.execute_command(f"mkdir -p {raw_data_dir}")

        # Create Results directory
        results_dir = os.path.join(self.config.output_dir, "Results")
        self.ssh.execute_command(f"mkdir -p {results_dir}")

        # Only create these 3 specific subdirectories under Results/Taxonomic_Profiling
        # DO NOT create 3_DNA_Bracken_To_Krona_Python or 4_DNA_Alpha_Beta_Diversity_Python
        profiling_dir = os.path.join(
            self.config.output_dir, "Results", "Taxonomic_Profiling"
        )
        kraken2_dir = os.path.join(profiling_dir, "1_DNA_Kraken2")
        bracken_dir = os.path.join(profiling_dir, "2_DNA_Bracken")
        abundance_dir = os.path.join(
            profiling_dir, "5_DNA_Relative_Abundance_Matrix_Python"
        )
        create_dirs_cmd = f"mkdir -p {kraken2_dir} {bracken_dir} {abundance_dir}"
        self.ssh.execute_command(create_dirs_cmd)

    def _generate_snakefile(self):
        """Generate Snakefile and upload to HPC."""
        # Get Snakefile template
        snakefile_template = self._get_snakefile_template()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(snakefile_template)
            temp_path = temp_file.name

        # Upload to HPC
        self.ssh.upload_file(temp_path, self.snakefile_path)

        # Remove temporary file
        os.unlink(temp_path)

    def _generate_config(self):
        """Generate config.yaml and upload to HPC."""
        # Get config from configuration
        config_dict = self.config.get_snakemake_config()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            yaml.dump(config_dict, temp_file, default_flow_style=False)
            temp_path = temp_file.name

        # Upload to HPC
        self.ssh.upload_file(temp_path, self.config_path)

        # Remove temporary file
        os.unlink(temp_path)

    def _generate_environment(self):
        """Generate environment.yaml and upload to HPC."""
        # Get environment template
        env_template = self._get_environment_template()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(env_template)
            temp_path = temp_file.name

        # Upload to HPC
        self.ssh.upload_file(temp_path, self.env_path)

        # Remove temporary file
        os.unlink(temp_path)

    def _generate_scripts(self):
        """Generate scripts and upload to HPC."""
        # Get script template
        script_template = self._get_script_template()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(script_template)
            temp_path = temp_file.name

        # Upload to HPC
        self.ssh.upload_file(temp_path, self.script_path)

        # Remove temporary file
        os.unlink(temp_path)

        # Create scripts directory on HPC if it doesn't exist
        scripts_dir = os.path.join(self.workflow_dir, "scripts")
        self.ssh.execute_command(f"mkdir -p {scripts_dir}")

        # Make script executable
        self.ssh.execute_command(f"chmod +x {self.script_path}")

    def _get_snakefile_template(self):
        """
        Get Snakefile template.

        Returns:
            str: Snakefile template
        """
        return '''# Snakemake workflow for emtax
# Generated by emtax

# Configuration
configfile: "config.yaml"

# Define samples from config
SAMPLES = config["SAMPLES"]
LANES = config["LANES"]

# Define rules
rule all:
    input:
        "Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/abundance_matrix.csv",
        expand("Taxonomic_Profiling/1_DNA_Kraken2/{sample}.kraken", sample=SAMPLES),
        expand("Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report", sample=SAMPLES),
        expand("Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}_R1.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}_R2.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}.json", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}.html", sample=SAMPLES),
        expand("Preprocessed_Data/{sample}_dehost_R1.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/{sample}_dehost_R2.fastq.gz", sample=SAMPLES)


# Combine lanes first

rule combine_lanes:
    output:
        r1 = "Preprocessed_Data/combined/{sample}_R1.fastq.gz",
        r2 = "Preprocessed_Data/combined/{sample}_R2.fastq.gz"
    threads: config["threads"]
    run:
        import os
        import glob
        shell("mkdir -p Preprocessed_Data/combined")
        r1_files = []
        r2_files = []
        for lane in LANES:
            r1_pattern = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_{lane}_R1.fastq.gz")
            r2_pattern = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_{lane}_R2.fastq.gz")
            r1_files.extend(glob.glob(r1_pattern))
            r2_files.extend(glob.glob(r2_pattern))
        shell("cat {r1s} > {out_r1}".format(r1s=" ".join(r1_files), out_r1=output.r1))
        shell("cat {r2s} > {out_r2}".format(r2s=" ".join(r2_files), out_r2=output.r2))

# Copy files to fastp directory first to ensure they exist
rule copy_to_fastp:
    input:
        r1 = "Preprocessed_Data/combined/{sample}_R1.fastq.gz",
        r2 = "Preprocessed_Data/combined/{sample}_R2.fastq.gz"
    output:
        r1_copy = temp("Preprocessed_Data/fastp/{sample}_R1.raw.fastq.gz"),
        r2_copy = temp("Preprocessed_Data/fastp/{sample}_R2.raw.fastq.gz")
    shell:
        """
        # Ensure directory exists
        mkdir -p Preprocessed_Data/fastp
        
        # Copy files to fastp directory
        cp {input.r1} {output.r1_copy}
        cp {input.r2} {output.r2_copy}
        """

rule fastp:
    input:
        r1 = "Preprocessed_Data/fastp/{sample}_R1.raw.fastq.gz",
        r2 = "Preprocessed_Data/fastp/{sample}_R2.raw.fastq.gz"
    output:
        r1_trim = "Preprocessed_Data/fastp/{sample}_R1.fastq.gz",
        r2_trim = "Preprocessed_Data/fastp/{sample}_R2.fastq.gz",
        html = "Preprocessed_Data/fastp/{sample}.html",
        json = "Preprocessed_Data/fastp/{sample}.json"
    threads: config["threads"]
    log:
        "Logs/fastp/{sample}.log"
    shell:
        """
        # Ensure directory exists
        mkdir -p Preprocessed_Data/fastp
        mkdir -p Logs/fastp
        
        # Verify input files exist and have content
        echo "Checking input files:" > {log}
        ls -la {input.r1} {input.r2} >> {log} 2>&1
        
        # Check if R2 is valid or corrupt
        echo "Validating R2 file..." >> {log}
        gzip -t {input.r2} >> {log} 2>&1
        R2_VALID=$?
        
        if [ $R2_VALID -eq 0 ] && [ -s {input.r2} ]; then
            echo "R2 file is valid, running fastp in paired-end mode" >> {log}
            # Run fastp with explicit paths for reports
            set +e
            fastp -i {input.r1} -I {input.r2} \
                  -o {output.r1_trim} -O {output.r2_trim} \
                  --json {output.json} --html {output.html} \
                  --thread {threads} \
                  --report_title "{wildcards.sample} Quality Report" \
                  >> {log} 2>&1
            FASTP_EXIT=$?
            set -e
        else
            echo "R2 file is invalid or corrupt, running fastp in single-end mode" >> {log}
            # Run fastp in single-end mode
            set +e
            fastp -i {input.r1} \
                  -o {output.r1_trim} \
                  --json {output.json} --html {output.html} \
                  --thread {threads} \
                  --report_title "{wildcards.sample} Quality Report" \
                  >> {log} 2>&1
            FASTP_EXIT=$?
            set -e
            
            # Create an empty R2 file
            touch {output.r2_trim}
        fi
        
        # Check if fastp succeeded
        if [ $FASTP_EXIT -ne 0 ] || [ ! -f {output.json} ] || [ ! -f {output.html} ]; then
            echo "WARNING: fastp failed for {wildcards.sample}" >> {log}
            
            # Create minimal output files to allow workflow to continue
            if [ ! -f {output.r1_trim} ]; then
                echo "Creating R1 output file from input" >> {log}
                # Ensure the output directory exists again just to be safe
                mkdir -p "$(dirname {output.r1_trim})"
                cp {input.r1} {output.r1_trim}
            fi
            
            if [ ! -f {output.r2_trim} ]; then
                echo "Creating empty R2 output file" >> {log}
                touch {output.r2_trim}
            fi
            
            # Create minimal JSON and HTML files
            echo "{{}}" > {output.json}
            echo "<html><body><h1>Fastp failed for {wildcards.sample}</h1></body></html>" > {output.html}
        fi
        
        # Verify reports were created
        echo "Fastp reports generated for {wildcards.sample}:" >> {log}
        ls -la {output.json} {output.html} >> {log} 2>&1
        """

# Remove host DNA
rule dehost:
    input:
        r1 = "Preprocessed_Data/fastp/{sample}_R1.fastq.gz",
        r2 = "Preprocessed_Data/fastp/{sample}_R2.fastq.gz"
    output:
        unmapped_r1 = "Preprocessed_Data/{sample}_dehost_R1.fastq.gz",
        unmapped_r2 = "Preprocessed_Data/{sample}_dehost_R2.fastq.gz"
    params:
        index_prefix = config["CORN_DB"],
        dehost_dir = "Preprocessed_Data"
    threads: config["threads"]
    log:
        "Logs/dehost/{sample}.log"
    shell:
        """
        set -euo pipefail
        # Ensure output and log dirs
        mkdir -p {params.dehost_dir} Logs/dehost
        echo "Dehosting {wildcards.sample}" > {log}

        # Run Bowtie2, writing unaligned pairs to dehost_R1/R2 directly
        bowtie2 -p {threads} -x "{params.index_prefix}" \
            -1 "{input.r1}" \
            -2 "{input.r2}" \
            --un-conc-gz "{params.dehost_dir}/{wildcards.sample}_dehost_R%.fastq.gz" \
            -S /dev/null >> {log} 2>&1

        # Fallback if needed
        if [ ! -f "{params.dehost_dir}/{wildcards.sample}_dehost_R1.fastq.gz" ]; then
            echo "WARNING: R1 dehost missing, copying input" >> {log}
            cp "{input.r1}" "{output.unmapped_r1}"
        fi
        if [ ! -f "{params.dehost_dir}/{wildcards.sample}_dehost_R2.fastq.gz" ]; then
            echo "WARNING: R2 dehost missing, copying input" >> {log}
            cp "{input.r2}" "{output.unmapped_r2}"
        fi
        """

# Run Kraken2 on dehosted files
rule kraken2:
    input:
        r1 = "Preprocessed_Data/{sample}_dehost_R1.fastq.gz",
        r2 = "Preprocessed_Data/{sample}_dehost_R2.fastq.gz"
    output:
        kraken = "Taxonomic_Profiling/1_DNA_Kraken2/{sample}.kraken",
        report = "Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report"
    threads: config["threads"]
    log:
        "Logs/kraken2/{sample}.log"
    shell:
        """
        mkdir -p Taxonomic_Profiling/1_DNA_Kraken2
        mkdir -p Logs/kraken2
        
        # Verify input files exist and have content
        echo "Checking input files for kraken2:" > {log}
        ls -la {input.r1} {input.r2} >> {log} 2>&1
        
        # Check if R2 is empty (could be a single-end sample)
        if [ -s {input.r2} ]; then
            echo "Running kraken2 in paired-end mode" >> {log}
            kraken2 --db {config[KRAKEN2_DB_DIR]} \
                    --threads {threads} \
                    --paired \
                    --output {output.kraken} \
                    --report {output.report} \
                    {input.r1} {input.r2} >> {log} 2>&1
        else
            echo "R2 file is empty, running kraken2 in single-end mode" >> {log}
            kraken2 --db {config[KRAKEN2_DB_DIR]} \
                    --threads {threads} \
                    --output {output.kraken} \
                    --report {output.report} \
                    {input.r1} >> {log} 2>&1
        fi
        
        # Verify output files were created
        echo "Kraken2 output files for {wildcards.sample}:" >> {log}
        ls -la {output.kraken} {output.report} >> {log} 2>&1
        """

rule bracken:
    input:
        report = "Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report"
    output:
        bracken = "Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken"
    log:
        "Logs/bracken/{sample}.log"
    shell:
        """
        mkdir -p Taxonomic_Profiling/2_DNA_Bracken
        mkdir -p Logs/bracken
        
        # Verify input file exists and has content
        echo "Checking input file for bracken:" > {log}
        ls -la {input.report} >> {log} 2>&1
        
        # Run bracken with proper error handling
        echo "Running bracken for {wildcards.sample}" >> {log}
        bracken -d {config[KRAKEN2_DB_DIR]} \
                -i {input.report} \
                -o {output.bracken} \
                -r 150 -l S -t 10 >> {log} 2>&1
        
        # Verify output file was created
        echo "Bracken output file for {wildcards.sample}:" >> {log}
        ls -la {output.bracken} >> {log} 2>&1
        """

rule abundance_matrix:
    input:
        brackens=expand("Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken", sample=SAMPLES)
    output:
        matrix = "Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/abundance_matrix.csv"
    shell:
        """
        mkdir -p Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python
        python scripts/create_abundance_matrix.py \\
            Taxonomic_Profiling/2_DNA_Bracken \\
            {output.matrix}
        """
'''

    def _get_environment_template(self):
        """
        Get environment.yaml template.

        Returns:
            str: environment.yaml template
        """
        return """name: emtax_env
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
  - scikit-bio==0.5.8
  - pip=23.3.1
  - pip:
"""

    def _get_script_template(self):
        """
        Get script template.

        Returns:
            str: script template
        """
        return """#!/usr/bin/env python3
# Script to create abundance matrix from Bracken files
# Generated by emtax

import os
import sys
import glob
import argparse
import logging
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def check_dependencies():
    \"\"\"Check if required dependencies are installed.\"\"\"
    try:
        import pandas as pd
        logging.info("pandas is installed")
        return True
    except ImportError:
        logging.error("pandas is not installed")
        return False

def create_abundance_matrix(input_files, output_file):
    \"\"\"
    Create abundance matrix from Bracken files.
    
    Args:
        input_files (list): List of Bracken output files
        output_file (str): Output CSV file
    
    Returns:
        str: Path to output file
    \"\"\"
    logging.info(f"Creating abundance matrix from {len(input_files)} Bracken files")
    
    # Process each Bracken file
    all_data = []
    for file_path in input_files:
        logging.info(f"Processing {file_path}")
        
        # Extract sample name from file path
        sample_name = os.path.basename(file_path).split('.')[0]
        
        # Read Bracken file
        df = pd.read_csv(file_path, sep='\\t')
        
        # Check for required columns and handle variations
        if 'fraction_total_reads' in df.columns:
            df_rel = df[['name', 'fraction_total_reads']].copy()
        elif 'new_est_frac_reads' in df.columns:
            df_rel = df[['name', 'new_est_frac_reads']].copy()
            df_rel.rename(columns={'new_est_frac_reads': 'fraction_total_reads'}, inplace=True)
        else:
            raise ValueError(f"Required columns not found in {file_path}")
        
        df_rel.rename(columns={'fraction_total_reads': sample_name}, inplace=True)
        all_data.append(df_rel)
    
    # Merge dataframes
    merged_df = all_data[0]
    for df in all_data[1:]:
        merged_df = pd.merge(merged_df, df, on='name', how='outer')  # outer join
    
    merged_df.fillna(0, inplace=True)  # Replace NaN with 0
    merged_df.set_index('name', inplace=True)  # Set 'name' as index
    merged_df.to_csv(output_file)  # Save as CSV
    
    return output_file


def main():
    parser = argparse.ArgumentParser(description='Create abundance matrix from Bracken files')
    parser.add_argument('--input_files', nargs='+', required=True, help='Bracken output files')
    parser.add_argument('--output', required=True, help='Output CSV file')
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Create abundance matrix
    create_abundance_matrix(args.input_files, args.output)
    
    logging.info(f"Abundance matrix saved to: {args.output}")


if __name__ == "__main__":
    main()
"""

    def _generate_job_script(self):
        """
        Generate job script for HPC submission.

        Returns:
            str: Path to job script on HPC
        """
        # Create job script path
        job_script_path = os.path.join(self.workflow_dir, "submit_job.sh")

        # Get sample names from config
        samples = self.config.samples
        samples_str = " ".join(samples)

        # Use the template file instead of creating the script directly
        template_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates"
        )
        template_path = os.path.join(template_dir, "simple_job_script.sh")

        # Read the template file
        with open(template_path, "r") as f:
            job_script = f.read()

        # Replace placeholders with actual values
        job_script = job_script.replace("PARTITION", self.config.partition)
        job_script = job_script.replace("THREADS_VALUE", str(self.config.threads))
        job_script = job_script.replace("MEMORY", self.config.memory)
        job_script = job_script.replace("TIME", self.config.time)
        job_script = job_script.replace("WORKDIR_PATH", self.workflow_dir)
        job_script = job_script.replace("RAWDATA_DIR_PATH", self.config.raw_data_dir)
        job_script = job_script.replace("RESULTS_DIR_PATH", self.config.results_dir)
        job_script = job_script.replace("KRAKEN_DB_PATH", self.config.kraken_db)
        job_script = job_script.replace("CORN_DB_PATH", self.config.corn_db)
        job_script = job_script.replace("SAMPLES", samples_str)

        # Get the conda environment name from the environment template
        env_yaml = yaml.safe_load(self._get_environment_template())
        conda_env_name = env_yaml.get(
            "name", "emtax_env"
        )  # Default to emtax_env if not specified

        # Handle conda environment - always use emtax_env
        job_script = job_script.replace("emtax_env", conda_env_name)

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(job_script)
            temp_path = temp_file.name

        # Upload to HPC
        self.ssh.upload_file(temp_path, job_script_path)

        # Remove temporary file
        os.unlink(temp_path)

        # Make job script executable
        self.ssh.execute_command(f"chmod +x {job_script_path}")

        logger.info(f"Job script generated at {job_script_path}")
        return job_script_path

    def configure(self):
        """Configure workflow on HPC."""
        # Generate Snakefile
        logger.info("Generating Snakefile")
        self._generate_snakefile()

        # Generate config.yaml
        logger.info("Generating config.yaml")
        self._generate_config()

        # Generate environment.yaml
        logger.info("Generating environment.yaml")
        self._generate_environment()

        # Generate scripts
        logger.info("Generating scripts")
        self._generate_scripts()

    def _upload_raw_data(self):
        """
        Upload raw data files to the HPC system.

        Returns:
            bool: True if successful, False otherwise
        """
        # Create raw data directory on HPC
        logger.info(f"Creating raw data directory: {self.config.raw_data_dir}")
        self.ssh.execute_command(f"mkdir -p {self.config.raw_data_dir}")

        # Check which files already exist on HPC to avoid re-uploading
        logger.info("Checking for existing files on HPC...")

        # First check if the directory exists
        stdout, _, exit_code = self.ssh.execute_command(
            f"test -d {self.config.raw_data_dir} && echo 'exists'"
        )
        if "exists" not in stdout:
            logger.info(f"Raw data directory does not exist yet, will upload all files")
            existing_files = set()
        else:
            # Check for each file individually instead of using find
            existing_files = set()
            for raw_file in self.config.raw_files:
                filename = os.path.basename(raw_file)
                remote_path = os.path.join(self.config.raw_data_dir, filename)
                stdout, _, _ = self.ssh.execute_command(
                    f"test -f {remote_path} && echo 'exists'"
                )
                if "exists" in stdout:
                    logger.info(f"Found existing file: {filename}")
                    existing_files.add(filename)

        # Upload each raw file if it doesn't already exist
        upload_count = 0
        skip_count = 0
        for raw_file in self.config.raw_files:
            local_path = raw_file
            filename = os.path.basename(local_path)
            remote_path = os.path.join(self.config.raw_data_dir, filename)

            if filename in existing_files:
                logger.info(f"Skipping upload of {filename} (already exists on HPC)")
                skip_count += 1
                continue

            # Double check if file exists on HPC (in case it was uploaded in a previous run)
            remote_path = os.path.join(self.config.raw_data_dir, filename)
            stdout, _, _ = self.ssh.execute_command(
                f"test -f {remote_path} && echo 'exists'"
            )
            if "exists" in stdout:
                logger.info(f"Skipping upload of {filename} (already exists on HPC)")
                skip_count += 1
                continue

            logger.info(f"Uploading {filename} to HPC...")
            success = self.ssh.upload_file(local_path, remote_path, progress=True)

            if success:
                upload_count += 1
                logger.info(f"Successfully uploaded {filename}")
            else:
                logger.error(f"Failed to upload {filename}")
                return False

        logger.info(
            f"Raw data upload complete: {upload_count} files uploaded, {skip_count} files skipped (already existed)"
        )
        return True

    def submit(self):
        """
        Submit workflow to HPC.

        Returns:
            str: Job ID
        """
        # Configure workflow
        self.configure()

        # Upload raw data files if not skipped
        if not self.config.no_upload_data:
            logger.info("Uploading raw data files")
            if not self._upload_raw_data():
                raise RuntimeError("Failed to upload raw data files")
        else:
            logger.info("Skipping raw data upload (no_upload_data is set)")

        # Generate job script
        logger.info("Generating job script")
        job_script_path = self._generate_job_script()

        # Submit job
        logger.info("Submitting job")
        stdout, stderr, exit_code = self.ssh.execute_command(
            f"sbatch {job_script_path}"
        )

        if exit_code != 0:
            raise RuntimeError(f"Failed to submit job: {stderr}")

        # Extract job ID
        job_id = stdout.strip().split()[-1]

        return job_id
