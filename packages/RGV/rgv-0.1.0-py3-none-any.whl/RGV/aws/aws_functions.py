import sys
import os
import time
import boto3
import s3fs
import json
import csv
import openpyxl
import logging
import pymysql
import pandas as pd
import polars as pl
import geopandas as gpd
import pyarrow.parquet as pq
from decimal import Decimal
from dotenv import load_dotenv
from botocore.config import Config
from botocore.exceptions import ClientError
from collections import defaultdict

# VARIABLES GENERALES
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_ = os.listdir(parent_dir)
os.chdir(parent_dir)

def setup_logger(verbose: bool = False):
    """
    Configura el logger global de la librería según el parámetro verbose.

    Args:
        verbose (bool): Si es True, establece nivel INFO. Si es False, 
        establece nivel WARNING.
    """
    logging_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Función para encontrar automáticamente la ruta del archivo CSV con credenciales
def obtener_ruta_csv_credenciales(nombre_csv='authorization.csv', verbose=False):
    setup_logger(verbose)
    repositorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    for root, dirs, files in os.walk(repositorio_raiz):
        if f'05_otros{os.sep}{nombre_csv}' in os.path.join(root, nombre_csv):
            ruta_completa = os.path.join(root, nombre_csv)
            if os.path.isfile(ruta_completa):
                return ruta_completa
    return None

# Función para cargar credenciales de AWS
def cargar_credenciales_aws(sistema='aws', verbose=False):
    setup_logger(verbose)
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION")

    # Si las variables de entorno no están disponibles, intenta cargar desde CSV
    if not aws_access_key or not aws_secret_key:
        ruta_csv = obtener_ruta_csv_credenciales()
        if ruta_csv:
            df_credenciales = pd.read_csv(ruta_csv)
            credenciales = df_credenciales[df_credenciales['sistema'] == sistema].iloc[0]
            aws_access_key = credenciales['usuario']
            aws_secret_key = credenciales['contrasena']

    return aws_access_key, aws_secret_key, aws_region


load_dotenv()

AWS_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
lambda_access_key = os.getenv("LAMBDA_AWS_ACCESS_KEY_ID")
lambda_secret_key = os.getenv("LAMBDA_AWS_SECRET_ACCESS_KEY")

BUCKET = 'ameq'

print(BUCKET)

STORAGE_OPTIONS = {
    "aws_access_key_id": AWS_ID,
    "aws_secret_access_key": AWS_SECRET,
    "aws_region": AWS_REGION,
}



