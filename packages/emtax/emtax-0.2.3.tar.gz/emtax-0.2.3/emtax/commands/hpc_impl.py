#!/usr/bin/env python3
"""
HPC command implementation module for TaxoPipe
"""
import os
import sys
import logging
import tempfile
import shutil
from pathlib import Path
from tqdm import tqdm

logger = logging.getLogger(__name__)

def create_directories(ssh, config):
    """
    Create necessary directories on the HPC system.
    
    Args:
        ssh (SSHClient): SSH client for HPC connection
        config (Config): TaxoPipe configuration
    """
    # Check if output directory already exists
    stdout, _, _ = ssh.execute_command(f"test -d {config.output_dir} && echo 'exists'")
    if "exists" in stdout:
        logger.info(f"Output directory already exists at {config.output_dir}, using existing directory")
        
        # Check if workflow directory exists
        stdout, _, _ = ssh.execute_command(f"test -d {config.workflow_dir} && echo 'exists'")
        if "exists" in stdout:
            logger.info(f"Workflow directory already exists at {config.workflow_dir}, using existing directory")
            
            # Check for existing results
            bracken_dir = os.path.join(config.output_dir, "Taxonomic_Profiling/2_DNA_Bracken")
            stdout, _, _ = ssh.execute_command(f"test -d {bracken_dir} && echo 'exists'")
            if "exists" in stdout:
                logger.info(f"Found existing bracken results at {bracken_dir}")
                
                # Check if abundance matrix exists
                abundance_matrix = os.path.join(config.output_dir, "Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/abundance_matrix.csv")
                stdout, _, _ = ssh.execute_command(f"test -f {abundance_matrix} && echo 'exists'")
                if "exists" in stdout:
                    logger.info(f"Found existing abundance matrix at {abundance_matrix}")
    else:
        logger.info(f"Creating new output directory at {config.output_dir}")
    
    # Create main directories
    directories = [
        config.output_dir,
        config.raw_data_dir,
        config.preprocessed_data_dir,
        config.results_dir,
        config.logs_dir,
        config.taxonomic_profiling_dir,
        config.kraken2_dna_dir,
        config.bracken_dna_dir,
        config.rel_abundance_matrix_dir,
        config.fastp_logs_dir,
        config.bowtie2_host_logs_dir,
        config.kraken2_db_logs_dir,
        config.kraken2_dna_logs_dir,
        config.bracken_dna_logs_dir,
        config.rel_abundance_matrix_logs_dir
    ]
    
    # Create sample-specific directories - only for required directories
    for sample in config.samples:
        directories.extend([
            os.path.join(config.kraken2_dna_dir, sample),
            os.path.join(config.bracken_dna_dir, sample),
            os.path.join(config.fastp_logs_dir, sample),
            os.path.join(config.bowtie2_host_logs_dir, sample),
            os.path.join(config.kraken2_dna_logs_dir, sample),
            os.path.join(config.bracken_dna_logs_dir, sample)
        ])
    
    # Create directories (mkdir -p will not overwrite existing directories)
    for directory in directories:
        logger.debug(f"Ensuring directory exists: {directory}")
        ssh.execute_command(f"mkdir -p {directory}")

def upload_raw_files(ssh, config):
    """
    Upload raw FASTQ files to the HPC system.
    
    Args:
        ssh (SSHClient): SSH client for HPC connection
        config (Config): TaxoPipe configuration
    """
    # Calculate total size of all files
    total_size = 0
    files_to_upload = []
    skipped_files = []
    
    # Check which files need to be uploaded
    for local_path in config.raw_files:
        if os.path.exists(local_path):
            file_name = os.path.basename(local_path)
            remote_path = os.path.join(config.raw_data_dir, file_name)
            
            # Check if file already exists on HPC
            stdout, _, _ = ssh.execute_command(f"test -f {remote_path} && echo 'exists'")
            if "exists" in stdout:
                logger.info(f"Found existing file: {file_name}")
                skipped_files.append(local_path)
            else:
                files_to_upload.append(local_path)
                total_size += os.path.getsize(local_path)
    
    # Convert to MB
    total_size_mb = total_size / (1024 * 1024)
    
    # Log summary before starting uploads
    if files_to_upload:
        logger.info(f"Starting upload of {len(files_to_upload)} files ({total_size_mb:.2f} MB total)")
    else:
        logger.info("No new files to upload, all files already exist on HPC")
        return
    
    # Track successful uploads
    successful_uploads = 0
    
    # Upload each raw file
    for local_path in files_to_upload:
        # Get file name
        file_name = os.path.basename(local_path)
        
        # Create remote path
        remote_path = os.path.join(config.raw_data_dir, file_name)
        
        # Upload file
        logger.info(f"Uploading {file_name} to HPC...")
        if ssh.upload_file(local_path, remote_path, progress=True):
            successful_uploads += 1
            logger.info(f"Successfully uploaded {file_name}")
    
    # Log summary after uploads complete
    logger.info(f"Raw data upload complete: {successful_uploads} files uploaded, {len(skipped_files)} files skipped (already existed)")

def setup_reference_databases(ssh, config):
    """
    Download and set up reference databases on the HPC system.
    
    Args:
        ssh (SSHClient): SSH client for HPC connection
        config (Config): TaxoPipe configuration
    """
    # Check if Kraken2 database exists
    stdout, _, _ = ssh.execute_command(f"test -d {config.kraken_db} && echo 'exists'")
    if "exists" not in stdout:
        # Create directory
        ssh.execute_command(f"mkdir -p {config.kraken_db}")
        
        # Download Kraken2 database
        logger.info("Downloading Kraken2 database (this may take a while)")
        kraken_url = "https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz"
        ssh.execute_command(f"cd {config.kraken_db} && wget -q --show-progress {kraken_url} && tar -xzf k2_standard_20240112.tar.gz && rm k2_standard_20240112.tar.gz")
    else:
        logger.info(f"Kraken2 database already exists at {config.kraken_db}")
    
    # Check if corn genome database exists
    stdout, _, _ = ssh.execute_command(f"test -d {config.corn_db} && echo 'exists'")
    if "exists" not in stdout:
        # Create directory
        ssh.execute_command(f"mkdir -p {config.corn_db}")
        
        # Download corn genome database
        logger.info("Downloading corn genome database (this may take a while)")
        corn_url = "https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip"
        ssh.execute_command(f"cd {config.corn_db} && wget -q --show-progress {corn_url} && unzip corn_db.zip && rm corn_db.zip")
    else:
        logger.info(f"Corn genome database already exists at {config.corn_db}")
