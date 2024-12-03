bl_info = {
    "name": "Shortcut Buttons",
    "author": "Sanath111",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Side Panel >Shortcuts",
    "description": "Adds a menu to control various shortcuts.",
    "category": "Shortcuts",
}


import bpy


class UndoRedoPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_undo_redo_panel"
    bl_label = "Undo/Redo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shortcuts'

    def draw(self, context):
        layout = self.layout
        
        if bpy.context.object.type == "GPENCIL":
            column = layout.column()
            op = column.operator("object.mode_set", text="Object Mode", icon="OBJECT_DATAMODE")
            op.mode = "OBJECT"
            op = column.operator("object.mode_set", text="Edit Mode", icon="EDITMODE_HLT")
            op.mode = "EDIT_GPENCIL"
            op = column.operator("object.mode_set", text="Sculpt Mode", icon="SCULPTMODE_HLT")
            op.mode = "SCULPT_GPENCIL"
            op = column.operator("object.mode_set", text="Draw Mode", icon="GREASEPENCIL")
            op.mode = "PAINT_GPENCIL"
        
        if bpy.context.object.type == "MESH":
            column = layout.column()
            op = column.operator("object.mode_set", text="Object Mode", icon="OBJECT_DATAMODE")
            op.mode = "OBJECT"
            op = column.operator("object.mode_set", text="Edit Mode", icon="EDITMODE_HLT")
            op.mode = "EDIT"
            op = column.operator("object.mode_set", text="Sculpt Mode", icon="SCULPTMODE_HLT")
            op.mode = "SCULPT"
        
        layout.separator()
        
        column = layout.column()
        column.operator("transform.translate", text="Move", icon="EVENT_G")
        column.operator("transform.rotate", text="Rotate", icon="EVENT_R")
        column.operator("transform.resize", text="Scale", icon="EVENT_S")
        
        layout.separator()
        
        column = layout.column()
        column.operator("gpencil.delete", text="Delete", icon="EVENT_X")
        
        layout.separator()
        
        row = layout.row()
        row.operator("gpencil.copy", text="Copy", icon="COPYDOWN")
        row.operator("gpencil.paste", text="Paste", icon="PASTEDOWN")
        
        layout.separator()
        
        row = layout.row()
        row.operator("ed.undo", text="Undo", icon="LOOP_BACK")
        row.operator("ed.redo", text="Redo", icon="LOOP_FORWARDS")
        
        layout.separator()
        
        column = layout.column()
        brush = bpy.context.tool_settings.gpencil_paint.brush
        column.prop(brush.gpencil_settings, "use_settings_stabilizer", text="Stabilize")


classes = (
    UndoRedoPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()