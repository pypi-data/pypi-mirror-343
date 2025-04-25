import os
import yaml
import numpy as np
from typing import Dict, Any
from scipy.spatial.transform import Rotation as R

_HERE = os.path.dirname(os.path.abspath(__file__))

def load_task_cfg(task): 
    if os.path.exists(os.path.join(_HERE, "..", "cfgs", f"{task}.yaml")):
        with open(os.path.join(_HERE, "..", "cfgs", f"{task}.yaml"), "r") as f:
            return yaml.load(f, Loader = yaml.FullLoader)
    elif os.path.exists(os.path.join(_HERE, "..", "cfgs", f"{task}.py")):
        task_cfg = __import__(f"mj_envs.cfgs.{task}", fromlist = ["task_cfg"])
        return task_cfg.task_cfg
    else:
        raise ValueError(f"Task config {task} not found")
    
def load_robot_cfg(robot): 
    robot_cfg = __import__(f"mj_envs.robot_cfgs.{robot}", fromlist = ["robot_cfg"])
    return robot_cfg.robot_cfg


def get_random_perturbed_pose(
    old_pose: np.ndarray,
    reset_spec: Dict[str, Any],
) -> np.ndarray:
    new_pose = old_pose.copy()
    
    # perturb position
    min_pos = np.array(reset_spec['min_pos'])
    max_pos = np.array(reset_spec['max_pos'])
    new_pose[:3] = old_pose[:3] + np.random.rand(3) * (max_pos - min_pos) + min_pos

    # get angle perturbation as euler angles
    max_euler = np.array(reset_spec['max_rot'])
    min_euler = np.array(reset_spec['min_rot'])
    euler_perturbation = np.random.rand(3) * (max_euler - min_euler) + min_euler

    # perturb orientation by euler angles
    r = R.from_euler('xyz', euler_perturbation, degrees=True)
    old_rot = R.from_quat(old_pose[3:])
    new_rot = r * old_rot
    new_pose[3:] = new_rot.as_quat()

    return new_pose
