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
        
        # Define paths for workflow subdirectories
        self.preprocessed_dir = os.path.join(self.workflow_dir, "Preprocessed_Data")
        self.logs_dir = os.path.join(self.workflow_dir, "Logs")

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
            
            # Create Logs and Preprocessed_Data directories INSIDE the workflow directory
            preproc_dir = os.path.join(self.workflow_dir, "Preprocessed_Data")
            logs_dir = os.path.join(self.workflow_dir, "Logs")
            self.ssh.execute_command(f"mkdir -p {preproc_dir} {logs_dir}")

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

# Check for single-end samples
SINGLE_END_SAMPLES = config.get("SINGLE_END_SAMPLES", [])

# Define rules
rule all:
    input:
        "../Results/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/abundance_matrix.csv",
        expand("../Results/Taxonomic_Profiling/1_DNA_Kraken2/{sample}.kraken", sample=SAMPLES),
        expand("../Results/Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report", sample=SAMPLES),
        expand("../Results/Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken", sample=SAMPLES),
        # Paired-end files
        expand("Preprocessed_Data/fastp/{sample}_R1.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}_R2.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/{sample}_dehost_R1.fastq.gz", sample=SAMPLES),
        expand("Preprocessed_Data/{sample}_dehost_R2.fastq.gz", sample=SAMPLES),
        # Single-end files
        expand("Preprocessed_Data/fastp/{sample}.fastq.gz", sample=SINGLE_END_SAMPLES),
        expand("Preprocessed_Data/{sample}_dehost.fastq.gz", sample=SINGLE_END_SAMPLES),
        # Common files
        expand("Preprocessed_Data/fastp/{sample}.json", sample=SAMPLES),
        expand("Preprocessed_Data/fastp/{sample}.html", sample=SAMPLES)


# Combine lanes if needed

rule combine_lanes:
    output:
        r1 = "Preprocessed_Data/combined/{sample}_R1.fastq.gz",
        r2 = "Preprocessed_Data/combined/{sample}_R2.fastq.gz",
        single_end = "Preprocessed_Data/combined/{sample}.fastq.gz"
    threads: config["threads"]
    run:
        import os
        import glob
        shell("mkdir -p Preprocessed_Data/combined")
        
        # Check if this is a single-end sample
        is_single_end = wildcards.sample in SINGLE_END_SAMPLES
        
        # Check for different file patterns
        no_lane_r1 = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_R1.fastq.gz")
        no_lane_r2 = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_R2.fastq.gz")
        # Check for single-end files (no R1/R2, no lane info)
        single_end_file = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}.fastq.gz")
        
        if is_single_end and os.path.exists(single_end_file):
            # This is a single-end file, copy it with its original name
            shell(f"cp {single_end_file} {output.single_end}")
            # Create empty R1/R2 files for compatibility with existing rules
            shell(f"touch {output.r1}")
            shell(f"touch {output.r2}")
            shell(f"echo 'Preserved original filename for single-end sample {wildcards.sample}'")
        elif os.path.exists(no_lane_r1) or os.path.exists(no_lane_r2):
            # Files are already lane-combined, just copy them
            if os.path.exists(no_lane_r1):
                shell(f"cp {no_lane_r1} {output.r1}")
            else:
                shell(f"touch {output.r1}")
            if os.path.exists(no_lane_r2):
                shell(f"cp {no_lane_r2} {output.r2}")
            else:
                shell(f"touch {output.r2}")
        else:
            # Need to combine lanes
            r1_files = []
            r2_files = []
            for lane in LANES:
                r1_pattern = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_{lane}_R1.fastq.gz")
                r2_pattern = os.path.join(config["RAW_DATA_DIR"], f"{wildcards.sample}_{lane}_R2.fastq.gz")
                r1_files.extend(glob.glob(r1_pattern))
                r2_files.extend(glob.glob(r2_pattern))
        
            if r1_files:
                shell("cat {r1s} > {out_r1}".format(r1s=" ".join(r1_files), out_r1=output.r1))
            else:
                shell(f"touch {output.r1}")
            
            if r2_files:
                shell("cat {r2s} > {out_r2}".format(r2s=" ".join(r2_files), out_r2=output.r2))
            else:
                # For single-end samples, create a marker file
                if is_single_end:
                    shell(f"echo 'SINGLE_END_MARKER' > {output.r2}")
                else:
                    shell(f"touch {output.r2}")

