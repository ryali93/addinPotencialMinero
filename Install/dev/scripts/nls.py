#!/usr/bin/python
# -*- coding: utf-8 -*-


class Messages(object):
    init_process = u'\n\tIniciando procesamiento'
    end_process = u'\n\tProceso finalizado con éxito\n'
    make_dir = u'\t1. Creando espacio de trabajo'
    make_gdb = u'\t2. Construyendo geodatabase'
    get_info = u'\t3. Consultando capas disponibles en base de datos'
    check_gdb = u'\t1. Comprobando la existencia de la geodatabase ingresada'
    check_info = u'\t2. Verificando datos erroneos'
    send_database = u'\t3. Enviando información a geodatabase'
    error_gdb_type = u'El tipo de espacio de trabajo agregado no es correcto'
    error_info = u'Se detectaron registros incorrectos'

    """ Calculo del Potencial Minero """

    eval_ug = u'\n\t1. Evaluación de variable de Unidades Geológicas'

    eval_fg = u'\n\t2. Evaluación de variable de Fallas Geológicas'
    eval_fg_task_radio = u'\t   - Estimando el radio de influencia para cada falla geológica'
    eval_fg_task_influencia = u'\t   - Calculando las zonas de influencia'

    eval_cm = u'\n\t3. Evaluación de variable de Concesiones Mineras'
    eval_cm_task_overlap = u'\t   - Superposición entre el insumo de Catastro Minero y Unidades Geológicas'

    eval_dm = u'\n\t4. Evaluación de variable de Depositos Minerales'

    eval_gq = u'\n\t5. Evaluación de variable de Geoquímica'
    eval_gq_task = u'\t   - Se comprobó existencia del dataset raster de Geoquímica'

    eval_sr = u'\n\t6. Evaluación de variable Sensores Remotos'

    eval_pm = u'\n\t7. Evaluación el Potencial Minero'
    eval_pm_task = u'\t   - Algebra de mapas entre las variables establecidas'

    gen_task_grade = u'\t   - Estimando el grado y valor'
    gen_task_limites = u'\t   - Configurando límites en base a la región'
    gen_task_save_fc = u'\t   - Almacenando resultado como Feature Class en el File Geodatabase'
    gen_task_save_ra = u'\t   - Almacenando resultado como Raster Dataset en el File Geodatabase'
