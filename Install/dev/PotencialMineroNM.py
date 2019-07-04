# -*- coding: utf-8 -*-

import arcpy
import threading
import webbrowser
import time
import shutil
from config import *
from messages import Messages

arcpy.env.overwriteOutput = True

ws = arcpy.GetParameterAsText(0)
pixel = arcpy.GetParameterAsText(1)
exportar = arcpy.GetParameterAsText(2)
publicar = arcpy.GetParameterAsText(3)
visualizar = arcpy.GetParameterAsText(4)

msg = Messages()

limitePoligonal = os.path.join(ws, ds_insumos, cuadrante) if os.path.exists(
    os.path.join(ws, ds_insumos, cuadrante)) else os.path.join(ws, ds_insumos, region)
controlador = []

crs = arcpy.Describe(os.path.join(ws, ds_insumos)).spatialReference
arcpy.env.outputCoordinateSystem = crs

def V1_UnidadGeologica(ws=ws, controlador=controlador):
    arcpy.AddMessage(" V1: {}...".format(geologia_tex))
    fc_unidadesGeologicas = os.path.join(ws, ds_insumos, geologia)
    if arcpy.GetCount_management(fc_unidadesGeologicas)[0] != u'0':
        arcpy.CopyFeatures_management(fc_unidadesGeologicas, os.path.join(ws, ds_variables, geologia_fc))
        arcpy.AddMessage("   {}...".format(msg.exportRaster))
        arcpy.PolygonToRaster_conversion(fc_unidadesGeologicas, fd_valor, os.path.join(ws, geologia_ras), "CELL_CENTER", fd_valor, pixel)
        controlador.append([1, '{}'.format(geologia_tex)])
    else:
        controlador.append([0, '{}'.format(geologia_tex)])

def V2_variableConcesionesMineras(ws=ws, limitePoligonal=limitePoligonal, pixel=pixel):
    arcpy.AddMessage(" V2: {}...".format(concesiones_tex))
    fc_unidadesGeologicas = os.path.join(ws, ds_insumos, geologia)
    fc_catastroMinero = os.path.join(ws, ds_insumos, catastro)
    dissolve = arcpy.Dissolve_management(fc_catastroMinero, 'in_memory\\Dissolve_CM', 'LEYENDA;NATURALEZA', '#', 'MULTI_PART', 'DISSOLVE_LINES')
    union = arcpy.Union_analysis([dissolve, fc_unidadesGeologicas], os.path.join(ws, ds_variables, concesiones_fc), 'ALL', '#', 'GAPS')
    arcpy.AddMessage("   {}...".format(msg.reviewFields))
    with arcpy.da.UpdateCursor(union, [fd_valor, fd_grado, fd_leyenda, fd_condicion]) as cursorUC:
        for i in cursorUC:
            if i[3] != '':
                if i[2] == 'TITULADO' and i[3] == 'Metalotecto':
                    i[0], i[1] = 2.9, 'Muy Alto'
                elif i[2] == '' and i[3] == 'Metalotecto':
                    i[0], i[1] = 2.5, 'Alto'
                elif i[2] == 'TITULADO' and i[3] == 'No metalotecto':
                    i[0], i[1] = 2.0, 'Medio'
                elif i[2] == '' and i[3] == 'No metalotecto':
                    i[0], i[1] = 1.6, 'Bajo'
                cursorUC.updateRow(i)
            else:
                cursorUC.deleteRow()
    del cursorUC
    with arcpy.da.UpdateCursor(union, [fd_leyenda, fd_condicion], "NATURALEZA = '' AND LEYENDA = ''") as cursorUC:
        for i in cursorUC:
            i[0], i[1] == '-', '-'
            cursorUC.updateRow(i)
    del cursorUC
    deleteFields = ["FID_Dissolve_CM", "FID_{}".format(geologia)]
    arcpy.DeleteField_management(union, deleteFields)
    arcpy.AddMessage("   {}...".format(msg.exportRaster))
    arcpy.PolygonToRaster_conversion(union, fd_valor, os.path.join(ws, concesiones_ras), "CELL_CENTER", fd_valor, pixel)
    controlador.append([1, '{}'.format(concesiones_tex)])
