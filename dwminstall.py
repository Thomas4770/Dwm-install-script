import argparse
import pathlib
import sys
import subprocess
from time import sleep


def main():
    parse = argparse.ArgumentParser(
        description="Download and installs dwm a suckless window manager."
    )
    parse.add_argument(
        "-b",
        "--background",
        metavar="PATH",
        help="File path of image to add as a background",
        type=str,
    )
    parse.add_argument(
        "-d",
        "--default-dwm",
        action="store_true",
        help="If flag is set, default dwm will be installed instead of a custom dwm",
    )
    parse.add_argument(
        "-r",
        "--reboot",
        action="store_true",
        help="If flag is set, system will automatically reboot after script is done executing",
    )
    parse.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="If flag set, add a higher level of verbosity (by default verbose level already high)",
    )
    parse.add_argument(
        "-p",
        "--powersaver",
        action="store_false",
        help="If flag is set, enable powersaver mode (by default it's set to off)",
    )
    args = parse.parse_args()

    inst = install_dep(args.background, args.default_dwm, args.verbose)
    status = clone_repos(args.default_dwm, args.verbose)

    st = False
    if status == 2:
        st = change_terminal(verbose=args.verbose)

    cmp = compile(args.verbose)
    initstat = init(status, args.background, args.powersaver, args.verbose)

    if args.verbose:
        print("---------------------------------------------------------------------")
        print("installing dependencies function return:", inst)
        print("return code for cloning repos:", status)
        print("Return code for change terminal:", st)
        print("Return code for compile:", cmp)
        print("Return code for init:", initstat)

    print("---------------------------------------------------------------------")
    try:
        if args.reboot:
            print("SYSTEM WILL REBOOT IN")
            seconds = 5
            for _ in range(seconds):
                print(seconds, "." * seconds)
                seconds -= 1
                sleep(1)
            print("SYSTEM REBOOTING NOW")
            sleep(0.5)
            subprocess.run(["sudo", "reboot"], check=True)
    except (subprocess.SubprocessError, BaseException, KeyboardInterrupt):
        print("Error: Failed to restart system")
        sys.exit(1)

    print("REBOOT SYSTEM OR LOG OUT OF USER FOR CHANGES TO TAKE EFFECT!!")


def install_dep(bg, base_dwm=False, verbose=False, autoconfirm=True):
    # Required dependencies
    pack_dep = [
        "base-devel",
        "git",
        "vim",
        "xorg-server",
        "xorg-xinit",
        "xorg-xset",
        "libx11",
        "libxinerama",
        "libxft",
        "webkit2gtk",
    ]
    # Pacman install command
    pacman_args = ["pacman", "-Sy"]

    if autoconfirm:
        pacman_args.append("--noconfirm")

    # Check for optional dependency flags
    if bg:
        pack_dep.append("feh")

    if not base_dwm:
        pack_dep += ["xcompmgr", "ttf-font-awesome", "pamixer"]

    # Execute command and install packages
    try:
        p1 = subprocess.run(["sudo"] + pacman_args + pack_dep)
    except (subprocess.SubprocessError, BaseException, KeyboardInterrupt) as error:
        print(error)
        sys.exit(1337)

    # Check if command executed flawlessly
    if p1.returncode != 0:
        print("An error occurred: failed to download system dependencies")
        if verbose:
            print(f"Error code: {p1.returncode}")
        sys.exit(p1.returncode)

    # Return True if Success
    return True