# Copy files to fastp directory first to ensure they exist
rule copy_to_fastp:
    input:
        r1 = "Preprocessed_Data/combined/{sample}_R1.fastq.gz",
        r2 = "Preprocessed_Data/combined/{sample}_R2.fastq.gz",
        single_end = "Preprocessed_Data/combined/{sample}.fastq.gz"
    output:
        r1_copy = temp("Preprocessed_Data/fastp/{sample}_R1.raw.fastq.gz"),
        r2_copy = temp("Preprocessed_Data/fastp/{sample}_R2.raw.fastq.gz"),
        single_end_copy = temp("Preprocessed_Data/fastp/{sample}.raw.fastq.gz")
    shell:
        """
        # Ensure directory exists
        mkdir -p Preprocessed_Data/fastp
        
        # Check if this is a single-end sample
        IS_SINGLE_END=0
        if [ "{wildcards.sample}" = "$(echo '{SINGLE_END_SAMPLES}' | grep -o '{wildcards.sample}')" ]; then
            IS_SINGLE_END=1
        fi
        
        if [ $IS_SINGLE_END -eq 1 ] && [ -s {input.single_end} ]; then
            # Copy single-end file with original name
            cp {input.single_end} {output.single_end_copy}
            # Create empty files for R1/R2 for compatibility
            touch {output.r1_copy}
            touch {output.r2_copy}
        else
            # Copy paired-end files
            cp {input.r1} {output.r1_copy}
            cp {input.r2} {output.r2_copy}
            # Create empty single-end file for compatibility
            touch {output.single_end_copy}
        fi
        """

