domains = {
    "unidadesGeologicas": {
        "GRADO": ["muy alto", "alto", "medio", "bajo", "muy bajo"],
        "VALOR": {"min": 1.2, "max": 3.0},
        "CONDICION": ["metalotecto", "no metalotecto"]
    },
    "fallasGeologicas": {
        "DESCRIPCION": ["falla", "falla normal","falla inversa","falla de rumbo","eje anticlinal","eje sinclinal","eje anticlinal volcado","eje sinclinal volcado"]
    },
    "depositosMinerales": {
        "GRADO": ["muy alto", "alto", "medio", "bajo", "muy bajo"],
        "VALOR": {"min": 1.2, "max": 3.0}
    }
}

directoryStructure = {
    "dataBase": {
        "entityUsed": {
            "departamento": {
                "fdname": "DATA_GIS.DS_BASE_CATASTRAL_GEOWGS84",
                "fcname": "DATA_GIS.GPO_DEP_DEPARTAMENTO",
                "fullname": "DATA_GIS.DS_BASE_CATASTRAL_GEOWGS84\\DATA_GIS.GPO_DEP_DEPARTAMENTO",
                "fieldSql": "NM_DEPA"
            },
            "catastro": {
                "fcname": "GPO_CMI_CATASTRO_MINERO_G84"
            }
        },
        "sqlSpatial": {
            "fieldSelect": "OBJECTID, SHAPE, LEYENDA, NATURALEZA",
            "fromfc": "GPO_CMI_CATASTRO_MINERO_G84",
            "where": "(LEYENDA = 'TITULADO') AND (NATURALEZA = 'M')",
            "uniqueField": "OBJECTID"
        }
    },
    "nameElements": {
        "modelId": "PM__",
        "folderMain": "PM_Region",
        "gdb": "POTENCIAL_MINERO",
        "fds": {
            "insumos": "FD1_INSUMOS",
            "variables": "FD2_VARIABLES"
        },
        "fcs": {
            "region": "PM_V0_Region",
            "catastro": "PM_V0_CatastroMinero",
            "geologia": "PM_V1_UnidadesGeologicas",
            "fallas": "PM_V3_FallasGeologicas",
            "depositos": "PM_V4_DepositosMinerales",
            "sensores": "PM_V6_SensoresRemotos"
        }
    },
    "featureClass": {
        "geologia": {
            "nombre": "PM_V1_UnidadesGeologicas",
            "esrijson": {
                "displayFieldName": "",
                "fieldAliases": {
                    "CODI": "CODI",
                    "GRADO": "GRADO",
                    "VALOR": "VALOR",
                    "CONDICION": "CONDICION"
                },
                "geometryType": "esriGeometryPolygon",
                "fields": [
                    {
                        "name": "CODI",
                        "type": "esriFieldTypeSmallInteger",
                        "alias": "CODI",
                        "length": 4
                    },
                    {
                        "name": "GRADO",
                        "type": "esriFieldTypeString",
                        "alias": "GRADO",
                        "length": 50
                    },
                    {
                        "name": "VALOR",
                        "type": "esriFieldTypeDouble",
                        "alias": "VALOR"
                    },
                    {
                        "name": "CONDICION",
                        "type": "esriFieldTypeString",
                        "alias": "CONDICION",
                        "length": 50
                    }
                ],
                "features": []
            }
        },
        "fallas": {
            "nombre": "PM_V3_FallasGeologicas",
            "esrijson": {
                "displayFieldName": "",
                "fieldAliases": {
                    "CODI": "CODI",
                    "DESCRIPCION": "DESCRIPCION"
                },
                "geometryType": "esriGeometryPolyline",
                "fields": [
                    {
                        "name": "CODI",
                        "type": "esriFieldTypeSmallInteger",
                        "alias": "CODI",
                        "length": 4
                    },
                    {
                        "name": "DESCRIPCION",
                        "type": "esriFieldTypeString",
                        "alias": "DESCRIPCION",
                        "length": 50
                    }
                ],
                "features": []
            }
        },
        "depositos": {
            "nombre": "PM_V4_DepositosMinerales",
            "esrijson": {
                "displayFieldName": "",
                "fieldAliases": {
                    "GRADO": "GRADO",
                    "VALOR": "VALOR"
                },
                "geometryType": "esriGeometryPolygon",
                "fields": [
                    {
                        "name": "GRADO",
                        "type": "esriFieldTypeString",
                        "alias": "GRADO",
                        "length": 50
                    },
                    {
                        "name": "VALOR",
                        "type": "esriFieldTypeDouble",
                        "alias": "VALOR"
                    }
                ],
                "features": []
            }
        },
        "sensores": {
            "nombre": "PM_V6_SensoresRemotos",
            "esrijson": {
                "displayFieldName": "",
                "fieldAliases": {
                    "TIPO_ARC": "TIPO_ARC",
                    "TIPO_OXI": "TIPO_OXI",
                    "TIPO": "TIPO"
                },
                "geometryType": "esriGeometryPolygon",
                "fields": [
                    {
                        "name": "TIPO_ARC",
                        "type": "esriFieldTypeString",
                        "alias": "TIPO_ARC",
                        "length": 50
                    },
                    {
                        "name": "TIPO_OXI",
                        "type": "esriFieldTypeString",
                        "alias": "TIPO_OXI",
                        "length": 50
                    },
                    {
                        "name": "TIPO",
                        "type": "esriFieldTypeString",
                        "alias": "TIPO",
                        "length": 50
                    }
                ],
                "features": []
            }
        }
    }
}


ds_insumos = 'FD1_INSUMOS'
ds_variables = 'FD2_VARIABLES'

cuadrante = 'PM_V0_Cuadrante'
region = 'PM_V0_Region'
catastro = "PM_V0_CatastroMinero",
geologia = "PM_V1_UnidadesGeologicas",
fallas = "PM_V3_FallasGeologicas",
depositos = "PM_V4_DepositosMinerales",
sensores = "PM_V6_SensoresRemotos"

fd_codi = 'CODI'
fd_descrip = 'DESCRIPCION'
fd_valor = 'VALOR'
fd_grado = 'GRADO'
fd_leyenda = 'LEYENDA'
fd_condicion = 'CONDICION'
fd_influencia = 'INFLUENCIA'
fd_tipo = 'TIPO'

geologia_fc = 'VAR_UNID_GEOLOGI_VEC'
geologia_ras = 'VAR_UNID_GEOLOGI_RAS'
geologia_tex = 'Unidades Geologicas'

concesiones_fc = 'VAR_CONC_MINERAS_VEC'
concesiones_ras = 'VAR_CONC_MINERAS_RAS'
concesiones_tex = 'Concesiones Mineras'

fallas_fc = 'VAR_FALLAS_VEC'
fallas_ras = 'VAR_FALLAS_RAS'
fallas_tex = 'Fallas Geologicas'

depositos_fc = 'VAR_DEPO_MINERAL_VEC'
depositos_ras = 'VAR_DEPO_MINERAL_RAS'
depositos_tex = 'Depositos Minerales'

geoquimica_ras = 'VAR_GEOQUIMICA_RAS'
geoquimica_tex = 'Geoquimica'

sensores_fc = 'VAR_SENS_REMOTOS_VEC'
sensores_ras = 'VAR_SENS_REMOTOS_RAS'
sensores_tex = 'Sensores Remotos'

potMinero_ras = 'POTENCIAL_MINERO_RAS'
