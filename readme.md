# Procesador de Video: Extracción de Texto desde un Video

Este es un programa en Python que permite extraer el texto de un archivo de video utilizando reconocimiento de voz. El programa utiliza una interfaz gráfica de usuario (GUI) para facilitar su uso y permite al usuario seleccionar un archivo de video, procesarlo y generar un archivo de texto con los subtítulos extraídos.

## Características

- **Extracción de audio**: Extrae el audio de un archivo de video.
- **Reconocimiento de voz**: Utiliza la API de Google Speech Recognition para convertir el audio en texto.
- **Interfaz gráfica**: Proporciona una interfaz gráfica fácil de usar con botones para agregar un video y detener el proceso.
- **Barra de progreso**: Muestra el progreso del procesamiento y el tiempo restante estimado.
- **Guardado de subtítulos**: Guarda los subtítulos extraídos en un archivo de texto y lo abre automáticamente en el bloc de notas.

## Requisitos

Para ejecutar este programa, necesitas tener instalado Python 3.x y las siguientes bibliotecas:

- `moviepy`
- `speechrecognition`
- `tkinter`

Puedes instalar las bibliotecas necesarias utilizando `pip`:

```bash
pip install moviepy speechrecognition
```
