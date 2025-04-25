from mj_envs.envs.base_env import MJEnv
from mj_envs.asset_manager import AssetManager
import os

def get_asset_manager() -> AssetManager:
    """Create and return a new AssetManager instance."""
    return AssetManager(
        base_url="https://mj-envs.s3.us-east-1.amazonaws.com/assets",
        tasks_url="https://mj-envs.s3.us-east-1.amazonaws.com/tasks"
    )

def download_all_assets():
    """Download all assets from the S3 bucket and ensure local files match S3 exactly."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    asset_manager = get_asset_manager()
    asset_manager.download_all_assets()

def download_all_tasks():
    """Download all task files from the S3 bucket and ensure local files match S3 exactly."""
    cfgs_dir = os.path.join(os.path.dirname(__file__), "cfgs")
    os.makedirs(cfgs_dir, exist_ok=True)
    
    asset_manager = get_asset_manager()
    asset_manager.download_all_tasks()

def make(task="bolt_nut_sort", robot="dual_panda", headless=False):
    """
    Create a MuJoCo environment with the specified task and robot.

    Args:
        task (str): The task to create the environment for
        robot (str): The robot to use in the environment
        headless (bool): If True, no viewer will be created

    Returns:
        MJEnv: An instance of the MuJoCo environment
    """
    download_all_assets()
    download_all_tasks()
    return MJEnv(task=task, robot=robot, headless=headless)