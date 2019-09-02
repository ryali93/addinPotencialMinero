from model import *
from nls import *

arcpy.env.overwriteOutput = True


class Geoquimica(object):
    """
    Clase que contiene el procesamiento para el tratamiento
    de la variable geoquimica
    """
    ws = arcpy.GetParameterAsText(0)
    raster = arcpy.GetParameterAsText(1)

    raster_dataset = ras_geoquimica(ws)
    messages = Messages()

    def process(self):
        """
        Enviando el raster ingresado al File Geodatabase
        :return:
        """
        arcpy.AddMessage(u'\t1. Verificando disponibilidad de licencia SPATIAL ANALYST')
        license = arcpy.CheckExtension('spatial')
        if license != 'Available':
            raise RuntimeError('\tError: %s' % license)

        arcpy.AddMessage(u'\t2. Enviando informacion a la GEODATABASE')
        arcpy.CheckOutExtension('spatial')
        geoquimica = arcpy.sa.Fill(self.raster)
        geoquimica.save(self.raster_dataset.path)
        arcpy.CheckInExtension('spatial')
        arcpy.SetParameterAsText(2, self.raster_dataset.path)

    def main(self):
        """
        Funcion principal del proceso
        :return:
        """
        try:
            arcpy.AddMessage(self.messages.init_process)
            desc = arcpy.Describe(self.ws)
            if desc.datatype != 'Workspace':
                raise RuntimeError(self.messages.error_gdb_type)
            self.process()
            arcpy.AddMessage(self.messages.end_process)
        except Exception as e:
            arcpy.AddError(e.message)


if __name__ == "__main__":
    poo = Geoquimica()
    poo.main()
