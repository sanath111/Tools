#addon Info
bl_info={
    "name":"Rotate Canvas",
    "desctiption":"Creates a new camera parented to the active one and a driver in Z rotation in order to rotate the camera canvas like. Usefull to 2D artist who want to start using Grease Pencil",
    "author":"Francisco Paez",
    "version":(0,1,0),
    "blender":(2,80,0),
    "location": "View3D > Tool Shelf > Addons Tab",
    "warning":"Very experimantal. Known bugs: Rotation property looks for an object called 'canvas' that doesen't exists before a canvas system is created. Planned Feautures: Flip canvas. Shortcut to the rotation. Reset function deletes keyframes",
    "wiki_url":"",
    "category":"Camera"
    }

import bpy
from bpy.types import Panel
from bpy import context
from bpy.props import BoolProperty# import bool property
from bpy.props import IntProperty, FloatProperty



#operator01
class OBJECT_OT_createCameras(bpy.types.Operator):
    """Adds two cameras linked together"""
    bl_label="Create Camera and Canvas"
    bl_idname="cam.add_canvas"
    bl_options= {'REGISTER','UNDO'}
    
    @classmethod
    def poll(cls, context):
        # print("Poll called")
        return True
   
   
    #execution
    def execute(self,context):
       
        
     #GoToObjectMode
        
        MiObjeto=bpy.context.active_object
        MiModo= bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT') 
        
        #limpieza de otras instancias del addon
        for obj in bpy.context.scene.objects:
            if obj.name == 'canvas':
                obj.hide_select = False
                obj.name='excanvas'                
            elif obj.name =='Cam_anim':
                obj.name='excamAnim'
        
        #creacion de las camaras y emparentamiento        
        bpy.ops.object.camera_add( location=(0,0,0), rotation=(1.5708, 0, 0)) 
        bpy.context.object.name = 'Cam_anim'         
        bpy.ops.object.camera_add( location=(0,0,0), rotation=(0, 0, 0))
        bpy.context.object.name = 'canvas'    
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects['Cam_anim']
        bpy.context.object.lock_location[0] = True
        bpy.context.object.lock_location[1] = True
        bpy.context.object.lock_location[2] = True
        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.scene.camera = bpy.data.objects['canvas']
        bpy.context.object.data.display_size = 2
        bpy.context.object.hide_select = True       
        bpy.ops.object.camera_add( rotation=(1.5708, 0, 0))
        bpy.context.object.name = 'Cam_anim' 
        
       
         #volver al objeto seleccionado
        MiObjeto.select_set (state=True)
        bpy.context.view_layer.objects.active = MiObjeto
        bpy.ops.object.mode_set(mode=MiModo)
        
        context.scene.my_bool_property = not context.scene.my_bool_property
        self.report({'INFO'}, "Simple Operator executed.")


        
        return {'FINISHED'}
 


    
#operator02
class OBJECT_OT_createCanvas(bpy.types.Operator):
    """Cretes canvas from an existing one"""
    bl_label="Create Canvas"
    bl_idname="cam.add_canvas_for_cam"
    bl_options= {'REGISTER','UNDO'}
    
    @classmethod
    def poll(cls, context):
        # print("Poll called")
        return True


    def execute(self, context):
      
        
        #GoToObjectMode
        MiObjeto=bpy.context.active_object
        MiModo= bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #limpieza de otras instancias del addon
        for obj in bpy.context.scene.objects:
            if obj.name == 'canvas':
                obj.hide_select = False
                obj.name='excanvas'                
            elif obj.name =='Cam_anim':
                obj.name='excamAnim'
        
        
            
        #creacion de las camaras y emparentamiento    
        bpy.ops.object.select_camera()
        bpy.context.object.name = 'Cam_anim' 
        bpy.ops.object.camera_add(location=(0,0,0), rotation=(0, 0, 0))
        bpy.context.object.name = 'canvas'    
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects['Cam_anim']
        bpy.context.object.lock_location[0] = True
        bpy.context.object.lock_location[1] = True
        bpy.context.object.lock_location[2] = True
        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.scene.camera = bpy.data.objects['canvas']
        bpy.data.objects['canvas'].select_set (state=True)
        bpy.context.view_layer.objects.active = bpy.data.objects['canvas']
        bpy.context.object.data.display_size = 2
        bpy.context.object.hide_select = True
       
       
        #volver al objeto seleccionado
        MiObjeto.select_set (state=True)
        bpy.context.view_layer.objects.active = MiObjeto
        bpy.ops.object.mode_set(mode=MiModo)
      
       #switch bool property to opposite. if you don't toggle just set to False
        context.scene.my_bool_property = not context.scene.my_bool_property
        self.report({'INFO'}, "Simple Operator executed.")



        
        return {'FINISHED'}

#operator03
class OBJECT_OT_deleteCanvas(bpy.types.Operator):
    """Delete canvas"""
    bl_label="Delete Canvas"
    bl_idname="cam.del_canvas"
    bl_options= {'REGISTER','UNDO'}
    
    
    
    #execution
    def execute(self,context):
        
        #GoToObjectMode
        MiObjeto=bpy.context.active_object
        MiModo= bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode=MiModo)

        for obj in bpy.context.scene.objects:
            if obj.name == 'canvas':
                obj.hide_select = False
                obj.name='teBorro'
                bpy.data.objects.remove(obj)
            elif obj.name =='Cam_anim':
                obj.name='Camera'
                bpy.context.scene.camera = bpy.data.objects['Camera']
        
         #switch bool property to opposite. if you don't toggle just set to False
        context.scene.my_bool_property = not context.scene.my_bool_property
        self.report({'INFO'}, "Simple Operator executed.")

        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        
        return {'FINISHED'}


