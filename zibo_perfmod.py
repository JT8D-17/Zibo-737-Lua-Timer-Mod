#!/usr/bin/python
'''
LIBRARIES
'''
import pathlib
import os
import shutil
'''
VARIABLES
'''
#Path to file from location of this Python script, interval at which the file should be run
files = [
    ("B738.a_AXP_4_FMOD_logic/B738.a_AXP_4_FMOD_logic.lua",0.05),
    ("B738.a_fms/B738.a_fms.lua",0.05),
    ("B738.anav/B738.anav.lua",0.05),
    ("B738.calc/B738.calc.lua",0.05),
    ("B738.glaresheild/B738.glaresheild.lua",0.05),
    ("B738.LATLON/B738.LATLON.lua",0.05),
    ("B738.tablet/B738.tablet.lua",0.05),
    ("B738.zz.sim_cockpit/B738.zz.sim_cockpit.lua",0.05),
    ("B738.ZZZ_AXP_5_added_logic_ULTIMATE/B738.ZZZ_AXP_5_added_logic_ULTIMATE.lua",0.05),
    ]
'''
PROGRAM LOGIC
'''
# Iterate through file list
for x in files:
    file = os.path.join(pathlib.Path(__file__).parent.resolve(), x[0])
    f = open(file,'r')
    filedata = f.read()
    f.close()
    # Make a backup of the file if it contains any physics functions
    if 'function before_physics()' or "function after_physics()" in filedata:
        shutil.copyfile(file, file+".bak")
        print("Modification process starting; making backup of "+x[0])
    # Change name of before_physics() function, if it's present
    if 'function before_physics()' in filedata:
        newdata = filedata.replace("function before_physics()","function timed_before_physics()")
        newdata = newdata + "\nrun_at_interval(timed_before_physics,"+str(x[1])+")"
        print("Found and modified before_physics() in "+x[0])
    # Change name of after_physics() function, if it's present
    if "function after_physics()" in filedata:
        newdata = filedata.replace("function after_physics()","function timed_after_physics()")
        newdata = newdata + "\nrun_at_interval(timed_after_physics,"+str(x[1])+")"
        print("Found and modified after_physics() in "+x[0])
    f = open(file,'w')
    f.write(newdata)
    f.close()
    print("Finished modification of "+x[0]+"\n")
