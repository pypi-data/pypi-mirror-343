import json

from django.db import connections, ProgrammingError

from isapilib.models import ApiLogs


def execute_query(query, sp_params=None, using='default'):
    cursor = connections[using].cursor()

    try:
        cursor.execute(query, sp_params or [])
        results = cursor.fetchall()
    finally:
        cursor.close()

    return results


def declare_variable(name, type, length):
    declaration = f'{name} '

    if type in ('varchar', 'char'):
        declaration += f"{type}({'MAX' if length == -1 else length})"
    else:
        declaration += f'{type}'

    return declaration


def execute_sp(sp_name, sp_params=None, using='default'):
    sp_params = sp_params or []
    sp_output = execute_query('''
        SELECT 
            PARAMETER_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
        FROM information_schema.parameters WHERE SPECIFIC_NAME = %s AND PARAMETER_MODE = 'INOUT'
        ''', [sp_name], using=using)

    if isinstance(sp_params, dict):
        parameters = ', '.join([f'@{i}=%s' for i in sp_params.keys()])
    else:
        parameters = ', '.join(['%s' for _ in sp_params])

    sp_call = f'''
        {'SET NOCOUNT ON;' if len(sp_output) > 0 else ''}
        {'DECLARE' if len(sp_output) > 0 else ''} {', '.join([declare_variable(name, type, length) for name, type, length in sp_output])};
        EXEC {sp_name} {parameters}{', ' if len(sp_output) > 0 else ''}{', '.join([f'{name}={name} OUTPUT' for name, _, _ in sp_output])};
        {'SELECT' if len(sp_output) > 0 else ''} {', '.join([name for name, _, _ in sp_output])};
    '''

    cursor = connections[using].cursor()

    try:
        cursor.execute(sp_call, list(sp_params.values()) if isinstance(sp_params, dict) else sp_params or [])
        results = []
        while True:
            try:
                result = cursor.fetchall()
                results.append(result)
                cursor.nextset()
            except ProgrammingError:
                return results[-1] if len(results) > 0 else None
    finally:
        cursor.close()


def execute_fn(fn_name, fn_params=None, using='default'):
    query = f'''SELECT dbo.{fn_name}({', '.join(['%s' for _ in fn_params])})'''
    return execute_query(query, fn_params, using=using)


def get_sucursal(modulo='VTAS', mov='Servicio', sucursal=0, using='default'):
    results = execute_fn("fnCA_GeneraSucursalValida", [modulo, mov, sucursal], using=using)
    return results[0][0]


def get_almacen(modulo='VTAS', mov='Servicio', sucursal=0, using='default'):
    results = execute_fn("fnCA_GeneraAlmacenlValido", [modulo, mov, sucursal], using=using)
    return results[0][0]


def get_uen(modulo='VTAS', mov='Servicio', sucursal=0, concepto='Publico', using='default'):
    results = execute_fn("fnCA_GeneraUENValida", [modulo, mov, sucursal, concepto], using=using)
    return results[0][0]


def get_param_empresa(interfaz, clave, using='default'):
    results = execute_fn('fnCA_BusquedaClaveParametroInterfazEmpresa', [interfaz, clave], using=using)
    return results[0][0]


def get_param_sucursal(sucursal, clave, using='default'):
    results = execute_fn('fnCA_CatParametrosSucursalValor', [sucursal, clave], using=using)
    return results[0][0]


def insert_log(request, response, interfaz, tipo, time=0):
    try:
        response_content = response.content
        log = ApiLogs()
        log.iduser = request.user.pk
        log.tipo = str(tipo or '')
        log.header = str(json.dumps(dict(request.headers)))
        log.request = str(json.dumps(request.data) if isinstance(request.data, (dict, list)) else request.data or '')
        log.response = str(response_content.decode('utf-8') or '')
        log.status = response.status_code if hasattr(response, 'status_code') else 0
        log.url = request.build_absolute_uri()
        log.interfaz = str(interfaz or '')
        log.response_time = time
        log.save()
    except Exception as e:
        print(f'Warning: Failed to save logs', e)


def clean_request_json(request: dict) -> dict:
    cleaned_request = {}
    for k, v in request.items():
        if v is None or v == '':
            continue

        if isinstance(v, dict):
            v = clean_request_json(v)

        cleaned_request[k] = v

    return cleaned_request
