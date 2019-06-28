import arcpy
from config import *
from messages import Messages

arcpy.env.overwriteOutput = True

class geoquimica(object):
    def __init__(self):
        self.msg = Messages()
        self.ws = arcpy.GetParameterAsText(0)
        self.raster = arcpy.GetParameterAsText(1)
        self.rasterOut = geoquimica_ras

    def main(self):
        arcpy.AddMessage("\n {}: {}... ".format(self.msg.evaluateGdb, os.path.basename(self.ws)))
        try:
            desc = arcpy.Describe(self.ws)
            if desc.datatype == u'Workspace':
                arcpy.AddMessage("  {}...".format(self.msg.updateinfo))
                # arcpy.CheckOutExtension("spatial")
                geoquimica = arcpy.sa.Fill(self.raster)
                geoquimica.save(os.path.join(self.ws, self.rasterOut))
                # arcpy.CheckInExtension("spatial")
                arcpy.SetParameterAsText(2, os.path.join(self.ws, self.rasterOut))
            else:
                arcpy.AddMessage("\n {}... \n".format(self.msg.wsunexist))
        except Exception as e:
            arcpy.arcpy.AddError("\n {} \n".format(self.msg.unlicencedSA))

        arcpy.AddMessage(" {} \n".format(self.msg.finish))

if __name__ == "__main__":
    poo = geoquimica()
    poo.main()
