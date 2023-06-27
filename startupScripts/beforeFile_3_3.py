import bpy
import addon_utils
import sys
bpy.context.preferences.filepaths.use_relative_paths= False

def isLessThanEqualVersion(ver):
  app_version = list(bpy.app.version)
  if(type(ver) == str):
    ver_list = [int(x) for x in ver.split(".")]
    if(ver_list[0] >= app_version[0]):
      print(ver_list[0],app_version[0])
      if (ver_list[1] >= app_version[1]):
        print(ver_list[1], app_version[1])
        if (ver_list[2] >= app_version[2]):
          print(ver_list[2], app_version[2])
          return True
    return False


if(isLessThanEqualVersion("2.78.0")):
  bpy.context.preferences.filepaths.use_load_ui = False
  print("NOT LOADING UI")
bpy.context.preferences.filepaths.save_version = 0
bpy.context.preferences.filepaths.use_scripts_auto_execute = True
bpy.context.preferences.filepaths.temporary_directory = "/crap/LOCAL.crap"


if(isLessThanEqualVersion("2.78.0")):
  try:
    addon_utils.disable("bone_selection_groups")
  except:
    print(sys.exc_info())

  try:
    addon_utils.enable("bone_selection_groups")
    print("bone_selection_groups enabled")
  except:
    print(sys.exc_info())

else:
  try:
    addon_utils.disable("bone_selection_sets")
  except:
    print(sys.exc_info())

  try:
    addon_utils.enable("bone_selection_sets")
    print("bone_selection_sets enabled")
  except:
    print(sys.exc_info())
