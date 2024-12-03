bl_info = {
    "name": "Camera Background Image Addon",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy

# Set the default image path here
DEFAULT_IMAGE_PATH = "/crap/crap.server/AUM/logo_andePirki_aum_half.png"


class CameraBackgroundPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Camera Background Image"
    bl_idname = "OBJECT_PT_camera_background"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera BG'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "bg_image_path")  # File picker for background image
        layout.prop(scene, "use_camera_bg_image")  # Checkbox to show/hide the image


def set_camera_background_image(context, filepath):
    scene = context.scene

    # Ensure a camera is active
    if scene.camera is None:
        print("No active camera found.")
        return

    camera = scene.camera.data

    # Ensure the background image exists
    if not camera.background_images:
        bg = camera.background_images.new()
    else:
        bg = camera.background_images[0]  # Use the first one

    # Load the image
    bg.image = bpy.data.images.load(filepath)

    # Set image properties
    bg.display_depth = 'FRONT'
    bg.alpha = 0.5  # Set opacity (now called alpha)
    bg.frame_method = 'FIT'

    # Get camera resolution to calculate the offset
    render = scene.render
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y

    # Calculate offset as per the new formula
    offset_x = (4 / resolution_y) * 100  # Offset based on resolution_y
    offset_y = (4 / resolution_x) * 100  # Offset based on resolution_x

    bg.offset[0] = offset_x  # X offset
    bg.offset[1] = offset_y  # Y offset

    # Set scale to 0.25
    bg.scale = 0.25

    # Set visibility based on the checkbox state
    bg.show_background_image = scene.use_camera_bg_image


def update_background_image_visibility(self, context):
    scene = context.scene

    # Enable overlays if they're off, but disable all other options
    view = context.space_data.overlay

    if scene.use_camera_bg_image:
        if not view.show_overlays:
            view.show_overlays = True

        # Disable all overlay options except background images
        view.show_extras = False
        view.show_relationship_lines = False
        view.show_floor = False
        view.show_axis_x = False
        view.show_axis_y = False
        view.show_cursor = False
        view.show_text = False
        view.show_stats = False
        view.show_ortho_grid = False

    # Toggle visibility of the background image
    if scene.camera and scene.camera.data.background_images:
        scene.camera.data.background_images[0].show_background_image = scene.use_camera_bg_image


def update_background_image(self, context):
    scene = context.scene
    filepath = scene.bg_image_path

    # If a valid path is chosen, set the background image
    if filepath:
        set_camera_background_image(context, filepath)


def load_default_image(context):
    """Load the default image when the addon is first registered."""
    scene = context.scene

    # Set the background image using the default path
    set_camera_background_image(context, DEFAULT_IMAGE_PATH)


def register():
    bpy.utils.register_class(CameraBackgroundPanel)

    # Property for file path of the background image
    bpy.types.Scene.bg_image_path = bpy.props.StringProperty(
        name="Background Image",
        subtype='FILE_PATH',
        description="Select background image",
        default=DEFAULT_IMAGE_PATH,  # Set default path
        update=update_background_image  # Set background image when file is picked
    )

    # Property for enabling/disabling the background image
    bpy.types.Scene.use_camera_bg_image = bpy.props.BoolProperty(
        name="Use Camera Background Image",
        description="Enable/Disable background image for the camera",
        default=False,
        update=update_background_image_visibility  # Toggle visibility when checkbox is clicked
    )

    # Enable background images for the camera by default and load default image
    if bpy.context.scene.camera:
        bpy.context.scene.camera.data.show_background_images = True
        load_default_image(bpy.context)  # Load default image on startup


def unregister():
    bpy.utils.unregister_class(CameraBackgroundPanel)

    del bpy.types.Scene.bg_image_path
    del bpy.types.Scene.use_camera_bg_image


if __name__ == "__main__":
    register()
