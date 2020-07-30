import bpy
import math
from bpy.app.handlers import persistent

objData = bpy.data.objects['face_geo_clean']
modShr1 = objData.modifiers["Shrinkwrap"]
modShr2 = objData.modifiers["Shrinkwrap.001"]

prevVal = 0.0
prevRotVal = 0.0
stickLimit = math.radians(5)


def stickLips(val):
    global prevVal
    global objData
    global modShr1
    global modShr2

    currVal = val
    diff = currVal - prevVal
    if (diff > 0):
        #        print("True")
        if (modShr1.show_viewport == False):
            modShr1.show_viewport = True
        if (modShr2.show_viewport == False):
            modShr2.show_viewport = True

        if (modShr1.show_render == False):
            modShr1.show_render = True
        if (modShr2.show_render == False):
            modShr2.show_render = True

    elif (diff < 0):
        #        print("False")
        if (currVal < stickLimit):
            pass
        else:
            if (modShr1.show_viewport == True):
                modShr1.show_viewport = False
            if (modShr2.show_viewport == True):
                modShr2.show_viewport = False

            if (modShr1.show_render == True):
                modShr1.show_render = False
            if (modShr2.show_render == True):
                modShr2.show_render = False
    else:
        pass

    prevVal = currVal
    return val


# Add function to driver_namespace.
bpy.app.driver_namespace['stickLips'] = stickLips


@persistent
def load_handler(scene):
    global prevRotVal
    global objData
    global modShr1
    global modShr2

    currRotVal = bpy.data.objects['rig'].pose.bones["c_jawbone.x"].rotation_euler[0]
    diff = currRotVal - prevRotVal

    if (diff > 0):
        if (modShr1.show_in_editmode == False):
            modShr1.show_in_editmode = True
        if (modShr2.show_in_editmode == False):
            modShr2.show_in_editmode = True

    elif (diff < 0):
        #        print("False")
        if (currRotVal < stickLimit):
            pass
        else:
            if (modShr1.show_in_editmode == True):
                modShr1.show_in_editmode = False
            if (modShr2.show_in_editmode == True):
                modShr2.show_in_editmode = False
    else:
        pass

    prevRotVal = currRotVal


bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(load_handler)
bpy.app.handlers.depsgraph_update_post.append(load_handler)
