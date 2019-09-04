from settings import *


class gpo_dep_departamento(object):
    """
    FEATURE CLASS DE DEPARTAMENTOS EN LA GEODATABASECOORPORATIVA
    """

    def __init__(self):
        self.mn_depa = "NM_DEPA"

    @property
    def dataset(self):
        return 'DATA_GIS.DS_BASE_CATASTRAL_GEOWGS84'

    @property
    def name(self):
        return 'DATA_GIS.GPO_DEP_DEPARTAMENTO'

    @property
    def path(self):
        return os.path.join(CONN, self.dataset, self.name)


class gpo_cmi_catastro_minero(object):
    """
    FEATURE CLASS DE CATASTRO MINERO EN LA GEODATABASE COORPORATIVA
    """

    def __init__(self):
        self.id         = "OBJECTID"
        self.shape      = "SHAPE"
        self.leyenda    = "LEYENDA"
        self.naturaleza = "NATURALEZA"

    @property
    def dataset(self):
        return 'DATA_GIS.DS_CATASTRO_MINERO_GEOWGS84'

    @property
    def name(self):
        return 'DATA_GIS.GPO_CMI_CATASTRO_MINERO_G84'

    @property
    def path(self):
        return os.path.join(CONN, self.dataset, self.name)


class pm_region(object):
    """
    FEATURE CLASS DE DEPARTAMENTOS EN EL FILE GEODATABASE
    """

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_00_GPO_Region'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class pm_catastro_minero(object):
    """
    FEATURE CLASS DE CATASTRO MINERO EN EL FILE GEODATABASE
    """
    leyenda    = "LEYENDA"
    naturaleza = "NATURALEZA"

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_04_GPO_CatastroMinero'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class pm_gpl_fallageologica(object):
    """
    FEATURE CLASS DE FALLAS GEOLOGICAS EN EL FILE GEODATABASE
    """
    codi        = 'CODI'
    descripcion = 'DESCRIPCION'
    distancia   = 'DISTANCIA'

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_02_GPL_FallaGeologica'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class tb_falla_geologica(object):
    """
    FEATURE CLASS DE FALLAS GEOLOGICAS EN EL FILE GEODATABASE
    """
    nombre_falla = 'NOMBRE_FALLA'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_FG_Descripcion'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class gpo_unidad_geologica(object):
    """
    FEATURE CLASS DE UNIDADES GEOLOGICAS EN EL FILE GEODATABASE
    """
    codi = "CODI"
    nombre = "NOMBRE"
    descripcion = "DESCRIPCION"
    unidad = "UNIDAD"
    grado = "GRADO"
    valor = "VALOR"
    condicion = "CONDICION"

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_01_GPO_UnidadGeologica'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class tb_nivel(object):
    """
    TABLA QUE CONTIENE ELS NIVELES DE POTENCIAL PARA CADA VARIABEL
    EN EL FILE GEODATABASE
    """
    code  = "CODE"
    grado = "GRADO"
    vmin  = "VMIN"
    vmax  = "VMAX"

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_Grado'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class tb_ug_condicion(object):
    """
    TABLA QUE CONTIENE LA CONDICION METALOTECTO O NO METALOTECTO PARA EL
    FEATURE CLASS DE UNIDADES GEOLOGICAS
    """
    code = "CODE"
    descrip = "DESCRIP"

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_UG_Condicion'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class gpo_deposito_mineral(object):
    """
    FEATURE CLASS DE DEPOSITOS MINERALES EN EL FILE GEODATABASE
    """
    dimension = "DIMENSION"
    unidad    = "UNIDAD"
    grado     = "GRADO"
    valor     = "VALOR"

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_03_GPO_DepositoMineral'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class gpo_sensores_remotos(object):
    """
    FEATURE CLASS DE LA VARIABLE SENSORES REMOTOS
    """
    tipo_arc = "TIPO_ARC"
    tipo_oxi = "TIPO_OXI"
    tipo     = "TIPO"

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'PM_05_GPO_SensorRemoto'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class ras_geoquimica(object):
    """
    RASTER DE LA VARIABLE GEOQUIMICA EN EL FILE GEODATABASE
    """

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        """
        Nombre de la capa
        :return:
        """
        return 'PM_VAR_RAS_Geoquimica'

    @property
    def path(self):
        """
        Direccion de la capa
        :return:
        """
        return os.path.join(self.ws, self.name)


class tb_config(object):
    region    = 'REGION'
    zona      = 'ZONA'
    ubicacion = 'UBICACION'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return '_config'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class var_unidad_geologica(object):
    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'PM_VAR_GPO_UnidadGeologica'

    @property
    def dataset(self):
        return 'DS_02_Variables'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class var_falla_geologica(var_unidad_geologica):
    grado      = 'GRADO'
    valor      = 'VALOR'
    influencia = 'INFLUENCIA'

    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_GPO_FallaGeologica'


