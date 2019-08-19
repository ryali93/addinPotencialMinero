# -*- coding: utf-8 -*-

from model import *
from nls import *

arcpy.env.overwriteOutput = True


class PotencialMinero(object):

    ws = arcpy.GetParameterAsText(0)
    pixel = arcpy.GetParameterAsText(1)
    exportar = arcpy.GetParameterAsText(2)
    publicar = arcpy.GetParameterAsText(3)
    visualizar = arcpy.GetParameterAsText(4)

    config = tb_config(ws)
    messages = Messages()

    limite = pm_region(ws)
    unidad_geologica = gpo_unidad_geologica(ws)
    catastro_minero = pm_catastro_minero(ws)
    falla_geologica = pm_gpl_fallageologica(ws)
    deposito_mineral = gpo_deposito_mineral(ws)
    sensor_remoto = gpo_sensores_remotos(ws)
    geoquimica = ras_geoquimica(ws)

    v_unidad_geologica = var_unidad_geologica(ws)
    v_falla_geologica = var_falla_geologica(ws)
    v_catastro_minero = var_concesion_minera(ws)
    v_deposito_mineral = var_deposito_mineral(ws)
    v_sensor_remoto = var_sensor_remoto(ws)

    r_unidad_geologica = ras_unidad_geologica(ws)
    r_falla_geologica = ras_falla_geologica(ws)
    r_catastro_minero = ras_concesion_minera(ws)
    r_deposito_mineral = ras_deposito_mineral(ws)
    r_sensor_remoto = ras_sensor_remoto(ws)

    pm_factor = tb_pm_factor(ws)
    r_potencial_minero = ras_potencial_minero(ws)

    src = [i[0] for i in arcpy.da.SearchCursor(config.path, [config.zona])][0]

    def value_resources(self):
        license = arcpy.CheckExtension('spatial')
        if license != 'Available':
            raise RuntimeError(u'\n\tError de licencia Spatial Analyst\n')

    def pre_treatment(self, insumo, feature, raster):
        name = os.path.basename(insumo)

        if arcpy.GetCount_management(insumo).__str__() == '0':
            raise RuntimeError(u'\tLa capa de %s no contiene registros' % name)

        arcpy.DeleteRows_management(feature)

        if arcpy.Exists(raster):
            arcpy.Delete_management(raster)

    def method_unidades_geologicas(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.eval_ug)

        self.pre_treatment(self.unidad_geologica.path, self.v_unidad_geologica.path, self.r_unidad_geologica.path)

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(self.unidad_geologica.path, self.v_unidad_geologica.path, 'NO_TEST')

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.unidad_geologica.path, self.unidad_geologica.valor,
                                         self.r_unidad_geologica.path, "CELL_CENTER", self.unidad_geologica.valor,
                                         self.pixel)

    def method_concesiones_mineras(self):
        """

        :return:
        """

        arcpy.AddMessage(self.messages.eval_cm)

        self.pre_treatment(self.catastro_minero.path, self.v_catastro_minero.path, self.r_catastro_minero.path)

        fields = [self.catastro_minero.leyenda, self.catastro_minero.naturaleza]

        dissolve = arcpy.Dissolve_management(self.catastro_minero.path, 'in_memory\\feature', fields, '#', 'MULTI_PART',
                                             'DISSOLVE_LINES')

        input_feature = [dissolve, self.unidad_geologica.path]

        arcpy.AddMessage(self.messages.eval_cm_task_overlap)
        union = arcpy.Union_analysis(input_feature, 'in_memory\\union', 'ALL', '#', 'GAPS')

        fields = [self.catastro_minero.leyenda, self.unidad_geologica.condicion, self.unidad_geologica.valor,
                  self.unidad_geologica.grado, ]

        cm_grado = tb_cm_grado(self.ws)

        grade = [i for i in arcpy.da.SearchCursor(cm_grado.path, fields)]

        arcpy.AddMessage(self.messages.gen_task_grade)
        with arcpy.da.UpdateCursor(union, fields) as cursor:
            for i in cursor:
                cond = i[0]
                if cond in (None, '', ' '):
                    cond = None
                if cond:
                    cond = i[0].lower()
                for r in grade:
                    if cond == r[0] and i[1].lower() == r[1]:
                        i[2] = r[2]
                        i[3] = r[3]
                        break
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(union, self.v_catastro_minero.path, 'NO_TEST')

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.v_catastro_minero.path, self.unidad_geologica.valor,
                                         self.r_catastro_minero.path, "CELL_CENTER", self.unidad_geologica.valor,
                                         self.pixel)

    def method_fallas_geologicas(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.eval_fg)

        self.pre_treatment(self.falla_geologica.path, self.v_falla_geologica.path, self.r_falla_geologica.path)

        feature = arcpy.CopyFeatures_management(self.falla_geologica.path, 'in_memory\\feature')

        arcpy.AddField_management(feature, self.v_falla_geologica.influencia, 'DOUBLE')

        fields = [self.falla_geologica.distancia, self.v_falla_geologica.influencia]

        fg_grado = tb_fg_grado(self.ws)
        fields_grado = [fg_grado.dist_min, fg_grado.dist_max, fg_grado.influencia, fg_grado.grado, fg_grado.valor]

        grade = [i for i in arcpy.da.SearchCursor(fg_grado.path, fields_grado)]

        arcpy.AddMessage(self.messages.eval_fg_task_radio)
        with arcpy.da.UpdateCursor(feature, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if x[1] is None:
                        if i[0] >= x[0]:
                            i[1] = x[2]
                            break
                    else:
                        if x[0] <= i[0] < x[1]:
                            i[1] = x[2]
                            break
                cursor.updateRow(i)
            del cursor

        dissolve = arcpy.Dissolve_management(feature, 'in_memory\\dissolve', self.v_falla_geologica.influencia, "#",
                                             'MULTI_PART', 'DISSOLVE_LINES')

        arcpy.AddMessage(self.messages.eval_fg_task_influencia)
        influencia = arcpy.Buffer_analysis(dissolve, 'in_memory\\buffer', self.v_falla_geologica.influencia)

        arcpy.Append_management(influencia, self.v_falla_geologica.path, 'NO_TEST')

        erase = arcpy.Erase_analysis(self.limite.path, self.v_falla_geologica.path, 'in_memory\\erase')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(erase, self.v_falla_geologica.path, 'NO_TEST')

        del fields[0]

        fields.append(self.v_falla_geologica.grado)
        fields.append(self.v_falla_geologica.valor)

        arcpy.AddMessage(self.messages.gen_task_grade)
        with arcpy.da.UpdateCursor(self.v_falla_geologica.path, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if i[0] == x[2]:
                        i[1], i[2] = x[3], x[4]
                        break
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.v_falla_geologica.path, self.v_falla_geologica.valor,
                                         self.r_falla_geologica.path, "CELL_CENTER", self.v_falla_geologica.valor,
                                         self.pixel)

    def method_depositos_minerales(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.eval_dm)

        self.pre_treatment(self.deposito_mineral.path, self.v_deposito_mineral.path, self.r_deposito_mineral.path)

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(self.deposito_mineral.path, self.v_deposito_mineral.path, 'NO_TEST')

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.deposito_mineral.path, self.unidad_geologica.valor,
                                         self.r_deposito_mineral.path, "CELL_CENTER", self.unidad_geologica.valor,
                                         self.pixel)

    def method_geo_quimica(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.eval_gq)
        if arcpy.Exists(self.geoquimica.path):
            arcpy.AddMessage(self.messages.eval_gq_task)
        else:
            raise RuntimeError(u'\tEl Raster Dataset de Geoquimica no existe o no fue cargado')

    def method_sensores_remotos(self):
        arcpy.AddMessage(self.messages.eval_sr)
        self.pre_treatment(self.sensor_remoto.path, self.v_sensor_remoto.path, self.r_sensor_remoto.path)

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(self.sensor_remoto.path, self.v_sensor_remoto.path, 'NO_TEST')

        erase = arcpy.Erase_analysis(self.limite.path, self.v_sensor_remoto.path, 'in_memory\\erase')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(erase, self.v_sensor_remoto.path, 'NO_TEST')

        sr_grado = tb_sr_grado(self.ws)

        fields = [sr_grado.condicion, sr_grado.grado, sr_grado.valor]
        grade = [i for i in arcpy.da.SearchCursor(sr_grado.path, fields)]

        del fields[0]
        fields.insert(0, self.sensor_remoto.tipo)

        arcpy.AddMessage(self.messages.gen_task_grade)
        with arcpy.da.UpdateCursor(self.v_sensor_remoto.path, fields) as cursor:
            for i in cursor:
                cond = i[0]
                if i[0] in (None, '', ' '):
                    cond = None
                if cond:
                    cond = i[0].lower()
                for x in grade:
                    if cond == x[0]:
                        i[1], i[2] = x[1], x[2]
                        break
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.v_sensor_remoto.path, sr_grado.valor, self.r_sensor_remoto.path,
                                         "CELL_CENTER", sr_grado.valor, self.pixel)

    def get_power_mining(self):
        arcpy.AddMessage(self.messages.eval_pm)

        if arcpy.Exists(self.r_potencial_minero.path):
            arcpy.Delete_management(self.r_potencial_minero.path)

        arcpy.env.outputCoordinateSystem = 4326
        fields = [self.pm_factor.nom_ras, self.pm_factor.factor]

        arcpy.AddMessage(self.messages.eval_pm_task)
        arcpy.CheckOutExtension("spatial")

        values = [arcpy.sa.Raster(os.path.join(self.ws, i[0])) * i[1] for i in
                  arcpy.da.SearchCursor(self.pm_factor.path, fields) if arcpy.Exists(os.path.join(self.ws, i[0]))]

        pm = sum(values)

        arcpy.AddMessage('\t   - Ponderacion:')
        for i in arcpy.da.SearchCursor(self.pm_factor.path, fields):
            if arcpy.Exists(os.path.join(self.ws, i[0])):
                arcpy.AddMessage('\t     * {:<30} {:>10}'.format(i[0], i[1]))

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        pm.save(self.r_potencial_minero.path)
        arcpy.CheckInExtension("spatial")

        arcpy.env.outputCoordinateSystem = self.src

        arcpy.SetParameterAsText(5, self.r_potencial_minero.path)

    def main(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.init_process)
        try:
            self.value_resources()
            self.method_unidades_geologicas()
            self.method_fallas_geologicas()
            self.method_concesiones_mineras()
            self.method_depositos_minerales()
            self.method_geo_quimica()
            self.method_sensores_remotos()
            self.get_power_mining()
            arcpy.AddMessage(self.messages.end_process)
        except Exception as e:
            arcpy.AddError('\n\t' + e.message + '\t')


if __name__ == '__main__':
    poo = PotencialMinero()
    arcpy.env.outputCoordinateSystem = poo.src
    poo.main()
