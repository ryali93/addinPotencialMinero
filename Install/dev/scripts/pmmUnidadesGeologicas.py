from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()

class UnidGeo(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.codi = args[2]
        self.name = args[3]
        self.desc = args[4]
        self.unid = args[5]
        self.grade = args[6]
        self.value = args[7]
        self.condition = args[8]
        self.fc_unidgeo = pmm_gpo_ugeol(self.ws)
        self.tb_grade = tb_nivel(self.ws)
        self.tb_cond = pmm_tb_ugeol_condicion(self.ws)
        self.fields = {
            self.fc_unidgeo.codi: self.codi,
            self.fc_unidgeo.nombre: self.name,
            self.fc_unidgeo.descripcion: self.desc,
            self.fc_unidgeo.unidad: self.unid,
            self.fc_unidgeo.grado: self.grade,
            self.fc_unidgeo.valor: self.value,
            self.fc_unidgeo.condicion: self.condition
        }

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_unidgeo.path):
            raise RuntimeError(msg.error_gdb_type)

    def check_grade(self):
        domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_grade.path, [self.tb_grade.grado]
        )]
        self.info = [x for x in arcpy.da.SearchCursor(self.fc, ['OID@', self.grade, self.condition])]
        errors = [x for x in self.info if x[1].lower() not in domain or x[-1] in [None, False, '', ' ']]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: %s  |  %s' % (x[0], x[1]))
                raise RuntimeError(msg.error_info)

    def check_condition(self):
        domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_cond.path, [self.tb_cond.descrip]
        )]
        errors = [x for x in self.info if x[-1].lower() not in domain or x[-1] in [None, False, '', ' ']]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: FID %s | %s' % (x[0], x[-1]))
                raise RuntimeError(msg.error_info)

    def load_data(self):
        copy = arcpy.CopyFeatures_management(self.fc, "in_memory\\unidadesGeologicas")
        with arcpy.da.UpdateCursor(copy, [self.grade, self.condition]) as cursorUC:
            for row in cursorUC:
                row[0], row[1] = row[0].lower(), row[1].lower()
                cursorUC.updateRow(row)
        del cursorUC
        arcpy.DeleteRows_management(self.fc_unidgeo.path)
        for k, v in self.fields.items():
            if v:
                arcpy.AlterField_management(copy, v, k)
        arcpy.Append_management(
            copy, self.fc_unidgeo.path, "NO_TEST"
        )

    def main(self):
        arcpy.AddMessage(msg.init_process)
        arcpy.AddMessage(msg.check_gdb)
        self.check_geodatabase()
        self.check_exist_feature()
        arcpy.AddMessage(msg.check_info)
        self.check_grade()
        self.check_condition()
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
        condition = arcpy.GetParameterAsText(8)

        poo = UnidGeo(
            ws, fc, codi, name, desc,
            unid, grade, value, condition
        )
        poo.main()
        arcpy.SetParameterAsText(9, poo.fc_unidgeo.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
