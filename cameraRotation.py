bl_info = {
    "name": "Camera Rotation",
    "description": "Extends Rotate Canvas Addon",
    "author": "Sanath Shetty",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Sidebar > Item",
    "warning": "",
    "category": "3D View"
}

import bpy
import addon_utils

origRot = None

class OBJECT_PT_camrot(bpy.types.Panel):
    bl_label = "Camera Rotation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw_header(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "enable_cam_rot")

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.enabled = scene.enable_cam_rot
        row = layout.row()
        row.operator("object.store_cam_rot", text="Store", icon="NONE")
        row = layout.row()
        row.operator("object.reset_cam_rot", text="Reset", icon="NONE")


class OBJECT_OT_camStoreRot(bpy.types.Operator):
    bl_label = "Store Camera Rotation Operator"
    bl_idname = "object.store_cam_rot"
    bl_description = "Stores Camera Rotation"

    def execute(self, context):
        global origRot
        self.report({'INFO'}, "Saving Camera Rotation")
        print ("storing...")
        print (origRot)
        origRot = bpy.context.scene.camera.rotation_euler.copy()
        print (origRot)
        return {'FINISHED'}


class OBJECT_OT_camResetRot(bpy.types.Operator):
    bl_label = "Restore Camera Rotation Operator"
    bl_idname = "object.reset_cam_rot"
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


def toggleCamRot(self, context):
    global origRot
    bpy.ops.preferences.addon_disable(module="rotate_canvas-master")
    if (bpy.context.scene.enable_cam_rot == True):
        bpy.ops.preferences.addon_enable(module="rotate_canvas-master")
        origRot = bpy.context.scene.camera.rotation_euler.copy()
        print("enabled.")
    else:
        bpy.ops.preferences.addon_disable(module="rotate_canvas-master")
        rotMode = bpy.context.scene.camera.rotation_mode
        bpy.context.scene.camera.rotation_mode = 'XYZ'
        bpy.context.scene.camera.rotation_euler = origRot
        bpy.context.scene.camera.rotation_mode = rotMode
        print("disabled.")


class camRotProps(bpy.types.PropertyGroup):
    bpy.types.Scene.enable_cam_rot = bpy.props.BoolProperty(name="", description="Enable Camera Rotation Addon", default=False, update=toggleCamRot)


classes = (
OBJECT_PT_camrot,
OBJECT_OT_camStoreRot,
OBJECT_OT_camResetRot,
camRotProps,
)

def register():
    print("registering.")
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    addon_utils.disable("rotate_canvas-master", default_set=True)

def unregister():
    print("unregistering.")
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