rule fastp:
    input:
        r1 = "Preprocessed_Data/fastp/{sample}_R1.raw.fastq.gz",
        r2 = "Preprocessed_Data/fastp/{sample}_R2.raw.fastq.gz",
        single_end = "Preprocessed_Data/fastp/{sample}.raw.fastq.gz"
    output:
        r1_trim = "Preprocessed_Data/fastp/{sample}_R1.fastq.gz",
        r2_trim = "Preprocessed_Data/fastp/{sample}_R2.fastq.gz",
        single_end_trim = "Preprocessed_Data/fastp/{sample}.fastq.gz",
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
        
        # Check if this is a single-end sample
        IS_SINGLE_END=0
        if [ "{wildcards.sample}" = "$(echo '{SINGLE_END_SAMPLES}' | grep -o '{wildcards.sample}')" ]; then
            IS_SINGLE_END=1
            echo "Detected single-end sample: {wildcards.sample}" > {log}
        fi
        
        # Check if single-end file exists and has content
        if [ $IS_SINGLE_END -eq 1 ] && [ -s {input.single_end} ]; then
            echo "Running fastp in single-end mode with original filename for {wildcards.sample}" >> {log}
            # Run fastp in single-end mode with original filename
            set +e
            fastp -i {input.single_end} \
                  -o {output.single_end_trim} \
                  --json {output.json} --html {output.html} \
                  --thread {threads} \
                  --report_title "{wildcards.sample} Quality Report" \
                  >> {log} 2>&1
            FASTP_EXIT=$?
            set -e
            
            # Touch the R1/R2 files for compatibility
            touch {output.r1_trim}
            touch {output.r2_trim}
            echo "Preserved original filename for single-end sample" >> {log}
        else
            # Verify input files exist and have content
            echo "Checking input files for paired-end mode:" >> {log}
            ls -la {input.r1} {input.r2} >> {log} 2>&1
            
            # Check if R2 is valid
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
                echo "R2 file is invalid or corrupt, falling back to single-end mode" >> {log}
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
        r2 = "Preprocessed_Data/fastp/{sample}_R2.fastq.gz",
        single_end = "Preprocessed_Data/fastp/{sample}.fastq.gz"
    output:
        r1_dehost = "Preprocessed_Data/{sample}_dehost_R1.fastq.gz",
        r2_dehost = "Preprocessed_Data/{sample}_dehost_R2.fastq.gz",
        single_end_dehost = "Preprocessed_Data/{sample}_dehost.fastq.gz"
    threads: config["threads"]
    log:
        "Logs/dehost/{sample}.log"
    shell:
        """
        mkdir -p Logs/dehost
        
        # Check if this is a single-end sample
        IS_SINGLE_END=0
        if [ "{wildcards.sample}" = "$(echo '{SINGLE_END_SAMPLES}' | grep -o '{wildcards.sample}')" ]; then
            IS_SINGLE_END=1
            echo "Detected single-end sample: {wildcards.sample}" > {log}
        fi
        
        # Determine the correct index path
        INDEX_PATH="{config[CORN_DB]}"
        if [ -e "{config[CORN_DB]}.1.bt2" ] || [ -e "{config[CORN_DB]}.1.bt2l" ]; then
            INDEX_PATH="{config[CORN_DB]}"
        elif [ -e "{config[CORN_DB]}/corn_db.1.bt2" ] || [ -e "{config[CORN_DB]}/corn_db.1.bt2l" ]; then
            INDEX_PATH="{config[CORN_DB]}/corn_db"
        elif [ -e "{config[CORN_DB]}/Zm-B73-REFERENCE-NAM-5.0.1.bt2" ] || [ -e "{config[CORN_DB]}/Zm-B73-REFERENCE-NAM-5.0.1.bt2l" ]; then
            INDEX_PATH="{config[CORN_DB]}/Zm-B73-REFERENCE-NAM-5.0"
        fi
        echo "Using Bowtie2 index at: $INDEX_PATH" >> {log}
        
        # Check if single-end file exists and has content
        if [ $IS_SINGLE_END -eq 1 ] && [ -s {input.single_end} ]; then
            echo "Running bowtie2 in single-end mode with original filename for {wildcards.sample}" >> {log}
            # Run bowtie2 with single-end mode using original filename
            bowtie2 -p {threads} -x "$INDEX_PATH" \
                    -U {input.single_end} \
                    -S /dev/null \
                    --un-gz {output.single_end_dehost} || true
            
            # Touch the R1/R2 files for compatibility
            touch {output.r1_dehost}
            touch {output.r2_dehost}
            echo "Preserved original filename for single-end sample" >> {log}
            
            # Check if dehosting was successful
            if [ ! -f {output.single_end_dehost} ]; then
                echo "WARNING: Dehost failed, copying input file" >> {log}
                cp {input.single_end} {output.single_end_dehost}
            fi
        else
            echo "Running bowtie2 in paired-end mode for {wildcards.sample}" >> {log}
            # Run Bowtie2 in paired-end mode
            bowtie2 -p {threads} -x "$INDEX_PATH" \
                -1 {input.r1} \
                -2 {input.r2} \
                --un-conc-gz {output.r1_dehost%_R1.fastq.gz}_R%.fastq.gz \
                -S /dev/null >> {log} 2>&1 || true

            # Create empty single-end file for compatibility
            touch {output.single_end_dehost}
            
            # Fallback if needed
            if [ ! -f {output.r1_dehost} ]; then
                echo "WARNING: R1 dehost missing, copying input" >> {log}
                cp {input.r1} {output.r1_dehost}
            fi
            if [ ! -f {output.r2_dehost} ]; then
                echo "WARNING: R2 dehost missing, copying input" >> {log}
                cp {input.r2} {output.r2_dehost}
            fi
        fi
        """

