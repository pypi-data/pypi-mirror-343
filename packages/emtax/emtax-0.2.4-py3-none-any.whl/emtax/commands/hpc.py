#!/usr/bin/env python3
"""
HPC command module for emtax
"""
import os
import sys
import logging
import click
from pathlib import Path

from emtax.utils.ssh import SSHClient
from emtax.utils.workflow_updated import SnakemakeWorkflow
from emtax.utils.config import Config
from emtax.commands.hpc_impl import create_directories, upload_raw_files, setup_reference_databases

logger = logging.getLogger(__name__)

@click.command('hpc')
@click.option('-r', '--raw-file', multiple=True, required=True, help='Raw FASTQ file(s) to process')
@click.option('-o', '--output-dir', required=True, help='Output directory on HPC')
@click.option('--kraken-db', required=True, help='Path to Kraken2 database on HPC')
@click.option('--corn-db', required=True, help='Path to corn genome database on HPC')
@click.option('--host', required=True, help='HPC hostname')
@click.option('--port', default=22, help='SSH port')
@click.option('--username', required=True, help='HPC username')
@click.option('--key-file', help='Path to SSH key file')
@click.option('--key-passphrase', help='Passphrase for SSH key')
@click.option('--password-auth', is_flag=True, help='Use password authentication')
@click.option('--partition', default='normal', help='HPC partition')
@click.option('--threads', default=8, type=int, help='Number of threads to use')
@click.option('--memory', default='16G', help='Memory to allocate')
@click.option('--time', default='24:00:00', help='Time limit')
@click.option('--no-upload-data', is_flag=True, help='Skip uploading raw data')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def hpc_command(raw_file, output_dir, kraken_db, corn_db, host, port, username, key_file, key_passphrase, password_auth, partition, threads, memory, time, no_upload_data, verbose):
    """
    Run emtax workflow on HPC system.
    
    This command will:
    1. Connect to the HPC system
    2. Create necessary directories
    3. Upload raw FASTQ files
    4. Set up reference databases
    5. Configure and submit workflow
    """
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Connect to HPC system
    logger.info(f"Connecting to HPC system: {host}")
    ssh = SSHClient(host=host, username=username, identity_file=key_file, password_auth=password_auth)
    
    # Create configuration
    config = Config(
        raw_files=raw_file,
        output_dir=output_dir,
        kraken_db=kraken_db,
        corn_db=corn_db,
        partition=partition,
        threads=threads,
        memory=memory,
        time=time,
        no_upload_data=no_upload_data
    )
    
    # Create directories on HPC
    logger.info("Creating directories on HPC")
    create_directories(ssh, config)
    
    # Upload raw files to HPC
    logger.info(f"Uploading {len(raw_file)} raw files to HPC")
    upload_raw_files(ssh, config)
    
    # Set up reference databases
    logger.info("Setting up reference databases")
    setup_reference_databases(ssh, config)
    
    # Configure and submit workflow
    logger.info("Configuring and submitting workflow")
    workflow = SnakemakeWorkflow(ssh, config)
    job_id = workflow.submit()
    
    logger.info(f"Workflow submitted with job ID: {job_id}")
    logger.info(f"Output will be available at: {output_dir}")
