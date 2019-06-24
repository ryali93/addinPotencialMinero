import arcpy
from config import *
from messages import Messages

arcpy.env.overwriteOutput = True

class unidGeo:
    def __init__(self):
        self.ws = arcpy.GetParameterAsText(0)
        self.fc = arcpy.GetParameterAsText(1)
        self.codi = arcpy.GetParameterAsText(2)
        self.grado = arcpy.GetParameterAsText(3)
        self.value = arcpy.GetParameterAsText(4)
        self.condition = arcpy.GetParameterAsText(5)
        self.params = arcpy.GetParameterInfo()
        self.domains = domains["unidadesGeologicas"]
        self.msg = Messages()
        self.information = []
        self.dataset = "FD1_INSUMOS"
        self.feature = "PM_V1_UnidadesGeologicas"
        self.campo = ["GRADO", "VALOR", "CONDICION"]

    def consistency_01_Grado(self):
        arcpy.AddMessage("\n {}: {}...".format(self.msg.evaluate.format(self.campo[0]), self.grado))
        errores = [[1, x[0], x[1].lower()] for x in arcpy.da.SearchCursor(self.fc, ["OID@", self.grado]) if
                   x[1].lower() not in self.domains[self.campo[0]]]
        if len(errores) != 0: self.information.extend(errores)

    def consistency_02_Value(self):
        arcpy.AddMessage(" {}: {}...".format(self.msg.evaluate.format(self.campo[1]), self.value))
        errores = [[2, x[0], x[1]] for x in arcpy.da.SearchCursor(self.fc, ["OID@", self.value]) if
                   x[1] < self.domains[self.campo[1]]["min"] and x[1] > self.domains[self.campo[1]]["max"]]
        if len(errores) != 0: self.information.extend(errores)

    def consistency_03_Condition(self):
        arcpy.AddMessage(" {}: {}...".format(self.msg.evaluate.format(self.campo[2]), self.condition))
        errores = [[3, x[0], x[1].lower()] for x in arcpy.da.SearchCursor(self.fc, ["OID@", self.condition]) if
                   x[1].lower() not in self.domains[self.campo[2]]]
        if len(errores) != 0: self.information.extend(errores)

    def consistency_04_Nulls(self):
        arcpy.AddMessage(" {}...".format(self.msg.nullidentify))
        for x in self.params[2:6]:
            for m in arcpy.da.SearchCursor(self.fc, ["OID@", x.valueAsText]):
                if m[0] == None: self.information.append([4, x.valueAsText])

    def process(self):
        arcpy.AddMessage("\n {}: {}... ".format(self.msg.updateinfo, os.path.basename(self.ws)))
        try:
            desc = arcpy.Describe(self.ws)
            if desc.datatype == u'Workspace':
                if arcpy.Exists(os.path.join(self.ws, self.dataset, self.feature)):
                    if len(self.information) > 0:
                        arcpy.AddMessage("  Errores:")
                        for x in self.information:
                            e = self.msg.incorrectfield.format(self.campo[x[0]])
                            arcpy.AddWarning("   {}: FID: {}, Valor: {}".format(e, x[1], x[2]))
                    else:
                        arcpy.AddMessage("  {}...".format(self.msg.updateinfo))
                        copia = arcpy.CopyFeatures_management(self.fc, "in_memory\\unidadesGeologicas")
                        with arcpy.da.UpdateCursor(copia, [self.grado, self.condition]) as cursorUC:
                            for row in cursorUC:
                                row[0], row[1] = row[0].lower(), row[1].lower()
                                cursorUC.updateRow(row)
                        del cursorUC
                        campos = {"CODI": self.codi, self.campo[0]: self.grado, self.campo[1]: self.value, self.campo[2]: self.condition}
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
        self.consistency_03_Condition()
        self.consistency_04_Nulls()
        self.process()


if __name__ == "__main__":
    obj = unidGeo()
    obj.main()