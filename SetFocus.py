import bpy

bl_info = {
    "name": "Set Focus Point",
    "author": "Deep Belief",
    "version": (1, 3),
    "blender": (2, 93, 0),
    "location": "3D View > Sidebar > Set Focus",
    "description": "Sets the active object as the focus point for the camera's Depth of Field",
    "category": "3D View",
}

class SetFocusOperator(bpy.types.Operator):
    bl_idname = "object.set_focus_point"
    bl_label = "Set Focus Point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        camera = None
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                camera = obj
                break

        if camera is None:
            # Create new camera if it doesn't exist
            bpy.ops.object.camera_add(align='VIEW', enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0))
            camera = context.active_object
            camera.name = "Camera"
            bpy.ops.view3d.view_all()

        focus_object = context.active_object
        camera.select_set(True)
        context.view_layer.objects.active = camera

        camera.data.dof.use_dof = True
        camera.data.dof.focus_object = focus_object

        return {'FINISHED'}

class SetFocusPanel(bpy.types.Panel):
    bl_label = "Set Focus"
    bl_idname = "OBJECT_PT_set_focus"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Set Focus"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.set_focus_point")

        camera = context.scene.camera
        if camera:
            camera_data = camera.data
            col = layout.column()
            col.prop(camera_data.dof, "use_dof", text="Use Depth of Field")
            col.prop(camera_data.dof, "aperture_fstop", text="F-Stop")

def menu_func(self, context):
    self.layout.operator(SetFocusOperator.bl_idname)

def register():
    bpy.utils.register_class(SetFocusOperator)
    bpy.utils.register_class(SetFocusPanel)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SetFocusOperator)
    bpy.utils.unregister_class(SetFocusPanel)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
