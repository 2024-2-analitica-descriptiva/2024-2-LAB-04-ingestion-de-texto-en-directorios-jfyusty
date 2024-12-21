# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# Importa las bibliotecas necesarias.
import os # Para interactuar con el sistema de archivos.
import zipfile # Para trabajar con archivos ZIP (abrir, extraer, etc.).
import pandas as pd


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """

    """
    Función para extraer archivos de un ZIP, crear conjuntos de datos a partir de archivos
    de texto organizados por sentimientos y guardar los datos como archivos CSV.

    Dependencias:
        - os
        - zipfile
        - pandas
    """

    # Define las rutas principales para trabajar con el ZIP y los directorios de salida.
    zip_file_path = 'files/input.zip' # Ruta del archivo ZIP.
    output_directory = 'files' # Carpeta base para la extracción y salida.
    extraction_subdirectory = os.path.join(output_directory, 'input') # Subdirectorio de extracción.
    output_dir = os.path.join(output_directory, 'output') # Subdirectorio para guardar los CSV.

    try:
        # Verifica si la carpeta de extracción ya existe
        if os.path.exists(extraction_subdirectory):
            print(f"La carpeta '{extraction_subdirectory}' ya existe. No se realizará ninguna operación.")
        else:
            # Crea el directorio base si no existe
            os.makedirs(output_directory, exist_ok=True)

            # Extrae el contenido del archivo ZIP
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(output_directory)

            print(f"Contenido extraído exitosamente en '{output_directory}'.")

        # Opcional: Muestra los archivos extraídos en el directorio base.
        print("Archivos en la carpeta de salida:")
        for file in os.listdir(output_directory):
            print(file)

        # Define una función para crear un DataFrame a partir de los archivos de texto.
        def create_dataset(directory):
            data = [] # Lista para almacenar las frases y sus etiquetas.
            for sentiment in ['negative', 'positive', 'neutral']: # Itera por los tipos de sentimiento.
                sentiment_path = os.path.join(directory, sentiment) # Ruta del subdirectorio del sentimiento.
                for filename in os.listdir(sentiment_path): # Itera por los archivos en ese subdirectorio.
                    file_path = os.path.join(sentiment_path, filename) # Ruta completa del archivo.
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read().strip() # Lee y limpia el contenido del archivo.
                    data.append({'phrase': text, 'target': sentiment})  # Agrega la frase y el sentimiento como fila.
            return pd.DataFrame(data) # Retorna un DataFrame con las frases y etiquetas.

        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Crea los conjuntos de datos para entrenamiento y prueba.
        train_data = create_dataset(os.path.join(extraction_subdirectory, 'train'))
        test_data = create_dataset(os.path.join(extraction_subdirectory, 'test'))

        # Guarda los conjuntos de datos en formato CSV.
        train_data.to_csv(os.path.join(output_dir, 'train_dataset.csv'), index=False)
        test_data.to_csv(os.path.join(output_dir, 'test_dataset.csv'), index=False)

        print("Archivos CSV creados correctamente en la carpeta 'files/output/'.")

    # Manejo de errores comunes.
    except FileNotFoundError:
        print(f"El archivo ZIP '{zip_file_path}' no existe.") # Si el archivo ZIP no se encuentra.
    except zipfile.BadZipFile:
        print(f"El archivo '{zip_file_path}' no es un archivo ZIP válido.") # Si el archivo no es un ZIP válido.
    except Exception as e:
        print(f"Ocurrió un error: {e}") # Para manejar cualquier otro error inesperado.

# Llama a la función para ejecutar todo el proceso.
pregunta_01()