import bpy
import math
import mathutils
from mathutils import Euler

origRot = None
# print(origRot)
#
# rotMode =  bpy.context.scene.camera.rotation_mode
# bpy.context.scene.camera.rotation_mode = 'XYZ'
# bpy.context.scene.camera.rotation_euler = origRot
# bpy.context.scene.camera.rotation_mode = rotMode

class OBJECT_PT_camrot(bpy.types.Panel):
    bl_label = "Camera Rotation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.storecamrot", text="Store", icon="NONE")
        row = layout.row()
        row.operator("object.restorecamrot", text="Reset", icon="NONE")

class OBJECT_OT_camStoreRot(bpy.types.Operator):
    bl_label = "Store Camera Rotation Operator"
    bl_idname = "object.storecamrot"
    bl_description = "Stores Camera Rotation"

    def execute(self, context):
        global origRot
        self.report({'INFO'}, "Saving Camera Rotation")

        print ("storing...")
        print (origRot)
        origRot = bpy.context.scene.camera.rotation_euler.copy()
        print (origRot)

        return {'FINISHED'}

class OBJECT_OT_camRestoreRot(bpy.types.Operator):
    bl_label = "Restore Camera Rotation Operator"
    bl_idname = "object.restorecamrot"
    bl_description = "Restores Camera Rotation"

    def execute(self, context):
        global origRot
        self.report({'INFO'}, "Defaulting to Stored Camera Rotation")

        print ("restoring...")
        print (origRot)
        rotMode = bpy.context.scene.camera.rotation_mode
        bpy.context.scene.camera.rotation_mode = 'XYZ'
        bpy.context.scene.camera.rotation_euler = origRot
        bpy.context.scene.camera.rotation_mode = rotMode

        return {'FINISHED'}

classes = (
OBJECT_PT_camrot,
OBJECT_OT_camStoreRot,
OBJECT_OT_camRestoreRot,
)

def register():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
