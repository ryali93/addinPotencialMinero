import arcpy
import time
from config import *
from messages import Messages

class directorios(object):
    def __init__(self):
        self.ws = arcpy.GetParameterAsText(0)
        self.codigo_tmp = arcpy.GetParameterAsText(1)
        self.zona = arcpy.GetParameterAsText(2)
        self.codigo = self.codigo_tmp[0:2]
        self.nombreReg = self.codigo_tmp[5:]
        self.fecha = time.strftime("%d%m%Y")
        self.hora = time.strftime('%H%M%S')
        self.wkid = int('327{}'.format(self.zona))
        self.db = directoryStructure['dataBase']
        self.elm = directoryStructure['nameElements']
        self.fcs = directoryStructure['featureClass']
        self.msg = Messages()
        self.depaFc = os.path.join(CONN, self.db['entityUsed']['departamento']['fullname'])
        self.addwhere = "{} = '{}'".format(self.db['entityUsed']['departamento']['fieldSql'], self.nombreReg)
        self.pathgdb = ""
        self.dataset = ""

    def directorioPrincipal(self):
        dirr = os.path.join(self.ws, self.elm['folderMain'])
        if not os.path.exists(dirr):
            arcpy.CreateFolder_management(self.ws, self.elm['folderMain'])
        self.directoriosSecundarios(dirr)

    def directoriosSecundarios(self, dirr):
        nameFile = u'{}{}__{}_{}'.format(self.elm['modelId'], self.nombreReg, self.fecha, self.hora)
        folderMain = arcpy.CreateFolder_management(dirr, nameFile)
        gdb = arcpy.CreateFileGDB_management(folderMain, self.elm['gdb'], "10.0")
        for k, v in self.elm['fds'].items():
            arcpy.CreateFeatureDataset_management(gdb, v, arcpy.SpatialReference(self.wkid))
        self.pathgdb = arcpy.Describe(gdb).catalogPath

    def limiteDep(self):
        self.dataset = os.path.join(self.pathgdb, self.elm['fds']['insumos'])
        mfl = arcpy.MakeFeatureLayer_management(self.depaFc, "Poligono", self.addwhere)
        arcpy.CopyFeatures_management(mfl, os.path.join(self.dataset, self.elm['fcs']['region']))

    def catastro(self):
        sqlSpatial = '''SELECT {} FROM {} A WHERE {} AND SDE.ST_INTERSECTS((SELECT SDE.ST_TRANSFORM(SHAPE, 4326) FROM {} B  WHERE {}), A.SHAPE) = 1'''.format(
            self.db['sqlSpatial']['fieldSelect'], self.db['sqlSpatial']['fromfc'], self.db['sqlSpatial']['where'],
            self.db['entityUsed']['departamento']['fcname'], self.addwhere)
        mql = arcpy.MakeQueryLayer_management(CONN, "CatastroMinero", sqlSpatial,
                                              self.db['sqlSpatial']['uniqueField'], "POLYGON", self.wkid,
                                              arcpy.SpatialReference(self.wkid))
        arcpy.CopyFeatures_management(mql, os.path.join(self.pathgdb, self.elm['fds']['insumos'],
                                                        self.elm['fcs']['catastro']))

    def crearFeatures(self):
        for k, v in self.fcs.items():
            shp = arcpy.AsShape(v['esrijson'], True)
            arcpy.CopyFeatures_management(shp, os.path.join(self.dataset, v['nombre']))
        arcpy.SetParameterAsText(3, os.path.join(self.dataset, self.elm['fcs']['region']))
        arcpy.SetParameterAsText(4, os.path.join(self.dataset, self.elm['fcs']['catastro']))

    def main(self):
        try:
            self.directorioPrincipal()
            self.limiteDep()
            self.catastro()
            self.crearFeatures()
        except Exception as e:
            arcpy.AddWarning(e)


if __name__ == "__main__":
    obj = directorios()
    obj.main()
