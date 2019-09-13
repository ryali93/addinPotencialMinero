from nls import *
from model import *
from function import *

arcpy.env.overwriteOutput = True
msg = Messages()


class MakeGdb(object):
    global pm_region
    def __init__(self, path, type_pot, region, zone):
        self.path = path
        self.type_pot = type_pot
        self.region = region
        self.zone = zone
        self.code = self.region[0:2]
        self.name_reg = self.region[5:]
        self.gdb_input = path_database_input(self.zone)
        self.main_folder = str()
        self.name_main_folder = name_folder(self.name_reg)


    def get_main_folder(self):
        dirr = os.path.join(self.path, self.name_main_folder)
        if not os.path.exists(dirr):
            arcpy.CreateFolder_management(self.path, self.name_main_folder)
            self.main_folder = dirr

    def copy_gdb(self):
        self.output_path_gdb = os.path.join(self.main_folder, os.path.basename(self.gdb_input))
        arcpy.Copy_management(self.gdb_input, self.output_path_gdb)

    def need_features(self):
        self.dep = pm_region(self.output_path_gdb)
        self.via = rmi_gpl_accesos(self.output_path_gdb)
        self.sustancia = rmi_gpt_sustancias(self.output_path_gdb)

        if self.type_pot == "Metalico":
            self.cat = pmm_gpo_concmin(self.output_path_gdb)
        else:
            self.cat = rmi_gpo_concmin(self.output_path_gdb)

    def limit_region(self):
        dep = gpo_region()
        query = "%s = '%s'" % (dep.mn_depa, self.name_reg)
        lim_reg_mfl = arcpy.MakeFeatureLayer_management(dep.path, "mfl_dep", query)
        arcpy.Append_management(lim_reg_mfl, self.dep.path, "NO_TEST")

    def catastro_mine(self):
        cat = gpo_catastro_minero()
        if self.type_pot == "Metalico":
            query = "%s = 'TITULADO' AND (%s = 'M')" % (cat.leyenda, cat.naturaleza)
        else:
            query = "%s = 'TITULADO' AND (%s = 'N')" % (cat.leyenda, cat.naturaleza)

        catastro_tmp = arcpy.MakeFeatureLayer_management(cat.path, 'mfl_cat_min', query)

        arcpy.SelectLayerByLocation_management(catastro_tmp, "INTERSECT", self.dep.path, "#", "NEW_SELECTION", "NOT_INVERT")

        fc_download = arcpy.CopyFeatures_management(catastro_tmp, os.path.join(TMP_GDB, 'catastro_copy'))

        cmi_clip_for_region = arcpy.Clip_analysis(fc_download, self.dep.path, os.path.join(TMP_GDB, 'catastro_clip'))

        arcpy.Append_management(cmi_clip_for_region, self.cat.path, "NO_TEST")

    def vias(self):
        if self.type_pot == "No Metalico":
            vias = rmi_accesos()
            vias_tmp = arcpy.MakeFeatureLayer_management(vias.path, 'mfl_vias')

            arcpy.SelectLayerByLocation_management(vias_tmp, "INTERSECT", self.dep.path, "#", "NEW_SELECTION",
                                                   "NOT_INVERT")

            fc_download = arcpy.CopyFeatures_management(vias_tmp, os.path.join(TMP_GDB, 'vias_copy'))

            vias_clip_for_region = arcpy.Clip_analysis(fc_download, self.dep.path, os.path.join(TMP_GDB, 'vias_clip'))

            arcpy.Append_management(vias_clip_for_region, self.via.path, "NO_TEST")

            try:
                update_fields_accesos(self.via.path)
            except:
                pass

            arcpy.SetParameterAsText(6, poo.via.path)

    def sustancias(self):
        if self.type_pot == "No Metalico":
            sust = rmi_sustancias()
            sust_tmp = arcpy.MakeFeatureLayer_management(sust.path, 'mfl_sust')

            arcpy.SelectLayerByLocation_management(sust_tmp, "INTERSECT", self.dep.path, "#", "NEW_SELECTION",
                                                   "NOT_INVERT")

            fc_download = arcpy.CopyFeatures_management(sust_tmp, os.path.join(TMP_GDB, 'sust_copy'))

            sust_clip_for_region = arcpy.Clip_analysis(fc_download, self.dep.path, os.path.join(TMP_GDB, 'sust_clip'))

            arcpy.Append_management(sust_clip_for_region, self.sustancia.path, "NO_TEST")

            arcpy.SetParameterAsText(7, poo.sustancia.path)

    def update_config(self):
        config = tb_config(self.output_path_gdb)
        cursor = arcpy.da.InsertCursor(config.path, [config.region, config.zona, config.ubicacion])
        cursor.insertRow((self.name_reg, int('327' + str(self.zone)), self.path))
        del cursor

    def main(self):
        arcpy.AddMessage(msg.init_process)
        arcpy.AddMessage(msg.make_dir)
        self.get_main_folder()
        arcpy.AddMessage(msg.make_gdb)
        self.copy_gdb()
        arcpy.AddMessage(msg.get_info)
        self.need_features()
        self.limit_region()
        self.catastro_mine()
        self.vias()
        self.sustancias()
        self.update_config()
        arcpy.AddMessage(msg.end_process)

if __name__ == "__main__":
    try:
        path = arcpy.GetParameterAsText(0)
        type_pot = arcpy.GetParameterAsText(1)
        region = arcpy.GetParameterAsText(2)
        zone = arcpy.GetParameterAsText(3)
        poo = MakeGdb(path, type_pot, region, zone)
        poo.main()
        arcpy.SetParameterAsText(4, poo.dep.path)
        arcpy.SetParameterAsText(5, poo.cat.path)

    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
