from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()


class DepoMin(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.unid = args[2]
        self.dimension = args[3]
        self.grade = args[4]
        self.value = args[5]
        self.fc_depomin = pmm_gpo_depmineral(self.ws)
        self.tb_grade = tb_nivel(self.ws)
        self.fields = {
            self.fc_depomin.grado: self.grade,
            self.fc_depomin.unidad: self.unid,
            self.fc_depomin.dimension: self.dimension,
            self.fc_depomin.valor: self.value
        }

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_depomin.path):
            raise RuntimeError(msg.error_gdb_type)

    def check_grade(self):
        domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_grade.path, [self.tb_grade.grado]
        )]
        info = [x for x in arcpy.da.SearchCursor(self.fc, ['OID@', self.grade])]
        errors = [x for x in info if x[1].lower() not in domain]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: %s  |  %s' % (x[0], x[1]))
                raise RuntimeError(msg.error_info)

    def load_data(self):
        copy = arcpy.CopyFeatures_management(self.fc, "in_memory\\depositosMinerales")
        with arcpy.da.UpdateCursor(copy, [self.grade]) as cursorUC:
            for row in cursorUC:
                row[0] = row[0].lower()
                cursorUC.updateRow(row)
        del cursorUC
        arcpy.DeleteRows_management(self.fc_depomin.path)
        for k, v in self.fields.items():
            if v:
                arcpy.AlterField_management(copy, v, k)
        arcpy.Append_management(
            copy, self.fc_depomin.path, "NO_TEST"
        )

    def main(self):
        arcpy.AddMessage(msg.init_process)
        arcpy.AddMessage(msg.check_gdb)
        self.check_geodatabase()
        self.check_exist_feature()
        arcpy.AddMessage(msg.check_info)
        self.check_grade()
        arcpy.AddMessage(msg.send_database)
        self.load_data()
        arcpy.AddMessage(msg.end_process)


if __name__ == '__main__':
    try:
        ws = arcpy.GetParameterAsText(0)
        fc = arcpy.GetParameterAsText(1)
        unid = arcpy.GetParameterAsText(2)
        dimension = arcpy.GetParameterAsText(3)
        grade = arcpy.GetParameterAsText(4)
        value = arcpy.GetParameterAsText(5)

        poo = DepoMin(
            ws, fc, unid, dimension, grade, value
        )
        poo.main()
        arcpy.SetParameterAsText(6, poo.fc_depomin.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
