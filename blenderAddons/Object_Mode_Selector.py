bl_info = {
"name": "Object Mode Selector",
"author":"Sanath Shetty K",
"version": (0, 1),
"blender": (3, 3, 0),
"location": "View3D",
"description": "Press TAB to switch modes",
"warning": "",
"wiki_url": "",
"category": "3D View",
}


import bpy
from bpy.types import Menu

class VIEW3D_MT_Mode_Selector_Pie(Menu):

    bl_label = "Select Mode"

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


addon_keymaps = []

def register():
    bpy.utils.register_class(VIEW3D_MT_Mode_Selector_Pie)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_Mode_Selector_Pie"
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_Mode_Selector_Pie)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_Mode_Selector_Pie")
