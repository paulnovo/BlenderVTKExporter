bl_info = {
    "name": "VTK Exporter",
    "description": "Exports current mesh to a VTK poly data file.",
    "author": "Paul Novotny",
    "version": (0, 1),
    "blender": (2, 59, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}


import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty


def get_current_mesh():
    scene = bpy.data.scenes[0]
    obj = scene.objects.active
    mesh = obj.data
    return mesh


class ExportVTKData(bpy.types.Operator, ExportHelper):
    '''Export the currently selected mesh to a vtk poly file'''
    bl_idname = "export.vtk"  # this is important since its how bpy.ops.export.some_data is constructed
    bl_label = "Export Mesh to VTK"

    # ExportHelper mixin class uses this
    filename_ext = ".vtk"

    filter_glob = StringProperty(default="*.vtk", options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        with open(self.filepath, 'w') as f:
            mesh = get_current_mesh()
            f.write("# vtk DataFile Version 3.0\n")
            f.write("vtk output\n")
            f.write("ASCII\n")
            f.write("DATASET POLYDATA\n")

            f.write("POINTS {0} float\n".format(len(mesh.vertices)))
            for vertex in mesh.vertices:
                f.write("{0} {1} {2}\n".format(*vertex.co))

            num_entries = 3*len(mesh.edges)
            f.write("LINES %i %i\n" % (len(mesh.edges), num_entries))
            for edge in mesh.edges:
                f.write("2 {0} {1}\n".format(*edge.vertices))

            num_entries = 0
            for face in mesh.faces:
                num_entries += len(face.vertices) + 1
            f.write("\nPOLYGONS {0} {1}\n".format(len(mesh.faces), num_entries))
            for face in mesh.faces:
                vertices= " ".join(["{0}".format(v) for v in face.vertices])
                f.write("{0} {1}\n".format(len(face.vertices), vertices))

        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(ExportVTKData.bl_idname, text="VTK Export Operator")


def register():
    bpy.utils.register_class(ExportVTKData)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportVTKData)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export.vtk('INVOKE_DEFAULT')

