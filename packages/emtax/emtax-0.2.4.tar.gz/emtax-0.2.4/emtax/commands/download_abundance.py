#!/usr/bin/env python3
"""
Command to download the abundance matrix file from the HPC system.
Simplified version that creates a results directory in the current working directory.
"""
import os
import sys
import time
import logging
import click
from pathlib import Path

from emtax.utils.ssh import SSHClient

logger = logging.getLogger(__name__)

@click.command(name="download", help="Download the abundance matrix file from the HPC system")
@click.option("--output-dir", required=True, help="Output directory on the HPC system")
@click.option("--host", help="HPC hostname")
@click.option("--username", help="HPC username")
@click.option("--identity-file", help="Path to SSH identity file (private key)")
@click.option("--password-auth", is_flag=True, help="Use password authentication instead of key-based")
@click.option("--job-id", help="Job ID to check before downloading (will wait for job completion)")
def download_abundance_command(output_dir, host, username, identity_file, password_auth, job_id):
    """
    Download the abundance matrix file from the HPC system.
    
    Args:
        output_dir (str): Output directory on the HPC system
        host (str): HPC hostname
        username (str): HPC username
        identity_file (str): Path to SSH identity file (private key)
        password_auth (bool): Use password authentication instead of key-based
        job_id (str): Job ID to check before downloading (will wait for job completion)
    """
    # Create results directory in current working directory
    local_dir = os.path.join(os.getcwd(), "results")
    os.makedirs(local_dir, exist_ok=True)
    
    # Connect to HPC
    logger.info(f"Connecting to HPC system: {host}")
    
    # Create SSH client with the provided authentication parameters
    ssh = SSHClient(host=host, username=username, identity_file=identity_file, password_auth=password_auth)
    
    # Check if job is complete if job_id is provided
    if job_id:
        logger.info(f"Checking if job {job_id} is complete...")
        while True:
            stdout, stderr, exit_code = ssh.execute_command(f"sacct -j {job_id} --format=State --noheader | head -n 1")
            state = stdout.strip()
            
            if state in ["COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"]:
                logger.info(f"Job {job_id} is in state: {state}")
                break
            elif state in ["PENDING", "RUNNING"]:
                logger.info(f"Job {job_id} is still {state}. Waiting 30 seconds before checking again...")
                time.sleep(30)  # Wait for 30 seconds before checking again
            else:
                logger.info(f"Job {job_id} is in state: {state}. Waiting 30 seconds before checking again...")
                time.sleep(30)  # Wait for 30 seconds before checking again
    
    # Define the remote and local paths
    abundance_matrix_path = os.path.join(output_dir, "Results", "Taxonomic_Profiling", 
                                        "5_DNA_Relative_Abundance_Matrix_Python", "abundance_matrix.csv")
    local_path = os.path.join(local_dir, "abundance_matrix.csv")
    
    # Check if the abundance matrix file exists
    stdout, stderr, exit_code = ssh.execute_command(f"test -f {abundance_matrix_path} && echo 'exists'")
    if "exists" not in stdout:
        logger.error(f"Abundance matrix file not found at {abundance_matrix_path}")
        logger.error("The job may not have completed successfully or the file path is incorrect.")
        sys.exit(1)
    
    # Download the abundance matrix file
    logger.info(f"Downloading abundance matrix file from {abundance_matrix_path} to {local_path}...")
    success = ssh.download_file(abundance_matrix_path, local_path)
    
    if success and os.path.exists(local_path):
        logger.info(f"Successfully downloaded abundance matrix file to {local_path}")
    else:
        logger.error("Failed to download abundance matrix file")
        sys.exit(1)