def init_aws_clients(verbose: bool = False) -> dict:
    setup_logger(verbose)
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION")
    lambda_access_key = os.getenv("LAMBDA_AWS_ACCESS_KEY_ID")
    lambda_secret_key = os.getenv("LAMBDA_AWS_SECRET_ACCESS_KEY")

    lambda_config = Config(read_timeout=30000, connect_timeout=3600)
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=lambda_access_key,
        aws_secret_access_key=lambda_secret_key,
        region_name=aws_region,
        config=lambda_config
    )

    kinesis_client = boto3.client(
        'kinesis',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    kinesis_response_client = boto3.client(
        'kinesis',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    if verbose:
        logging.info("AWS clients initialized.")
    return {
        "lambda_client": lambda_client,
        "kinesis_client": kinesis_client,
        "kinesis_response_client": kinesis_response_client,
        "dynamodb": dynamodb,
    }
    
    
s3_client = boto3.client('s3', aws_access_key_id=AWS_ID, 
                         aws_secret_access_key=AWS_SECRET,
                         region_name =  AWS_REGION)

s3_fs = s3fs.S3FileSystem(key=AWS_ID,secret=AWS_SECRET)

# S3
def abrir_parquet_s3_pl(s3_file_path, bucket, storage_options=STORAGE_OPTIONS,
                        dataframe='polars', lazy=False, verbose=False):
    """
    Abre un archivo parquet directamente desde AWS S3 usando Polars.

    Parámetros:
        s3_file_path (str): Ruta al archivo parquet en S3.
        bucket (str): Nombre del bucket S3.
        storage_options (dict): Opciones para acceder al S3.
        dataframe (str): Tipo de DataFrame de retorno ('polars' o 'pandas').
        lazy (bool): Indica si el DataFrame es evaluado en forma lazy.

    Retorna:
        DataFrame (Polars o Pandas) o None si no existe el archivo.
    """
    setup_logger(verbose)
    try:
        if existe_archivo_en_s3(bucket, s3_file_path):
            logging.info(f"Archivo encontrado en s3://{bucket}/{s3_file_path}")
            df = pl.scan_parquet(f's3://{bucket}/{s3_file_path}',
                                 storage_options=storage_options)

            if dataframe == 'pandas':
                logging.info("Retornando DataFrame de Pandas.")
                return df.collect().to_pandas()
            else:
                if lazy:
                    logging.info("Retornando DataFrame de Polars en modo lazy.")
                    return df
                else:
                    logging.info("Retornando DataFrame de Polars en modo eager.")
                    return df.collect()
        else:
            logging.warning(f"Archivo no encontrado: s3://{bucket}/{s3_file_path}")
            return None
    except Exception as e:
        logging.error(f"Error al abrir parquet desde S3: {e}")
        return None
    
def obtener_gpdv2(path, data_temp='./04_data/temp/voa/', bucket=BUCKET, verbose=False):
    """
    Descarga un archivo parquet desde S3 y lo convierte en GeoDataFrame.

    Parámetros:
        path (str): Ruta del archivo en S3.
        data_temp (str): Ruta local temporal para descargar el archivo.
        bucket (str): Nombre del bucket en S3.

    Retorna:
        GeoDataFrame o None si el archivo no existe o hay un error.
    """
    setup_logger(verbose)
    path_gpd = os.path.join(data_temp, os.path.basename(path))

    try:
        if existe_archivo_en_s3(bucket, path):
            logging.info(f"Archivo encontrado en s3://{bucket}/{path}")

            if not os.path.exists(data_temp):
                os.makedirs(data_temp)
                logging.info(f"Directorio temporal creado: {data_temp}")

            if not os.path.exists(path_gpd):
                logging.info("Descargando archivo...")
                s3_client.download_file(bucket, path, path_gpd)

            logging.info("Cargando GeoDataFrame...")
            gdf = gpd.read_parquet(path_gpd)

            return gdf
        else:
            logging.warning(f"Archivo no encontrado: s3://{bucket}/{path}")
            return None

    except Exception as e:
        logging.error(f"Error al obtener GeoDataFrame desde S3: {e}")
        return None

    finally:
        if os.path.exists(path_gpd):
            os.remove(path_gpd)
            logging.info("Archivo temporal eliminado.")
    
    
    
    
    
    
def obtener_gpd(path, data_temp='./04_data/temp/voa/', bucket=BUCKET, verbose=False):
    """
    Descarga un archivo parquet desde S3, lo convierte en GeoDataFrame con 
    manejo de reintentos.

    Parámetros:
        path (str): Ruta del archivo en S3.
        data_temp (str): Ruta local temporal para descargar el archivo.
        bucket (str): Nombre del bucket en S3.

    Retorna:
        GeoDataFrame o None si el archivo no existe o no se puede leer.
    """
    setup_logger(verbose)
    path_gpd = os.path.join(data_temp, os.path.basename(path))

    if not existe_archivo_en_s3(bucket, path):
        logging.warning(f"Archivo no encontrado: s3://{bucket}/{path}")
        return None

    if not os.path.exists(data_temp):
        os.makedirs(data_temp)
        logging.info(f"Directorio temporal creado: {data_temp}")

    try:
        logging.info("Descargando archivo desde S3...")
        s3_client.download_file(bucket, path, path_gpd)

        intentos, max_intentos = 0, 5
        while intentos < max_intentos:
            try:
                logging.info(f"Intento {intentos + 1}: Leyendo archivo parquet.")
                gdf = gpd.read_parquet(path_gpd)
                logging.info("Archivo parquet leído exitosamente.")
                return gdf
            except PermissionError as e:
                logging.warning(f"Permiso denegado en intento {intentos + 1}: {e}. Reintentando en 5 segundos...")
                intentos += 1
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error inesperado en intento {intentos + 1}: {e}")
                return None

        logging.error("Se agotaron los intentos para leer el archivo.")
        return None

    except Exception as e:
        logging.error(f"Error al descargar o leer GeoDataFrame desde S3: {e}")
        return None

    finally:
        if os.path.exists(path_gpd):
            os.remove(path_gpd)
            logging.info("Archivo temporal eliminado.")


def obtener_json(path, bucket, data_temp='./04_data/', delete_temp_file=True, verbose=False):
    """
    Descarga un archivo JSON desde S3 y lo convierte en diccionario.

    Parámetros:
        path (str): Ruta del archivo en S3.
        bucket (str): Nombre del bucket.
        data_temp (str): Ruta temporal local.
        delete_temp_file (bool): Si es True, elimina el archivo tras cargarlo.

    Retorna:
        dict o None si ocurre un error o el archivo no existe.
    """
    setup_logger(verbose)
    path_json = os.path.join(data_temp, os.path.basename(path))

    if not existe_archivo_en_s3(bucket, path):
        logging.warning(f"Archivo JSON no encontrado: s3://{bucket}/{path}")
        return None

    if not os.path.exists(data_temp):
        os.makedirs(data_temp)
        logging.info(f"Directorio temporal creado: {data_temp}")

    try:
        logging.info("Descargando archivo JSON desde S3...")
        s3_client.download_file(bucket, path, path_json)
        with open(path_json, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error al obtener JSON desde S3: {e}")
        return None
    finally:
        if delete_temp_file and os.path.exists(path_json):
            os.remove(path_json)
            logging.info("Archivo temporal JSON eliminado.")


def obtener_lista_archivos(s3_path=None, bucket=BUCKET, verbose=False):
    """
    Obtiene una lista de archivos disponibles en un bucket de AWS S3.

    Parámetros:
        s3_path (str, opcional): Ruta específica para filtrar los archivos del bucket.
        bucket (str): Nombre del bucket en S3.

    Retorna:
        list: Lista con las claves (paths) de los archivos encontrados.
    """
    setup_logger(verbose)
    archivos = []
    continuation_token = None

    try:
        while True:
            if continuation_token:
                response = s3_client.list_objects_v2(Bucket=bucket, ContinuationToken=continuation_token)
            else:
                response = s3_client.list_objects_v2(Bucket=bucket)

            for obj in response.get('Contents', []):
                if s3_path is None or s3_path in obj['Key']:
                    archivos.append((obj['Key'], obj['LastModified']))

            if response.get('IsTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break

        logging.info(f"Se encontraron {len(archivos)} archivos.")
        return [archivo[0] for archivo in archivos]

    except Exception as e:
        logging.error(f"Error al obtener lista de archivos desde S3: {e}")
        return []


def obtener_ultima_fecha_disponible(s3_path, last=True, bucket=BUCKET, verbose=False):
    """
    Obtiene la última fecha disponible desde un path específico en AWS S3.

    Parámetros:
        s3_path (str): Ruta del archivo o carpeta en S3.
        last (bool): True para obtener la última fecha disponible, False para la primera.
        bucket (str): Nombre del bucket en S3.

    Retorna:
        str: Fecha disponible en formato 'YYYY/MM/DD' o None si ocurre un error.
    """
    setup_logger(verbose)
    try:
        archivos = obtener_lista_archivos(s3_path, bucket)
        if not archivos:
            logging.warning(f"No se encontraron archivos en el path: {s3_path}")
            return None

        idx = 0 if last else -1
        archivo_seleccionado = sorted(archivos, reverse=True)[idx]
        fecha_disponible = '/'.join(archivo_seleccionado.split('/')[-4:-1])

        logging.info(f"Fecha disponible obtenida: {fecha_disponible}")
        return fecha_disponible

    except Exception as e:
        logging.error(f"Error al obtener última fecha disponible: {e}")
        return None



def existe_archivo_en_s3(bucket_name, key, verbose=False):
    """
    Verifica si un archivo existe en un bucket de AWS S3.

    Parámetros:
        bucket_name (str): Nombre del bucket.
        key (str): Ruta del archivo en el bucket.

    Retorna:
        bool: True si el archivo existe, False si no.
    """
    setup_logger(verbose)
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        logging.info(f"Archivo encontrado: s3://{bucket_name}/{key}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.warning(f"Archivo no encontrado: s3://{bucket_name}/{key}")
            return False
        else:
            logging.error(f"Error al verificar archivo en S3: {e}")
            raise
## FUNCIONES DEL REPOSITORIO DE RGV
# correr query y descargar data
def run_query(path_query, database, athena_client, s3_staging_dir, aws_bucket, s3_client, verbose=False):
    """
    Ejecuta una consulta en AWS Athena y descarga el resultado desde S3.

    Parámetros:
        path_query (str): Ruta al archivo que contiene la consulta SQL.
        database (str): Nombre de la base de datos en Athena.
        athena_client (obj): Cliente AWS Athena.
        s3_staging_dir (str): Directorio de almacenamiento temporal de resultados en S3.
        aws_bucket (str): Nombre del bucket en S3.
        s3_client (obj): Cliente AWS S3.

    Retorna:
        str: Ruta al archivo descargado localmente con los resultados.
    """
    setup_logger(verbose)
    try:
        with open(path_query, 'r') as file:
            sql_query = file.read()

        query_response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": s3_staging_dir,
                "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
            },
        )

        query_execution_id = query_response['QueryExecutionId']
        file_name = query_execution_id + '.csv'

        logging.info(f"Consulta iniciada, ID de ejecución: {query_execution_id}")

        intentos, max_intentos = 0, 20
        while intentos < max_intentos:
            try:
                s3_client.download_file(aws_bucket, file_name, 'athena_query_results.csv')
                logging.info("Resultados de la consulta descargados exitosamente.")
                return 'athena_query_results.csv'
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    logging.info(f"Intento {intentos + 1}: Resultados aún no disponibles, reintentando en 15 segundos...")
                    intentos += 1
                    time.sleep(15)
                else:
                    logging.error(f"Error inesperado al descargar archivo: {e}")
                    raise

        logging.error("Tiempo de espera agotado, resultados no disponibles.")
        return None

    except Exception as e:
        logging.error(f"Error al ejecutar consulta en Athena: {e}")
        return None


def run_query_text(sql_query, database, athena_client, s3_staging_dir, aws_bucket, s3_client, verbose=False):
    """
    Ejecuta una consulta SQL proporcionada como texto en AWS Athena y descarga los resultados desde S3.

    Parámetros:
        sql_query (str): Consulta SQL a ejecutar.
        database (str): Nombre de la base de datos en Athena.
        athena_client (obj): Cliente AWS Athena.
        s3_staging_dir (str): Directorio de almacenamiento temporal de resultados en S3.
        aws_bucket (str): Nombre del bucket en S3.
        s3_client (obj): Cliente AWS S3.

    Retorna:
        str: Ruta al archivo descargado localmente con los resultados, o None en caso de error.
    """
    setup_logger(verbose)
    try:
        query_response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": s3_staging_dir,
                "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
            },
        )

        query_execution_id = query_response['QueryExecutionId']
        file_name = query_execution_id + '.csv'

        logging.info(f"Consulta iniciada, ID de ejecución: {query_execution_id}")

        intentos, max_intentos = 0, 20
        while intentos < max_intentos:
            try:
                s3_client.download_file(aws_bucket, file_name, 'athena_query_results.csv')
                logging.info("Resultados de la consulta descargados exitosamente.")
                return 'athena_query_results.csv'
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    logging.info(f"Intento {intentos + 1}: Resultados aún no disponibles, reintentando en 15 segundos...")
                    intentos += 1
                    time.sleep(15)
                else:
                    logging.error(f"Error inesperado al descargar archivo: {e}")
                    raise

        logging.error("Tiempo de espera agotado, resultados no disponibles.")
        return None

    except Exception as e:
        logging.error(f"Error al ejecutar consulta en Athena: {e}")
        return None

# crear tabla en AWS athena

def create_table(path_query, database, athena_client, s3_staging_dir, verbose=False):
    """
    Crea una tabla en AWS Athena a partir de una consulta SQL en un archivo.

    Parámetros:
        path_query (str): Ruta al archivo que contiene la consulta SQL para crear la tabla.
        database (str): Nombre de la base de datos en Athena.
        athena_client (obj): Cliente AWS Athena.
        s3_staging_dir (str): Directorio de almacenamiento temporal de resultados en S3.

    Retorna:
        dict: Respuesta de AWS Athena sobre la ejecución de la consulta, o None si ocurre un error.
    """
    setup_logger(verbose)
    try:
        with open(path_query, 'r') as file:
            sql_query = file.read()

        query_response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": s3_staging_dir,
                "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
            },
        )

        query_execution_id = query_response['QueryExecutionId']
        logging.info(f"Creación de tabla iniciada, ID de ejecución: {query_execution_id}")
        return query_response

    except Exception as e:
        logging.error(f"Error al crear tabla en Athena: {e}")
        return None