def clone_repos(base_dwm=False, verbose=False):
    # Set git and fonts link based on argument passed
    if base_dwm:
        git_repos = [
            "https://git.suckless.org/dwm",
            "https://git.suckless.org/slstatus",
            "https://git.suckless.org/st",
            "https://git.suckless.org/dmenu",
        ]
    else:
        git_repos = [
            "https://github.com/N0pulse/dwm",
            "https://github.com/N0pulse/slstatus",
            "https://github.com/N0pulse/st",
            "https://git.suckless.org/dmenu",
        ]

    if not pathlib.Path(f"{pathlib.Path.home()}/Suckless").exists():
        # Make Suckless folder in user's home directory and check for success
        try:
            p1 = subprocess.run(["mkdir", "Suckless"], cwd=pathlib.Path.home())
        except (subprocess.SubprocessError, BaseException, KeyboardInterrupt) as error:
            print(error)
            sys.exit(1337)
        if p1.returncode != 0:
            print(
                "An error occurred: failed to make Suckless folder in user's home directory"
            )
            if verbose:
                print(f"Error code: {p1.returncode}")
            sys.exit(p1.returncode)

    # clone each git repository to the Suckless folder and check for success
    for link in git_repos:
        git_link = [link]
        try:
            p2 = subprocess.run(
                ["git", "clone"] + git_link, cwd=f"{pathlib.Path.home()}/Suckless"
            )
        except (subprocess.SubprocessError, BaseException, KeyboardInterrupt) as error:
            print(error)
            sys.exit(1337)
        if p2.returncode != 0:
            print("An error occurred: failed to clone git repository")
            if verbose:
                print(f"Error code: {p2.returncode}")
            sys.exit(p2.returncode)

    # Return 2 if base suckless repos were downloaded successfully else return 1
    if base_dwm:
        return 2
    return 1


def change_terminal(base_dwm=True, verbose=False):
    # If a custom dwm was downloaded return 0
    if not base_dwm:
        return 0

    # Replace default shell with st using sed then write it to config.def.h using buffer
    try:
        p1 = subprocess.run(
            r"sed 's/bin\/sh/usr\/local\/bin\/st/' config.def.h > config.def && cp config.def config.def.h && rm config.def",
            shell=True,
            cwd=f"{pathlib.Path.home()}/Suckless/dwm",
        )
    except (subprocess.SubprocessError, BaseException, KeyboardInterrupt) as error:
        print(error)
        return 0
    if p1.returncode != 0:
        print("An error occurred: Failed to change terminal from default shell to st")
        if verbose:
            print(f"Error code: {p1.returncode}")
        return 0

    # Return True if success
    return True


def compile(verbose=False):
    # Programs to compile
    directories = ["st", "dmenu", "slstatus", "dwm"]

    # Compile each program if error terminate script
    for dir in directories:
        try:
            p1 = subprocess.run(
                ["sudo", "make", "clean", "install"],
                cwd=f"{pathlib.Path.home()}/Suckless/{dir}",
            )
        except (subprocess.SubprocessError, BaseException, KeyboardInterrupt) as error:
            print(error)
            sys.exit(1337)
        if p1.returncode != 0:
            print(f"An error occurred: Failed to compile {dir}")
            if verbose:
                print(f"Error code: {p1.returncode}")
            sys.exit(p1.returncode)

    # Return True if success
    return True


def init(custom_dwm, bg=False, powersaver_off=True, verbose=False):
    # open or make .xinitrc and add neccessary commands
    try:
        with open(f"{pathlib.Path.home()}/.xinitrc", "a") as file:
            # Expecting output of clone_repos function
            if custom_dwm != 2:
                file.write("xcompmgr &\n")
            # Turn off power saver mode which turns screen off after 5min inactivity
            if powersaver_off:
                file.write("xset s off -dpms &\n")
            # If bg contains something and the first character is ~ replace it with users home path
            if bg:
                if "~" in bg[0]:
                    bg = str(pathlib.Path.home()) + bg[1:]
                # If bg path exists add to .xinitrc else print error message
                if pathlib.Path(bg).exists():
                    file.write(f"feh --bg-fill {bg} &\n")
                else:
                    print("Error: Failed to add background, File not found.")

            # Add neccessary commands for dwm and slstatus
            file.write("exec dwm &\nslstatus")
    except OSError as error:
        print("Failed to open .xinitrc file")
        if verbose:
            print(f"Error: {error}")
        sys.exit(1337)

    # Add startx to .bash_profile
    try:
        with open(f"{pathlib.Path.home()}/.bash_profile", "a") as file:
            file.write("\nstartx")
    except OSError as error:
        print("Failed to open .bash_profile file")
        if verbose:
            print(f"Error: {error}")
        sys.exit(1337)

    # return True if success
    return True


if __name__ == "__main__":
    main()
