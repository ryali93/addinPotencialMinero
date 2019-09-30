# -*- coding: utf-8 -*-

from model import *
from nls import *

arcpy.env.overwriteOutput = True

class PotencialMinero(object):
    ws = arcpy.GetParameterAsText(0)
    pm_metalico = arcpy.GetParameterAsText(1)
    pm_no_metalico = arcpy.GetParameterAsText(2)

    config = tb_config(ws)
    messages = Messages()

    pm_factor = pm_tb_factor(ws)
    r_potencial_no_metalico = ras_potencial_minero_no_metalico(ws)
    r_potencial_metalico = ras_potencial_minero_metalico(ws)
    r_potencial_minero = ras_potencial_minero(ws)

    def mining_potential(self):
        arcpy.AddMessage(self.messages.eval_potmin)

        if arcpy.Exists(self.r_potencial_minero.path) and arcpy.Exists(self.r_potencial_minero.path):
            pass
        product_raster = '{} * {}'.format(self.r_potencial_no_metalico.path, self.r_potencial_metalico.path)
        arcpy.gp.RasterCalculator_sa(product_raster, self.r_potencial_minero.path)

    def main(self):
        arcpy.AddMessage(self.messages.init_process)
        self.mining_potential()

        arcpy.SetParameterAsText(3, self.r_potencial_minero.path)

if __name__ == "__main__":

    try:
        poo = PotencialMinero()
        poo.main()

    except Exception as e:
        arcpy.AddError('\n\t%s\n' % e.message)
