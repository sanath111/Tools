#import bpy
#import math
#from bpy.app.handlers import persistent

#prevRotVal = 0.0
#objData = bpy.data.objects['face_geo_clean']
#modShr1 = objData.modifiers["Shrinkwrap"]
#modShr2 = objData.modifiers["Shrinkwrap.001"]

#@persistent
#def load_handler(scene):
#    global prevRotVal
#    global objData
#    global modShr1
#    global modShr2

#    currRotVal = bpy.data.objects['rig'].pose.bones["c_jawbone.x"].rotation_euler[0]
#    diff = currRotVal - prevRotVal

#    if (diff<0):
#        print("True")
#        if (modShr1.show_viewport == False):
#            modShr1.show_viewport = True
##            modShr1.keyframe_insert('show_viewport')
#        if (modShr2.show_viewport == False):
#            modShr2.show_viewport = True
##            modShr2.keyframe_insert('show_viewport')
#        if (modShr1.show_render == False):
#            modShr1.show_render = True
#        if (modShr2.show_render == False):
#            modShr2.show_render = True
#    
#    elif (diff>0):
#        print("False")
#        if (currRotVal<0.09):
#            pass
#        else:
#            if (modShr1.show_viewport == True):
#                modShr1.show_viewport = False
##                modShr1.keyframe_insert('show_viewport')
#            if (modShr2.show_viewport == True):
#                modShr2.show_viewport = False
##                modShr2.keyframe_insert('show_viewport')
#            if (modShr1.show_render == True):
#                modShr1.show_render = False
#            if (modShr2.show_render == True):
#                modShr2.show_render = False

#    else:
#        pass

#    prevRotVal = currRotVal


#bpy.app.handlers.depsgraph_update_post.clear()
#bpy.app.handlers.depsgraph_update_post.append(load_handler)

import bpy
#import bpy
#import math
from bpy.app.handlers import persistent

#prevRotVal = 0.0
objData = bpy.data.objects['face_geo_clean']
modShr1 = objData.modifiers["Shrinkwrap"]
modShr2 = objData.modifiers["Shrinkwrap.001"]

#@persistent
#def load_handler(scene):
#    global prevRotVal

prevVal = 0.0

def myFunc(val):
    global prevVal
    global objData
    global modShr1
    global modShr2
    
    currVal = val
    diff = currVal - prevVal
    if (diff>0):
        print("True")
        if (modShr1.show_viewport == False):
            modShr1.show_viewport = True
#            modShr1.keyframe_insert('show_viewport')
        if (modShr2.show_viewport == False):
            modShr2.show_viewport = True
#            modShr2.keyframe_insert('show_viewport')
        if (modShr1.show_render == False):
            modShr1.show_render = True
        if (modShr2.show_render == False):
            modShr2.show_render = True
    
    elif (diff<0):
        print("False")
        if (currVal<0.09):
            pass
        else:
            if (modShr1.show_viewport == True):
                modShr1.show_viewport = False
#                modShr1.keyframe_insert('show_viewport')
            if (modShr2.show_viewport == True):
                modShr2.show_viewport = False
#                modShr2.keyframe_insert('show_viewport')
            if (modShr1.show_render == True):
                modShr1.show_render = False
            if (modShr2.show_render == True):
                modShr2.show_render = False

    else:
        pass
    prevVal = currVal
    return val

# Add function to driver_namespace.
bpy.app.driver_namespace['myFunc'] = myFunc
