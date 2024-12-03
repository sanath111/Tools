bl_info = {
    "name": "Camera Watermark Addon",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "sanath111",
    "description": "Addon to viewport render with watermark image",
}

import bpy

# Set the default image path here
DEFAULT_IMAGE_PATH = "/crap/crap.server/AUM/logo_andePirki_aum_half.png"

# Dictionary to store old overlay states
old_overlay_states = {
    "show_extras": None,
    "show_relationship_lines": None,
    "show_floor": None,
    "show_axis_x": None,
    "show_axis_y": None,
    "show_cursor": None,
    "show_text": None,
    "show_stats": None,
    "show_ortho_grid": None,
    "show_annotation": None,
    "show_bones": None,
    "show_motion_paths": None,
    "show_object_origins": None,
    "use_gpencil_onion_skin": None,
    "show_outline_selected": None,
}

def set_camera_watermark(context, filepath):
    scene = context.scene

    # Ensure a camera is active
    if scene.camera is None:
        print("No active camera found.")
        return

    camera = scene.camera.data

    # Ensure the watermark image exists
    if not camera.background_images:
        bg = camera.background_images.new()
    else:
        bg = camera.background_images[0]  # Use the first one

    # Load the image
    bg.image = bpy.data.images.load(filepath)

    # Set image properties
    bg.display_depth = 'FRONT'
    bg.alpha = 0.5  # Set opacity (alpha)
    bg.frame_method = 'FIT'

    # Get camera resolution to calculate the offset
    render = scene.render
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y

    # Calculate offset based on the new formula
    offset_x = (4 / resolution_y) * 100  # Offset based on resolution_y
    offset_y = (4 / resolution_x) * 100  # Offset based on resolution_x

    bg.offset[0] = offset_x  # X offset
    bg.offset[1] = offset_y  # Y offset

    # Set scale to 0.25
    bg.scale = 0.25

    # Set visibility based on the checkbox state
    bg.show_background_image = scene.use_camera_watermark


def update_watermark_visibility(self, context):
    scene = context.scene
    space = context.area.spaces.active if context.area else None

    if space and hasattr(space, 'overlay'):
        if scene.use_camera_watermark:
            # Save current overlay states
            for key in old_overlay_states:
                old_overlay_states[key] = getattr(space.overlay, key, None)

            if not space.overlay.show_overlays:
                space.overlay.show_overlays = True

            # Disable all overlay options except watermark image
            space.overlay.show_extras = False
            space.overlay.show_relationship_lines = False
            space.overlay.show_floor = False
            space.overlay.show_axis_x = False
            space.overlay.show_axis_y = False
            space.overlay.show_cursor = False
            space.overlay.show_text = False
            space.overlay.show_stats = False
            space.overlay.show_ortho_grid = False

            # Additional Grease Pencil overlays
            space.overlay.show_annotation = False
            space.overlay.show_bones = False
            space.overlay.show_motion_paths = False
            space.overlay.show_object_origins = False
            space.overlay.use_gpencil_onion_skin = False
            space.overlay.show_outline_selected = False

            if scene.camera and scene.camera.data.background_images:
                scene.camera.data.background_images[0].show_background_image = True
            # Start viewport render
            bpy.ops.render.opengl(animation=True)

            # Use a modal operator to uncheck the checkbox after render is done
            bpy.ops.object.uncheck_watermark_checkbox_after_render('INVOKE_DEFAULT')

        else:
            # Restore the old overlay states
            for key, value in old_overlay_states.items():
                if value is not None:
                    setattr(space.overlay, key, value)

    else:
        print("No valid space found for overlay operations.")


class OBJECT_OT_uncheck_watermark_checkbox_after_render(bpy.types.Operator):
    bl_idname = "object.uncheck_watermark_checkbox_after_render"
    bl_label = "Uncheck Watermark Checkbox After Render"

    def execute(self, context):
        scene = context.scene
        # Check if render is complete
        if bpy.data.images.get('Render Result'):
            scene.camera.data.background_images[0].show_background_image = False
            context.scene.use_camera_watermark = False
            # Restore old overlay states
            update_watermark_visibility(self, context)
        return {'FINISHED'}


class CameraWatermarkPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Camera Watermark"
    bl_idname = "OBJECT_PT_camera_watermark"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Watermark'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # File picker for watermark image
        layout.prop(scene, "watermark_image_path", text="Image")

        # Checkbox to show/hide the watermark
        layout.prop(scene, "use_camera_watermark", text="Render with Watermark")


def update_watermark_image(self, context):
    scene = context.scene
    filepath = scene.watermark_image_path

    if filepath:
        set_camera_watermark(context, filepath)


def load_default_image():
    """Load the default image when the addon is first registered."""
    if bpy.context.scene.camera:
        bpy.context.scene.camera.data.show_background_images = True
        set_camera_watermark(bpy.context, DEFAULT_IMAGE_PATH)


def register():
    bpy.utils.register_class(CameraWatermarkPanel)
    bpy.utils.register_class(OBJECT_OT_uncheck_watermark_checkbox_after_render)

    # Property for file path of the watermark image
    bpy.types.Scene.watermark_image_path = bpy.props.StringProperty(
        name="Watermark Image",
        subtype='FILE_PATH',
        description="Select watermark image",
        default=DEFAULT_IMAGE_PATH,  # Set default path
        update=update_watermark_image  # Set watermark image when file is picked
    )

    # Property for enabling/disabling the watermark image
    bpy.types.Scene.use_camera_watermark = bpy.props.BoolProperty(
        name="Use Camera Watermark",
        description="Enable/Disable watermark image for the camera",
        default=False,
        update=update_watermark_visibility  # Toggle visibility when checkbox is clicked
    )

    # Use a timer to defer loading the default image
    # Ensures the context is properly initialized
    bpy.app.timers.register(lambda: load_default_image())


def unregister():
    bpy.utils.unregister_class(CameraWatermarkPanel)
    bpy.utils.unregister_class(OBJECT_OT_uncheck_watermark_checkbox_after_render)

    del bpy.types.Scene.watermark_image_path
    del bpy.types.Scene.use_camera_watermark


if __name__ == "__main__":
    register()
