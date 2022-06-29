# Zibo-737-Lua-Timer-Mod
Python3 scripts to modify the timing methodology in select Lua files of the popular Zibo mod for X-Plane 11.

&nbsp;

## Background

Zibo's modified 737, with it's complex systems, contains a lot of code in its Lua files to run the logic of, e.g. the FMC, tablet, audio system, etc.  
A lot of this code runs in Xlua flightloops before or after X-Plane's physics simulation. These flightloops are created by the parsing of "before_physics()" and "after_physics()" upon Lua file loading and are executed at framerate. This means that, at 75 FPS, the Lua code is evaluated 75 times a second.  
As the 737 runs a **lot** of stuff in these flightloops, the frame rate of the simulator will suffer accordingly as X-Plane (11) is very CPU dependent and these flightloops basically block everything.   
One remedy for this issue is setting the refresh rate of these flight loops at a fixed value to detach it from the simulator framerate by using XLua's timer functions. This means that the 737's Lua code will only be evaluated 20 times a second while the rest of X-Plane refreshes 90 times a second. This will free up a considerable amount of CPU cycles that can do other tasks in the meantime.
To achieve this fixed refresh rate, however, one must make the assumption that none of the code running in those Lua files is framerate critical. Such code would be, e.g. one that actively overrides core simulator datarefs or contains an active autopilot PID controller that outputs directly to control surfaces. After looking over the Lua code of Zibo's 737, non eof it struck me as framerate critical. And if the aircraft still works at X-Planes's minimum framerate of 20 FPS, the FMS, tablet and all other stuff controlled by the Lua files may just as well run at 20 FPS regardless of simulator framerate. Most of the framerate critical flight model and display drawing stuff is running in Zibo's C++ plugin anyway.  
To prevent Xlua and X-Plane from running the "before/after_physics()" functions as flight loops, it is sufficient to rename them. _Zibo_perfmod.py_ timer mod will do just that and add a call for the related timer function(s) to the end of the file. With these edits, the logic from the formar "before/after_physics()" functions is run as a timer and updated at the specified interval.

&nbsp;

## Effect

On my system the framerate increase after this mode is around 8%. Your mileage will vary.

&nbsp;

## Disclaimer

- **YOU ARE NOT ELIGIBLE FOR SUPPORT FROM ZIBO OR HIS TEAM IF YOU MOD THE 737'S SYSTEM FILES!   
DO NOT COMPLAIN TO ZIBO OR HIS TEAM IF YOU ENCOUNTER BUGS OR OTHER ABNORMAL BEHAVIOR CAUSED BY THE MODIFIED FILES!   
YOU'RE IN HOSTILE TERRITORY AND ON YOUR OWN IF YOU RUN THESE SCRIPTS!   
YOU HAVE BEEN WARNED!**
- Although the script creates a backup of thew original files and although there is a script to restore said backups, **MAKE A BACKUP OF YOUR _B737-800X/plugins/xlua/scripts_ FOLDER BEFORE TRYING THIS**
- I take no responsibility if usage of these scripts do mess up something outside of the _B737-800X/plugins/xlua/scripts_ folder.  
I've coded everything to the best of my Python knowledge, but stuff just finds a way to not work or break if you just don't expect it.
- Read and understand the "Functionality" and "FAQ" sections below before going on.

&nbsp;

## Functionality

### _Zibo_perfmod.py_
Contains a list of file paths and an associated numerical value (stored in an array). The file path states the file that is to be checked for modification while the numerical value is the update frequency (in seconds) with which the updated files will run.   
For each file path in the array, the script will read the file's content and check for the presence of a "function before_physics()" and "function after_physics()" string. If either string, or both of them, is found, the file is backed up with a _.bak_ extension.  
Then, the string "function before_physics()" or/and "function after_physics()" is replaced with "function timed_before_physics()" and "function timed_after_physics()" respectively. Commented "function before_physics()" or "function after_physics()" lines are ignored.  
At the end of the file "run_at_interval(timed_before_physics,0.05)" or "run_at_interval(timed_after_physics,0.05)" is added, referring to the modified function strings and containing the interval (in seconds) in which said function will be updated.   
Only then, the modified file content is being written to a Lua file.   
For verification of the result of this operation, see the "Verification" section below.

### _Zibo_perfmod_restorebackup.py_
This script checks the file paths stored in the array for the presence of a file with the same filename and a ".bak" extension.  
If backup file is found, it is copied and renamed to the name of the original Lua file.

&nbsp;

## Requirements
- X-Plane 11 or 12
- An installation of [Python 3.10.5 or newer](https://www.python.org/)
- A working installation of the [popular Zibo mod of X-Plane 11's Boeing 737-800](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/)

&nbsp;

## Installation

- Move _zibo_perfmod.py_ and _zibo_perfmod_restorebackup.py_ into _B737-800X/plugins/xlua/scripts_

&nbsp;

## Usage

- Open a terminal or console window in _B737-800X/plugins/xlua/scripts_ or open a terminal or console window and navigate to wherever your _B737-800X_ folder is located
- Run `python zibo_perfmod.py` to modify the 737's Lua files, creating a backup and modifying the Lua files specified in the script.

&nbsp;

## Verification

The file modifications were successful if:
- There is a copy of any modified Lua file with a _".bak"_ extension in any modified subfolder in _B737-800X/plugins/xlua/scripts_
and
- There is no more "before_physics()" and "after_physics()" in any modified Lua file (except those that were commented out int he first place).
and
- There is a "run_at_interval(timed_before_physics,0.05)" and/or "run_at_interval(timed_after_physics,0.05)" at the end of each modified Lua file.
- Framerate when using Zibo's 737 has increased a bit.

&nbsp;

## FAQ

Is this good for past or future releases of Zibo's 737?
- Most likely yes, but no guarantees.

There is a new incremental update for Zibo's 737, what do I do?
- Check if any Lua files were modified and in case of doubt, rerun the script.

What about completely new milestone new releases of Zibo's 737?
- As you're supposed to do a fresh install upon a new major release anyway, you'll have to rerun the script.

Can I use this for the X-Plane 12 release of Zibo's 737 as well?
- Most likely, yes.

Python doesn't work on my system. Help?
- Not my problem; contact Python support.

I wish to add or ecxlude files or change the update interval for a certain file.
- Edit _zibo_perfmod.py_.

Can I use this with other aircraft?
- Sure, if you adapt the list of files accordingly. Don't expect support from the original author or myself though.

My framerate has not increased after the modifications!
- Verify that the mods were applied correctly. In case of doubt, eveery system is different and will produce different results.

HELP!! I did not read the readme and now I have messed up my system with your scripts!!
- Tough luck. :)
