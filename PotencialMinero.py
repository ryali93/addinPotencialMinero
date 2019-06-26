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

sistReferencia = arcpy.Describe(os.path.join(ws, ds_insumos)).spatialReference
arcpy.env.outputCoordinateSystem = sistReferencia

# Funciones

def V1_variableUnidadGeologica(ws=ws, controlador=controlador):
    arcpy.AddMessage(" V1: {}...".format(geologia_tex))
    fc_unidadesGeologicas = os.path.join(ws, ds_insumos, geologia)
    if arcpy.GetCount_management(fc_unidadesGeologicas)[0] != u'0':
        arcpy.CopyFeatures_management(fc_unidadesGeologicas, os.path.join(ws, ds_variables, geologia_fc))
        arcpy.AddMessage("   {}...".format(msg.exportRaster))
        arcpy.PolygonToRaster_conversion(fc_unidadesGeologicas, fd_valor, os.path.join(ws, geologia_ras),
                                         "CELL_CENTER", fd_valor, pixel)
        controlador.append([1, '{}'.format(geologia_tex)])
    else:
        controlador.append([0, '{}'.format(geologia_tex)])

def V2_variableConcesionesMineras(ws=ws, limitePoligonal=limitePoligonal, pixel=pixel):
    arcpy.AddMessage(" V2: {}...".format(concesiones_tex))
    fc_unidadesGeologicas = os.path.join(ws, ds_insumos, geologia)
    fc_catastroMinero = os.path.join(ws, ds_insumos, catastro)
    dissolve = arcpy.Dissolve_management(fc_catastroMinero, 'in_memory\\Dissolve_CM', 'LEYENDA;NATURALEZA', '#',
                                         'MULTI_PART', 'DISSOLVE_LINES')
    union = arcpy.Union_analysis([dissolve, fc_unidadesGeologicas],
                                 os.path.join(ws, ds_variables, concesiones_fc), 'ALL', '#', 'GAPS')
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

def V3_variableFallasGeologicas(ws=ws, limitePoligonal=limitePoligonal, pixel=pixel):
    arcpy.AddMessage(" V3: {}...".format(fallas_tex))
    fc = os.path.join(ws, ds_insumos, fallas)
    campos = [[fd_influencia, "SHORT", "3"], [fd_grado, "TEXT", "50"], [fd_valor, "DOUBLE", "#"]]
    if arcpy.GetCount_management(fc)[0] != u'0':

        camposActuales = [x.name for x in arcpy.ListFields(fc)]
        for i in campos:
            if i[0] in camposActuales:
                arcpy.DeleteField_management(fc, i[0])
        for i in campos:
            if i[1] == "TEXT":
                arcpy.AddField_management(fc, i[0], i[1], '#', '#', i[2], '#', 'NULLABLE', 'NON_REQUIRED', '#')
            else:
                arcpy.AddField_management(fc, i[0], i[1], i[2], '#', '#', '#', 'NULLABLE', 'NON_REQUIRED', '#')

        arcpy.AddMessage("   {}...".format(msg.reviewFields))

        with arcpy.da.UpdateCursor(fc, [fd_influencia, fd_grado, fd_valor, "Shape_Length"]) as cursorUC:
            for x in cursorUC:
                if x[3] >= 50000.0:
                    x[0], x[1], x[2] = 5000, "Muy Alto", 2.9
                elif x[3] >= 10000.0 and x[1] < 50000.0:
                    x[0], x[1], x[2] = 1000, "Alto", 2.5
                else:
                    x[0], x[1], x[2] = 500, "Medio", 2.0
                cursorUC.updateRow(x)
        del cursorUC

        dissolve = arcpy.Dissolve_management(fc, 'in_memory\\Dissolve_FG', fd_valor,
                                             '{} FIRST;{} FIRST;{} FIRST;{} FIRST', 'MULTI_PART',
                                             'DISSOLVE_LINES'.format(fd_codi, fd_descrip, fd_influencia, fd_grado))
        influencia = arcpy.Buffer_analysis(dissolve, "in_memory\\influencia", 'FIRST_{}'.format(fd_influencia))
        clip = arcpy.Clip_analysis(influencia, limitePoligonal, os.path.join(ws, ds_variables, fallas_fc))
        erase = arcpy.Erase_analysis(limitePoligonal, clip, "in_memory\\erase")
        arcpy.Append_management(erase, clip, "NO_TEST")

        alterFields = {"FIRST_{}".format(fd_codi): fd_codi,
                       "FIRST_{}".format(fd_descrip): fd_descrip,
                       "FIRST_{}".format(fd_influencia): fd_influencia,
                       "FIRST_{}".format(fd_grado): fd_grado,
                       fd_valor: fd_valor}
        for k, v in alterFields.items():
            arcpy.AlterField_management(clip, k, v)

        deleteFields = ["BUFF_DIST", "ORIG_FID"]
        arcpy.DeleteField_management(clip, deleteFields)

        with arcpy.da.UpdateCursor(clip, [fd_influencia, fd_codi, fd_descrip, fd_grado, fd_valor], "VALOR IS NULL") as cursorUC:
            for x in cursorUC:
                x[0], x[1], x[2], x[3], x[4] = 0, 0, "Ausencia", "Bajo", 1.6
                cursorUC.updateRow(x)
        del cursorUC

        arcpy.AddMessage("   {}...".format(msg.exportRaster))

        arcpy.PolygonToRaster_conversion(clip, fd_valor, os.path.join(ws, fallas_ras), "CELL_CENTER", fd_valor, pixel)
        controlador.append([1, fallas_tex])
    else:
        controlador.append([0, fallas_tex])
        pass

