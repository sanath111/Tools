bl_info = {
    "name": "Object Mode Pie Menu",
    "description": "Adds a pie menu for switching object modes",
    "author": "Sanath",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D",
    "category": "Object"
}

import bpy
from bpy.types import Menu, AddonPreferences
from bpy.props import StringProperty, BoolProperty

class ObjectModePie(Menu):
    bl_idname = "OBJECT_MT_object_mode_pie"
    bl_label = "Object Mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        
        if bpy.context.object.type == "GPENCIL":
            op = pie.operator("object.mode_set", text="Object Mode", icon="OBJECT_DATAMODE")
            op.mode = "OBJECT"
            op = pie.operator("object.mode_set", text="Edit Mode", icon="EDITMODE_HLT")
            op.mode = "EDIT_GPENCIL"
            op = pie.operator("object.mode_set", text="Sculpt Mode", icon="SCULPTMODE_HLT")
            op.mode = "SCULPT_GPENCIL"
            op = pie.operator("object.mode_set", text="Draw Mode", icon="GREASEPENCIL")
            op.mode = "PAINT_GPENCIL"
        else:
            pie.operator_enum("object.mode_set", "mode")

class MyAddonPreferences(AddonPreferences):
    bl_idname = __name__

    pie_menu_key: StringProperty(
        name="Key",
        description="Keyboard Key",
        default="TAB"
    )
    
    pie_menu_ctrl: BoolProperty(
        name="Ctrl",
        description="Set Ctrl",
        default=True
    )
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "pie_menu_ctrl")
        row.prop(self, "pie_menu_key")
        
addon_keymaps = []

def register():
    bpy.utils.register_class(ObjectModePie)
    bpy.utils.register_class(MyAddonPreferences)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    if bpy.context.preferences.addons[__name__].preferences.pie_menu_ctrl:
        kmi = km.keymap_items.new('wm.call_menu_pie', bpy.context.preferences.addons[__name__].preferences.pie_menu_key, 'PRESS', ctrl=True)
        bpy.context.window_manager.keyconfigs.active.keymaps['Object Non-modal'].keymap_items['view3d.object_mode_pie_or_toggle'].active = False
    else:
        kmi = km.keymap_items.new('wm.call_menu_pie', bpy.context.preferences.addons[__name__].preferences.pie_menu_key, 'PRESS')
        bpy.context.window_manager.keyconfigs.active.keymaps['Object Non-modal'].keymap_items['view3d.object_mode_pie_or_toggle'].active = True
    kmi.properties.name = "OBJECT_MT_object_mode_pie"
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(ObjectModePie)
    bpy.utils.unregister_class(MyAddonPreferences)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    
    bpy.context.window_manager.keyconfigs.active.keymaps['Object Non-modal'].keymap_items['view3d.object_mode_pie_or_toggle'].active = True

    
if __name__ == "__main__":
    register()
