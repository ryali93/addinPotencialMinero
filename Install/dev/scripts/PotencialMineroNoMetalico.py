# -*- coding: utf-8 -*-

from model import *
from nls import *

arcpy.env.overwriteOutput = True


class PotencialMineroNoMetalico(object):
    tipo_pot = 'no metalico'

    ws = arcpy.GetParameterAsText(0)
    pixel = arcpy.GetParameterAsText(1)
    exportar = arcpy.GetParameterAsText(2)
    publicar = arcpy.GetParameterAsText(3)
    visualizar = arcpy.GetParameterAsText(4)

    config = tb_config(ws)
    messages = Messages()

    limite = pm_region(ws)
    litologia = rmi_gpo_litologia(ws)
    accesos = rmi_gpl_accesos(ws)
    catastro_minero = rmi_gpo_concmin(ws)
    sensor_remoto = rmi_gpo_sensores(ws)
    sustancia = rmi_gpt_sustancias(ws)

    v_litologia = rmi_var_litologia(ws)
    v_accesos = rmi_var_accesos(ws)
    v_catastro_minero = rmi_var_concmin(ws)
    v_sensor_remoto = rmi_var_sensores(ws)
    v_sustancia = rmi_var_sustancias(ws)

    r_accesos = rmi_ras_accesos(ws)
    r_litologia = rmi_ras_litologia(ws)
    r_catastro_minero = rmi_ras_concmin(ws)
    r_sensor_remoto = rmi_ras_sensores(ws)
    r_sustancia = rmi_ras_sustancias(ws)

    pm_factor = rmi_tb_factor(ws)
    r_potencial_minero = ras_potencial_minero_no_metalico(ws)

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

    def method_litologia(self):
        """
        :return:
        """
        arcpy.AddMessage(self.messages.eval_lito)

        self.pre_treatment(self.litologia.path, self.v_litologia.path, self.r_litologia.path)

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(self.litologia.path, self.v_litologia.path, 'NO_TEST')

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.litologia.path, self.litologia.valor,
                                         self.r_litologia.path, "CELL_CENTER", self.litologia.valor,
                                         self.pixel)

    def method_concesiones(self):
        """
        :return:
        """
        arcpy.AddMessage(self.messages.eval_cm)

        self.pre_treatment(self.catastro_minero.path, self.v_catastro_minero.path, self.r_catastro_minero.path)

        fields = [self.catastro_minero.leyenda, self.catastro_minero.naturaleza]

        dissolve = arcpy.Dissolve_management(self.catastro_minero.path, 'in_memory\\feature', fields, '#', 'MULTI_PART',
                                             'DISSOLVE_LINES')

        input_feature = [dissolve, self.litologia.path]

        arcpy.AddMessage(self.messages.eval_cm_task_overlap)
        union = arcpy.Union_analysis(input_feature, 'in_memory\\union', 'ALL', '#', 'GAPS')

        fields = [self.catastro_minero.leyenda, self.litologia.condicion, self.litologia.valor,
                  self.litologia.grado, ]

        cm_grado = rmi_tb_concmin_grado(self.ws)

        query = "{} = '{}'".format(cm_grado.tipo, self.tipo_pot)
        grade = [i for i in arcpy.da.SearchCursor(cm_grado.path, fields, query)]

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
        arcpy.PolygonToRaster_conversion(self.v_catastro_minero.path, self.litologia.valor,
                                         self.r_catastro_minero.path, "CELL_CENTER", self.litologia.valor,
                                         self.pixel)


    def method_accesos(self):
        arcpy.AddMessage(self.messages.eval_vias)

        self.pre_treatment(self.accesos.path, self.v_accesos.path, self.r_accesos.path)

        feature = arcpy.CopyFeatures_management(self.accesos.path, 'in_memory\\feature')

        arcpy.AddField_management(feature, self.accesos.influencia, 'DOUBLE')

        fields = [self.accesos.tipo, self.accesos.influencia]

        tb_vias = rmi_tb_accesos(self.ws)

        fields_vias_tipo = [tb_vias.tipo, tb_vias.grado, tb_vias.influencia, tb_vias.valor]

        grade = [i for i in arcpy.da.SearchCursor(tb_vias.path, fields_vias_tipo)]

        arcpy.AddMessage(self.messages.eval_vias_task_radio)

        with arcpy.da.UpdateCursor(feature, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if x[0] == i[0]:
                        i[1] = x[2]
                        break
                cursor.updateRow(i)
            del cursor

        dissolve = arcpy.Dissolve_management(feature, 'in_memory\\dissolve', self.v_accesos.influencia, "#",
                                             'MULTI_PART', 'DISSOLVE_LINES')

        arcpy.AddMessage(self.messages.eval_vias_task_influencia)
        influencia = arcpy.Buffer_analysis(dissolve, 'in_memory\\buffer', self.v_accesos.influencia)

        arcpy.Append_management(influencia, self.v_accesos.path, 'NO_TEST')

        erase = arcpy.Erase_analysis(self.limite.path, self.v_accesos.path, 'in_memory\\erase')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(erase, self.v_accesos.path, 'NO_TEST')

        del fields[0]

        fields.append(self.v_accesos.grado)
        fields.append(self.v_accesos.valor)

        arcpy.AddMessage(self.messages.gen_task_grade)
        valores = [x[0] for x in arcpy.da.SearchCursor(tb_vias.path, [tb_vias.valor])]
        with arcpy.da.UpdateCursor(self.v_accesos.path, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if i[0] == x[2]:
                        i[1], i[2] = x[1], x[3]
                        break
                if i[0] == None:
                    i[2] = min(valores)
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.v_accesos.path, self.v_accesos.valor,
                                         self.r_accesos.path, "CELL_CENTER", self.v_accesos.valor,
                                         self.pixel)

    def method_sensores_remotos(self):
        arcpy.AddMessage(self.messages.eval_sr_rmi)
        self.pre_treatment(self.sensor_remoto.path, self.v_sensor_remoto.path, self.r_sensor_remoto.path)

        arcpy.AddMessage(self.messages.gen_task_save_fc)
        arcpy.Append_management(self.sensor_remoto.path, self.v_sensor_remoto.path, 'NO_TEST')

        erase = arcpy.Erase_analysis(self.limite.path, self.v_sensor_remoto.path, 'in_memory\\erase')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(erase, self.v_sensor_remoto.path, 'NO_TEST')

        sr_grado = pmm_tb_sensores_grado(self.ws)

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

    def method_sustancias(self):
        arcpy.AddMessage(self.messages.eval_sust)

        self.pre_treatment(self.sustancia.path, self.v_sustancia.path, self.r_sustancia.path)

        feature = arcpy.CopyFeatures_management(self.sustancia.path, 'in_memory\\feature')

        arcpy.AddField_management(feature, self.v_sustancia.influencia, 'DOUBLE')

        fields = [self.v_sustancia.sustancia, self.v_sustancia.influencia, self.v_sustancia.valor, self.v_sustancia.grado]

        sust_grado = rmi_tb_sustancias(self.ws)

        fields_grado = [sust_grado.sustancia, sust_grado.influencia, sust_grado.valor, sust_grado.grado]

        grade = [i for i in arcpy.da.SearchCursor(sust_grado.path, fields_grado)]

        arcpy.AddMessage(self.messages.eval_sust_task_radio)

        with arcpy.da.UpdateCursor(feature, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if i[0] == x[0]:
                        i[1] = x[1]
                        i[2] = x[2]
                        i[3] = x[3]
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.eval_sust_task_influencia)
        influencia = arcpy.Buffer_analysis(feature, 'in_memory\\buffer', self.v_sustancia.influencia)

        arcpy.Append_management(influencia, self.v_sustancia.path, 'NO_TEST')

        erase = arcpy.Erase_analysis(self.limite.path, self.v_sustancia.path, 'in_memory\\erase')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(erase, self.v_sustancia.path, 'NO_TEST')

        arcpy.AddMessage(self.messages.gen_task_grade)
        with arcpy.da.UpdateCursor(self.v_sustancia.path, fields) as cursor:
            for i in cursor:
                for x in grade:
                    if i[0] == x[0]:
                        i[2] = x[2]
                        i[3] = x[3]
                if i[0] == None:
                    i[2] = 1
                cursor.updateRow(i)
            del cursor

        arcpy.AddMessage(self.messages.gen_task_save_ra)
        arcpy.PolygonToRaster_conversion(self.v_sustancia.path, self.v_sustancia.valor,
                                         self.r_sustancia.path, "CELL_CENTER", self.v_sustancia.valor,
                                         self.pixel)

    def get_no_metalic_potential(self):
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
            self.method_litologia()
            self.method_sustancias()
            self.method_concesiones()
            self.method_sensores_remotos()
            self.method_accesos()
            self.get_no_metalic_potential()
            arcpy.AddMessage(self.messages.end_process)
        except Exception as e:
            arcpy.AddError('\n\t' + e.message + '\t')

if __name__ == '__main__':
    poo = PotencialMineroNoMetalico()
    arcpy.env.outputCoordinateSystem = poo.src
    poo.main()
