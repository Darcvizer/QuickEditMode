import bpy


bl_info = {
	"name": "Quick Edit Mode :)",
	"location": "View3D > Add > Mesh > Quick Edit Mode,",
	"description": ".",
	"author": "Vladislav Kindushov",
	"version": (1, 0, 0),
	"blender": (2, 80, 0),
	"category": "Mesh",
}

def check(context):
	act = False
	if context.active_object != None:
		if context.active_object.type == 'MESH' or context.active_object.type ==  'CURVE':
			act = True
		else:
			curve = None
			mesh = None
			end = True
			if len(context.selected_objects) != 0:
				for i in context.selected_objects:
					if i.type ==  'CURVE':
						curve = i
					if i.type == 'MESH':
						mesh = i
						context.view_layer.objects.active = i
						act = True
						end = False
						break
				if end:
					context.view_layer.objects.active = curve


	return act


class SetVerts(bpy.types.Operator):
	bl_idname = "mesh.set_verts"
	bl_label = "SetVerts"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.space_data.type == "VIEW_3D"

	def execute(self, context):
		if check(context):
			if bpy.context.mode == 'EDIT_MESH':
				if context.active_object.type !=  'CURVE':
					bpy.ops.mesh.select_mode(type="VERT")
			else:
				bpy.ops.object.mode_set(mode='EDIT')
				if context.active_object.type != 'CURVE':
					bpy.ops.mesh.select_mode(type="VERT")

		return {'FINISHED'}

class SetEdges(bpy.types.Operator):
	bl_idname = "mesh.set_edges"
	bl_label = "SetEdges"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.space_data.type == "VIEW_3D"

	def execute(self, context):
		if check(context):
			if bpy.context.mode == 'EDIT_MESH':
				if context.active_object.type !=  'CURVE':
					bpy.ops.mesh.select_mode(type="EDGE")
			else:
				bpy.ops.object.mode_set(mode='EDIT')
				if context.active_object.type != 'CURVE':
					bpy.ops.mesh.select_mode(type="EDGE")

		return {'FINISHED'}

class SetFaces(bpy.types.Operator):
	bl_idname = "mesh.set_faces"
	bl_label = "SetFaces"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.space_data.type == "VIEW_3D"

	def execute(self, context):
		if check(context):
			if bpy.context.mode == 'EDIT_MESH':
				if context.active_object.type !=  'CURVE':
					bpy.ops.mesh.select_mode(type="FACE")
			else:
				bpy.ops.object.mode_set(mode='EDIT')
				if context.active_object.type != 'CURVE':
					bpy.ops.mesh.select_mode(type="FACE")

		return {'FINISHED'}

class SetObjectMode(bpy.types.Operator):
	bl_idname = "mesh.set_mode"
	bl_label = "SetObjectMode"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.space_data.type == "VIEW_3D"

	def execute(self, context):
		if bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'EDIT_CURVE':
			bpy.ops.object.mode_set(mode='OBJECT')
		else:
			if check(context):
				bpy.ops.object.mode_set(mode='EDIT')

		return {'FINISHED'}


classes = (SetVerts, SetEdges, SetFaces, SetObjectMode)

def register():
	for c in classes:
		bpy.utils.register_class(c)
	activConfig = bpy.context.window_manager.keyconfigs.active.name
	i = 0
	count = 0
	while (True):
		if bpy.context.window_manager.keyconfigs[activConfig].keymaps['Mesh'].keymap_items[i].idname == 'mesh.select_mode':
			bpy.context.window_manager.keyconfigs[activConfig].keymaps['Mesh'].keymap_items[i].active = False
			count = count + 1
		if count == 3:
			break
		i = i + 1
	i = 0
	count = 0
	while (True):
		if bpy.context.window_manager.keyconfigs[activConfig].keymaps['Object Mode'].keymap_items[i].idname == 'object.hide_collection':
			z = bpy.context.window_manager.keyconfigs[activConfig].keymaps['Object Mode'].keymap_items[i]
			if z.type == 'ONE' or z.type == 'TWO' or z.type == 'THREE' or z.type == 'FOUR':
				z.active = False
				count = count + 1
		if count == 4:
			break
		i = i + 1

	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
		kmi = km.keymap_items.new('mesh.set_verts', 'ONE', 'PRESS', )
		kmi = km.keymap_items.new('mesh.set_edges', 'TWO', 'PRESS', )
		kmi = km.keymap_items.new('mesh.set_faces', 'THREE', 'PRESS', )
		kmi = km.keymap_items.new('mesh.set_mode', 'FOUR', 'PRESS', )


def unregister():
	for c in reversed(classes):
		bpy.utils.unregister_class(c)

	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps["3D View"]
		for kmi in km.keymap_items:
			if kmi.idname == 'mesh.set_verts' or kmi.idname == 'mesh.set_edges' or kmi.idname == 'mesh.set_verts' or kmi.idname == 'mesh.set_mode':
				km.keymap_items.remove(kmi)
	activConfig = bpy.context.window_manager.keyconfigs.active.name
	i = 0
	count = 0
	while (True):
		if bpy.context.window_manager.keyconfigs[activConfig].keymaps['Mesh'].keymap_items[i].idname == 'mesh.select_mode':
			bpy.context.window_manager.keyconfigs[activConfig].keymaps['Mesh'].keymap_items[i].active = True
			count = count + 1

		if count == 3:
			break
		i = i + 1
	i = 0
	count = 0
	while (True):
		if bpy.context.window_manager.keyconfigs[activConfig].keymaps['Object Mode'].keymap_items[i].idname == 'object.hide_collection':
			z = bpy.context.window_manager.keyconfigs[activConfig].keymaps['Object Mode'].keymap_items[i]
			if z.type == 'ONE' or z.type == 'TWO' or z.type == 'THREE' or z.type == 'FOUR':
				z.active = True
				count = count + 1


		if count == 4:
			break
		i = i + 1


if __name__ == "__main__":
	register()
