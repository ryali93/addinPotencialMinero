from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()


class FallGeo(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.codi = args[2]
        self.desc = args[3]
        self.dist = args[4]
        self.tb_fallgeo = pmm_tb_fallageol(self.ws)
        self.fc_fallgeo = pmm_gpl_fallageol(self.ws)
        self.fields = {
            self.fc_fallgeo.codi: self.codi,
            self.fc_fallgeo.descripcion: self.desc,
            self.fc_fallgeo.distancia: self.dist
        }

    def get_domain(self):
        self.domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_fallgeo.path, [self.tb_fallgeo.nombre_falla]
        )]

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_fallgeo.path):
            raise RuntimeError(msg.error_gdb_type)

    def check_info(self):
        info = arcpy.da.SearchCursor(self.fc, ['OID@', self.desc, self.dist])
        errors = [x for x in info if x[1].lower() not in self.domain or x[-1] in (None, False, '', ' ')]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: FID: %s  |  %s  |  %s' % (x[0], x[1], x[-1]))
                raise RuntimeError(msg.error_info)

    def load_data(self):
        copy = arcpy.CopyFeatures_management(
            self.fc, "in_memory\\fallasGeologicas"
        )
        with arcpy.da.UpdateCursor(copy, [self.desc]) as cursorUC:
            for row in cursorUC:
                row[0] = row[0].lower()
                cursorUC.updateRow(row)
        del cursorUC

        arcpy.DeleteRows_management(self.fc_fallgeo.path)

        for k, v in self.fields.items():
            arcpy.AlterField_management(copy, v, k)

        arcpy.Append_management(
            copy, self.fc_fallgeo.path, "NO_TEST"
        )

    def main(self):
        arcpy.AddMessage(msg.init_process)
        self.get_domain()
        arcpy.AddMessage(msg.check_gdb)
        self.check_geodatabase()
        self.check_exist_feature()
        arcpy.AddMessage(msg.check_info)
        self.check_info()
        arcpy.AddMessage(msg.send_database)
        self.load_data()
        arcpy.AddMessage(msg.end_process)


if __name__ == '__main__':
    try:
        ws = arcpy.GetParameterAsText(0)
        fc = arcpy.GetParameterAsText(1)
        codi = arcpy.GetParameterAsText(2)
        desc = arcpy.GetParameterAsText(3)
        dist = arcpy.GetParameterAsText(4)

        poo = FallGeo(ws, fc, codi, desc, dist)
        poo.main()
        arcpy.SetParameterAsText(5, poo.fc_fallgeo.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