def V4_variableDepositosMinerales(ws=ws):
    arcpy.AddMessage(" V4: {}...".format(depositos_tex))
    fc = os.path.join(ws, ds_insumos, depositos)
    arcpy.CopyFeatures_management(fc, os.path.join(ws, ds_variables, depositos_fc))
    arcpy.AddMessage("   {}...".format(msg.exportRaster))
    arcpy.PolygonToRaster_conversion(fc, fd_valor, os.path.join(ws, depositos_ras), "CELL_CENTER", fd_valor, pixel)

def V5_variableGeoquimica(ws=ws, controlador=controlador):
    arcpy.AddMessage(" V5: {}...".format(geoquimica_tex))
    geoquimica = os.path.join(ws, geoquimica_ras)
    if arcpy.Exists(geoquimica):
        arcpy.AddMessage("   {}...".format(msg.exists))
        time.sleep(1)
        controlador.append([1, geoquimica_tex])
    else:
        controlador.append([0, geoquimica_tex])

def V6_variableSesoresRemotos(ws=ws, limitePoligonal=limitePoligonal, pixel=pixel):
    arcpy.AddMessage(" V6: {}...".format(sensores_tex))
    fc = os.path.join(ws, ds_insumos, sensores)
    fc_copy = arcpy.CopyFeatures_management(fc, "in_memory\\sensoresRemotos")
    campos = [[fd_grado, "TEXT", "50"], [fd_valor, "DOUBLE", "#"]]
    for i in campos:
        if i[1] == "TEXT":
            arcpy.AddField_management(fc_copy, i[0], i[1], '#', '#', i[2], '#', 'NULLABLE', 'NON_REQUIRED', '#')
        else:
            arcpy.AddField_management(fc_copy, i[0], i[1], i[2], '#', '#', '#', 'NULLABLE', 'NON_REQUIRED', '#')

    erase = arcpy.Erase_analysis(limitePoligonal, fc_copy, "in_memory\\erase")
    arcpy.Append_management(erase, fc_copy, "NO_TEST")

    arcpy.AddMessage("   {}...".format(msg.reviewFields))

    with arcpy.da.UpdateCursor(fc_copy, [fd_tipo, fd_grado, fd_valor, "TIPO_ARC", "TIPO_OXI"], "VALOR IS NULL") as cursorUC:
        for x in cursorUC:
            if x[0] == "Arcillas - Oxidos":
                x[1], x[2] = 'Muy Alto', 2.9
            elif x[0] == "Oxidos":
                x[1], x[2] = 'Alto', 2.7
            elif x[0] == "Arcillas":
                x[1], x[2] = 'Medio', 2.5
            elif x[0] == None:
                x[0], x[1], x[2], x[3], x[4] = 'Ausencia', 'Bajo', 1.8, 'Ausencia', 'Ausencia'

            cursorUC.updateRow(x)
    del cursorUC
    sr = arcpy.CopyFeatures_management(fc_copy, os.path.join(ws, ds_variables, sensores_fc))

    arcpy.AddMessage("   {}...".format(msg.exportRaster))
    arcpy.PolygonToRaster_conversion(sr, fd_valor, os.path.join(ws, sensores_ras), "CELL_CENTER", fd_valor, pixel)

