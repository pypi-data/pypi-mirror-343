import numpy as np
import mujoco
import mujoco.viewer
from mj_envs.utils.scene_gen import construct_scene
import time
from copy import deepcopy
from scipy.spatial.transform import Rotation as R
from mj_envs.utils.misc import load_task_cfg, load_robot_cfg, get_random_perturbed_pose

class MJEnv:
    def __init__(self, task="bolt_nut_sort", robot="dual_panda", headless=False):
        # Initialize MuJoCo model and data
        self.model = construct_scene(task, robot)
        self.data = mujoco.MjData(self.model)
        
        # Load task and robot configs
        self.cfg = load_task_cfg(task)
        self.robot_cfg = load_robot_cfg(robot)
        self.robot_name = self.robot_cfg["name"]
        
        # Define action space using actual joint limits
        ctrl_range = np.zeros((self.model.nu, 2))  # [low, high] for each actuator
        
        for i in range(self.model.nu):
            actuator = self.model.actuator(i)
            
            # Get joint index for this actuator
            joint_idx = actuator.trnid[0]
            joint = self.model.joint(joint_idx)
            
            # Get joint limits
            if joint.range is not None and joint.range.size > 0:
                # Use joint range if specified
                ctrl_range[i, 0] = joint.range[0]
                ctrl_range[i, 1] = joint.range[1]
            else:
                # Use actuator ctrlrange if specified
                if actuator.ctrlrange is not None and actuator.ctrlrange.size > 0:
                    ctrl_range[i, 0] = actuator.ctrlrange[0]
                    ctrl_range[i, 1] = actuator.ctrlrange[1]
                else:
                    # Default to [-1, 1] if no limits specified
                    ctrl_range[i, 0] = -1.0
                    ctrl_range[i, 1] = 1.0
        
        self.action_space = {
            'shape': (self.model.nu,),  # Number of actuators
            'low': ctrl_range[:, 0],    # Minimum control values
            'high': ctrl_range[:, 1],   # Maximum control values
            'dtype': np.float32
        }
        
        # Initialize observation space with detailed structure
        self.observation_space = {
            'observation.state': {
                'shape': (self.robot_cfg["obj_startidx"],),
                'dtype': np.float32
            },
            'observation.environment_state': {
                'shape': (self.model.nq - self.robot_cfg["obj_startidx"],),
                'dtype': np.float32
            },
            'observation.qvel': {
                'shape': (self.robot_cfg["obj_startidx"],),
                'dtype': np.float32
            },
            'observation.env_qvel': {
                'shape': (self.model.nv - self.robot_cfg["obj_startidx"],),
                'dtype': np.float32
            },
        }
        
        # Viewer settings
        self.headless = headless
        self.viewer = None
        self._viewer_initialized = False
        
        # Initialize viewer if not headless
        if not self.headless:
            self._init_viewer()

        # Store initial state for reset
        self.init_data = None
        self.init = False
        
    def reset(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
            
        # Reset to home position
        mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)
        mujoco.mj_step(self.model, self.data)
        
        # Reset scene objects
        self._reset_scene()
        
        # Update viewer if not headless
        if not self.headless:
            self._update_viewer()
            
        return self._get_obs()
        
    def _reset_scene(self):
        """Reset the scene objects to their initial positions"""
        print("resetting scene")
        reset_func = self.cfg.get('reset_function', None)
        
        if reset_func is not None:
            print("resetting scene with custom function")
            reset_func(self.model, self.data, self.robot_cfg, self.cfg)
        else:
            id = self.robot_cfg["obj_startidx"]
            vid = self.robot_cfg["obj_startidx"]
            
            try:
                reset_cfg = self.cfg.get('reset_perturbation', {})
            except:
                pass
                
            for ii, obj in enumerate(self.cfg['objects']):
                try:
                    if obj not in reset_cfg:
                        print(f"[WARN] Object {obj} does not specify how to perturb its pose. Skipping...")
                        new_posquat = np.array(self.cfg['default_poses'][obj]).copy()
                    else:
                        new_posquat = get_random_perturbed_pose(
                            old_pose=np.array(self.cfg['default_poses'][obj]),
                            reset_spec=reset_cfg[obj],
                        )
                    
                    self.data.qpos[id:id+7] = new_posquat
                    self.data.qvel[vid:vid+6] = 0.0
                    
                except:
                    rand_range = self.cfg['randomize_range']
                    posquat = np.array(self.cfg['default_poses'][obj])
                    self.data.qpos[id:id+7] = posquat
                    
                    if self.cfg['randomize_pos'][obj]:
                        self.data.qpos[id] += np.random.uniform(-rand_range, rand_range)
                        self.data.qpos[id+1] += np.random.uniform(-rand_range, rand_range)
                        
                    if self.cfg['randomize_rot'][obj]:
                        rand_quat = np.random.uniform(-1, 1, 4)
                        rand_quat /= np.linalg.norm(rand_quat)
                        self.data.qpos[id+3:id+7] = rand_quat
                        
                    self.data.qvel[vid:vid+6] = 0.0
                    
                id += 7
                vid += 6
                
        mujoco.mj_step(self.model, self.data)
        
    def _get_obs(self):
        """Get observation in the format used for logging"""
        # Get base states
        qpos = np.array(deepcopy(self.data.qpos), dtype=np.float32)
        qvel = np.array(deepcopy(self.data.qvel), dtype=np.float32)
        
        # Split into robot and environment states
        robot_qpos = qpos[:self.robot_cfg["obj_startidx"]]
        env_state = qpos[self.robot_cfg["obj_startidx"]:]
        robot_qvel = qvel[:self.robot_cfg["obj_startidx"]]
        env_qvel = qvel[self.robot_cfg["obj_startidx"]:]
        
        # Get end-effector poses
        ee_poses = []
        for body_name in ['r_robot/left_finger_tip', 'r_robot/right_finger_tip', 
                         'r_robot/left_finger_base', 'r_robot/right_finger_base',
                         'l_robot/left_finger_tip', 'l_robot/right_finger_tip', 
                         'l_robot/left_finger_base', 'l_robot/right_finger_base']:
            body = self.data.body(body_name)
            ee_poses.extend(body.xpos[:3])
            ee_poses.extend(body.xquat[:4])
            
        # Get fingertip targets
        fingertip_targets = []
        for target_name in ['right_lb_target', 'right_lf_target', 
                          'right_rb_target', 'right_rf_target',
                          'left_lb_target', 'left_lf_target', 
                          'left_rb_target', 'left_rf_target']:
            target = self.data.body(target_name)
            fingertip_targets.extend(target.xpos[:3])
            
        return {
            'observation.state': robot_qpos,
            'observation.environment_state': env_state,
            'observation.qvel': robot_qvel,
            'observation.env_qvel': env_qvel,
            # 'observation.ee_pose': np.array(ee_poses, dtype=np.float32),
            'action.fingertip_target': np.array(fingertip_targets, dtype=np.float32)
        }
        
    def step(self, action):

        for _ in range(10):
            # Set control values
            self.data.ctrl[:] = action
            
            # Step simulation
            mujoco.mj_step(self.model, self.data)
        

            # Update viewer if not headless
            if not self.headless:
                self._update_viewer()
                time.sleep(1/500)

        # Get observation
        obs = self._get_obs()
        
        # Calculate reward and done
        reward = self._get_reward()
        done = self._get_done()
        info = {}
        
            
        return obs, reward, done, info
        
    def _get_reward(self):
        # Implement reward calculation based on task
        return 0.0
        
    def _get_done(self):
        # Implement termination condition
        return False
        
    def _init_viewer(self):
        """Initialize the viewer if not already initialized."""
        if not self._viewer_initialized:
            self.viewer = mujoco.viewer.launch_passive(
                model=self.model, 
                data=self.data, 
                show_left_ui=True, 
                show_right_ui=True
            )
            self._viewer_initialized = True
            
    def _update_viewer(self):
        """Update the viewer with current state."""
        if self.viewer is not None:
            self.viewer.sync()
            
    def render(self, width=640, height=480, camera_id=0):
        """
        Render the current state to an RGB image.
        
        Args:
            width (int): Width of the rendered image
            height (int): Height of the rendered image
            camera_id (int): ID of the camera to use for rendering
            
        Returns:
            np.ndarray: RGB image of shape (height, width, 3)
        """
        # Create a new renderer if needed
        if not hasattr(self, '_renderer'):
            self._renderer = mujoco.Renderer(self.model, height, width)
            
        # Update renderer with current state
        self._renderer.update_scene(self.data, camera_id)
        
        # Render and return RGB image
        return self._renderer.render()
            
    def close(self):
        """Close the viewer and clean up."""
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
            self._viewer_initialized = False 