# crear tabla en AWS athena con variables
def create_table_var(sql_query, database, athena_client, s3_staging_dir, verbose=False):
    """
    Crea una tabla en AWS Athena a partir de una consulta SQL proporcionada como texto.

    Parámetros:
        sql_query (str): Consulta SQL para crear la tabla.
        database (str): Nombre de la base de datos en Athena.
        athena_client (obj): Cliente AWS Athena.
        s3_staging_dir (str): Directorio de almacenamiento temporal de resultados en S3.

    Retorna:
        dict: Respuesta de AWS Athena sobre la ejecución de la consulta, o None si ocurre un error.
    """
    setup_logger(verbose)
    try:
        query_response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": s3_staging_dir,
                "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
            },
        )

        query_execution_id = query_response['QueryExecutionId']
        logging.info(f"Creación de tabla iniciada, ID de ejecución: {query_execution_id}")
        return query_response

    except Exception as e:
        logging.error(f"Error al crear tabla en Athena: {e}")
        return None

# borrar tabla aws
def delete_table(table_name, database, athena_client, s3_staging_dir, verbose=False):
    """
    Elimina una tabla en AWS Athena si existe.

    Parámetros:
        table_name (str): Nombre de la tabla que se desea eliminar.
        database (str): Nombre de la base de datos en Athena.
        athena_client (obj): Cliente AWS Athena.
        s3_staging_dir (str): Directorio de almacenamiento temporal de resultados en S3.

    Retorna:
        dict: Respuesta de AWS Athena sobre la ejecución de la consulta, o None si ocurre un error.
    """
    setup_logger(verbose)
    try:
        sql_query = f"DROP TABLE IF EXISTS {table_name}"
        query_response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": s3_staging_dir,
                "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
            },
        )

        query_execution_id = query_response['QueryExecutionId']
        logging.info(f"Eliminación de tabla iniciada, ID de ejecución: {query_execution_id}")
        return query_response

    except Exception as e:
        logging.error(f"Error al eliminar tabla en Athena: {e}")
        return None


