import pytest
from dwminstall import install_dep, clone_repos, change_terminal, compile, init

# Rember to remove Suckless directory along with .xinitrc and startx lines from .bash_profile
# Before each run to avoid errors

def test_install_dep():
    assert install_dep(bg=True, base_dwm=False, verbose=False) == True
    assert install_dep(bg="~/Pictures/fantasy.jpg", base_dwm=False, verbose=False) == True
    assert install_dep(bg=False, base_dwm=False, verbose=False) == True
    assert install_dep(bg=False, base_dwm=True, verbose=False) == True
    assert install_dep(bg=False, base_dwm=False, verbose=True) == True
    assert install_dep(bg=False, base_dwm=True, verbose=True) == True
    assert install_dep(bg=True, base_dwm=True, verbose=True) == True
    with pytest.raises(TypeError):
        install_dep()


# For this test only one assert must be ran at a time as 
# git will throw an error since directory will already exist
def test_clone_repos():
#    assert clone_repos() == 1
#    assert clone_repos(base_dwm=False, verbose=False) == 1
#    assert clone_repos(base_dwm=False, verbose=True) == 1
    assert clone_repos(base_dwm=True, verbose=False) == 2
#    assert clone_repos(base_dwm=True, verbose=True) == 2

# if return == 1 custom dwm installed with no problems and function executed flawlessly
# if return == 2 base dwm install was flawless 


# For this test up to two tests can be ran at a time if base_dwm=False
# is one of them else only one at a time as sed will not find text to change
def test_change_terminal():
#    assert change_terminal(base_dwm=True) == True
    assert change_terminal(base_dwm=False) == 0
#    assert change_terminal(verbose=True) == True
    assert change_terminal() == True

# if return == 0 Failed to change default terminal from /bin/sh to usr/local/bin/st
# if return == True Function executed flawlessly


def test_compile():
    assert compile(verbose=True) == True
    assert compile() == True

def test_init():
    assert init(custom_dwm=True, bg=False, powersaver_off=True, verbose=False) == True
    assert init(custom_dwm=True, bg=False, powersaver_off=False, verbose=False) == True
    assert init(custom_dwm=False, bg=False, powersaver_off=False, verbose=False) == True
    assert init(custom_dwm=True, bg="~/mntfs/fantasy.jpg", powersaver_off=False, verbose=False) == True
    assert init(custom_dwm=True, bg="~/mntfs/fantasy.jpg", powersaver_off=True, verbose=True) == True
    with pytest.raises(TypeError):
        init()
