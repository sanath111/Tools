# coding: utf-8
bl_info = {
    "name": "Rig Panels 1.0",
    "description": "Creates a panel for hiding rigs and meshes",
    "author": "Ujwal Virat, Sanath Shetty K",
    "version": (0, 0, 1),
    "blender": (2, 78, 5),
    "location": "View3D > Tool Shelf > Rig Panel",
    "warning": "",
    "wiki_url": "",
    "category": "Armature" }

import bpy
from mathutils import Matrix, Vector
from math import acos, pi, radians
from bpy.props import BoolProperty

rig_id = "script"


from bpy.types import (
    Operator,
    Menu,
    Panel,
    UIList,
    PropertyGroup,
)

from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty,
    CollectionProperty,
)


############################
## Math utility functions ##
############################

def perpendicular_vector(v):
    """ Returns a vector that is perpendicular to the one given.
        The returned vector is _not_ guaranteed to be normalized.
    """
    # Create a vector that is not aligned with v.
    # It doesn't matter what vector.  Just any vector
    # that's guaranteed to not be pointing in the same
    # direction.
    if abs(v[0]) < abs(v[1]):
        tv = Vector((1,0,0))
    else:
        tv = Vector((0,1,0))

    # Use cross prouct to generate a vector perpendicular to
    # both tv and (more importantly) v.
    return v.cross(tv)


def rotation_difference(mat1, mat2):
    """ Returns the shortest-path rotational difference between two
        matrices.
    """
    q1 = mat1.to_quaternion()
    q2 = mat2.to_quaternion()
    angle = acos(min(1,max(-1,q1.dot(q2)))) * 2
    if angle > pi:
        angle = -angle + (2*pi)
    return angle

def tail_distance(angle,bone_ik,bone_fk):
    """ Returns the distance between the tails of two bones
        after rotating bone_ik in AXIS_ANGLE mode.
    """
    rot_mod=bone_ik.rotation_mode
    if rot_mod != 'AXIS_ANGLE':
        bone_ik.rotation_mode = 'AXIS_ANGLE'
    bone_ik.rotation_axis_angle[0] = angle
    bpy.context.scene.update()

    dv = (bone_fk.tail - bone_ik.tail).length

    bone_ik.rotation_mode = rot_mod
    return dv

def find_min_range(bone_ik,bone_fk,f=tail_distance,delta=pi/8):
    """ finds the range where lies the minimum of function f applied on bone_ik and bone_fk
        at a certain angle.
    """
    rot_mod=bone_ik.rotation_mode
    if rot_mod != 'AXIS_ANGLE':
        bone_ik.rotation_mode = 'AXIS_ANGLE'

    start_angle = bone_ik.rotation_axis_angle[0]
    angle = start_angle
    while (angle > (start_angle - 2*pi)) and (angle < (start_angle + 2*pi)):
        l_dist = f(angle-delta,bone_ik,bone_fk)
        c_dist = f(angle,bone_ik,bone_fk)
        r_dist = f(angle+delta,bone_ik,bone_fk)
        if min((l_dist,c_dist,r_dist)) == c_dist:
            bone_ik.rotation_mode = rot_mod
            return (angle-delta,angle+delta)
        else:
            angle=angle+delta

def ternarySearch(f, left, right, bone_ik, bone_fk, absolutePrecision):
    """
    Find minimum of unimodal function f() within [left, right]
    To find the maximum, revert the if/else statement or revert the comparison.
    """
    while True:
        #left and right are the current bounds; the maximum is between them
        if abs(right - left) < absolutePrecision:
            return (left + right)/2

        leftThird = left + (right - left)/3
        rightThird = right - (right - left)/3

        if f(leftThird, bone_ik, bone_fk) > f(rightThird, bone_ik, bone_fk):
            left = leftThird
        else:
            right = rightThird

#########################################
## "Visual Transform" helper functions ##
#########################################

def get_pose_matrix_in_other_space(mat, pose_bone):
    """ Returns the transform matrix relative to pose_bone's current
        transform space.  In other words, presuming that mat is in
        armature space, slapping the returned matrix onto pose_bone
        should give it the armature-space transforms of mat.
        TODO: try to handle cases with axis-scaled parents better.
    """
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()
    if pose_bone.parent:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    # Get matrix in bone's current transform space
    smat = rest_inv * (par_rest * (par_inv * mat))

    # Compensate for non-local location
    #if not pose_bone.bone.use_local_location:
    #    loc = smat.to_translation() * (par_rest.inverted() * rest).to_quaternion()
    #    smat.translation = loc

    return smat


def get_local_pose_matrix(pose_bone):
    """ Returns the local transform matrix of the given pose bone.
    """
    return get_pose_matrix_in_other_space(pose_bone.matrix, pose_bone)


def set_pose_translation(pose_bone, mat):
    """ Sets the pose bone's translation to the same translation as the given matrix.
        Matrix should be given in bone's local space.
    """
    if pose_bone.bone.use_local_location == True:
        pose_bone.location = mat.to_translation()
    else:
        loc = mat.to_translation()

        rest = pose_bone.bone.matrix_local.copy()
        if pose_bone.bone.parent:
            par_rest = pose_bone.bone.parent.matrix_local.copy()
        else:
            par_rest = Matrix()

        q = (par_rest.inverted() * rest).to_quaternion()
        pose_bone.location = q * loc


def set_pose_rotation(pose_bone, mat):
    """ Sets the pose bone's rotation to the same rotation as the given matrix.
        Matrix should be given in bone's local space.
    """
    q = mat.to_quaternion()

    if pose_bone.rotation_mode == 'QUATERNION':
        pose_bone.rotation_quaternion = q
    elif pose_bone.rotation_mode == 'AXIS_ANGLE':
        pose_bone.rotation_axis_angle[0] = q.angle
        pose_bone.rotation_axis_angle[1] = q.axis[0]
        pose_bone.rotation_axis_angle[2] = q.axis[1]
        pose_bone.rotation_axis_angle[3] = q.axis[2]
    else:
        pose_bone.rotation_euler = q.to_euler(pose_bone.rotation_mode)


def set_pose_scale(pose_bone, mat):
    """ Sets the pose bone's scale to the same scale as the given matrix.
        Matrix should be given in bone's local space.
    """
    pose_bone.scale = mat.to_scale()


