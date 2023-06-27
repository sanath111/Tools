bl_info = {
    "name": "Mute Audio",
    "author": "sanath111, chat-gpt",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Tool",
    "description": "Mute and unmute audio sink inputs",
    "category": "Tool",
}

import bpy
import subprocess


def extract_application_name(lines):
    for line in lines:
        line = line.strip()
        if line.startswith("application.name = "):
            app_name = line.split('=')[1].strip().strip('"')
            return app_name
    return ""


def extract_mute_state(lines):
    for line in lines:
        line = line.strip()
        if line.startswith("muted:"):
            mute_state = line.split(':')[1].strip()
            return mute_state == "yes"
    return False


class MUTE_AUDIO_OT_operator(bpy.types.Operator):
    bl_idname = "audio.mute_audio_operator"
    bl_label = ""

    index: bpy.props.IntProperty()

    def execute(self, context):
        index_info_dict = self.get_sink_input_info()

        if self.index in index_info_dict:
            info = index_info_dict[self.index]
            mute_state = info['muted']
            command = ["pacmd", "set-sink-input-mute", str(self.index), str(not mute_state).lower()]
            subprocess.run(command)

        return {'FINISHED'}

    def get_sink_input_info(self):
        index_info_dict = {}
        output = subprocess.check_output(["pacmd", "list-sink-inputs"]).decode()
        blocks = output.split('index:')

        for block in blocks[1:]:
            lines = block.strip().split('\n')
            index = int(lines[0].strip())
            app_name = extract_application_name(lines)
            mute_state = extract_mute_state(lines)
            index_info_dict[index] = {'application': app_name, 'muted': mute_state}

        return index_info_dict


class MUTE_AUDIO_PT_panel(bpy.types.Panel):
    bl_label = "Mute Audio"
    bl_idname = "MUTE_AUDIO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        index_info_dict = MUTE_AUDIO_OT_operator.get_sink_input_info(None)

        for index, info in index_info_dict.items():
            app_name = info['application']
            mute_state = info['muted']
            icon = "MUTE_IPO_OFF" if mute_state else "MUTE_IPO_ON"
            layout.operator("audio.mute_audio_operator", text=app_name, icon=icon).index = index


classes = (MUTE_AUDIO_OT_operator, MUTE_AUDIO_PT_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
