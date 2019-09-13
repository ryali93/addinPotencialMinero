from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()


class Sustancias(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.sust = args[2]
        self.grado = args[3]
        self.valor = args[4]
        self.tb_sust = rmi_tb_sustancias(self.ws)
        self.fc_sust = rmi_gpt_sustancias(self.ws)
        self.fields = {
            self.fc_sust.grado: self.grado,
            self.fc_sust.valor: self.valor
        }

    def get_domain(self):
        self.domain = [x[0] for x in arcpy.da.SearchCursor(
            self.tb_sust.path, [self.tb_sust.sustancia]
        )]

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_sust.path):
            raise RuntimeError(msg.error_gdb_type)

    def check_info(self):
        info = arcpy.da.SearchCursor(self.fc, ['OID@', self.sust])
        errors = [x for x in info if x[1].lower() not in self.domain]
        if len(errors) > 0:
            for x in errors:
                arcpy.AddWarning('\t\tError: FID: %s  |  %s ' % (x[0], x[1]))
                raise RuntimeError(msg.error_info)

    def load_data(self):
        copy = arcpy.CopyFeatures_management(
            self.fc, "in_memory\\sustancias"
        )
        with arcpy.da.UpdateCursor(copy, [self.sust]) as cursorUC:
            for row in cursorUC:
                row[0] = row[0].lower()
                cursorUC.updateRow(row)
        del cursorUC

        arcpy.DeleteRows_management(self.fc_sust.path)

        for k, v in self.fields.items():
            arcpy.AlterField_management(copy, v, k)

        arcpy.Append_management(
            copy, self.fc_sust.path, "NO_TEST"
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
        sust = arcpy.GetParameterAsText(2)
        grado = arcpy.GetParameterAsText(3)
        valor = arcpy.GetParameterAsText(4)

        poo = Sustancias(ws, fc, sust, grado, valor)
        poo.main()
        arcpy.SetParameterAsText(5, poo.fc_sust.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
