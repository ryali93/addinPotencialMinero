# -*- coding: utf-8 -*-

from model import *
from nls import *

arcpy.env.overwriteOutput = True


class PotencialMineroNoMetalico(object):


    ws = r'D:\RYali\TDR5\4product\borrar\PM_PIURA_5b47d4da-50f9-4df1-b7b1-5d80490eee3f\DRME_PM.gdb'
    pixel = '300'
    exportar = 'true'
    publicar = 'true'
    visualizar = 'true'
    # ws = arcpy.GetParameterAsText(0)
    # pixel = arcpy.GetParameterAsText(1)
    # exportar = arcpy.GetParameterAsText(2)
    # publicar = arcpy.GetParameterAsText(3)
    # visualizar = arcpy.GetParameterAsText(4)

    config = tb_config(ws)
    messages = Messages()

    limite = pm_region(ws)
    litologia = rmi_gpo_litologia(ws)
    accesos = rmi_gpl_accesos(ws)
    # catastro_minero = pm_catastro_minero(ws)
    # falla_geologica = pm_gpl_fallageologica(ws)
    # deposito_mineral = gpo_deposito_mineral(ws)
    sensor_remoto = rmi_gpo_sensores(ws)
    # geoquimica = ras_geoquimica(ws)

    var_litologia = rmi_var_litologia(ws)
    v_accesos = rmi_var_accesos(ws)
    # v_falla_geologica = var_falla_geologica(ws)
    # v_catastro_minero = var_concesion_minera(ws)
    # v_deposito_mineral = var_deposito_mineral(ws)
    v_sensor_remoto = rmi_var_sensores(ws)

    r_accesos = rmi_ras_accesos(ws)
    r_litologia = rmi_ras_litologia(ws)
    # r_falla_geologica = ras_falla_geologica(ws)
    # r_catastro_minero = ras_concesion_minera(ws)
    # r_deposito_mineral = ras_deposito_mineral(ws)
    r_sensor_remoto = rmi_ras_sensores(ws)

    pm_factor = rmi_tb_factor(ws)
    # r_potencial_minero = ras_potencial_minero(ws)

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

        intersect = arcpy.Intersect_analysis([erase, self.limite.path],
                                             os.path.join(TMP_GDB, "RMI_VAR_GPO_Accesos"),
                                             'ALL', '#', 'INPUT')

        arcpy.AddMessage(self.messages.gen_task_limites)
        arcpy.Append_management(intersect, self.v_accesos.path, 'NO_TEST')

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

    def get_no_metalic_potential(self):
        arcpy.AddMessage(self.messages.eval_pm)

    def main(self):
        """

        :return:
        """
        arcpy.AddMessage(self.messages.init_process)
        try:
            self.value_resources()
            self.method_accesos()
            self.get_no_metalic_potential()
            arcpy.AddMessage(self.messages.end_process)
        except Exception as e:
            arcpy.AddError('\n\t' + e.message + '\t')

if __name__ == '__main__':
    poo = PotencialMineroNoMetalico()
    arcpy.env.outputCoordinateSystem = poo.src
    poo.main()
