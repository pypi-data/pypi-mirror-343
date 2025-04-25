# mj_envs

MuJoCo environments for DART (Dynamic Animation and Robotics Toolkit).

## Installation

```bash
pip install mj_envs
```

## Features

- MuJoCo-based simulation environments
- Support for dual Panda robot
- Interactive keyboard controls for environment manipulation
- Various tasks including pick and place operations

## Usage

```python
import mj_envs

# Create environment
env = mj_envs.make(task="pick_mug", robot="dual_panda", headless=False)

# Reset environment
obs = env.reset()

# Step through environment
action = env.action_space.sample()
obs, reward, done, info = env.step(action)
```

## Keyboard Controls

- R: Reset robot to initial position
- S: Reset scene objects
- Q: Quit

## Requirements

- Python >= 3.7
- MuJoCo
- dm_control
- numpy
- scipy
- pyyaml
- gdown
- qpsolvers

## License

MIT License