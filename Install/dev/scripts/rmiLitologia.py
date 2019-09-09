from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()

class Litologia(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.codi = args[2]
        self.name = args[3]
        self.desc = args[4]
        self.unid = args[5]
        self.grade = args[6]
        self.value = args[7]
        self.fc_litologia = rmi_gpo_litologia(self.ws)
        self.tb_grade = tb_nivel(self.ws)
        self.tb_cond = pmm_tb_ugeol_condicion(self.ws)
        self.fields = {
            self.fc_litologia.codi: self.codi,
            self.fc_litologia.nombre: self.name,
            self.fc_litologia.descripcion: self.desc,
            self.fc_litologia.unidad: self.unid,
            self.fc_litologia.grado: self.grade,
            self.fc_litologia.valor: self.value
        }

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_litologia.path):
            raise RuntimeError(msg.error_gdb_type)

    def check_grade(self):
        domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_grade.path, [self.tb_grade.grado]
        )]
        self.info = [x for x in arcpy.da.SearchCursor(self.fc, ['OID@', self.grade])]
        errors = [x for x in self.info if x[1].lower() not in domain]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: %s  |  %s' % (x[0], x[1]))
                raise RuntimeError(msg.error_info)

    def load_data(self):
        copy = arcpy.CopyFeatures_management(self.fc, "in_memory\\litologia")
        with arcpy.da.UpdateCursor(copy, [self.grade]) as cursorUC:
            for row in cursorUC:
                row[0] = row[0].lower()
                cursorUC.updateRow(row)
        del cursorUC
        arcpy.DeleteRows_management(self.fc_litologia.path)
        for k, v in self.fields.items():
            if v:
                arcpy.AlterField_management(copy, v, k)
        arcpy.Append_management(
            copy, self.fc_litologia.path, "NO_TEST"
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
        codi = arcpy.GetParameterAsText(2)
        name = arcpy.GetParameterAsText(3)
        desc = arcpy.GetParameterAsText(4)
        unid = arcpy.GetParameterAsText(5)
        grade = arcpy.GetParameterAsText(6)
        value = arcpy.GetParameterAsText(7)

        poo = Litologia(
            ws, fc, codi, name, desc,
            unid, grade, value
        )
        poo.main()
        arcpy.SetParameterAsText(9, poo.fc_litologia.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)

