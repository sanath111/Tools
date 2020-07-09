#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import bpy

class OBJECT_PT_shadeit(bpy.types.Panel):
    bl_label = "Shade It"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.shadesolid", text="Solid", icon="SHADING_SOLID")


class OBJECT_OT_shadeSolid(bpy.types.Operator):
    bl_label = "Shade Solid Operator"
    bl_idname = "object.shadesolid"
    bl_description = "Shade Solid"

    def execute(self, context):
        self.report({'INFO'}, "Shading Solid")

        my_areas = bpy.context.workspace.screens[0].areas
        my_shading = 'SOLID'
        my_lighting = 'MATCAP'
        my_color = 'RANDOM'
        my_cavity_type = 'BOTH'

        for area in my_areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = my_shading
                    space.shading.light = my_lighting
                    space.shading.color_type = my_color
                    space.shading.show_shadows = True
                    space.shading.show_cavity = True
                    space.shading.cavity_type = my_cavity_type

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_shadeit)
    bpy.utils.register_class(OBJECT_OT_shadeSolid)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_shadeit)
    bpy.utils.unregister_class(OBJECT_OT_shadeSolid)


if __name__ == "__main__":
    register()
