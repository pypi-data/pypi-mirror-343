#!/usr/bin/env python3
"""
SSH utility module for emtax
"""
import os
import sys
import logging
import paramiko
import getpass
from pathlib import Path
from tqdm import tqdm

logger = logging.getLogger(__name__)

class SSHClient:
    """SSH client for connecting to HPC systems."""
    
    def __init__(self, host=None, username=None, identity_file=None, password_auth=False):
        """
        Initialize SSH client.
        
        Args:
            host (str): Hostname of the HPC system
            username (str): Username for SSH authentication
        """
        self.host = host
        self.username = username
        self.identity_file = identity_file
        self.password_auth = password_auth
        self.client = None
        self.sftp = None
        self.connect()
    
    def connect(self):
        """Establish SSH connection to the HPC system."""
        try:
            # If host or username not provided, try to get from SSH config
            if not self.host or not self.username:
                ssh_config = paramiko.SSHConfig()
                user_config_file = os.path.expanduser("~/.ssh/config")
                if os.path.exists(user_config_file):
                    with open(user_config_file) as f:
                        ssh_config.parse(f)
                    
                    # Get the first host entry if not specified
                    if not self.host:
                        hosts = list(ssh_config.get_hostnames())
                        if hosts and hosts[0] != '*':
                            self.host = hosts[0]
                            logger.info(f"Using host from SSH config: {self.host}")
                    
                    # Get username for the specified host
                    if self.host:
                        host_config = ssh_config.lookup(self.host)
                        if 'user' in host_config and not self.username:
                            self.username = host_config['user']
                            logger.info(f"Using username from SSH config: {self.username}")
            
            # If still not set, prompt user
            if not self.host:
                self.host = input("Enter HPC hostname: ")
            if not self.username:
                self.username = input(f"Enter username for {self.host}: ")
            
            # Create SSH client
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Authentication method selection
            auth_methods_tried = []
            auth_success = False
            
            # If password authentication is explicitly requested
            if self.password_auth:
                logger.info("Using password authentication as requested...")
                try:
                    auth_methods_tried.append("password")
                    password = getpass.getpass(f"Password for {self.username}@{self.host}: ")
                    self.client.connect(
                        hostname=self.host,
                        username=self.username,
                        password=password,
                        timeout=10
                    )
                    auth_success = True
                    logger.info("Password authentication successful")
                except paramiko.AuthenticationException as e:
                    logger.error(f"Password authentication failed: {str(e)}")
                except Exception as e:
                    logger.error(f"Error during password authentication: {str(e)}")
            else:
                # Try key-based authentication first
                logger.info("Trying key-based authentication...")
                try:
                    auth_methods_tried.append("key-based")
                    connect_kwargs = {
                        "hostname": self.host,
                        "username": self.username,
                        "timeout": 10
                    }
                    
                    # If identity file is provided, check if it exists
                    if self.identity_file:
                        identity_path = os.path.expanduser(self.identity_file)
                        if os.path.isfile(identity_path):
                            logger.info(f"Using identity file: {identity_path}")
                            connect_kwargs["key_filename"] = identity_path
                            # Don't look for other keys if specific one is provided
                            connect_kwargs["look_for_keys"] = False
                            connect_kwargs["allow_agent"] = False
                        else:
                            logger.warning(f"Specified identity file not found: {identity_path}")
                            logger.info("Looking for alternative SSH keys...")
                            
                            # Check for common SSH key files
                            ssh_dir = os.path.expanduser("~/.ssh")
                            potential_keys = []
                            if os.path.isdir(ssh_dir):
                                for key_file in os.listdir(ssh_dir):
                                    if key_file.endswith("_rsa") or key_file.endswith("id_rsa") and not key_file.endswith(".pub"):
                                        potential_keys.append(os.path.join(ssh_dir, key_file))
                            
                            if potential_keys:
                                logger.info(f"Found {len(potential_keys)} potential SSH keys: {', '.join(potential_keys)}")
                                connect_kwargs["key_filename"] = potential_keys
                            else:
                                # Fall back to default behavior
                                connect_kwargs["look_for_keys"] = True
                                connect_kwargs["allow_agent"] = True
                    else:
                        # Otherwise, try to use any available keys
                        connect_kwargs["look_for_keys"] = True
                        connect_kwargs["allow_agent"] = True
                        
                    self.client.connect(**connect_kwargs)
                    auth_success = True
                    logger.info("Key-based authentication successful")
                except paramiko.AuthenticationException:
                    logger.info("Key-based authentication failed, trying password...")
                    # If key-based auth fails, try password
                    try:
                        auth_methods_tried.append("password")
                        password = getpass.getpass(f"Password for {self.username}@{self.host}: ")
                        self.client.connect(
                            hostname=self.host,
                            username=self.username,
                            password=password,
                            timeout=10
                        )
                        auth_success = True
                        logger.info("Password authentication successful")
                    except paramiko.AuthenticationException as e:
                        logger.error(f"Password authentication failed: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error during password authentication: {str(e)}")
                except paramiko.SSHException as e:
                    logger.error(f"SSH error: {str(e)}")
                except Exception as e:
                    logger.error(f"Connection error: {str(e)}")
            
            # If authentication failed with all methods, raise an exception
            if not auth_success:
                methods_str = ", ".join(auth_methods_tried)
                raise Exception(f"All authentication methods failed ({methods_str}). Please check your SSH keys or credentials.")
            
            # Create SFTP client
            self.sftp = self.client.open_sftp()
            logger.info(f"Connected to {self.username}@{self.host}")
            
        except Exception as e:
            logger.error(f"Failed to connect to {self.host}: {str(e)}")
            logger.error("Troubleshooting tips:")
            logger.error("1. Check if your SSH key is set up correctly (usually in ~/.ssh/)")
            logger.error("2. Verify that your username and hostname are correct")
            logger.error("3. Try connecting manually with 'ssh username@hostname' to verify access")
            logger.error("4. Use --password-auth to use password authentication instead of keys")
            logger.error("5. Use --dry-run to test without connecting")
            
            # List available SSH keys
            ssh_dir = os.path.expanduser("~/.ssh")
            if os.path.isdir(ssh_dir):
                key_files = [f for f in os.listdir(ssh_dir) if not f.endswith(".pub") and "id_" in f or "_rsa" in f]
                if key_files:
                    logger.error(f"Available SSH keys in ~/.ssh/: {', '.join(key_files)}")
                    logger.error(f"Try using one of these with --identity-file ~/.ssh/KEY_FILENAME")
            sys.exit(1)
    
    def execute_command(self, command, timeout=60):
        """
        Execute a command on the HPC system.
        
        Args:
            command (str): Command to execute
            timeout (int): Timeout in seconds
            
        Returns:
            tuple: (stdout, stderr, exit_code)
        """
        try:
            logger.debug(f"Executing command: {command}")
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()
            stdout_str = stdout.read().decode('utf-8')
            stderr_str = stderr.read().decode('utf-8')
            
            if exit_code != 0:
                logger.warning(f"Command exited with code {exit_code}: {command}")
                logger.warning(f"stderr: {stderr_str}")
            
            return stdout_str, stderr_str, exit_code
        except Exception as e:
            logger.error(f"Error executing command '{command}': {str(e)}")
            return "", str(e), 1
    
    def upload_file(self, local_path, remote_path, progress=True):
        """
        Upload a file to the HPC system.
        
        Args:
            local_path (str): Path to local file
            remote_path (str): Path on remote system
            progress (bool): Show progress bar
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create remote directory if it doesn't exist
            remote_dir = os.path.dirname(remote_path)
            self.execute_command(f"mkdir -p {remote_dir}")
            
            # Get file size for progress bar
            file_size = os.path.getsize(local_path)
            file_name = os.path.basename(local_path)
            
            # Log file upload start with size information
            size_mb = file_size / (1024 * 1024)
            logger.info(f"Uploading {file_name} ({size_mb:.2f} MB) to HPC")
            
            # Upload with progress bar
            if progress and file_size > 1024*1024:  # Only show for files > 1MB
                with tqdm(total=file_size, unit='B', unit_scale=True, 
                          desc=f"Uploading {file_name}") as pbar:
                    
                    # Define callback for progress updates
                    def update_progress(transferred, to_be_transferred):
                        pbar.update(transferred - pbar.n)
                    
                    # Upload file with progress callback
                    self.sftp.put(local_path, remote_path, callback=update_progress)
            else:
                # Upload without progress bar
                self.sftp.put(local_path, remote_path)
            
            # Log successful upload at info level
            logger.info(f"Successfully uploaded {file_name} to HPC")
            return True
        except Exception as e:
            logger.error(f"Failed to upload {local_path}: {str(e)}")
            return False
    
    def download_file(self, remote_path, local_path, progress=True):
        """
        Download a file from the HPC system.
        
        Args:
            remote_path (str): Path on remote system
            local_path (str): Path to local file
            progress (bool): Show progress bar
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create local directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Get file size for progress bar
            try:
                file_size = self.sftp.stat(remote_path).st_size
            except:
                file_size = 0
            
            # Download with progress bar
            if progress and file_size > 1024*1024:  # Only show for files > 1MB
                with tqdm(total=file_size, unit='B', unit_scale=True, 
                          desc=f"Downloading {os.path.basename(remote_path)}") as pbar:
                    
                    # Define callback for progress updates
                    def update_progress(transferred, to_be_transferred):
                        pbar.update(transferred - pbar.n)
                    
                    # Download file with progress callback
                    self.sftp.get(remote_path, local_path, callback=update_progress)
            else:
                # Download without progress bar
                self.sftp.get(remote_path, local_path)
            
            logger.debug(f"Downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to download {remote_path}: {str(e)}")
            return False
    
    def close(self):
        """Close the SSH connection."""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        logger.debug(f"Closed connection to {self.host}")