#operator04
class OBJECT_OT_resetRotation(bpy.types.Operator):
    """Adds two cameras linked togheter"""
    bl_label="Reset Rotation"
    bl_idname="camera.reset_rotacion"
    bl_options= {'REGISTER','UNDO'}
    
    @classmethod
    def poll(cls, context):
        # print("Poll called")
        return True
    
    #execution
    def execute(self,context):
        bpy.data.objects['canvas'].rotation_euler[2]=0
        
        
        
        return {'FINISHED'}



#panel 01
class PANEL_PT_AddCanvasPanel(Panel):
    """Add Canvas Panel"""
    #revisar la ubicacion en Blender2.8
    bl_label = 'Create Canvas'
    bl_idname = 'OBJECT_PT_CreateCanvas'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Rotate Canvas"
    bl_label = "Create/Delete Canvas"
     
    #Agregar funcionalidad
    def draw(self, context):
       
        scene = context.scene
        layout = self.layout
        
       
        
        if scene.my_bool_property:#if bool property is true, show rows, else don't            
            layout.operator(OBJECT_OT_createCanvas.bl_idname, text='Using existing Camera', icon="OUTLINER_OB_CAMERA")
            layout.operator(OBJECT_OT_createCameras.bl_idname, text='Adding a new camera', icon="PLUS")
        else:
            layout.operator(OBJECT_OT_deleteCanvas.bl_idname, text='Delete Canvas', icon="CANCEL")
        
        
       
#panel 02         
class PANEL_PT_RotateCanvasPanel(Panel):
    
    bl_label = 'Rotate Canvas'
    bl_idname = 'OBJECT_PT_RotateCanvas'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rotate Canvas"
    bl_label = "Rotate Canvas"
     
    #Agregar funcionalidad
    def draw(self, context):
       
        scene = context.scene
        layout = self.layout
        
        if not scene.my_bool_property:
            canvas=bpy.data.objects['canvas']
            #layout.label(text=" Canvas Rotation:")
            row0 = layout.row(align=True)
            row0.prop(scene, 'left_handed')
            row1 = layout.row(align=True)
            row1.prop(canvas, "rotation_euler", index=2,text='rot')
            row1.prop(scene, 'my_float_property', slider=True)
            row2 = layout.row(align=True)
            row2.operator(OBJECT_OT_modalOperator.bl_idname, text = 'move', icon="MOUSE_MOVE")
            row2.operator(OBJECT_OT_resetRotation.bl_idname, text='reset', icon="FILE_REFRESH")
        else:
            layout.label(text='First create a Canvas')




class OBJECT_OT_modalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal Operator"

    first_mouse_x = IntProperty()
    first_value = FloatProperty()

    def modal(self, context, event):
        # self.delta1 = self.first_mouse_y - event.mouse_y
        if event.type == 'MOUSEMOVE':
            self.delta = self.first_mouse_y - event.mouse_y

            v = context.scene.my_float_property

            if context.scene.left_handed:
                bpy.data.objects['canvas'].rotation_euler[2] = bpy.data.objects['canvas'].rotation_euler[2] - (self.delta * v)
            else:
                bpy.data.objects['canvas'].rotation_euler[2] = bpy.data.objects['canvas'].rotation_euler[2] + (self.delta * v)
            self.first_mouse_y = event.mouse_y

        elif event.type == 'MIDDLEMOUSE':

            if event.value == 'RELEASE':
                return {'FINISHED'}

        elif event.type in {'LEFTMOUSE','ESC'}:
            
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # variable to remember left mouse button state
        self.lmb = False

        if context.object:
            self.first_mouse_y = event.mouse_y
            self.first_value = context.object.rotation_euler.z

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}




#agregar boton en otras partes
def add_object_button(self,context):
    self.layout.operator(
            OBJECT_OT_createCameras.bl_idname,
            icon="OUTLINER_OB_CAMERA"          
            )


addon_keymaps = []


def register_keymaps():
    # pref = get_addon_prefs()
    # if not pref.canvas_use_shortcut:
    #     return
    addon = bpy.context.window_manager.keyconfigs.addon

    km = bpy.context.window_manager.keyconfigs.addon.keymaps.get("3D View")
    if not km:
        km = addon.keymaps.new(name="3D View", space_type="VIEW_3D")

    if 'view3d.modal_operator' not in km.keymap_items:
        km = addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('view3d.modal_operator',
                                  type='MIDDLEMOUSE', value="PRESS",
                                  alt=True, ctrl=True,
                                  shift=False, any=False)

        addon_keymaps.append(km)


def unregister_keymaps():
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


#register
       
__classes__ = (OBJECT_OT_createCameras, OBJECT_OT_createCanvas,OBJECT_OT_deleteCanvas, OBJECT_OT_resetRotation, PANEL_PT_AddCanvasPanel, PANEL_PT_RotateCanvasPanel, OBJECT_OT_modalOperator)

def register():
    for c in __classes__:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_bool_property = BoolProperty(name='My Bool Property', default = True)# create bool property for switching
    bpy.types.Scene.my_float_property = FloatProperty(name = 'sensitivity', default=0.005, min=0, max=0.1, step=3, precision=3)
    bpy.types.Scene.left_handed = BoolProperty(name = 'Left Handed', default=False)
    register_keymaps()
    
def unregister():
    unregister_keymaps()
    for c in reversed(__classes__):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_bool_property#remove property on unregister
    del bpy.types.Scene.my_float_property
    del bpy.types.Scene.left_handed
if __name__ == "__main__":
    register()
      
#  
