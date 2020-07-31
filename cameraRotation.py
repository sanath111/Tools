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
    if (bpy.context.scene.enable_cam_rot == True):
        origRot = bpy.context.scene.camera.rotation_euler.copy()
        bpy.ops.preferences.addon_enable(module="rotate_canvas-master")
        print("enabled.")
    else:
        rotMode = bpy.context.scene.camera.rotation_mode
        bpy.context.scene.camera.rotation_mode = 'XYZ'
        bpy.context.scene.camera.rotation_euler = origRot
        bpy.context.scene.camera.rotation_mode = rotMode
        bpy.ops.preferences.addon_disable(module="rotate_canvas-master")
        print("disabled.")


class camRotProps(bpy.types.PropertyGroup):
    bpy.types.Scene.enable_cam_rot = bpy.props.BoolProperty(name="", description="Enable Camera Rotation Addon", default=False, update=toggleCamRot)


classes = (
OBJECT_PT_camrot,
OBJECT_OT_camStoreRot,
OBJECT_OT_camResetRot,
camRotProps,
)

addon_keymaps = []


def register():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)

    addon = bpy.context.window_manager.keyconfigs.addon
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.get("3D View")
    if not km:
        km = addon.keymaps.new(name="3D View", space_type="VIEW_3D")  # valid only in 3d view

    if 'view3d.rotate_canvas' not in km.keymap_items:
        km = addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('object.reset_cam_rot',
                                  type="R", value="PRESS", alt=True, ctrl=True,
                                  shift=False, any=False)
        addon_keymaps.append(km)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()