def match_pose_translation(pose_bone, target_bone):
    """ Matches pose_bone's visual translation to target_bone's visual
        translation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_translation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_rotation(pose_bone, target_bone):
    """ Matches pose_bone's visual rotation to target_bone's visual
        rotation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_rotation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_scale(pose_bone, target_bone):
    """ Matches pose_bone's visual scale to target_bone's visual
        scale.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_scale(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

def correct_rotation(bone_ik, bone_fk):
    """ Corrects the ik rotation in ik2fk snapping functions
    """

    alfarange = find_min_range(bone_ik,bone_fk)
    alfamin = ternarySearch(tail_distance,alfarange[0],alfarange[1],bone_ik,bone_fk,0.1)

    rot_mod = bone_ik.rotation_mode
    if rot_mod != 'AXIS_ANGLE':
        bone_ik.rotation_mode = 'AXIS_ANGLE'
    bone_ik.rotation_axis_angle[0] = alfamin
    bone_ik.rotation_mode = rot_mod

##############################
## IK/FK snapping functions ##
##############################

def match_pole_target(ik_first, ik_last, pole, match_bone, length):
    """ Places an IK chain's pole target to match ik_first's
        transforms to match_bone.  All bones should be given as pose bones.
        You need to be in pose mode on the relevant armature object.
        ik_first: first bone in the IK chain
        ik_last:  last bone in the IK chain
        pole:  pole target bone for the IK chain
        match_bone:  bone to match ik_first to (probably first bone in a matching FK chain)
        length:  distance pole target should be placed from the chain center
    """
    a = ik_first.matrix.to_translation()
    b = ik_last.matrix.to_translation() + ik_last.vector

    # Vector from the head of ik_first to the
    # tip of ik_last
    ikv = b - a

    # Get a vector perpendicular to ikv
    pv = perpendicular_vector(ikv).normalized() * length

    def set_pole(pvi):
        """ Set pole target's position based on a vector
            from the arm center line.
        """
        # Translate pvi into armature space
        ploc = a + (ikv/2) + pvi

        # Set pole target to location
        mat = get_pose_matrix_in_other_space(Matrix.Translation(ploc), pole)
        set_pose_translation(pole, mat)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    set_pole(pv)

    # Get the rotation difference between ik_first and match_bone
    angle = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Try compensating for the rotation difference in both directions
    pv1 = Matrix.Rotation(angle, 4, ikv) * pv
    set_pole(pv1)
    ang1 = rotation_difference(ik_first.matrix, match_bone.matrix)

    pv2 = Matrix.Rotation(-angle, 4, ikv) * pv
    set_pole(pv2)
    ang2 = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Do the one with the smaller angle
    if ang1 < ang2:
        set_pole(pv1)


def fk2ik_arm(obj, fk, ik):
    """ Matches the fk bones in an arm rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]

    if 'auto_stretch' in handi.keys():
        # This is kept for compatibility with legacy rigify Human
        # Stretch
        if handi['auto_stretch'] == 0.0:
            uarm['stretch_length'] = handi['stretch_length']
        else:
            diff = (uarmi.vector.length + farmi.vector.length) / (uarm.vector.length + farm.vector.length)
            uarm['stretch_length'] *= diff

        # Upper arm position
        match_pose_rotation(uarm, uarmi)
        match_pose_scale(uarm, uarmi)

        # Forearm position
        match_pose_rotation(farm, farmi)
        match_pose_scale(farm, farmi)

        # Hand position
        match_pose_rotation(hand, handi)
        match_pose_scale(hand, handi)
    else:
        # Upper arm position
        match_pose_translation(uarm, uarmi)
        match_pose_rotation(uarm, uarmi)
        match_pose_scale(uarm, uarmi)

        # Forearm position
        #match_pose_translation(hand, handi)
        match_pose_rotation(farm, farmi)
        match_pose_scale(farm, farmi)

        # Hand position
        match_pose_translation(hand, handi)
        match_pose_rotation(hand, handi)
        match_pose_scale(hand, handi)


def ik2fk_arm(obj, fk, ik):
    """ Matches the ik bones in an arm rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]

    main_parent = obj.pose.bones[ik[4]]

    if ik[3] != "" and main_parent['pole_vector']:
        pole  = obj.pose.bones[ik[3]]
    else:
        pole = None


    if pole:
        # Stretch
        # handi['stretch_length'] = uarm['stretch_length']

        # Hand position
        match_pose_translation(handi, hand)
        match_pose_rotation(handi, hand)
        match_pose_scale(handi, hand)
        # Pole target position
        match_pole_target(uarmi, farmi, pole, uarm, (uarmi.length + farmi.length))

    else:
        # Hand position
        match_pose_translation(handi, hand)
        match_pose_rotation(handi, hand)
        match_pose_scale(handi, hand)

        # Upper Arm position
        match_pose_translation(uarmi, uarm)
        match_pose_rotation(uarmi, uarm)
        match_pose_scale(uarmi, uarm)
        # Rotation Correction
        correct_rotation(uarmi, uarm)

def fk2ik_leg(obj, fk, ik):
    """ Matches the fk bones in a leg rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh  = obj.pose.bones[fk[0]]
    shin   = obj.pose.bones[fk[1]]
    foot   = obj.pose.bones[fk[2]]
    mfoot  = obj.pose.bones[fk[3]]
    thighi = obj.pose.bones[ik[0]]
    shini  = obj.pose.bones[ik[1]]
    footi  = obj.pose.bones[ik[2]]
    mfooti = obj.pose.bones[ik[3]]

    if 'auto_stretch' in footi.keys():
        # This is kept for compatibility with legacy rigify Human
        # Stretch
        if footi['auto_stretch'] == 0.0:
            thigh['stretch_length'] = footi['stretch_length']
        else:
            diff = (thighi.vector.length + shini.vector.length) / (thigh.vector.length + shin.vector.length)
            thigh['stretch_length'] *= diff

        # Thigh position
        match_pose_rotation(thigh, thighi)
        match_pose_scale(thigh, thighi)

        # Shin position
        match_pose_rotation(shin, shini)
        match_pose_scale(shin, shini)

        # Foot position
        mat = mfoot.bone.matrix_local.inverted() * foot.bone.matrix_local
        footmat = get_pose_matrix_in_other_space(mfooti.matrix, foot) * mat
        set_pose_rotation(foot, footmat)
        set_pose_scale(foot, footmat)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    else:
        # Thigh position
        match_pose_translation(thigh, thighi)
        match_pose_rotation(thigh, thighi)
        match_pose_scale(thigh, thighi)

        # Shin position
        match_pose_rotation(shin, shini)
        match_pose_scale(shin, shini)

        # Foot position
        mat = mfoot.bone.matrix_local.inverted() * foot.bone.matrix_local
        footmat = get_pose_matrix_in_other_space(mfooti.matrix, foot) * mat
        set_pose_rotation(foot, footmat)
        set_pose_scale(foot, footmat)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')


