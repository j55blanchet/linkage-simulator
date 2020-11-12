# Linkage Simulator

A simulator for 2D rigid linkages. Intended to be used a test platform for experimenting with various forms of kinematics (inverse kinematics, differential kinematics, constraint kinematics).

## Setup
Project requires **python 3.8+**

Option 1: Use a virtual environment

1. `python -m venv .env` (`python3` for mac)
1. `source .env/bin.activate` (activate virtual environment, adjust for your platform)
1. `pip install -r requirements.txt`

Other Options. 

1. Manually install the necessary packages on your global python isntallation (`numpy`, `matplotlib`, etc.)
1. Download a python distribution that already has the necessary requirements.
    *  Example: https://github.com/microsoft/coding-pack-for-python

## Running

* The project has launch configurations predefined for visual studio code. You can chose them using the debugging tab.
* Or, you can run things with `python -m linkage-simulator.<subpackage>` 