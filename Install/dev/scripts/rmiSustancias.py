from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()


class Sustancias(object):
    def __init__(self, *args):
        self.ws = args[0]
        self.fc = args[1]
        self.prod = args[2]
        self.precios = args[3]
        self.usos = args[4]
        self.tb_sust = rmi_tb_sustancias(self.ws)
        self.fc_sust = rmi_gpt_sustancias(self.ws)
        self.fields = {
            self.fc_sust.prod: self.prod,
            self.fc_sust.precios: self.precios,
            self.fc_sust.usos: self.usos
        }

    def check_geodatabase(self):
        desc = arcpy.Describe(self.ws)
        if not desc.datatype.lower() == 'workspace':
            raise RuntimeError(msg.error_gdb_type)

    def check_exist_feature(self):
        if not arcpy.Exists(self.fc_sust.path):
            raise RuntimeError(msg.error_gdb_type)

    def main(self):
        arcpy.AddMessage(msg.init_process)

if __name__ == '__main__':
    try:
        ws = arcpy.GetParameterAsText(0)
        fc = arcpy.GetParameterAsText(1)
        prod = arcpy.GetParameterAsText(2)
        precios = arcpy.GetParameterAsText(3)
        usos = arcpy.GetParameterAsText(4)

        poo = Sustancias(ws, fc, prod, precios, usos)
        poo.main()
        arcpy.SetParameterAsText(5, poo.fc_sust.path)
    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
