#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import bpy
from mathutils import Vector, Matrix

handle = object()

# Triggers when an object is made active
subscribe_to = bpy.types.LayerObjects, "active"

def origin_to_bottom(ob):
    me = ob.data

    local_verts = [Vector(v[:]) for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.z = min(v.z for v in local_verts)

    me.transform(Matrix.Translation(-o))


def notify_test(context):
    if (context.object.type == 'MESH'
            and getattr(context.active_operator, "bl_idname", "").startswith("MESH_OT_primitive_")
            and context.mode == 'OBJECT'):
        print("Setting origin to bottom")
        origin_to_bottom(context.object)

bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=handle,
    args=(bpy.context,),
    notify=notify_test,
)

bpy.msgbus.publish_rna(key=subscribe_to)
