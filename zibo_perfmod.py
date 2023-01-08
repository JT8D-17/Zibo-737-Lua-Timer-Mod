#!/usr/bin/python
'''
LIBRARIES
'''
import pathlib,os,shutil,re
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
    score = 0
    newdata = None
    # Find physics functions in the files and make a backup if any are found
    if re.findall('^\sfunction before_physics',filedata,re.MULTILINE) or re.findall('^\sfunction after_physics',filedata,re.MULTILINE):
        shutil.copyfile(file, file+".bak")
        print("\nPhysics found in "+x[0]+", making a backup.")
    # Change name of before_physics() function, if it's present
    if re.findall('^\sfunction before_physics',filedata,re.MULTILINE):
        newdata = filedata.replace("function before_physics()","function timed_before_physics()")
        newdata = newdata + "\nrun_at_interval(timed_before_physics,"+str(x[1])+")"
        filedata = newdata # Write back to filedata
        print("Found and modified before_physics() in "+x[0])
    # Change name of after_physics() function, if it's present
    if re.findall('^\sfunction after_physics',filedata,re.MULTILINE):
        newdata = filedata.replace("function after_physics()","function timed_after_physics()")
        newdata = newdata + "\nrun_at_interval(timed_after_physics,"+str(x[1])+")"
        print("Found and modified after_physics() in "+x[0])
    if newdata is not None:
        f = open(file,'w')
        f.write(newdata)
        f.close()
        print("Finished modification of "+x[0]+"\n")
