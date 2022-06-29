#!/usr/bin/python
'''
LIBRARIES
'''
import pathlib
from pathlib import Path
import os
import shutil
'''
VARIABLES
'''
#Path to file from location of this Python script, interval at which the file should be run
files = [
    "B738.a_AXP_4_FMOD_logic/B738.a_AXP_4_FMOD_logic.lua",
    "B738.a_fms/B738.a_fms.lua",
    "B738.anav/B738.anav.lua",
    "B738.calc/B738.calc.lua",
    "B738.glaresheild/B738.glaresheild.lua",
    "B738.LATLON/B738.LATLON.lua",
    "B738.tablet/B738.tablet.lua",
    "B738.zz.sim_cockpit/B738.zz.sim_cockpit.lua",
    "B738.ZZZ_AXP_5_added_logic_ULTIMATE/B738.ZZZ_AXP_5_added_logic_ULTIMATE.lua",
    ]
'''
PROGRAM LOGIC
'''
# Iterate through file list
for x in files:
    file = os.path.join(pathlib.Path(__file__).parent.resolve(), x)
    bakfile = Path(file+".bak")
    if bakfile.is_file():
        print("Restoring",file)
        shutil.copyfile(bakfile,file)
