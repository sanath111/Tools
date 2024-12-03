import bpy
import sys

bpy.context.preferences.filepaths.use_relative_paths = False
bpy.context.preferences.filepaths.save_version = 0
bpy.context.preferences.filepaths.use_scripts_auto_execute = True
bpy.context.preferences.filepaths.temporary_directory = "/crap/LOCAL.crap"

app_version = list(bpy.app.version)
print(app_version)

try:
  bpy.ops.preferences.addon_enable(module="bl_ext.blender_org.node_wrangler")
  print("node wrangler enabled")
except:
  print(sys.exc_info())

