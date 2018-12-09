bl_info = {
    "name": "Vertex IDs from Material",
    "description": "Stores Material IDs in Vertex Colors",
    "author": "OlesenJonas",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "Object Mode -> Toolbar",
    "category": "Object",
    "support": "COMMUNITY"
}

import bpy
import random


#########################################  END PRE STUFF #####################################################

class idTransfer(bpy.types.Operator):
    """idTransfer class"""
    bl_idname = "myops.add_idtransfer"
    bl_label = "Transfer to Vert Color"

    def execute(self,context):
        #
        #has to start in object mode
        #
        bpy.ops.object.mode_set(mode = 'OBJECT')
    

        context = bpy.context
        obj = context.object
        mesh = obj.data

        #create vert color layer if not already
        if not mesh.vertex_colors:
            mesh.vertex_colors.new()

        #Cancel if Object has no materials
        if len(obj.material_slots) == 0:
            bpy.context.window_manager.popup_menu(idTransfer.drawErr, title="No Material Data to transfer", icon='ERROR')
            return {"CANCELLED"}

        #iterate faces                                              
        for poly in mesh.polygons:
            mat = obj.material_slots[poly.material_index].material
            rgb = mat.diffuse_color
            if mat is None:
                bpy.context.window_manager.popup_menu(idTransfer.drawErr, title="No Material Data to transfer", icon='ERROR')
                return {"CANCELLED"}
            else:
                for loop_index in poly.loop_indices:
                    mesh.vertex_colors.active.data[loop_index].color[0] = rgb[0]
                    mesh.vertex_colors.active.data[loop_index].color[1] = rgb[1]
                    mesh.vertex_colors.active.data[loop_index].color[2] = rgb[2]

        #after transfer set viewport colors to white:
        for mat in obj.material_slots:
            mat.material.diffuse_color = [1.0,1.0,1.0]

        #at end switch to vertex paint to see change
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        bpy.context.window_manager.popup_menu(idTransfer.drawFin, title="Done!", icon='FILE_TICK')
        return {"FINISHED"}

    def drawErr(self, context):
        self.layout.label(text = "One or more faces have no material assigned")

    def drawFin(self, context):
        self.layout.label(text = "Change viewport color back to white to see result")


##############################     END FUNCTIONALITY CLASS    #################################################################



class idTransferPanel(bpy.types.Panel):
    #creating Panel
    bl_label = "ID Transfer Panel"
    bl_idname = "VIEW3D_OT_idtran"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VertColTransfer"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("myops.add_idtransfer")


###########################################    END UI-PANEL CLASS   ########################################################


classes = (
    idTransfer,
    idTransferPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == '__main__':
    register()