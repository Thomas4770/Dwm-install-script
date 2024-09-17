# Dwm install script
## Video Demo: https://youtu.be/4ik-ZylPYpU
## Description
This is a Arch based installation and setup script for the Suckless dynamic window manager (dwm). This script allows you to install my version of dwm by default but allows you to install the standard dwm. This script will install necessary dependencies using pacman package manager. Download, install, and compile dwm. Add necessary lines to start X server and run dwm on login.

## Dependencies
* THIS SCRIPT WILL ONLY WORK ON ARCH BASED OPERATING SYSTEMS THAT USE THE PACMAN PACKAGE MANAGER.</br>
* The script must be run from a user's userspace with sudo privileges.</br>
* Python needs to be installed on the system</br>

To install python run:
```
$ sudo pacman -S python
```

## Installation
To install, simply clone this repository. No additional compilation is required. Run the script using Python:
```
$ git clone https://github.com/Thomas4770/Dwm-install-script
$ cd Dwm-install-script
$ python dwminstall.py [options]
```

## Usage
The script can be run with or without arguments to customize the installation process. Below are some usage examples:
### 1. Default installation (custom dwm):
```
$ python dwminstall.py
```
Installs the customized versions of <a href="https://github.com/N0pulse/dwm">dwm</a>, <a href="https://github.com/N0pulse/st">st</a>, and <a href="https://github.com/N0pulse/slstatus">slstatus</a>, and disables Display Power Management Signaling (DPMS).</br>

### 2. Run with sudo privileges:
```
$ sudo python dwminstall.py
```
Optionally run the script with elevated privileges.

### 3. Add a background image:
```
$ python dwminstall.py -b /path/to/background/image
```
The path to image can be the absolute path or the tilde path, /home/user/Pictures/image and ~/Pictures/image are both acceptable paths.</br>

### 4. Install default dwm:
```
$ python dwminstall.py -d
```
Installs the standard versions of <a href="https://dwm.suckless.org">dwm</a>, <a href="https://st.suckless.org">st</a>, <a href="https://git.suckless.org/dmenu">dmenu</a>, and <a href="https://git.suckless.org/slstatus">slstatus</a>.</br>

### 5. Automatic system reboot:
```
$ python dwminstall.py -r
```
Automatically reboots the system after the script completes.

### 6. Enable DPMS (default off):
```
$ python dwminstall.py -p
```
Enables Display Power Management Signaling, Screen will shut off after some amount of time.

## FAQ

Q1: Why does the script require sudo privileges?</br>
The script installs system-wide packages and makes changes to system configurations, which require root access. These actions include installing dependencies and modifying system files like .xinitrc.

Q2: Can I use this script on non-Arch-based systems?</br>
No, this script is specifically designed for Arch-based systems that use the pacman package manager. It may not work correctly on other distributions.

Q3: How can I revert the changes made by the script?</br>
To revert the changes, you can manually uninstall the packages using pacman and restore the original configuration files. However, it's recommended to back up your system before running the script.

Q4: What if the installation fails?</br>
If the script fails, it will print an error message and the error code. Check the error messages for clues and ensure all dependencies are correctly installed. You may also check for sufficient disk space and network connectivity.

Q5: Can I customize the installed dwm setup after installation?</br>
Yes, you can further customize the dwm setup by modifying the configuration files in the Suckless directory created in your home folder.

## Acknowledgments

This script leverages various open-source projects and contributions from the Suckless community. Special thanks to the developers and maintainers of <a href="https://dwm.suckless.org">dwm</a>, <a href="https://st.suckless.org">st</a>, <a href="https://git.suckless.org/dmenu">dmenu</a>, and <a href="https://git.suckless.org/slstatus">slstatus</a> for their invaluable tools and resources.</br>

Additionally, this script utilizes the following Python modules:
* argparse: For parsing command-line options and arguments.
* pathlib: For object-oriented filesystem paths.
* sys: For exiting the program on error.
* subprocess: For running system commands and managing input/output.
* time: For time-related functions such as sleep.

These modules are built into Python and provide the essential tools needed for the script to work.

## Security Considerations

* Sudo privileges: The script requires sudo access to install system-wide packages and make system changes. Be cautious when running scripts with elevated privileges, as they can modify critical system settings.

* Password prompts: Script will prompt user for password to run pacman and install needed dependencies and modify system configuration files, user password does not get stored in any variable or read by script, password prompt comes directly from pacman.

* System modifications: The script modifies system configuration files, primarily .xinitrc and .bash_profile. It's recommended to back up these files before running the script.

* Source code: The script clones repositories from GitHub, so ensure you trust the source or verify the contents of the repositories before proceeding.