# Run Kraken2 on dehosted files
rule kraken2:
    input:
        r1 = "Preprocessed_Data/{sample}_dehost_R1.fastq.gz",
        r2 = "Preprocessed_Data/{sample}_dehost_R2.fastq.gz",
        single_end = "Preprocessed_Data/{sample}_dehost.fastq.gz"
    output:
        kraken = "../Results/Taxonomic_Profiling/1_DNA_Kraken2/{sample}.kraken",
        report = "../Results/Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report"
    threads: config["threads"]
    log:
        "Logs/kraken2/{sample}.log"
    shell:
        """
        mkdir -p ../Results/Taxonomic_Profiling/1_DNA_Kraken2
        mkdir -p Logs/kraken2
        
        # Check if this is a single-end sample
        IS_SINGLE_END=0
        if [ "{wildcards.sample}" = "$(echo '{SINGLE_END_SAMPLES}' | grep -o '{wildcards.sample}')" ]; then
            IS_SINGLE_END=1
            echo "Detected single-end sample: {wildcards.sample}" > {log}
        fi
        
        # Check if single-end file exists and has content
        if [ $IS_SINGLE_END -eq 1 ] && [ -s {input.single_end} ]; then
            echo "Running kraken2 in single-end mode with original filename for {wildcards.sample}" >> {log}
            kraken2 --db {config[KRAKEN2_DB_DIR]} \
                    --threads {threads} \
                    --output {output.kraken} \
                    --report {output.report} \
                    {input.single_end} >> {log} 2>&1 || true
        else
            echo "Running kraken2 in paired-end mode for {wildcards.sample}" >> {log}
            kraken2 --db {config[KRAKEN2_DB_DIR]} \
                    --threads {threads} \
                    --paired \
                    --output {output.kraken} \
                    --report {output.report} \
                    {input.r1} {input.r2} >> {log} 2>&1 || true
        fi
        
        # Verify output files were created
        echo "Kraken2 output files for {wildcards.sample}:" >> {log}
        ls -la {output.kraken} {output.report} >> {log} 2>&1 || true
        
        # Create empty output files if they don't exist (to prevent workflow failures)
        if [ ! -f {output.kraken} ]; then
            echo "WARNING: Creating empty kraken output file" >> {log}
            touch {output.kraken}
        fi
        
        if [ ! -f {output.report} ]; then
            echo "WARNING: Creating empty kraken report file" >> {log}
            touch {output.report}
        fi
        """

rule bracken:
    input:
        kraken_report = "../Results/Taxonomic_Profiling/1_DNA_Kraken2/{sample}.report"
    output:
        bracken = "../Results/Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken"
    params:
        threshold = 10,
        read_len = 150,
        level = "S"  # Species level
    log:
        "Logs/bracken/{sample}.log"
    shell:
        """
        mkdir -p ../Results/Taxonomic_Profiling/2_DNA_Bracken
        mkdir -p Logs/bracken
        
        # Check if this is a single-end sample
        IS_SINGLE_END=0
        if [ "{wildcards.sample}" = "$(echo '{SINGLE_END_SAMPLES}' | grep -o '{wildcards.sample}')" ]; then
            IS_SINGLE_END=1
            echo "Processing bracken for single-end sample: {wildcards.sample}" > {log}
        else
            echo "Processing bracken for paired-end sample: {wildcards.sample}" > {log}
        fi
        
        # Run bracken (same command for both single and paired-end)
        bracken -d {config[KRAKEN2_DB_DIR]} \
                -i {input.kraken_report} \
                -o {output.bracken} \
                -t {params.threshold} \
                -r {params.read_len} \
                -l {params.level} >> {log} 2>&1 || true
        
        # Check if bracken succeeded
        if [ ! -f {output.bracken} ]; then
            echo "WARNING: Bracken failed, creating empty output file" >> {log}
            touch {output.bracken}
        fi
        echo "Bracken output file for {wildcards.sample}:" >> {log}
        ls -la {output.bracken} >> {log} 2>&1
        """