class var_concesion_minera(var_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_GPO_ConcesionMinera'


class var_deposito_mineral(var_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_GPO_DepositoMineral'


class var_sensor_remoto(var_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_GPO_SensorRemoto'


class ras_unidad_geologica(object):
    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'PM_VAR_RAS_UnidadGeologica'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class ras_falla_geologica(ras_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_RAS_FallaGeologica'


class ras_concesion_minera(ras_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_RAS_ConcesionMinera'


class ras_deposito_mineral(ras_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_RAS_DepositoMineral'


class ras_sensor_remoto(ras_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_VAR_RAS_SensorRemoto'


class ras_potencial_minero(ras_unidad_geologica):
    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'PM_RAS_PotencialMinero'


class tb_cm_grado(object):
    leyenda = 'LEYENDA'
    condicion = 'CONDICION'
    grado = 'GRADO'
    valor = 'VALOR'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_CM_Grado'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class tb_sr_grado(object):
    condicion = 'CONDICION'
    grado = 'GRADO'
    valor = 'VALOR'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_SR_Grado'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class tb_fg_grado(object):
    dist_min = 'DIST_MIN'
    dist_max = 'DIST_MAX'
    influencia = 'INFLUENCIA'
    grado = 'GRADO'
    valor = 'VALOR'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_FG_Grado'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)


class tb_pm_factor(object):
    nom_ras = 'NOM_RAS'
    factor = 'FACTOR'

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_PM_Factor'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)

########################################################################
# Potencial Minero No Metalico

class gpl_vias(object):
    """
    FEATURE CLASS DE VIAS EN LA GEODATABASE COORPORATIVA
    """

    def __init__(self):
        self.id = "OBJECTID"
        self.shape = "SHAPE"
        self.tipo = "RASGO_SECU"
        self.nombre = "NOMBRE"

    @property
    def dataset(self):
        return 'DATA_GIS.DS_IGN_BASE_PERU_500000'

    @property
    def name(self):
        return 'DATA_GIS.IGN_TRA_VIAS'

    @property
    def path(self):
        return os.path.join(CONN, self.dataset, self.name)

class gpt_sustancias(object):
    """
    FEATURE CLASS DE SUSTANCIAS EN LA GEODATABASE COORPORATIVA
    """
    def __init__(self):
        self.id = "OBJECTID"
        self.shape = "SHAPE"
        self.sustancia = "SUSTANCIA"

    @property
    def dataset(self):
        return 'DATA_EDIT.DS_GEOCATMIN'

    @property
    def name(self):
        return 'DATA_EDIT.GPT_RMI_Roc_Min_Ind'

    @property
    def path(self):
        return os.path.join(CONN, self.dataset, self.name)

class rmi_sustancias(object):
    """
    
    """

class rmi_accesos(object):
    """
    FEATURE CLASS DE ACCESOS EN EL FILE GEODATABASE
    """
    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'RMI_12_GPL_Accesos'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class tb_accesos(object):
    """
    TABLA DE ACCESOS EN EL FILE GEODATABASE
    """
    tipo = "TIPO"
    grado = "GRADO"
    buffer = "BUFFER"
    valor = "VALOR"

    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'TB_RMI_Accesos'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)

class gpo_litologia(object):
    """
    FEATURE CLASS DE UNIDADES GEOLOGICAS EN EL FILE GEODATABASE
    """
    codi = "CODI"
    nombre = "NOMBRE"
    descripcion = "DESCRIPCION"
    unidad = "UNIDAD"
    grado = "GRADO"
    valor = "VALOR"

    def __init__(self, ws):
        self.ws = ws

    @property
    def dataset(self):
        return 'DS_01_Insumos'

    @property
    def name(self):
        return 'RMI_08_GPO_Litologia'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)

class var_litologia(object):
    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'RMI_VAR_GPO_Litologia'

    @property
    def dataset(self):
        return 'DS_02_Variables'

    @property
    def path(self):
        return os.path.join(self.ws, self.dataset, self.name)


class var_accesos(var_litologia):
    """
    :return
    """
    tipo = 'TIPO'
    grado = 'GRADO'
    buffer = 'BUFFER'
    valor = 'VALOR'

    def __init__(self, ws):
        super(self.__class__, self).__init__(ws)

    @property
    def name(self):
        return 'RMI_VAR_GPO_Accesos'

class ras_accesos(object):
    def __init__(self, ws):
        self.ws = ws

    @property
    def name(self):
        return 'RMI_VAR_RAS_Accesos'

    @property
    def path(self):
        return os.path.join(self.ws, self.name)
