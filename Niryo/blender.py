import bpy
import mathutils

bpy.ops.object.mode_set(mode='OBJECT')
armature = bpy.data.objects['Armature']
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')
bone = armature.pose.bones['Bone.003']
print(bone)
bone.location += mathutils.Vector((100, 0, 0))
bpy.ops.object.mode_set(mode='OBJECT')