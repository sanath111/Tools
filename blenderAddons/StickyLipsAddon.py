import bpy
import math
from bpy.app.handlers import persistent


bl_info = {
    "name": "Sticky Lips",
    "description": "Sticky Lips Addon",
    "author": "Sanath",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "PROPERTIES > Object Properties > Sticky Lips",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Test"
}

import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


def enableStickyLips(self, context):
    if (bpy.context.scene.enable_sticky_lips == True):
        print("enabled.")
    else:
        print("disabled.")

class StickyLipsSettings(PropertyGroup):
    bpy.types.Scene.enable_sticky_lips = BoolProperty(name="", description="Enable Sticky Lips Addon", default=False, update=enableStickyLips)


class OBJECT_PT_stickylips(bpy.types.Panel):
    bl_label = "Sticky Lips"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw_header(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "enable_sticky_lips")

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
#        row.operator("object.enablestickylips", text="Enable Stickylips", icon="SHADING_SOLID")

        
#class OBJECT_OT_enablestickylips(bpy.types.Operator):
#    bl_label = "Sticky Lips Enable Operator"
#    bl_idname = "object.enablestickylips"
#    bl_description = "Sticky Lips Enable Operator"

#    def execute(self, context):
#        self.report({'INFO'}, "Enabling Sticky Lips")

#        print("enabling stickylips")

#        return {'FINISHED'}


def register():
    bpy.utils.register_class(StickyLipsSettings)
    bpy.utils.register_class(OBJECT_PT_stickylips)
#    bpy.utils.register_class(OBJECT_OT_enablestickylips)


def unregister():
    bpy.utils.unregister_class(StickyLipsSettings)
    bpy.utils.unregister_class(OBJECT_PT_stickylips)
#    bpy.utils.unregister_class(OBJECT_OT_enablestickylips)


if __name__ == "__main__":
    register()





#objData = bpy.data.objects['face_geo_clean']
#modShr1 = objData.modifiers["Shrinkwrap"]
#modShr2 = objData.modifiers["Shrinkwrap.001"]

#prevVal = 0.0
#prevRotVal = 0.0
#stickLimit = math.radians(5)


#def stickLips(val):
#    global prevVal
#    global objData
#    global modShr1
#    global modShr2

#    currVal = val
#    diff = currVal - prevVal
#    if (diff > 0):
#        #        print("True")
#        if (modShr1.show_viewport == False):
#            modShr1.show_viewport = True
#        if (modShr2.show_viewport == False):
#            modShr2.show_viewport = True

#        if (modShr1.show_render == False):
#            modShr1.show_render = True
#        if (modShr2.show_render == False):
#            modShr2.show_render = True

#    elif (diff < 0):
#        #        print("False")
#        if (currVal < stickLimit):
#            pass
#        else:
#            if (modShr1.show_viewport == True):
#                modShr1.show_viewport = False
#            if (modShr2.show_viewport == True):
#                modShr2.show_viewport = False

#            if (modShr1.show_render == True):
#                modShr1.show_render = False
#            if (modShr2.show_render == True):
#                modShr2.show_render = False
#    else:
#        pass

#    prevVal = currVal
#    return val


## Add function to driver_namespace.
#bpy.app.driver_namespace['stickLips'] = stickLips


#@persistent
#def load_handler(scene):
#    global prevRotVal
#    global objData
#    global modShr1
#    global modShr2

#    currRotVal = bpy.data.objects['rig'].pose.bones["c_jawbone.x"].rotation_euler[0]
#    diff = currRotVal - prevRotVal

#    if (diff > 0):
#        if (modShr1.show_in_editmode == False):
#            modShr1.show_in_editmode = True
#        if (modShr2.show_in_editmode == False):
#            modShr2.show_in_editmode = True

#    elif (diff < 0):
#        #        print("False")
#        if (currRotVal < stickLimit):
#            pass
#        else:
#            if (modShr1.show_in_editmode == True):
#                modShr1.show_in_editmode = False
#            if (modShr2.show_in_editmode == True):
#                modShr2.show_in_editmode = False
#    else:
#        pass

#    prevRotVal = currRotVal


#bpy.app.handlers.frame_change_post.clear()
#bpy.app.handlers.frame_change_post.append(load_handler)
#bpy.app.handlers.depsgraph_update_post.append(load_handler)
