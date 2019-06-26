import arcpy
from config import *
from messages import Messages

arcpy.env.overwriteOutput = True

class remoteSensing(object):
    def __init__(self):
        self.msg = Messages()
        self.gdb = arcpy.GetParameterAsText(0)
        self.arcillas = arcpy.GetParameterAsText(1)
        self.oxidos = arcpy.GetParameterAsText(2)
        self.dataset = 'FD1_INSUMOS'
        self.feature = 'PM_V6_SensoresRemotos'

    def preprocess(self):
        self.fc_arcillas = arcpy.Dissolve_management(self.arcillas, 'in_memory\\arcillas', "#", '#', 'MULTI_PART','DISSOLVE_LINES')
        self.fc_oxidos = arcpy.Dissolve_management(self.oxidos, 'in_memory\\oxidos', "#", '#', 'MULTI_PART', 'DISSOLVE_LINES')

    def modificarCampos(self):
        camposArcillas = [x.name for x in arcpy.ListFields(self.fc_arcillas)]
        camposOxidos = [x.name for x in arcpy.ListFields(self.fc_oxidos)]
        for x in camposArcillas:
            try:
                arcpy.DeleteField_management(self.fc_arcillas, x)
            except:
                pass
        for x in camposOxidos:
            try:
                arcpy.DeleteField_management(self.fc_oxidos, x)
            except:
                pass
        arcpy.AddField_management(self.fc_arcillas, "TIPO_ARC", "TEXT", '#', '#', "50", '#', 'NULLABLE', 'NON_REQUIRED', '#')
        arcpy.AddField_management(self.fc_oxidos, "TIPO_OXI", "TEXT", '#', '#', "50", '#', 'NULLABLE', 'NON_REQUIRED', '#')

        for x in [[self.fc_arcillas, "TIPO_ARC", "Arcillas"], [self.fc_oxidos, "TIPO_OXI", "Oxidos"]]:
            with arcpy.da.UpdateCursor(x[0], [x[1]]) as cursorUC:
                for m in cursorUC:
                    m[0] = x[2]
                    cursorUC.updateRow(m)
            del cursorUC

    def unionCapas(self):
        union = arcpy.Union_analysis([self.fc_arcillas, self.fc_oxidos], 'in_memory\\union', 'ALL', '#', 'GAPS')
        arcpy.AddField_management(union, "TIPO", "TEXT", '#', '#', "50", '#', 'NULLABLE', 'NON_REQUIRED', '#')
        with arcpy.da.UpdateCursor(union, ["TIPO", "TIPO_ARC", "TIPO_OXI"]) as cursorUC:
            for x in cursorUC:
                if x[1] != "" and x[2] != "":
                    x[0] = "{} - {}".format(x[1], x[2])
                elif x[1] != "" and x[2] == "":
                    x[0] = x[1]
                    x[2] = '-'
                elif x[1] == "" and x[2] != "":
                    x[0] = x[2]
                    x[1] = '-'
                cursorUC.updateRow(x)
        del cursorUC
        arcpy.DeleteField_management(union, ["FID_arcillas", "FID_oxidos"])
        arcpy.Append_management(union, os.path.join(self.gdb, self.dataset, self.feature), "NO_TEST")
        arcpy.SetParameterAsText(3, os.path.join(self.gdb, self.dataset, self.feature))
        arcpy.AddMessage("  {}...".format(self.msg.updateinfo))

    def main(self):
        arcpy.AddMessage("\n {}: {}... ".format(self.msg.evaluateGdb, os.path.basename(self.gdb)))
        self.preprocess()
        self.modificarCampos()
        self.unionCapas()
        arcpy.AddMessage(" {} \n".format(self.msg.finish))

if __name__ == "__main__":
    poo = remoteSensing()
    poo.main()