# generar las rutas para hacer el upload de particionadas en s3
def create_params_upload_from_path(path, partition_key='fecha', verbose=False):
    """
    Genera los parámetros necesarios para subir archivos a S3, soportando particionamiento.

    Parámetros:
        path (str): Ruta del archivo a subir a S3. Si está particionado,
                    debe incluir la clave de partición, p.ej.:
                    'catalogs/particionadas/match/fecha/match.parquet'.
        partition_key (str, opcional): Clave utilizada para particionar el archivo.
                                       Si no está particionado, usar None.
                                       Por defecto es 'fecha'.

    Retorna:
        tuple: (nombre del archivo, base, ruta aws) o ('', base, ruta aws)
    """
    setup_logger(verbose)
    try:
        file_name = os.path.basename(path)
        if partition_key:
            base = path.split(f'/{partition_key}')[0].split('/')[-1]
        else:
            base = '/'.join(path.split('/')[1:-1])

        aws_path = path.split(f'/{base}')[0] + '/'

        if '.' in file_name:
            logging.info(f"Parámetros generados para archivo: {file_name}")
            return file_name, base, aws_path
        else:
            base_ = file_name
            aws_path_ = aws_path + base + '/'
            logging.info(f"Parámetros generados para base sin archivo: {base_}")
            return '', base_, aws_path_

    except Exception as e:
        logging.error(f"Error al generar parámetros desde path: {e}")
        return None, None, None

