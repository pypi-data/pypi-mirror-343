#!/usr/bin/env python3
"""
Status command module for emtax
"""
import os
import sys
import click
import logging
from emtax.utils.ssh import SSHClient
from emtax.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command(name="status")
@click.argument('job_id', required=True)
@click.option('--host', help='HPC hostname')
@click.option('--username', help='HPC username')
@click.option('--identity-file', help='Path to SSH identity file (private key)')
@click.option('--password-auth', is_flag=True, help='Use password authentication instead of key-based')
def status_command(job_id, host, username, identity_file, password_auth):
    """
    Check the status of a submitted job on the HPC system.
    
    JOB_ID: The SLURM job ID to check
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
        
        # Check job status
        logger.info(f"Checking status of job {job_id}...")
        stdout, stderr, exit_code = ssh.execute_command(f"sacct -j {job_id} --format=JobID,JobName,State,Elapsed,NodeList,ExitCode -n")
        
        if exit_code != 0:
            logger.error(f"Failed to get job status: {stderr}")
            sys.exit(1)
        
        if not stdout.strip():
            logger.error(f"No information found for job {job_id}")
            sys.exit(1)
        
        # Parse and display job status
        logger.info(f"Job {job_id} status:")
        print("\nJob Status Information:")
        print("=" * 80)
        print(f"{'JobID':<15}{'JobName':<20}{'State':<15}{'Elapsed':<15}{'NodeList':<20}{'ExitCode':<10}")
        print("-" * 80)
        
        for line in stdout.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 6:
                job_id = parts[0]
                job_name = parts[1]
                state = parts[2]
                elapsed = parts[3]
                node_list = parts[4]
                exit_code = parts[5]
                print(f"{job_id:<15}{job_name:<20}{state:<15}{elapsed:<15}{node_list:<20}{exit_code:<10}")
        
        print("=" * 80)
        
        # Check if job is running or completed
        if "RUNNING" in stdout or "PENDING" in stdout:
            logger.info("Job is still running or pending.")
        elif "COMPLETED" in stdout:
            logger.info("Job has completed. You can download results using 'emtax download' command.")
        elif "FAILED" in stdout or "CANCELLED" in stdout:
            logger.error("Job has failed or been cancelled.")
            
            # Check for error logs
            logger.info("Checking error logs...")
            stdout, stderr, exit_code = ssh.execute_command(f"cat slurm-{job_id}.err 2>/dev/null || echo 'No error log found'")
            if stdout and "No error log found" not in stdout:
                logger.info("Error log content:")
                print("\nError Log:")
                print("-" * 80)
                print(stdout[:1000] + ("..." if len(stdout) > 1000 else ""))
                print("-" * 80)
        
        # Close SSH connection
        ssh.close()
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