def ik2fk_leg(obj, fk, ik):
    """ Matches the ik bones in a leg rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh    = obj.pose.bones[fk[0]]
    shin     = obj.pose.bones[fk[1]]
    mfoot    = obj.pose.bones[fk[2]]
    if fk[3] != "":
        foot      = obj.pose.bones[fk[3]]
    else:
        foot = None
    thighi   = obj.pose.bones[ik[0]]
    shini    = obj.pose.bones[ik[1]]
    footi    = obj.pose.bones[ik[2]]
    footroll = obj.pose.bones[ik[3]]

    main_parent = obj.pose.bones[ik[6]]

    if ik[4] != "" and main_parent['pole_vector']:
        pole     = obj.pose.bones[ik[4]]
    else:
        pole = None
    mfooti   = obj.pose.bones[ik[5]]

    if (not pole) and (foot):

        # Clear footroll
        set_pose_rotation(footroll, Matrix())

        # Foot position
        mat = mfooti.bone.matrix_local.inverted() * footi.bone.matrix_local
        footmat = get_pose_matrix_in_other_space(foot.matrix, footi) * mat
        set_pose_translation(footi, footmat)
        set_pose_rotation(footi, footmat)
        set_pose_scale(footi, footmat)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

        # Thigh position
        match_pose_translation(thighi, thigh)
        match_pose_rotation(thighi, thigh)
        match_pose_scale(thighi, thigh)

        # Rotation Correction
        correct_rotation(thighi,thigh)
        
    else:
        # Stretch
        if 'stretch_lenght' in footi.keys() and 'stretch_lenght' in thigh.keys():
            # Kept for compat with legacy rigify Human
            footi['stretch_length'] = thigh['stretch_length']

        # Clear footroll
        set_pose_rotation(footroll, Matrix())

        # Foot position
        mat = mfooti.bone.matrix_local.inverted() * footi.bone.matrix_local
        footmat = get_pose_matrix_in_other_space(mfoot.matrix, footi) * mat
        set_pose_translation(footi, footmat)
        set_pose_rotation(footi, footmat)
        set_pose_scale(footi, footmat)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

        # Pole target position
        match_pole_target(thighi, shini, pole, thigh, (thighi.length + shini.length))


##############################
## IK/FK snapping operators ##
##############################

class Rigify_Arm_FK2IK(bpy.types.Operator):
    """ Snaps an FK arm to an IK arm.
    """
    bl_idname = "pose.rigify_arm_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK arm to IK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Arm_IK2FK(bpy.types.Operator):
    """ Snaps an IK arm to an FK arm.
    """
    bl_idname = "pose.rigify_arm_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK arm to FK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")
    pole    = bpy.props.StringProperty(name="Pole IK Name")

    main_parent = bpy.props.StringProperty(name="Main Parent", default="")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik, self.pole, self.main_parent])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_FK2IK(bpy.types.Operator):
    """ Snaps an FK leg to an IK leg.
    """
    bl_idname = "pose.rigify_leg_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK leg to IK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    shin_fk  = bpy.props.StringProperty(name="Shin FK Name")
    foot_fk  = bpy.props.StringProperty(name="Foot FK Name")
    mfoot_fk = bpy.props.StringProperty(name="MFoot FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    shin_ik  = bpy.props.StringProperty(name="Shin IK Name")
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    mfoot_ik = bpy.props.StringProperty(name="MFoot IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_leg(context.active_object, fk=[self.thigh_fk, self.shin_fk, self.foot_fk, self.mfoot_fk], ik=[self.thigh_ik, self.shin_ik, self.foot_ik, self.mfoot_ik])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_IK2FK(bpy.types.Operator):
    """ Snaps an IK leg to an FK leg.
    """
    bl_idname = "pose.rigify_leg_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK leg to FK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    shin_fk  = bpy.props.StringProperty(name="Shin FK Name")
    mfoot_fk = bpy.props.StringProperty(name="MFoot FK Name")
    foot_fk = bpy.props.StringProperty(name="Foot FK Name", default="")
    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    shin_ik  = bpy.props.StringProperty(name="Shin IK Name")
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    footroll = bpy.props.StringProperty(name="Foot Roll Name")
    pole     = bpy.props.StringProperty(name="Pole IK Name")
    mfoot_ik = bpy.props.StringProperty(name="MFoot IK Name")

    main_parent = bpy.props.StringProperty(name="Main Parent", default="")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_leg(context.active_object, fk=[self.thigh_fk, self.shin_fk, self.mfoot_fk, self.foot_fk], ik=[self.thigh_ik, self.shin_ik, self.foot_ik, self.footroll, self.pole, self.mfoot_ik, self.main_parent])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}

        

class RigLayers(bpy.types.Panel):
    bl_label = "RigLayers"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Headmain')
        row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Headextra')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Neck')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Neck(Tweaks')
        
        row = col.row()
        row.separator()
        row = col.row()
        row.separator()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Torso')
        row.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Torso (Tweak)')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Fingers')
        row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Fingers (Tweak)')
        
        row = col.row()
        row.separator()
        row = col.row()
        row.separator()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=24, toggle=True, text='Arm(Extratweaks)')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Arm.L (IK)')
        row.prop(context.active_object.data, 'layers', index=10, toggle=True, text='Arm.R (IK)')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=8, toggle=True, text='Arm.L (FK)')
        row.prop(context.active_object.data, 'layers', index=11, toggle=True, text='Arm.R (FK)')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=9, toggle=True, text='Arm.L (Tweak)')
        row.prop(context.active_object.data, 'layers', index=12, toggle=True, text='Arm.R (Tweak)')
        
        row = col.row()
        row.separator()
        row = col.row()
        row.separator()

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=13, toggle=True, text='Leg.L (IK)')
        row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Leg.R (IK)')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Leg.L (FK)')
        row.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Leg.R (FK)')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=15, toggle=True, text='Leg.L (Tweak)')
        row.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Leg.R (Tweak)')
        
        row = col.row()
        row.separator()
        row = col.row()
        row.separator()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=25, toggle=True, text='LegFingers')
        
        row = col.row()
        row.separator()
        row = col.row()
        row.separator()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Tail')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=14, toggle=True, text='Tail(Tweaks)')

        row = col.row()
        row.separator()
        row = col.row()
        row.separator()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=26, toggle=True, text='cloth')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=27, toggle=True, text='extra')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=28, toggle=True, text='Root')
        
        
class Rigmain(bpy.types.Panel):
    bl_label = "Rigmain"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'        
        
        
    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            return

        def is_selected(names):
            # Returns whether any of the named bones are selected.
            if type(names) == list:
                for name in names:
                    if name in selected_bones:
                        return True
            elif names in selected_bones:
                return True
            return False



        
        controls = ['head', 'neck', 'chest', 'hips', 'torso']
        torso    = 'torso'
        
        if is_selected( controls ):
            if hasattr(pose_bones[torso],'["head_follow"]'):
                layout.prop( pose_bones[ torso ], '["head_follow"]', slider = True )
            if hasattr(pose_bones[torso],'["neck_follow"]'):
                layout.prop( pose_bones[ torso ], '["neck_follow"]', slider = True )
            if hasattr(pose_bones[torso],'["tail_follow"]'):
                layout.prop( pose_bones[ torso ], '["parachute"]', slider = True )
                

        

        
        controls = ['thigh_ik.L', 'thigh_fk.L', 'shin_fk.L', 'foot_fk.L', 'toe.L', 'foot_heel_ik.L', 'foot_ik.L', 'MCH-foot_fk.L', 'thigh_parent.L']
        tweaks   = ['thigh_tweak.L.001', 'shin_tweak.L', 'shin_tweak.L.001']
        ik_ctrl  = ['foot_ik.L', 'MCH-thigh_ik.L', 'MCH-thigh_ik_target.L']
        fk_ctrl  = 'thigh_fk.L'
        parent   = 'thigh_parent.L'
        foot_fk = 'foot_fk.L'
        pole = 'thigh_ik_target.L'
        
        # IK/FK Switch on all Control Bones
        if is_selected( controls ):
            layout.prop( pose_bones[parent], '["IK_FK"]', slider = True )
            props = layout.operator("pose.rigify_leg_fk2ik_" + rig_id, text="Snap FK->IK (" + fk_ctrl + ")")
            props.thigh_fk = controls[1]
            props.shin_fk  = controls[2]
            props.foot_fk  = controls[3]
            props.mfoot_fk = controls[7]
            props.thigh_ik = controls[0]
            props.shin_ik  = ik_ctrl[1]
            props.foot_ik = ik_ctrl[2]
            props.mfoot_ik = ik_ctrl[2]
            props = layout.operator("pose.rigify_leg_ik2fk_" + rig_id, text="Snap IK->FK (" + fk_ctrl + ")")
            props.thigh_fk  = controls[1]
            props.shin_fk   = controls[2]
            props.foot_fk  = controls[3]
            props.mfoot_fk  = controls[7]
            props.thigh_ik  = controls[0]
            props.shin_ik   = ik_ctrl[1]
            props.foot_ik   = controls[6]
            props.pole      = pole
            props.footroll  = controls[5]
            props.mfoot_ik  = ik_ctrl[2]
            props.main_parent = parent
        
        # BBone rubber hose on each Respective Tweak
        for t in tweaks:
            if is_selected( t ):
                layout.prop( pose_bones[ t ], '["rubber_tweak"]', slider = True )
        
        # IK Stretch and pole_vector on IK Control bone
        if is_selected( ik_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["IK_Stretch"]', slider = True )
            layout.prop( pose_bones[ parent ], '["pole_vector"]')
        
        # FK limb follow
        if is_selected( fk_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["FK_limb_follow"]', slider = True )
        
        controls = ['thigh_ik.L', 'foot_ik.L', 'foot_heel_ik.L', 'thigh_parent.L']
        ctrl    = 'thigh_parent.L'
        
        if is_selected( controls ):
            layout.prop( pose_bones[ ctrl ], '["IK_follow"]')
            if 'pole_follow' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["pole_follow"]', slider = True )
            if 'root/parent' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["root/parent"]', slider = True )
        

        
        controls = ['thigh_ik.R', 'thigh_fk.R', 'shin_fk.R', 'foot_fk.R', 'toe.R', 'foot_heel_ik.R', 'foot_ik.R', 'MCH-foot_fk.R', 'thigh_parent.R']
        tweaks   = ['thigh_tweak.R.001', 'shin_tweak.R', 'shin_tweak.R.001']
        ik_ctrl  = ['foot_ik.R', 'MCH-thigh_ik.R', 'MCH-thigh_ik_target.R']
        fk_ctrl  = 'thigh_fk.R'
        parent   = 'thigh_parent.R'
        foot_fk = 'foot_fk.R'
        pole = 'thigh_ik_target.R'
        
        # IK/FK Switch on all Control Bones
        if is_selected( controls ):
            layout.prop( pose_bones[parent], '["IK_FK"]', slider = True )
            props = layout.operator("pose.rigify_leg_fk2ik_" + rig_id, text="Snap FK->IK (" + fk_ctrl + ")")
            props.thigh_fk = controls[1]
            props.shin_fk  = controls[2]
            props.foot_fk  = controls[3]
            props.mfoot_fk = controls[7]
            props.thigh_ik = controls[0]
            props.shin_ik  = ik_ctrl[1]
            props.foot_ik = ik_ctrl[2]
            props.mfoot_ik = ik_ctrl[2]
            props = layout.operator("pose.rigify_leg_ik2fk_" + rig_id, text="Snap IK->FK (" + fk_ctrl + ")")
            props.thigh_fk  = controls[1]
            props.shin_fk   = controls[2]
            props.foot_fk  = controls[3]
            props.mfoot_fk  = controls[7]
            props.thigh_ik  = controls[0]
            props.shin_ik   = ik_ctrl[1]
            props.foot_ik   = controls[6]
            props.pole      = pole
            props.footroll  = controls[5]
            props.mfoot_ik  = ik_ctrl[2]
            props.main_parent = parent
        
        # BBone rubber hose on each Respective Tweak
        for t in tweaks:
            if is_selected( t ):
                layout.prop( pose_bones[ t ], '["rubber_tweak"]', slider = True )
        
        # IK Stretch and pole_vector on IK Control bone
        if is_selected( ik_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["IK_Stretch"]', slider = True )
            layout.prop( pose_bones[ parent ], '["pole_vector"]')
        
        # FK limb follow
        if is_selected( fk_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["FK_limb_follow"]', slider = True )
        
        controls = ['thigh_ik.R', 'foot_ik.R', 'foot_heel_ik.R', 'thigh_parent.R']
        ctrl    = 'thigh_parent.R'
        
        if is_selected( controls ):
            layout.prop( pose_bones[ ctrl ], '["IK_follow"]')
            if 'pole_follow' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["pole_follow"]', slider = True )
            if 'root/parent' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["root/parent"]', slider = True )
        

        
        controls    = ['leginfinger.l', 'leginfinger1.l', 'leginfinger2.l', 'leginfinger3.l', 'leginfin_master.l']
        master_name = 'leginfin_master.l'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['leginfinger.r', 'leginfinger1.r', 'leginfinger2.r', 'leginfinger3.r', 'leginfin_master.r']
        master_name = 'leginfin_master.r'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['legmidfinger.l', 'legmidfinger1.l', 'legmidfinger2.l', 'legmidfinger3.l', 'legmidfin_master.l']
        master_name = 'legmidfin_master.l'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['legmidfinger.r', 'legmidfinger1.r', 'legmidfinger2.r', 'legmidfinger3.r', 'legmidfin_master.r']
        master_name = 'legmidfin_master.r'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['legoutfinger.l', 'legoutfinger1.l', 'legoutfinger2.l', 'legoutfinger3.l', 'legoutfin_master.l']
        master_name = 'legoutfin_master.l'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['legoutfinger.r', 'legoutfinger1.r', 'legoutfinger2.r', 'legoutfinger3.r', 'legoutfin_master.r']
        master_name = 'legoutfin_master.r'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls = ['upper_arm_ik.L', 'upper_arm_fk.L', 'forearm_fk.L', 'hand_fk.L', 'hand_ik.L', 'MCH-hand_fk.L', 'upper_arm_parent.L']
        tweaks   = ['upper_arm_tweak.L.001', 'upper_arm_tweak.L.002', 'upper_arm_tweak.L.003', 'forearm_tweak.L', 'forearm_tweak.L.001', 'forearm_tweak.L.002', 'forearm_tweak.L.003']
        ik_ctrl  = ['hand_ik.L', 'MCH-upper_arm_ik.L', 'MCH-upper_arm_ik_target.L']
        fk_ctrl  = 'upper_arm_fk.L'
        parent   = 'upper_arm_parent.L'
        hand_fk   = 'hand_fk.L'
        pole = 'upper_arm_ik_target.L'
        
        # IK/FK Switch on all Control Bones
        if is_selected( controls ):
            layout.prop( pose_bones[parent], '["IK_FK"]', slider = True )
            props = layout.operator("pose.rigify_arm_fk2ik_" + rig_id, text="Snap FK->IK (" + fk_ctrl + ")")
            props.uarm_fk = controls[1]
            props.farm_fk = controls[2]
            props.hand_fk = controls[3]
            props.uarm_ik = controls[0]
            props.farm_ik = ik_ctrl[1]
            props.hand_ik = controls[4]
            props = layout.operator("pose.rigify_arm_ik2fk_" + rig_id, text="Snap IK->FK (" + fk_ctrl + ")")
            props.uarm_fk = controls[1]
            props.farm_fk = controls[2]
            props.hand_fk = controls[3]
            props.uarm_ik = controls[0]
            props.farm_ik = ik_ctrl[1]
            props.hand_ik = controls[4]
            props.pole = pole
            props.main_parent = parent
        
        
        # BBone rubber hose on each Respective Tweak
        for t in tweaks:
            if is_selected( t ):
                layout.prop( pose_bones[ t ], '["rubber_tweak"]', slider = True )
                
        # IK Stretch and pole_vector on IK Control bone
        if is_selected( ik_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["IK_Stretch"]', slider = True )
            layout.prop( pose_bones[ parent ], '["pole_vector"]')
        
        # FK limb follow
        if is_selected( fk_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["FK_limb_follow"]', slider = True )
        
        controls = ['upper_arm_ik.L', 'hand_ik.L', 'upper_arm_parent.L']
        ctrl    = 'upper_arm_parent.L'
        
        if is_selected( controls ):
            layout.prop( pose_bones[ ctrl ], '["IK_follow"]')
            if 'pole_follow' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["pole_follow"]', slider = True )
            if 'root/parent' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["root/parent"]', slider = True )
        

        
        controls = ['upper_arm_ik.R', 'upper_arm_fk.R', 'forearm_fk.R', 'hand_fk.R', 'hand_ik.R', 'MCH-hand_fk.R', 'upper_arm_parent.R']
        tweaks   = ['upper_arm_tweak.R.001', 'upper_arm_tweak.R.002', 'upper_arm_tweak.R.003', 'forearm_tweak.R', 'forearm_tweak.R.001', 'forearm_tweak.R.002', 'forearm_tweak.R.003']
        ik_ctrl  = ['hand_ik.R', 'MCH-upper_arm_ik.R', 'MCH-upper_arm_ik_target.R']
        fk_ctrl  = 'upper_arm_fk.R'
        parent   = 'upper_arm_parent.R'
        hand_fk   = 'hand_fk.R'
        pole = 'upper_arm_ik_target.R'
        
        # IK/FK Switch on all Control Bones
        if is_selected( controls ):
            layout.prop( pose_bones[parent], '["IK_FK"]', slider = True )
            props = layout.operator("pose.rigify_arm_fk2ik_" + rig_id, text="Snap FK->IK (" + fk_ctrl + ")")
            props.uarm_fk = controls[1]
            props.farm_fk = controls[2]
            props.hand_fk = controls[3]
            props.uarm_ik = controls[0]
            props.farm_ik = ik_ctrl[1]
            props.hand_ik = controls[4]
            props = layout.operator("pose.rigify_arm_ik2fk_" + rig_id, text="Snap IK->FK (" + fk_ctrl + ")")
            props.uarm_fk = controls[1]
            props.farm_fk = controls[2]
            props.hand_fk = controls[3]
            props.uarm_ik = controls[0]
            props.farm_ik = ik_ctrl[1]
            props.hand_ik = controls[4]
            props.pole = pole
            props.main_parent = parent
        
        
        # BBone rubber hose on each Respective Tweak
        for t in tweaks:
            if is_selected( t ):
                layout.prop( pose_bones[ t ], '["rubber_tweak"]', slider = True )
                
        # IK Stretch and pole_vector on IK Control bone
        if is_selected( ik_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["IK_Stretch"]', slider = True )
            layout.prop( pose_bones[ parent ], '["pole_vector"]')
        
        # FK limb follow
        if is_selected( fk_ctrl ) or is_selected(parent):
            layout.prop( pose_bones[ parent ], '["FK_limb_follow"]', slider = True )
        
        controls = ['upper_arm_ik.R', 'hand_ik.R', 'upper_arm_parent.R']
        ctrl    = 'upper_arm_parent.R'
        
        if is_selected( controls ):
            layout.prop( pose_bones[ ctrl ], '["IK_follow"]')
            if 'pole_follow' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["pole_follow"]', slider = True )
            if 'root/parent' in pose_bones[ctrl].keys():
                layout.prop( pose_bones[ ctrl ], '["root/parent"]', slider = True )
        

        
        controls    = ['f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'f_index_master.L']
        master_name = 'f_index_master.L'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'f_index_master.R']
        master_name = 'f_index_master.R'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'f_middle.03.L.001', 'f_middle_master.L']
        master_name = 'f_middle_master.L'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'f_middle.03.R.001', 'f_middle_master.R']
        master_name = 'f_middle_master.R'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'f_pinky.03.L.001', 'f_pinky_master.L']
        master_name = 'f_pinky_master.L'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R', 'f_pinky.03.R.001', 'f_pinky_master.R']
        master_name = 'f_pinky_master.R'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'f_ring.03.L.001', 'f_ring_master.L']
        master_name = 'f_ring_master.L'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
        

        
        controls    = ['f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'f_ring.03.R.001', 'f_ring_master.R']
        master_name = 'f_ring_master.R'
        if is_selected(controls):
            layout.prop(pose_bones[master_name], '["finger_curve"]', text="Curvature", slider=True)
               
               
###### Update Function ######
def prop_update(self, context):
    Hiding(context)

def Hiding(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    

    p_bones = bpy.context.active_object.pose.bones
    
    dict={"upperTeeth":"HideUpperTeethRig", "lowerTeeth":"HideLowerTeethRig", "faketeeth":"HideFakeTeethRig", "Tongue":"HideTongueRig", "fakeLeg01":"HideFakeLeg01Rig", "fakeLeg02":"HideFakeLeg02Rig", "fakeLeg03":"HideFakeLeg03Rig", "stroke_main1":"HideStroke01Rig", "stroke_main2":"HideStroke02Rig", "singlefoot":"HideSingleFootRig","innermouth":"HideInnerMouthRig","fakehand.R":"HidefakehandRRig","fakehand.L":"HidefakehandLRig","handstroke1.R":"Hidehandstroke1RRig","handstroke2.R":"Hidehandstroke2RRig","handstroke1.L":"Hidehandstroke1LRig","handstroke2.L":"Hidehandstroke2LRig"}

    
    #rigArmDict = {"Andyrig.":"armature_andy.","Pirkirig.":"armature_pirki."}
    #rigArmDict = {"Pirkirig.":"armature_pirki."}
    
    ob = bpy.context.object

    if ob.type == 'ARMATURE':
        armature = ob.data
        #print(armature)
        #print(ob.name)
    
        for b in p_bones:
            for key in dict.keys():
                if (key in b.name):
                    prop = armature[dict[key]]
                    bone = bpy.data.objects[ob.name].pose.bones[b.name].bone
                    if prop == 1:
                        bone.hide = False
                    else:
                        bone.hide = True
    
   
                                
                  
    
                        
 
                        
                
###### Creating Properties ######
bpy.types.Armature.HideUpperTeethRig = BoolProperty(name="HideUpperTeethRig", description="Upper Teeth Rig", default=False, update=prop_update)
bpy.types.Armature.HideLowerTeethRig = BoolProperty(name="HideLowerTeethRig", description="Lower Teeth Rig", default=False, update=prop_update)
bpy.types.Armature.HideFakeTeethRig = BoolProperty(name="HideFakeTeethRig", description="Fake Teeth Rig", default=False, update=prop_update)
bpy.types.Armature.HideTongueRig = BoolProperty(name="HideTongueRig", description="Tongue Rig", default=False, update=prop_update)
bpy.types.Armature.HideFakeLeg01Rig= BoolProperty(name="HideFakeLeg01Rig", description="FakeLeg01 Rig", default=False, update=prop_update)
bpy.types.Armature.HideFakeLeg02Rig= BoolProperty(name="HideFakeLeg02Rig", description="FakeLeg02 Rig", default=False, update=prop_update)
bpy.types.Armature.HideFakeLeg03Rig= BoolProperty(name="HideFakeLeg03Rig", description="FakeLeg03 Rig", default=False, update=prop_update)
bpy.types.Armature.HideStroke01Rig = BoolProperty(name="HideStroke01Rig", description="Stroke01 Rig", default=False, update=prop_update)
bpy.types.Armature.HideStroke02Rig = BoolProperty(name="HideStroke02Rig", description="Stroke02 Rig", default=False, update=prop_update)
bpy.types.Armature.HideSingleFootRig = BoolProperty(name="HideSingleFootRig", description="SingleFootMesh Rig", default=False, update=prop_update)
bpy.types.Armature.HideInnerMouthRig = BoolProperty(name="HideInnermouthRig", description="InnermouthRig", default=False, update=prop_update)
bpy.types.Armature.HidefakehandRRig = BoolProperty(name="HidefakehandRRig", description="fakehandRRig", default=False, update=prop_update)
bpy.types.Armature.HidefakehandLRig = BoolProperty(name="HidefakehandLRig", description="fakehandLRig", default=False, update=prop_update)
bpy.types.Armature.Hidehandstroke1RRig = BoolProperty(name="Hidehandstroke1RRig", description="handstroke1R", default=False, update=prop_update)
bpy.types.Armature.Hidehandstroke2RRig = BoolProperty(name="Hidehandstroke2RRig", description="handstroke2R", default=False, update=prop_update)
bpy.types.Armature.Hidehandstroke1LRig = BoolProperty(name="Hidehandstroke1LRig", description="handstroke1L", default=False, update=prop_update)
bpy.types.Armature.Hidehandstroke2LRig = BoolProperty(name="Hidehandstroke2LRig", description="handstroke2L", default=False, update=prop_update)

              
class Mouth(bpy.types.Panel):
    bl_label = "Mouth"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        row = col.split()
        row.prop(context.active_object.data, "HideUpperTeethRig", text="Upper Teeth Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideUpperTeethMesh"]', text="Upper Teeth Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideLowerTeethRig", text="Lower Teeth Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideLowerTeethMesh"]', text="Lower Teeth Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideFakeTeethRig", text="Fake Teeth Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideFakeTeethMesh"]', text="Fake Teeth Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideTongueRig", text="Tongue Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideTongueMesh"]', text="Tongue Teeth Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideInnerMouthRig", text="innermouth Rig", slider=False)


class FakeHand(bpy.types.Panel):
    bl_label = "FakeHand"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        row = col.split()
        row.prop(context.active_object.data, "HidefakehandRRig", text="R fakehand Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideRfakehandMesh"]', text="R fakehand Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HidefakehandLRig", text="L fakehand Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideLfakehandMesh"]', text="L fakehand Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "Hidehandstroke1RRig", text="R handstroke1 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideRhandstroke1Mesh"]', text="R handstroke1 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "Hidehandstroke2RRig", text="R handstroke2 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideRhandstroke2Mesh"]', text="R handstroke2 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "Hidehandstroke1LRig", text="L handstroke1 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideLhandstroke1Mesh"]', text="L handstroke1 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "Hidehandstroke2LRig", text="L handstroke1 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideLhandstroke2Mesh"]', text="L handstroke2 Mesh", slider=False)
        
                

class FakeLeg(bpy.types.Panel):
    bl_label = "FakeLeg"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        row = col.split()
        row.prop(context.active_object.data, "HideFakeLeg01Rig", text="Fake Leg01 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideFakeLeg01Mesh"]', text="Fake Leg01 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideFakeLeg02Rig", text="Fake Leg02 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideFakeLeg02Mesh"]', text="Fake Leg02 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideFakeLeg03Rig", text="Fake Leg03 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideFakeLeg03Mesh"]', text="Fake Leg03 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideStroke01Rig", text="Stroke01 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideStroke01Mesh"]', text="Stroke01 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideStroke02Rig", text="Stroke02 Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideStroke02Mesh"]', text="Stroke02 Mesh", slider=False)
        row = col.split()
        row.prop(context.active_object.data, "HideSingleFootRig", text="SingleFoot Rig", slider=False)
        row = row.split()
        row.prop(context.active_object.data, '["HideSingleFootMesh"]', text="SingleFoot Mesh", slider=False)
        
class Mask(bpy.types.Panel):
    bl_label = "Mask"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
   
    
    def draw(self, context):
        layout = self.layout 
        col = layout.column()
        
        col.prop(context.active_object.data, '["headmask"]', text="headmask", slider=True)
        col.prop(context.active_object.data, '["bodymask"]', text="bodymask", slider=True)
        col.prop(context.active_object.data, '["handmask"]', text="handmask", slider=True)  
        col.prop(context.active_object.data, '["legmask"]', text="legmask", slider=True)
        col.prop(context.active_object.data, '["tailmask"]', text="tailmask", slider=True)               
        
        
class Properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'        
        
        
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        pose_bones = context.active_object.pose.bones
        try:
            
            for p in context.selected_pose_bones:
                propList = p.keys()
                #print(propList)
                if propList:
                    for k in propList:
                        if k not in '_RNA_UI':
                            #print(k)
                            layout.prop(context.selected_pose_bones[0], '["%s"]'%k, text=k, slider=True)
                            
        except (AttributeError, TypeError):
            return



# Data Structure ##############################################################

# Note: bones are stored by name, this means that if the bone is renamed,
# there can be problems. However, bone renaming is unlikely during animation
class SelectionEntry(PropertyGroup):
    name = StringProperty(name="Bone Name")


class SelectionSet(PropertyGroup):
    name = StringProperty(name="Set Name")
    bone_ids = CollectionProperty(type=SelectionEntry)


# UI Panel w/ UIList ##########################################################

class POSE_MT_selection_sets_specials(Menu):
    bl_label = "Selection Sets Specials"

    def draw(self, context):
        layout = self.layout

        layout.operator("pose.selection_set_delete_all", icon='X')
        layout.operator("pose.selection_set_remove_bones", icon='X')


class POSE_PT_selection_sets(Panel):
    bl_label = "Selection Sets"
    bl_category = "RigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = "data"    

    @classmethod
    def poll(cls, context):
        return (context.object
            and context.object.type == 'ARMATURE'
            and context.object.pose)

    def draw(self, context):
        layout = self.layout

        ob = context.object
        arm = context.object

        row = layout.row()
        row.enabled = (context.mode == 'POSE')

        # UI list
        rows = 4  if len(arm.selection_sets) > 0 else 1
        row.template_list(
            "POSE_UL_selection_set", "", # type and unique id
            arm, "selection_sets", # pointer to the CollectionProperty
            arm, "active_selection_set", # pointer to the active identifier
            rows=rows
        )

        # add/remove/specials UI list Menu
        col = row.column(align=True)
        col.operator("pose.selection_set_add", icon='ZOOMIN', text="")
        col.operator("pose.selection_set_remove", icon='ZOOMOUT', text="")
        col.menu("POSE_MT_selection_sets_specials", icon='DOWNARROW_HLT', text="")

        # move up/down arrows
        if len(arm.selection_sets) > 0:
            col.separator()
            col.operator("pose.selection_set_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("pose.selection_set_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        # buttons
        row = layout.row()

        sub = row.row(align=True)
        sub.operator("pose.selection_set_assign", text="Assign")
        sub.operator("pose.selection_set_unassign", text="Remove")

        sub = row.row(align=True)
        sub.operator("pose.selection_set_select", text="Select")
        sub.operator("pose.selection_set_deselect", text="Deselect")


class POSE_UL_selection_set(UIList):
    def draw_item(self, context, layout, data, set, icon, active_data, active_propname, index):
        layout.prop(set, "name", text="", icon='GROUP_BONE', emboss=False)


class POSE_MT_create_new_selection_set(Menu):
    bl_idname = "pose.selection_set_create_new_popup"
    bl_label = "Choose Selection Set"

    def draw(self, context):
        layout = self.layout
        layout.operator("pose.selection_set_add_and_assign",
            text="New Selection Set")


# Operators ###################################################################

class PluginOperator(Operator):
    @classmethod
    def poll(self, context):
        return (context.object and
                context.object.type == 'ARMATURE' and
                context.mode == 'POSE')

class NeedSelSetPluginOperator(PluginOperator):
    @classmethod
    def poll(self, context):
        if super().poll(context):
            arm =  context.object
            return (arm.active_selection_set < len(arm.selection_sets)
                and arm.active_selection_set >= 0)
        return False


class POSE_OT_selection_set_delete_all(PluginOperator):
    bl_idname = "pose.selection_set_delete_all"
    bl_label = "Delete All Sets"
    bl_description = "Deletes All Selection Sets"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        arm.selection_sets.clear()
        return {'FINISHED'}


class POSE_OT_selection_set_remove_bones(PluginOperator):
    bl_idname = "pose.selection_set_remove_bones"
    bl_label = "Remove Bones from Sets"
    bl_description = "Removes the Active Bones from All Sets"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            for selset in arm.selection_sets:
                if bone.name in selset.bone_ids:
                    idx = selset.bone_ids.find(bone.name)
                    selset.bone_ids.remove(idx)

        return {'FINISHED'}


class POSE_OT_selection_set_move(NeedSelSetPluginOperator):
    bl_idname = "pose.selection_set_move"
    bl_label = "Move Selection Set in List"
    bl_description = "Move the active Selection Set up/down the list of sets"
    bl_options = {'UNDO', 'REGISTER'}

    direction = EnumProperty(
        name="Move Direction",
        description="Direction to move the active Selection Set: UP (default) or DOWN",
        items=[
            ('UP', "Up", "", -1),
            ('DOWN', "Down", "", 1),
        ],
        default='UP'
    )

    @classmethod
    def poll(self, context):
        if super().poll(context):
            arm =  context.object
            return len(arm.selection_sets) > 1
        return False

    def execute(self, context):
        arm = context.object

        active_idx = arm.active_selection_set
        new_idx = active_idx + (-1 if self.direction == 'UP' else 1)

        if new_idx < 0 or new_idx >= len(arm.selection_sets):
            return {'FINISHED'}

        arm.selection_sets.move(active_idx, new_idx)
        arm.active_selection_set = new_idx

        return {'FINISHED'}


class POSE_OT_selection_set_add(PluginOperator):
    bl_idname = "pose.selection_set_add"
    bl_label = "Create Selection Set"
    bl_description = "Creates a new empty Selection Set"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):
        arm = context.object

        new_sel_set = arm.selection_sets.add()

        # naming
        if "SelectionSet" not in arm.selection_sets:
            new_sel_set.name  = "SelectionSet"
        else:
            sorted_sets = []
            for selset in arm.selection_sets:
                if selset.name.startswith("SelectionSet."):
                    index = selset.name[13:]
                    if index.isdigit():
                        sorted_sets.append(index)
            sorted_sets = sorted(sorted_sets)
            min_index = 1
            for num in sorted_sets:
                num = int(num)
                if min_index < num:
                    break
                min_index = num + 1
            new_sel_set.name = "SelectionSet.{:03d}".format(min_index)

        # select newly created set
        arm.active_selection_set = len(arm.selection_sets) - 1

        return {'FINISHED'}


class POSE_OT_selection_set_remove(NeedSelSetPluginOperator):
    bl_idname = "pose.selection_set_remove"
    bl_label = "Delete Selection Set"
    bl_description = "Delete a Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object

        arm.selection_sets.remove(arm.active_selection_set)

        # change currently active selection set
        numsets = len(arm.selection_sets)
        if (arm.active_selection_set > (numsets - 1) and numsets > 0):
            arm.active_selection_set = len(arm.selection_sets) - 1

        return {'FINISHED'}


class POSE_OT_selection_set_assign(PluginOperator):
    bl_idname = "pose.selection_set_assign"
    bl_label = "Add Bones to Selection Set"
    bl_description = "Add selected bones to Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def invoke(self, context, event):
        arm = context.object

        if not (arm.active_selection_set < len(arm.selection_sets)):
            bpy.ops.wm.call_menu("INVOKE_DEFAULT",
                name="pose.selection_set_create_new_popup")
        else:
            bpy.ops.pose.selection_set_assign('EXEC_DEFAULT')

        return {'FINISHED'}


    def execute(self, context):
        arm = context.object
        act_sel_set = arm.selection_sets[arm.active_selection_set]

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            if bone.name not in act_sel_set.bone_ids:
                bone_id = act_sel_set.bone_ids.add()
                bone_id.name = bone.name

        return {'FINISHED'}


class POSE_OT_selection_set_unassign(NeedSelSetPluginOperator):
    bl_idname = "pose.selection_set_unassign"
    bl_label = "Remove Bones from Selection Set"
    bl_description = "Remove selected bones from Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.selection_sets[arm.active_selection_set]

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            if bone.name in act_sel_set.bone_ids:
                idx = act_sel_set.bone_ids.find(bone.name)
                act_sel_set.bone_ids.remove(idx)

        return {'FINISHED'}


class POSE_OT_selection_set_select(NeedSelSetPluginOperator):
    bl_idname = "pose.selection_set_select"
    bl_label = "Select Selection Set"
    bl_description = "Add Selection Set bones to current selection"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.selection_sets[arm.active_selection_set]

        for bone in context.visible_pose_bones:
            if bone.name in act_sel_set.bone_ids:
                 bone.bone.select = True

        return {'FINISHED'}


class POSE_OT_selection_set_deselect(NeedSelSetPluginOperator):
    bl_idname = "pose.selection_set_deselect"
    bl_label = "Deselect Selection Set"
    bl_description = "Remove Selection Set bones from current selection"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.selection_sets[arm.active_selection_set]

        for bone in context.selected_pose_bones:
            if bone.name in act_sel_set.bone_ids:
                bone.bone.select = False

        return {'FINISHED'}


class POSE_OT_selection_set_add_and_assign(PluginOperator):
    bl_idname = "pose.selection_set_add_and_assign"
    bl_label = "Create and Add Bones to Selection Set"
    bl_description = "Creates a new Selection Set with the currently selected bones"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        bpy.ops.pose.selection_set_add('EXEC_DEFAULT')
        bpy.ops.pose.selection_set_assign('EXEC_DEFAULT')
        return {'FINISHED'}

# Registry ####################################################################

classes = (
    POSE_MT_create_new_selection_set,
    POSE_MT_selection_sets_specials,
    POSE_PT_selection_sets,
    POSE_UL_selection_set,
    SelectionEntry,
    SelectionSet,
    POSE_OT_selection_set_delete_all,
    POSE_OT_selection_set_remove_bones,
    POSE_OT_selection_set_move,
    POSE_OT_selection_set_add,
    POSE_OT_selection_set_remove,
    POSE_OT_selection_set_assign,
    POSE_OT_selection_set_unassign,
    POSE_OT_selection_set_select,
    POSE_OT_selection_set_deselect,
    POSE_OT_selection_set_add_and_assign,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.selection_sets = CollectionProperty(
        type=SelectionSet,
        name="Selection Sets",
        description="List of groups of bones for easy selection"
    )
    bpy.types.Object.active_selection_set = IntProperty(
        name="Active Selection Set",
        description="Index of the currently active selection set",
        default=0
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.selection_sets
    del bpy.types.Object.active_selection_set

# def register():
#     bpy.utils.register_class(Rigify_Arm_FK2IK)
#     bpy.utils.register_class(Rigify_Arm_IK2FK)
#     bpy.utils.register_class(Rigify_Leg_FK2IK)
#     bpy.utils.register_class(Rigify_Leg_IK2FK)
#     bpy.utils.register_class(RigLayers)
#     bpy.utils.register_class(Mouth)
#     bpy.utils.register_class(Rigmain)
#     bpy.utils.register_class(FakeLeg)
#     bpy.utils.register_class(Mask)
#     bpy.utils.register_class(Properties)
#
#
# def unregister():
#     bpy.utils.unregister_class(Rigify_Arm_FK2IK)
#     bpy.utils.unregister_class(Rigify_Arm_IK2FK)
#     bpy.utils.unregister_class(Rigify_Leg_FK2IK)
#     bpy.utils.unregister_class(Rigify_Leg_IK2FK)
#     bpy.utils.unregister_class(RigLayers)
#     bpy.utils.unregister_class(Mouth)
#     bpy.utils.unregister_class(Rigmain)
#     bpy.utils.unregister_class(FakeLeg)
#     bpy.utils.unregister_class(Mask)
#     bpy.utils.unregister_class(Properties)
#
# register()
  
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
