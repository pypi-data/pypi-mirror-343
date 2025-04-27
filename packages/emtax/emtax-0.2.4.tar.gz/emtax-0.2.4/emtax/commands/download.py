#!/usr/bin/env python3
"""
Download command module for emtax
"""
import os
import sys
import click
import logging
from pathlib import Path
from emtax.utils.ssh import SSHClient
from emtax.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command(name="download")
@click.option('--output-dir', required=True, help='HPC output directory path')
@click.option('--local-dir', default='.', help='Local directory to save downloaded files')
@click.option('--host', help='HPC hostname')
@click.option('--username', help='HPC username')
@click.option('--identity-file', help='Path to SSH identity file (private key)')
@click.option('--password-auth', is_flag=True, help='Use password authentication instead of key-based')
@click.option('--file-pattern', default='*.csv', help='File pattern to download (default: *.csv)')
def download_command(output_dir, local_dir, host, username, identity_file, password_auth, file_pattern):
    """
    Download result files from the HPC system.
    """
    try:
        # Connect to HPC
        logger.info(f"Connecting to HPC system: {host}")
        try:
            ssh = SSHClient(host, username, identity_file, password_auth)
        except Exception as e:
            logger.error(f"Failed to connect to HPC system: {str(e)}")
            logger.error("Please check your SSH configuration.")
            sys.exit(1)
        
        # Create local directory if it doesn't exist
        local_dir_path = Path(local_dir)
        local_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Check if the output directory exists on HPC
        stdout, stderr, exit_code = ssh.execute_command(f"test -d {output_dir} && echo 'exists'")
        if "exists" not in stdout:
            logger.error(f"Output directory {output_dir} does not exist on HPC")
            sys.exit(1)
        
        # Find abundance matrix and other result files
        logger.info(f"Finding result files in {output_dir}...")
        
        # First, check for the abundance matrix specifically
        abundance_matrix_path = os.path.join(output_dir, "rel_abundance_matrix", "abundance_matrix.csv")
        stdout, stderr, exit_code = ssh.execute_command(f"test -f {abundance_matrix_path} && echo 'exists'")
        
        if "exists" in stdout:
            # Download abundance matrix
            local_abundance_path = os.path.join(local_dir, "abundance_matrix.csv")
            logger.info(f"Downloading abundance matrix to {local_abundance_path}...")
            success = ssh.download_file(abundance_matrix_path, local_abundance_path, progress=True)
            
            if success:
                logger.info(f"Successfully downloaded abundance matrix to {local_abundance_path}")
            else:
                logger.error(f"Failed to download abundance matrix")
        else:
            logger.warning(f"Abundance matrix not found at {abundance_matrix_path}")
            
        # Find other result files matching the pattern
        logger.info(f"Finding other result files matching pattern: {file_pattern}...")
        find_cmd = f"find {output_dir} -type f -name '{file_pattern}'"
        stdout, stderr, exit_code = ssh.execute_command(find_cmd)
        
        if exit_code != 0:
            logger.error(f"Failed to find result files: {stderr}")
        else:
            result_files = stdout.strip().split('\n')
            result_files = [f for f in result_files if f and f != abundance_matrix_path]
            
            if not result_files:
                logger.warning(f"No additional result files found matching pattern: {file_pattern}")
            else:
                logger.info(f"Found {len(result_files)} additional result files")
                
                # Download each result file
                for remote_path in result_files:
                    if not remote_path.strip():
                        continue
                        
                    # Create relative path structure
                    rel_path = os.path.relpath(remote_path, output_dir)
                    local_path = os.path.join(local_dir, rel_path)
                    
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    
                    # Download file
                    logger.info(f"Downloading {rel_path}...")
                    success = ssh.download_file(remote_path, local_path, progress=True)
                    
                    if success:
                        logger.info(f"Successfully downloaded to {local_path}")
                    else:
                        logger.error(f"Failed to download {remote_path}")
        
        # Close SSH connection
        ssh.close()
        
        logger.info("Download complete")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
