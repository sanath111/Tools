import bpy
import sys
import os
import re
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.system_rotation = 'DEGREES'
bpy.ops.file.make_paths_absolute()
bpy.context.scene.render.fps = 24
bpy.context.scene.render.fps_base = 1
bpy.context.scene.keying_sets_all.active = bpy.context.scene.keying_sets_all['LocRotScale']
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.progressive = 'BRANCHED_PATH'
bpy.context.scene.cycles.preview_aa_samples = 1
bpy.context.scene.display_settings.display_device = 'sRGB'
bpy.context.scene.view_settings.view_transform = 'Standard'


rbhus_isRendering = False

if("rbhus_isRendering" in os.environ):
  rbhus_isRendering = True

def getAssFileName():
  fileName = ""
  if("rp_assets_assName" in os.environ):
    if(str(os.environ['rp_assets_assName']) != "default"):
      fileName = str(os.environ['rp_assets_assName'])
  if(not re.search("^default$",str(os.environ['rp_assets_sequenceName']))):
    if(not re.search("^default$",str(os.environ['rp_assets_sceneName']))):
      if(fileName):
        fileName = fileName +"_"+ str(os.environ['rp_assets_sequenceName']) +"_" + str(os.environ['rp_assets_sceneName'])
      else:
        fileName = str(os.environ['rp_assets_sequenceName']) +"_" + str(os.environ['rp_assets_sceneName'])
    else:
      if(fileName):
        fileName = fileName +"_"+ str(os.environ['rp_assets_sequenceName'])
      else:
        fileName = str(os.environ['rp_assets_sequenceName'])
  if(not re.search("^default$",str(os.environ['rp_assets_stageType']))):
    if(fileName):
      fileName = fileName +"_"+ str(os.environ['rp_assets_stageType'])
    else:
      fileName = str(os.environ['rp_assets_stageType'])
  if(not re.search("^default$",str(os.environ['rp_assets_nodeType']))):
    if(fileName):
      fileName = fileName +"_"+ str(os.environ['rp_assets_nodeType'])
    else:
      fileName = str(os.environ['rp_assets_nodeType'])
  return(fileName)




def setOutPut():
  bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

  is_ntsc = (bpy.context.scene.render.fps != 25)

  bpy.context.scene.render.ffmpeg.format = "QUICKTIME"
  bpy.context.scene.render.ffmpeg.codec = "H264"

  if is_ntsc:
    bpy.context.scene.render.ffmpeg.gopsize = 18
  else:
    bpy.context.scene.render.ffmpeg.gopsize = 15

  bpy.context.scene.render.ffmpeg.video_bitrate = 6000
  bpy.context.scene.render.ffmpeg.maxrate = 9000
  bpy.context.scene.render.ffmpeg.minrate = 0
  bpy.context.scene.render.ffmpeg.buffersize = 224 * 8
  bpy.context.scene.render.ffmpeg.packetsize = 2048
  bpy.context.scene.render.ffmpeg.muxrate = 10080000
  bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
  bpy.context.scene.render.resolution_x = 1280
  bpy.context.scene.render.resolution_y = 720
  bpy.context.scene.render.resolution_percentage = 100


if(not rbhus_isRendering):
  try:
    assPath = os.environ['rp_assets_path']
    stageType = os.environ['rp_assets_stageType']
    nodeType = os.environ['rp_assets_nodeType']
    for x in bpy.data.cameras:
      x.show_safe_areas = True
    if(stageType == "anim"):
      setOutPut()
      bpy.context.scene.render.use_stamp = True
      bpy.context.scene.render.stamp_font_size = 20
      bpy.context.scene.render.use_stamp_time = False
      bpy.context.scene.render.use_stamp_date = False
      bpy.context.scene.render.use_stamp_render_time = False
      bpy.context.scene.render.use_stamp_frame = True
      bpy.context.scene.render.use_stamp_scene = False
      bpy.context.scene.render.use_stamp_camera = False
      bpy.context.scene.render.use_stamp_filename = False
      bpy.context.scene.render.use_stamp_note = True
      bpy.context.scene.render.filepath = "//"+ getAssFileName() +".mov"
      bpy.context.scene.use_audio_scrub = True
      for x in bpy.data.cameras:
        x.show_safe_areas = True

    if (stageType == "fx"):
      setOutPut()
      bpy.context.scene.render.use_stamp = False
      bpy.context.scene.render.resolution_x = 3840
      bpy.context.scene.render.resolution_y = 2160
      bpy.context.scene.render.resolution_percentage = 50
      bpy.context.scene.render.ffmpeg.format = "QUICKTIME"
      bpy.context.scene.render.ffmpeg.codec = 'PNG'
      bpy.context.scene.render.image_settings.color_mode = 'RGBA'
      bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'ULTRAFAST'
      bpy.context.scene.render.filepath = "//" + getAssFileName() + ".mov"
    elif(stageType == "postproduction" and nodeType == "lineUp"):
      setOutPut()
      bpy.context.scene.render.use_stamp = False
      bpy.context.scene.render.resolution_x = 3840
      bpy.context.scene.render.resolution_y = 2160
      bpy.context.scene.render.resolution_percentage = 50

      bpy.context.scene.render.ffmpeg.format = "QUICKTIME"
      # bpy.context.scene.render.image_settings.color_mode = 'RGB'
      # bpy.context.scene.render.ffmpeg.codec = 'PNG'
      # bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'ULTRAFAST'
      bpy.context.scene.render.filepath = "//" + getAssFileName() + ".mov"

    try:
      if (os.environ['rp_assets_fRange'] != "1"):
        bpy.context.scene.frame_start = int(os.environ['rp_assets_fRange'].split("-")[0])
        bpy.context.scene.frame_end = int(os.environ['rp_assets_fRange'].split("-")[1])
      else:
        if (os.environ['rp_sequenceScenes_sFrame'] != os.environ['rp_sequenceScenes_eFrame']):
          bpy.context.scene.frame_start = int(os.environ['rp_sequenceScenes_sFrame'])
          bpy.context.scene.frame_end = int(os.environ['rp_sequenceScenes_eFrame'])
        # if(os.environ['rp_assets_fRange'] != "1"):
        #   bpy.context.scene.frame_start = int(os.environ['rp_assets_fRange'].split("-")[0])
        #   bpy.context.scene.frame_end = int(os.environ['rp_assets_fRange'].split("-")[1])
    except:
      print(str(sys.exc_info()))

    if(os.environ['rp_assets_fileType'] != "default"):
      bpy.context.scene.render.stamp_note_text = ":".join(assPath.split(":")[0:-1])
    else:
      bpy.context.scene.render.stamp_note_text = assPath


    for x in bpy.data.scenes:
      x.safe_areas.title[0] = 0.1
      x.safe_areas.title[1] = 0.1
      x.safe_areas.action[0] = 0
      x.safe_areas.action[1] = 0



  except:
    bpy.context.scene.render.use_stamp = False
    print(str(sys.exc_info()))