def athena(aws_access_key, aws_secret_key, aws_region, verbose=False):
    """
    Inicializa un cliente de AWS Athena.

    Parámetros:
        aws_access_key (str): Clave de acceso de AWS.
        aws_secret_key (str): Clave secreta de AWS.
        aws_region (str): Región de AWS.

    Retorna:
        boto3.client: Cliente de AWS Athena.
    """
    setup_logger(verbose)
    try:
        cliente_athena = boto3.client(
            'athena',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        logging.info("Cliente AWS Athena inicializado correctamente.")
        return cliente_athena
    except Exception as e:
        logging.error(f"Error al inicializar cliente AWS Athena: {e}")
        return None


def s3(aws_access_key, aws_secret_key, aws_region, verbose=False):
    """
    Inicializa un cliente de AWS S3.

    Parámetros:
        aws_access_key (str): Clave de acceso de AWS.
        aws_secret_key (str): Clave secreta de AWS.
        aws_region (str): Región de AWS.

    Retorna:
        boto3.client: Cliente de AWS S3.
    """
    try:
        cliente_s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        logging.info("Cliente AWS S3 inicializado correctamente.")
        return cliente_s3
    except Exception as e:
        logging.error(f"Error al inicializar cliente AWS S3: {e}")
        return None


def get_aws_keys(aws_key_path, empresa, verbose=False):
    """
    Lee y filtra las credenciales de AWS desde un archivo CSV.

    Parámetros:
        aws_key_path (str): Ruta al archivo CSV con credenciales.
        empresa (str): Nombre del sistema o empresa para filtrar credenciales.

    Retorna:
        DataFrame: Credenciales filtradas o None si ocurre un error.
    """
    setup_logger(verbose)
    try:
        aws_keys = pd.read_csv(aws_key_path)
        aws_keys = aws_keys[aws_keys['aws'] == empresa].reset_index(drop=True)
        logging.info("Credenciales de AWS cargadas correctamente.")
        return aws_keys
    except Exception as e:
        logging.error(f"Error al cargar credenciales de AWS: {e}")
        return None

def upload_latest(s3_client, write_path, bucket, file_name, base, base_latest, 
                  partition, aws_path_partition, aws_path_non_partition, verbose=False):
    """Funcion para actualizar un archivo lateste, pero manteniendo un
    historico de las versiones

    path del particionado:
        <aws_path_partition>/<base>/<partition>/<file_name>
    path del no particionado:
        <aws_path_non_partition>/<base_latest>/<file_name>

    Args:
        s3_client (s3_client)
        write_path (str): path donde esta el archivo que se quiere subir
        bucket (str): nombre del bucket
        file_name (str): nombre del archivo que se quiere subir
        base (str): nombre de la base en la que se quiere subir
        base_latest (str): nombre de la base de latest, p.ej., latest
        partition (str): fecha de la particion en formato YYYY/MM/DD
        aws_path_partition (str): ruta de la particion de s3 en la que se
            quiere subir el archivo
        aws_path_non_partition (str): ruta de la no particion de s3 en la que se
            quiere subir el archivo
    """
    setup_logger(verbose)
    # subir el archivo particionado
    upload_partition(s3_client, write_path, bucket, 
                     file_name,
                     base,
                     partition,
                     aws_path_partition)
    # subir el archivo latest
    upload_non_partition(s3_client, write_path, bucket, 
                     file_name,
                     base_latest,
                     aws_path_non_partition)


def mysql_query_text(host, user, password, database, sql, port=3306, df_type='polars', verbose=False):
    """
    Ejecuta una consulta SQL en una base de datos MySQL/Aurora y devuelve los resultados en un DataFrame.

    Parámetros:
        host (str): Endpoint de la instancia MySQL/Aurora.
        user (str): Usuario para la conexión.
        password (str): Contraseña del usuario.
        database (str): Nombre de la base de datos a conectar.
        sql (str): Consulta SQL a ejecutar.
        port (int, opcional): Puerto para la conexión. Por defecto es 3306.
        df_type (str, opcional): Tipo de DataFrame ('polars' o 'pandas'). Por defecto es 'polars'.
        verbose (bool, opcional): Si es True, muestra logs adicionales. Por defecto es False.

    Retorna:
        DataFrame: Resultados de la consulta en formato Polars o Pandas, o None en caso de error.
    """
    setup_logger(verbose)
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        if verbose:
            logging.info("Conexión a la instancia MySQL/Aurora exitosa.")

        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        if df_type == 'pandas':
            df = pd.DataFrame(rows)
        else:
            df = pl.DataFrame(rows)

        if verbose:
            logging.info("Consulta ejecutada y resultados obtenidos correctamente.")

        return df

    except pymysql.MySQLError as e:
        logging.error(f"Error al ejecutar consulta en MySQL/Aurora: {e}")
        return None
    
    
def verify_parquet_file(s3_file_path, bucket, status=True, size=True, last_modified=True,
                        s3_client=s3_client, s3_fs=s3_fs, logger=None, verbose=False):
    """
    Verifica la existencia, tamaño, integridad y última modificación de un archivo en S3.

    Parámetros:
        s3_file_path (str): Ruta del archivo en S3 ('ruta/a/archivo.parquet').
        bucket (str): Nombre del bucket en S3.
        status (bool): Verificar existencia e integridad del archivo.
        size (bool): Devolver tamaño del archivo.
        last_modified (bool): Devolver última fecha de modificación.
        s3_client (obj): Cliente de AWS S3.
        s3_fs (obj): Sistema de archivos para acceso a S3.
        logger (obj): Sistema de logging externo, opcional.
        verbose (bool): Muestra logs adicionales si es True.

    Retorna:
        dict: Diccionario con existencia, tamaño, integridad, última modificación y errores.
    """
    setup_logger(verbose)
    resultado = {'exists': False, 'size': None, 'integrity_check': False,
                 'last_modified': None, 'error': {}}

    try:
        response = s3_client.head_object(Bucket=bucket, Key=s3_file_path)
        resultado['exists'] = True
        file_size_bytes = response['ContentLength']

        if size:
            for unit in ['bytes', 'KB', 'MB', 'GB']:
                if file_size_bytes < 1024.0:
                    resultado['size'] = f"{file_size_bytes:.2f} {unit}"
                    break
                file_size_bytes /= 1024.0

        if verbose:
            mensaje = f"Archivo existe. Tamaño: {resultado['size']}"
            logger.info(mensaje) if logger else logging.info(mensaje)

        if last_modified:
            resultado['last_modified'] = response['LastModified'].strftime("%Y-%m-%d %H:%M:%S %Z")

    except ClientError as e:
        mensaje_error = f"Archivo no encontrado o inaccesible: {e}"
        resultado['error']['exists'] = mensaje_error
        if verbose:
            logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return resultado

    if status:
        try:
            ext = s3_file_path.split('.')[-1].lower()

            with s3_fs.open(f's3://{bucket}/{s3_file_path}') as file:
                if ext == 'parquet':
                    pq.read_table(file)
                elif ext == 'log':
                    file.read()
                elif ext == 'json':
                    json.load(file)
                elif ext == 'xlsm':
                    workbook = openpyxl.load_workbook(file, read_only=True)
                    workbook.close()
                elif ext == 'csv':
                    csv_reader = csv.reader(file)
                    next(csv_reader, None)
                else:
                    raise ValueError(f"Extensión no soportada: {ext}")

            resultado['integrity_check'] = True
            if verbose:
                mensaje = "Chequeo de integridad exitoso. Archivo legible."
                logger.info(mensaje) if logger else logging.info(mensaje)

        except Exception as e:
            mensaje_error = f"Chequeo de integridad fallido, archivo posiblemente corrupto: {e}"
            resultado['error']['integrity'] = mensaje_error
            if verbose:
                logger.error(mensaje_error) if logger else logging.error(mensaje_error)

    return resultado


def upload_partition(s3_client, write_path, bucket, file_name, base, partition,
                     aws_path, secure_upload=True, logger=None, verbose=False):
    """
    Sube un archivo particionado a AWS S3 con chequeo opcional de integridad.

    Parámetros:
        s3_client (obj): Cliente AWS S3.
        write_path (str): Ruta local del archivo a subir.
        bucket (str): Nombre del bucket.
        file_name (str): Nombre del archivo.
        base (str): Nombre base del archivo.
        partition (str): Fecha de partición en formato YYYY/MM/DD.
        aws_path (str): Ruta en S3 para almacenar el archivo particionado.
        secure_upload (bool): Realizar chequeo de integridad tras subida.
        logger (obj, opcional): Logger externo.
        verbose (bool): Muestra logs adicionales si es True.

    Retorna:
        dict: Resultado del chequeo de integridad o None si no es seguro.
    """
    setup_logger(verbose)
    intento, max_intentos = 0, 5
    s3_file_path = f"{aws_path}{base}/{partition}/{file_name}"

    try:
        if secure_upload:
            resultado = {'integrity_check': False}

            while not resultado['integrity_check'] and intento < max_intentos:
                s3_client.upload_file(
                    Filename=os.path.join(write_path, file_name),
                    Bucket=bucket,
                    Key=s3_file_path
                )
                resultado = verify_parquet_file(s3_file_path, bucket)
                intento += 1

                if verbose:
                    mensaje = f"Intento {intento}: Resultado del chequeo - {resultado['integrity_check']}"
                    logger.info(mensaje) if logger else logging.info(mensaje)

            if not resultado['integrity_check']:
                mensaje_error = "Máximo número de intentos alcanzado, archivo podría estar corrupto."
                logger.error(mensaje_error) if logger else logging.error(mensaje_error)
            else:
                mensaje_exito = "Archivo subido exitosamente con integridad verificada."
                logger.info(mensaje_exito) if logger else logging.info(mensaje_exito)

            return resultado

        else:
            s3_client.upload_file(
                Filename=os.path.join(write_path, file_name),
                Bucket=bucket,
                Key=s3_file_path
            )
            mensaje_simple = "Archivo subido exitosamente sin chequeo de integridad."
            logger.info(mensaje_simple) if logger else logging.info(mensaje_simple)

    except Exception as e:
        mensaje_error = f"Error al subir archivo a S3: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return None


def upload_non_partition(s3_client, write_path, bucket, file_name, base, aws_path,
                         secure_upload=True, logger=None, verbose=False):
    """
    Sube un archivo no particionado a AWS S3 con chequeo opcional de integridad.

    Parámetros:
        s3_client (obj): Cliente AWS S3.
        write_path (str): Ruta local del archivo a subir.
        bucket (str): Nombre del bucket.
        file_name (str): Nombre del archivo.
        base (str): Nombre base del archivo.
        aws_path (str): Ruta en S3 para almacenar el archivo.
        secure_upload (bool): Realizar chequeo de integridad tras subida.
        logger (obj, opcional): Logger externo.
        verbose (bool): Muestra logs adicionales si es True.

    Retorna:
        dict: Resultado del chequeo de integridad o None si no es seguro.
    """
    setup_logger(verbose)
    intento, max_intentos = 0, 5
    s3_file_path = f"{aws_path}{base}/{file_name}"

    try:
        if secure_upload:
            resultado = {'integrity_check': False}

            while not resultado['integrity_check'] and intento < max_intentos:
                s3_client.upload_file(
                    Filename=os.path.join(write_path, file_name),
                    Bucket=bucket,
                    Key=s3_file_path
                )
                resultado = verify_parquet_file(s3_file_path, bucket)
                intento += 1

                if verbose:
                    mensaje = f"Intento {intento}: Resultado del chequeo - {resultado['integrity_check']}"
                    logger.info(mensaje) if logger else logging.info(mensaje)

            if not resultado['integrity_check']:
                mensaje_error = "Máximo número de intentos alcanzado, archivo podría estar corrupto."
                logger.error(mensaje_error) if logger else logging.error(mensaje_error)
            else:
                mensaje_exito = "Archivo subido exitosamente con integridad verificada."
                logger.info(mensaje_exito) if logger else logging.info(mensaje_exito)

            return resultado

        else:
            s3_client.upload_file(
                Filename=os.path.join(write_path, file_name),
                Bucket=bucket,
                Key=s3_file_path
            )
            mensaje_simple = "Archivo subido exitosamente sin chequeo de integridad."
            logger.info(mensaje_simple) if logger else logging.info(mensaje_simple)

    except Exception as e:
        mensaje_error = f"Error al subir archivo a S3: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return None






def format_size(size_in_bytes):
    """
    Convierte bytes a un formato legible por humanos.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"


def get_s3_environment_structure(logger=None, verbose=False):
    """
    Obtiene el tamaño y metadata de todos los buckets en S3 organizados en un diccionario anidado.

    Parámetros:
        logger (logging.Logger, opcional): Logger externo para registrar eventos.
        verbose (bool): Activa mensajes detallados de ejecución.

    Retorna:
        dict: Diccionario anidado con estructura de buckets, carpetas, archivos y metadatos.
    """
    setup_logger(verbose)
    s3_client = boto3.client('s3')
    try:
        buckets = s3_client.list_buckets()['Buckets']
        estructura_s3 = {}

        for bucket in buckets:
            bucket_name = bucket['Name']
            estructura_s3[bucket_name] = {'metadata': {'size': 0}, 'contenido': {}}

            paginator = s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name):
                for obj in page.get('Contents', []):
                    ruta = obj['Key'].split('/')
                    tamaño = obj['Size']

                    estructura_s3[bucket_name]['metadata']['size'] += tamaño
                    nivel_actual = estructura_s3[bucket_name]['contenido']

                    for parte in ruta[:-1]:
                        nivel_actual = nivel_actual.setdefault(
                            parte, {'metadata': {'size': 0}, 'contenido': {}}
                        )
                        nivel_actual['metadata']['size'] += tamaño
                        nivel_actual = nivel_actual['contenido']

                    nivel_actual[ruta[-1]] = {'metadata': {'size': tamaño}}

            if verbose:
                mensaje = f"Bucket '{bucket_name}' procesado con tamaño {format_size(estructura_s3[bucket_name]['metadata']['size'])}."
                logger.info(mensaje) if logger else logging.info(mensaje)

        return estructura_s3

    except ClientError as e:
        mensaje_error = f"Error de cliente AWS S3: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return None
    except Exception as e:
        mensaje_error = f"Error inesperado al procesar S3: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return None


def descargar_objeto_s3(s3_file_path, bucket, download_path='./04_data/',
                        open_file=True, delete_temp_file=True, logger=None, verbose=False):
    """
    Descarga un archivo de AWS S3 y opcionalmente lo abre según su tipo.

    Parámetros:
        s3_file_path (str): Ruta del archivo en S3.
        bucket (str): Nombre del bucket de S3.
        download_path (str): Ruta local para guardar el archivo.
        open_file (bool): Si es True, abre el archivo según extensión.
        delete_temp_file (bool): Si es True, elimina archivo después de usarlo.
        logger (logging.Logger, opcional): Logger externo.
        verbose (bool): Muestra logs adicionales si es True.

    Retorna:
        str | contenido: Mensaje de éxito o contenido del archivo.
    """
    setup_logger(verbose)
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        s3_client = boto3.client('s3')
        path_file = os.path.join(download_path, os.path.basename(s3_file_path))

        s3_client.download_file(Bucket=bucket, Key=s3_file_path, Filename=path_file)

        if verbose:
            mensaje = f"Archivo '{s3_file_path}' descargado exitosamente."
            logger.info(mensaje) if logger else logging.info(mensaje)

        if open_file:
            file_extension = os.path.splitext(path_file)[1].lower()

            with open(path_file, 'r', encoding='utf-8') as f:
                if file_extension == '.json':
                    data = json.load(f)
                elif file_extension in ['.log', '.csv', '.txt']:
                    data = f.read()
                else:
                    data = f"Tipo de archivo '{file_extension}' no soportado para apertura automática. Archivo descargado en: {download_path}"

            if delete_temp_file:
                os.remove(path_file)
                if verbose:
                    mensaje = f"Archivo temporal '{path_file}' eliminado."
                    logger.info(mensaje) if logger else logging.info(mensaje)

            return data

        return f"Archivo guardado correctamente en: {path_file}"

    except ClientError as e:
        mensaje_error = f"Error de AWS al descargar archivo: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return mensaje_error

    except Exception as e:
        mensaje_error = f"Error inesperado: {e}"
        logger.error(mensaje_error) if logger else logging.error(mensaje_error)
        return mensaje_error

    

def write_to_dynamodb(df_with_schema, table_name: str, verbose: bool = True):
    """
    Inicializa los registros de un data frame de polars a una tabla DynamoDB.
    
    Parameters:
        df_with_schema: Polars DataFrame con la información.
        table_name (str): Nombre de la tabla de DynamoDB.
        verbose (bool): Si es True imprime la información.
        
    Raises:
        Exception: Cualquier error durante la ejecución
    """
    setup_logger(verbose)
    try:
        aws_clients = init_aws_clients(verbose)
        dynamodb = aws_clients["dynamodb"]
        table = dynamodb.Table(table_name)
        
        if verbose:
            print(f"Writing data to DynamoDB table: {table_name}")
        
        def row_to_dynamodb_item(row: dict) -> dict:
            """
            Convierte los valores en un schema que Dynamo acepte.
            """
            for key, value in row.items():
                if isinstance(value, float):
                    row[key] = Decimal(str(value))
                elif isinstance(value, (list, dict)):
                    json_str = json.dumps(value)
                    row[key] = json.loads(json_str, parse_float=lambda x: Decimal(str(x)))
            return row

        # Write items to DynamoDB using the batch_writer for efficiency
        with table.batch_writer() as batch:
            for row in df_with_schema.iter_rows(named=True):
                item = row_to_dynamodb_item(row)
                batch.put_item(Item=item)
                
        if verbose:
            print("Data successfully written to DynamoDB.")
    
    except Exception as e:
        if verbose:
            print("Error writing to DynamoDB:", e)
        raise e       


