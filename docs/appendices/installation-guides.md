---
title: Installation Guides
sidebar_position: 2
description: Step-by-step setup instructions for all tools and frameworks
---

# Appendix A: Installation Guides

This appendix provides comprehensive installation guides for all tools and frameworks referenced in the textbook.

## Table of Contents
1. [Docusaurus Setup](#docusaurus-setup)
2. [ROS 2 Installation](#ros-2-installation)
3. [Gazebo Simulation](#gazebo-simulation)
4. [NVIDIA Isaac Setup](#nvidia-isaac-setup)
5. [Python Development Environment](#python-development-environment)
6. [Git and Version Control](#git-and-version-control)

## Docusaurus Setup

### Prerequisites
- Node.js (version 18.0 or higher)
- npm or yarn package manager

### Installation Steps
1. Install Node.js from [nodejs.org](https://nodejs.org/)
2. Verify installation:
   ```bash
   node --version
   npm --version
   ```
3. Create a new Docusaurus project:
   ```bash
   npx create-docusaurus@latest my-website classic
   ```
4. Navigate to your project directory:
   ```bash
   cd my-website
   ```
5. Start the development server:
   ```bash
   npm run start
   ```

### Configuration
- Edit `docusaurus.config.js` to customize your site
- Modify `sidebars.js` to organize documentation
- Add content to the `docs/` directory

## ROS 2 Installation

### Supported Platforms
- Ubuntu 22.04 (Jammy Jellyfish) - Recommended
- Ubuntu 20.04 (Focal Fossa)
- Windows 10/11 (via WSL2)
- macOS (limited support)

### Ubuntu Installation
1. Set locale:
   ```bash
   locale  # check for UTF-8
   sudo apt update && sudo apt install locales
   sudo locale-gen en_US.UTF-8
   ```
2. Add ROS 2 apt repository:
   ```bash
   sudo apt update && sudo apt install curl gnupg lsb-release
   curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```
3. Install ROS 2 packages:
   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop
   ```
4. Environment setup:
   ```bash
   source /opt/ros/humble/setup.bash
   ```
5. Install colcon for building packages:
   ```bash
   sudo apt install python3-colcon-common-extensions
   ```

## Gazebo Simulation

### Gazebo Garden Installation
1. Add Gazebo repository:
   ```bash
   sudo apt install wget lsb-release gnupg
   sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /tmp/gazebo.gpg
   sudo gpg --dearmor -o /usr/share/keyrings/gazebo-archive.gpg /tmp/gazebo.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gazebo-archive.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
   ```
2. Install Gazebo:
   ```bash
   sudo apt update
   sudo apt install gz-garden
   ```
3. Test installation:
   ```bash
   gz sim
   ```

## NVIDIA Isaac Setup

### Prerequisites
- NVIDIA GPU with CUDA support (Compute Capability 6.0 or higher)
- CUDA 11.8 or higher
- NVIDIA drivers (520 or higher)

### Isaac Sim Installation
1. Install NVIDIA Omniverse:
   - Download from NVIDIA Developer website
   - Follow installation instructions for your platform
2. Install Isaac Sim extension:
   - Launch Omniverse Create or Isaac Sim
   - Install Isaac Sim extension from Extensions Manager
3. Install Isaac ROS packages:
   ```bash
   sudo apt update
   sudo apt install ros-humble-isaac-ros-*  # Install all Isaac ROS packages
   ```

## Python Development Environment

### Virtual Environment Setup
1. Install Python 3.8 or higher
2. Install venv module:
   ```bash
   sudo apt install python3-venv  # Ubuntu
   ```
3. Create virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   # or
   myenv\Scripts\activate  # Windows
   ```
4. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

### Essential Python Packages
```bash
pip install numpy scipy matplotlib pandas jupyter notebook
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install tensorflow  # if needed
pip install opencv-python  # Computer vision
pip install openai  # If using OpenAI API
pip install qdrant-client  # For vector database
pip install psycopg2-binary  # For PostgreSQL
```

## Git and Version Control

### Git Installation
1. Install Git:
   ```bash
   sudo apt install git  # Ubuntu
   # or download from https://git-scm.com/
   ```
2. Configure Git:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### Basic Git Workflow
1. Clone a repository:
   ```bash
   git clone https://github.com/username/repository.git
   ```
2. Create a branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make changes and commit:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
4. Push changes:
   ```bash
   git push origin feature-branch
   ```

## Troubleshooting Common Issues

### ROS 2 Issues
- **Package not found**: Make sure to source ROS 2 environment:
  ```bash
  source /opt/ros/humble/setup.bash
  ```
- **Permission errors**: Use proper workspace setup and avoid running as root

### Python Environment Issues
- **Package conflicts**: Use virtual environments to isolate dependencies
- **CUDA not detected**: Verify CUDA installation and PyTorch installation with CUDA support

### Simulation Issues
- **Graphics errors**: Ensure proper GPU drivers are installed
- **Performance issues**: Close other applications to free up resources

## Additional Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Gazebo Documentation](https://gazebosim.org/docs)
- [NVIDIA Isaac Documentation](https://nvidia-isaac-ros.github.io/)

For platform-specific installation guides or troubleshooting, refer to the official documentation for each tool.