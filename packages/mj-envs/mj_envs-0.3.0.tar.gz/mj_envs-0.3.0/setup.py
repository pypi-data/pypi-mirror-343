from setuptools import setup, find_packages

setup(
    name="mj_envs",
    version="0.3.0",
    description="MuJoCo environments for DART",
    author="Younghyo Park",
    author_email="younghyo@mit.edu",
    packages=find_packages(),
    install_requires=[
        "dm_control",
        "numpy",
        "mujoco",
        "scipy",
        "pyyaml",
        "gdown",
        "qpsolvers",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 