rule abundance_matrix:
    input:
        brackens=expand("../Results/Taxonomic_Profiling/2_DNA_Bracken/{sample}.bracken", sample=SAMPLES)
    output:
        matrix = "../Results/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/abundance_matrix.csv"
    shell:
        """
        mkdir -p ../Results/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python
        python scripts/create_abundance_matrix.py \\
            ../Results/Taxonomic_Profiling/2_DNA_Bracken \\
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
        
        try:
            # Read Bracken file - use low_memory=False to avoid dtype warnings
            df = pd.read_csv(file_path, sep='\t', low_memory=False)
            
            # Check for required columns and handle variations
            if 'fraction_total_reads' in df.columns:
                df_rel = df[['name', 'fraction_total_reads']].copy()
            elif 'new_est_frac_reads' in df.columns:
                df_rel = df[['name', 'new_est_frac_reads']].copy()
                df_rel.rename(columns={'new_est_frac_reads': 'fraction_total_reads'}, inplace=True)
            else:
                # Try to use all columns if standard ones aren't found
                logging.warning(f"Standard columns not found in {file_path}, using all available columns")
                if 'name' in df.columns:
                    # If at least 'name' is present, use whatever abundance column is available
                    abundance_cols = [col for col in df.columns if col != 'name' and df[col].dtype.kind in 'fc']
                    if abundance_cols:
                        df_rel = df[['name', abundance_cols[0]]].copy()
                        df_rel.rename(columns={abundance_cols[0]: 'fraction_total_reads'}, inplace=True)
                    else:
                        raise ValueError(f"No numeric abundance columns found in {file_path}")
                else:
                    raise ValueError(f"'name' column not found in {file_path}")
            
            df_rel.rename(columns={'fraction_total_reads': sample_name}, inplace=True)
            all_data.append(df_rel)
        except Exception as e:
            logging.error(f"Error processing {file_path}: {str(e)}")
            # Create an empty dataframe with the sample name to ensure the sample is included
            df_rel = pd.DataFrame(columns=['name', sample_name])
            all_data.append(df_rel)
    
    # Merge dataframes
    if all_data:
        # First, collect all unique taxa names across all files
        all_taxa = set()
        for df in all_data:
            if not df.empty and 'name' in df.columns:
                all_taxa.update(df['name'].tolist())
        
        # Create a comprehensive dataframe with all taxa
        if all_taxa:
            # Sort taxa alphabetically
            all_taxa = sorted(list(all_taxa))
            
            # Create a base dataframe with all taxa
            base_df = pd.DataFrame({'name': all_taxa})
            
            # Merge each sample's data
            merged_df = base_df.copy()
            for df in all_data:
                if not df.empty and 'name' in df.columns:
                    sample_cols = [col for col in df.columns if col != 'name']
                    if sample_cols:
                        merged_df = pd.merge(merged_df, df, on='name', how='left')
            
            # Replace NaN with 0
            merged_df.fillna(0, inplace=True)
            
            # Set 'name' as index and save
            merged_df.set_index('name', inplace=True)
            merged_df.to_csv(output_file)
            
            logging.info(f"Created abundance matrix with {len(all_taxa)} taxa and {len(merged_df.columns)} samples")
        else:
            # Create an empty dataframe if no taxa found
            pd.DataFrame(columns=['name']).set_index('name').to_csv(output_file)
            logging.warning("No taxa found in any input files")
    else:
        # Create an empty dataframe if no input data
        pd.DataFrame(columns=['name']).set_index('name').to_csv(output_file)
        logging.warning("No input data provided")
    
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