# Potencial Minero

def calcularPotencialMinero(ws=ws):
    arcpy.AddMessage(" {}...".format(msg.potMinero))

    arcpy.env.outputCoordinateSystem = 4326

    unidadesGeologicas = os.path.join(ws, geologia_ras)
    concesionesMineras = os.path.join(ws, concesiones_ras)
    fallasGeologicas = os.path.join(ws, fallas_ras)
    depositosMinerales = os.path.join(ws, depositos_ras)
    geoquimica = os.path.join(ws, geoquimica_ras)
    sensoresRemotos = os.path.join(ws, sensores_ras)

    arcpy.AddMessage("   {}...".format(msg.ponderacion))
    # arcpy.CheckOutExtension("spatial")
    potencialMinero = arcpy.sa.Raster(unidadesGeologicas) * 0.481 + arcpy.sa.Raster(
        concesionesMineras) * 0.239 + arcpy.sa.Raster(fallasGeologicas) * 0.145 + arcpy.sa.Raster(
        depositosMinerales) * 0.0069 + arcpy.sa.Raster(geoquimica) * 0.038 + arcpy.sa.Raster(sensoresRemotos) * 0.027
    arcpy.AddMessage("   {}...".format(msg.exportRaster))
    potencialMinero.save(os.path.join(ws, potMinero_ras))
    # arcpy.CheckInExtension("spatial")

    arcpy.env.outputCoordinateSystem = sistReferencia

# Iniciar exportacion de mapas

def generacionMapa(exportar=exportar, ws=ws):
    if exportar:
        arcpy.AddMessage("   {}...".format(msg.exportMap))
        time.sleep(2)
        folderPdf = os.path.join(os.path.dirname(ws), 'PM_PDF')
        folderMxd = os.path.join(os.path.dirname(ws), 'PM_MXD')
        for x in [folderPdf, folderMxd]:
            if os.path.exists(x):
                shutil.rmtree(x)
            else:
                arcpy.CreateFolder_management(os.path.dirname(x), os.path.basename(x))
    else:
        arcpy.AddMessage("\n")

# Iniciar carga de datos a la BD True/False

def publicacionResultados(publicar=publicar):
    if publicar:
        arcpy.AddMessage("   {}...".format(msg.publishFinal))
        time.sleep(2)
    else:
        arcpy.AddMessage("\n")

# Iniciar GEOCATMIN en el Browser True/False

def estimaExtension(limitePoligonal=limitePoligonal):
    from json import loads
    info = \
    [x[0].extent.JSON for x in arcpy.da.SearchCursor(limitePoligonal, ["SHAPE@"], None, arcpy.SpatialReference(4326))][
        0]
    params = loads(info)
    return params

def definiUrl(params):
    urlIngemmet = 'http://geocatmin.ingemmet.gob.pe/geocatmin/index.html?extent={},{},{},{},4326'.format(params['xmin'],
                                                                                                         params['ymin'],
                                                                                                         params['xmax'],
                                                                                                         params['ymax'])
    webbrowser.open(urlIngemmet, new=0)

def iniciarGeocatmin(params):
    t = threading.Thread(target=definiUrl, args=(params,))
    t.start()
    t.join()

def visualizacionGeocatmin(visualizar=visualizar):
    if visualizar:
        arcpy.AddMessage(" Iniciando GEOCATMIN...")
        time.sleep(2)
        params = estimaExtension()
        iniciarGeocatmin(params)

# Ejecucion de procesos organizados

def main():
    arcpy.AddMessage("\n Iniciando proceso para la identificacion del Potencial Minero")
    V1_variableUnidadGeologica()
    V2_variableConcesionesMineras()
    V3_variableFallasGeologicas()
    V4_variableDepositosMinerales()
    V5_variableGeoquimica()
    V6_variableSesoresRemotos()
    try:
        calcularPotencialMinero()
        generacionMapa()
        publicacionResultados()
        visualizacionGeocatmin()
        arcpy.SetParameterAsText(5, os.path.join(ws, 'POTENCIAL_MINERO_RAS'))
        arcpy.AddMessage(" \n Proceso Finalizado")
    except:
        arcpy.AddWarning(" \n La licencia 'Spatial Analyst' no esta disponible en estos momentos \n")

if __name__ == "__main__":
    main()