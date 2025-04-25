import os
import json
import hashlib
import requests
from pathlib import Path
import shutil
from typing import Optional, List
import logging
from tqdm import tqdm
import multiprocessing
from tqdm.contrib.concurrent import process_map
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class AssetManager:
    def __init__(self, base_url: str, tasks_url: str, cache_dir: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.tasks_url = tasks_url.rstrip('/')
        self.cache_dir = os.path.join(CUR_PATH, 'assets')
        self.tasks_dir = os.path.join(CUR_PATH, 'cfgs')
        self.manifest_file = os.path.join(self.cache_dir, 'manifest.json')
        self.tasks_manifest_file = os.path.join(self.tasks_dir, 'manifest.json')
        self.manifest = self._load_manifest()
        self.tasks_manifest = self._load_tasks_manifest()

    def _load_manifest(self) -> dict:
        """Load the manifest file or create a new one if it doesn't exist."""
        if os.path.exists(self.manifest_file):
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Manifest file corrupted, creating new one")
        return {}

    def _save_manifest(self):
        """Save the current manifest to disk."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def _get_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_remote_file_list(self) -> List[str]:
        """
        Get list of all files from the HTTP server.
        
        Returns:
            List[str]: List of file paths
        """
        try:
            response = requests.get(f"{self.base_url}/file_list.txt")
            response.raise_for_status()
            return response.text.splitlines()
        except requests.RequestException as e:
            logger.error(f"Error getting file list: {str(e)}")
            raise

    def _download_file(self, asset_path: str, pbar: tqdm) -> bool:
        """
        Download a single file with progress bar.
        
        Args:
            asset_path (str): Path to the asset relative to the base_url
            pbar (tqdm): Progress bar to update
            
        Returns:
            bool: True if download was successful
        """
        local_path = os.path.join(self.cache_dir, asset_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        url = f"{self.base_url}/{asset_path}"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        pbar.update(len(chunk))
            
            # Update manifest
            self.manifest[asset_path] = self._get_file_hash(local_path)
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            return False

    def download_all_assets(self, num_processes: Optional[int] = None):
        """Download all assets from the HTTP server."""
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
            print(f"Using {num_processes} processes for downloading assets")

        # Get list of remote files
        remote_files = self._get_remote_file_list()
        remote_file_set = set(remote_files)
        
        # Get list of local files
        local_files = set()
        for root, _, files in os.walk(self.cache_dir):
            for file in files:
                if file == 'manifest.json':
                    continue
                rel_path = os.path.relpath(os.path.join(root, file), self.cache_dir)
                local_files.add(rel_path)

        # Delete files that don't exist remotely
        files_to_delete = local_files - remote_file_set
        for file_path in files_to_delete:
            full_path = os.path.join(self.cache_dir, file_path)
            os.remove(full_path)
            self.manifest.pop(file_path, None)
            print(f"Deleted local file not on server: {file_path}")

        # Determine which files need to be downloaded
        assets_to_download = []
        for asset_path in remote_files:
            local_path = os.path.join(self.cache_dir, asset_path)
            if os.path.exists(local_path) and asset_path in self.manifest:
                current_hash = self._get_file_hash(local_path)
                if current_hash == self.manifest[asset_path]:
                    continue
            assets_to_download.append(asset_path)

        if not assets_to_download and not files_to_delete:
            print("All assets are up to date.")
            return

        if assets_to_download:
            print(f"Downloading {len(assets_to_download)} files with {num_processes} processes")
            
            # Create a shared counter for progress tracking
            manager = multiprocessing.Manager()
            progress_counter = manager.Value('i', 0)
            
            # Create a progress bar
            with tqdm(total=len(assets_to_download), desc="Downloading assets") as pbar:
                # Create a pool of workers
                with multiprocessing.Pool(processes=num_processes) as pool:
                    # Create tasks
                    tasks = [(asset_path, progress_counter) for asset_path in assets_to_download]
                    
                    # Use map_async
                    result = pool.map_async(self._download_file_with_progress, tasks)
                    
                    # Update progress bar
                    while not result.ready():
                        pbar.update(progress_counter.value - pbar.n)
                        time.sleep(0.1)
                    
                    # Get results
                    results = result.get()
            
            # Update manifest with successful downloads
            for asset_path, success in zip(assets_to_download, results):
                if success:
                    local_path = os.path.join(self.cache_dir, asset_path)
                    self.manifest[asset_path] = self._get_file_hash(local_path)

        self._save_manifest()
        print("Synchronization complete.")

    def _download_file_with_progress(self, args: tuple) -> bool:
        """Download a file and update progress counter."""
        asset_path, progress_counter = args
        local_path = os.path.join(self.cache_dir, asset_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        url = f"{self.base_url}/{asset_path}"

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            progress_counter.value += 1
            return True
            
        except requests.RequestException as e:
            print(f"Failed to download {url}: {str(e)}")
            return False

    def get_asset_path(self, asset_path: str) -> str:
        """
        Get the path to an asset, downloading it if necessary.
        
        Args:
            asset_path (str): Path to the asset relative to the base_url
            
        Returns:
            str: Path to the downloaded/cached asset
        """
        local_path = os.path.join(self.cache_dir, asset_path)
        
        # Check if file exists and is up to date
        if os.path.exists(local_path):
            if asset_path in self.manifest:
                current_hash = self._get_file_hash(local_path)
                if current_hash == self.manifest[asset_path]:
                    return local_path
        
        # Download the asset
        self.download_all_assets()
        return local_path

    def _load_tasks_manifest(self) -> dict:
        """Load the tasks manifest file or create a new one if it doesn't exist."""
        if os.path.exists(self.tasks_manifest_file):
            try:
                with open(self.tasks_manifest_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Tasks manifest file corrupted, creating new one")
        return {}

    def _save_tasks_manifest(self):
        """Save the current tasks manifest to disk."""
        with open(self.tasks_manifest_file, 'w') as f:
            json.dump(self.tasks_manifest, f, indent=2)

    def _get_remote_tasks_list(self) -> List[str]:
        """
        Get list of all task files from the HTTP server.
        
        Returns:
            List[str]: List of task file paths
        """
        try:
            response = requests.get(f"{self.tasks_url}/file_list.txt")
            response.raise_for_status()
            return response.text.splitlines()
        except requests.RequestException as e:
            logger.error(f"Error getting tasks file list: {str(e)}")
            raise

    def download_all_tasks(self, num_processes: Optional[int] = None):
        """Download all task files from the HTTP server."""
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
            print(f"Using {num_processes} processes for downloading tasks")

        # Create tasks directory if it doesn't exist
        os.makedirs(self.tasks_dir, exist_ok=True)

        # Get list of remote files
        remote_files = self._get_remote_tasks_list()
        remote_file_set = set(remote_files)
        
        # Get list of local files
        local_files = set()
        for root, _, files in os.walk(self.tasks_dir):
            for file in files:
                if file == 'manifest.json':
                    continue
                rel_path = os.path.relpath(os.path.join(root, file), self.tasks_dir)
                local_files.add(rel_path)

        # Delete files that don't exist remotely
        files_to_delete = local_files - remote_file_set
        for file_path in files_to_delete:
            full_path = os.path.join(self.tasks_dir, file_path)
            os.remove(full_path)
            self.tasks_manifest.pop(file_path, None)
            print(f"Deleted local task file not on server: {file_path}")

        # Determine which files need to be downloaded
        tasks_to_download = []
        for task_path in remote_files:
            local_path = os.path.join(self.tasks_dir, task_path)
            if os.path.exists(local_path) and task_path in self.tasks_manifest:
                current_hash = self._get_file_hash(local_path)
                if current_hash == self.tasks_manifest[task_path]:
                    continue
            tasks_to_download.append(task_path)

        if not tasks_to_download and not files_to_delete:
            print("All task files are up to date.")
            return

        if tasks_to_download:
            print(f"Downloading {len(tasks_to_download)} task files with {num_processes} processes")
            
            # Create a shared counter for progress tracking
            manager = multiprocessing.Manager()
            progress_counter = manager.Value('i', 0)
            
            # Create a progress bar
            with tqdm(total=len(tasks_to_download), desc="Downloading task files") as pbar:
                # Create a pool of workers
                with multiprocessing.Pool(processes=num_processes) as pool:
                    # Create tasks
                    tasks = [(task_path, progress_counter) for task_path in tasks_to_download]
                    
                    # Use map_async
                    result = pool.map_async(self._download_task_file_with_progress, tasks)
                    
                    # Update progress bar
                    while not result.ready():
                        pbar.update(progress_counter.value - pbar.n)
                        time.sleep(0.1)
                    
                    # Get results
                    results = result.get()
            
            # Update manifest with successful downloads
            for task_path, success in zip(tasks_to_download, results):
                if success:
                    local_path = os.path.join(self.tasks_dir, task_path)
                    self.tasks_manifest[task_path] = self._get_file_hash(local_path)

        self._save_tasks_manifest()
        print("Task files synchronization complete.")

    def _download_task_file_with_progress(self, args: tuple) -> bool:
        """Download a task file and update progress counter."""
        task_path, progress_counter = args
        local_path = os.path.join(self.tasks_dir, task_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        url = f"{self.tasks_url}/{task_path}"

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            progress_counter.value += 1
            return True
            
        except requests.RequestException as e:
            print(f"Failed to download task file {url}: {str(e)}")
            return False

    def get_task_path(self, task_path: str) -> str:
        """
        Get the path to a task file, downloading it if necessary.
        
        Args:
            task_path (str): Path to the task file relative to the tasks_url
            
        Returns:
            str: Path to the downloaded/cached task file
        """
        local_path = os.path.join(self.tasks_dir, task_path)
        
        # Check if file exists and is up to date
        if os.path.exists(local_path):
            if task_path in self.tasks_manifest:
                current_hash = self._get_file_hash(local_path)
                if current_hash == self.tasks_manifest[task_path]:
                    return local_path
        
        # Download the task file
        self.download_all_tasks()
        return local_path

    def clear_cache(self):
        """Clear all cached assets and tasks."""
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        if os.path.exists(self.tasks_dir):
            shutil.rmtree(self.tasks_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.tasks_dir, exist_ok=True)
        self.manifest = {}
        self.tasks_manifest = {}
        self._save_manifest()
        self._save_tasks_manifest() 