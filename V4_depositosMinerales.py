import arcpy
from config import *
from messages import Messages

arcpy.env.overwriteOutput = True

class depoMin(object):
    def __init__(self):
        self.ws = arcpy.GetParameterAsText(0)
        self.fc = arcpy.GetParameterAsText(1)
        self.grade = arcpy.GetParameterAsText(2)
        self.value = arcpy.GetParameterAsText(3)

        self.domains = domains["depositosMinerales"]
        self.msg = Messages()
        self.information = []
        self.dataset = "FD1_INSUMOS"
        self.feature = "PM_V3_FallasGeologicas"
        self.campo = ["GRADO", "VALOR"]

    def consistency_01_Grado(self):
        arcpy.AddMessage("\n {}: {}...".format(self.msg.evaluate.format(self.campo[0]), self.grade))
        errores = [[1, x[0], x[1].lower()] for x in arcpy.da.SearchCursor(self.fc, ["OID@", self.grade]) if
                   x[1].lower() not in self.domains[self.campo[0]]]
        if len(errores) != 0:
            self.information.extend(errores)

    def consistency_02_Value(self):
        arcpy.AddMessage(" {}: {}...".format(self.msg.evaluate.format(self.campo[1]), self.value))
        errores = [[2, x[0], x[1]] for x in arcpy.da.SearchCursor(self.fc, ["OID@", self.value]) if
                   x[1] < self.domains["VALOR"]["min"] and x[1] > self.domains["VALOR"]["max"]]
        if len(errores) != 0:
            self.information.extend(errores)

    def process(self):
        arcpy.AddMessage("\n {}: {}... ".format(self.msg.evaluateGdb, os.path.basename(self.ws)))
        try:
            desc = arcpy.Describe(self.ws)
            if desc.datatype == u'Workspace':
                if arcpy.Exists(os.path.join(self.ws, self.dataset, self.feature)):
                    if len(self.information) > 0:
                        arcpy.AddMessage("  Errores:")
                        for x in self.information:
                            e = self.msg.incorrectfield.format(x[0])
                            arcpy.AddWarning("    {}: FID: {}, Valor: {}".format(e, x[1], x[2]))
                    else:
                        arcpy.AddMessage("  {}...".format(self.msg.updateinfo))
                        copia = arcpy.CopyFeatures_management(self.fc, "in_memory\\depositosMinerales")
                        with arcpy.da.UpdateCursor(copia, [self.grade]) as cursorUC:
                            for row in cursorUC:
                                row[0] = row[0].lower()
                                cursorUC.updateRow(row)
                        del cursorUC
                        campos = {self.campo[0]: self.grade, self.campo[1]: self.value}
                        arcpy.DeleteRows_management(os.path.join(self.ws, self.dataset, self.feature))
                        for k, v in campos.items():
                            arcpy.AlterField_management(copia, v, k)
                        arcpy.Append_management(copia, os.path.join(self.ws, self.dataset, self.feature), "NO_TEST")
                        arcpy.SetParameterAsText(4, os.path.join(self.ws, self.dataset, self.feature))
                        arcpy.AddMessage("\n {}... \n".format(self.msg.updateok))
                        arcpy.AddMessage("\n {} \n".format(self.msg.finish))
                else:
                    raise RuntimeError("\n {}... \n".format(self.msg.wsincorrect.format(self.feature)))
            else:
                raise RuntimeError("\n {}... \n".format(self.msg.wsunexist))
        except Exception as e:
            arcpy.AddWarning(e)

    def main(self):
        self.consistency_01_Grado()
        self.consistency_02_Value()
        self.process()


if __name__ == "__main__":
    poo = depoMin()
    poo.main()
