import moviepy.editor as mp
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import os

# Variable de control para detener el procesamiento
proceso_detenido = False

def procesar_video():
    global proceso_detenido
    agregar_video_button.config(state="disabled")  # Deshabilita el botón "Agregar Video"
    stop_button.config(state="active")  # Habilita el botón "Stop"
    
    def procesar():
        global proceso_detenido  # Usa la variable global en la función anidada
            
        # Establece la ubicación para los archivos temporales
        temp_audio_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_audio_dir, exist_ok=True)
        temp_audio_path = os.path.join(temp_audio_dir, "temp_audio.wav")
        output_file = os.path.join(temp_audio_dir, 'subtitulos.txt')

        video_file = filedialog.askopenfilename(title="Seleccionar archivo de video")
        if video_file:
            # Cargar el video
            video = mp.VideoFileClip(video_file)

            # Extraer el audio del video
            audio = video.audio

            # Inicializar el reconocedor de voz
            recognizer = sr.Recognizer()

            # Calcular la duración del audio
            audio_duration = int(audio.duration)
            step = 10  # Procesar en bloques de 10 segundos
            processed_time = 0

            with open(output_file, 'w', encoding='utf-8') as f:
                for i in range(0, audio_duration, step):
                    end_time = min(i + step, audio_duration)
                    audio_chunk = audio.subclip(i, end_time)
                    audio_chunk.write_audiofile(temp_audio_path, codec='pcm_s16le')
                    try:
                        with sr.AudioFile(temp_audio_path) as source:
                            audio_data = recognizer.record(source)
                        texto = recognizer.recognize_google(audio_data, language='es-ES')
                        print(f'Segundos {i}-{end_time}: {texto}')
                        f.write(f'Segundos {i}-{end_time}:\n{texto}\n\n')
                    except sr.UnknownValueError:
                        print(f'Segundos {i}-{end_time}: No se pudo reconocer el audio')
                    except sr.RequestError as e:
                        print(f'Segundos {i}-{end_time}: Error en la solicitud al servicio de reconocimiento de voz: {e}')

                    # Actualizar la barra de progreso y el tiempo restante estimado
                    processed_time += step
                    progress_var.set((processed_time / audio_duration) * 100)
                    tiempo_restante = (audio_duration - processed_time) * (1.0 / step)
                    estimado_var.set(f'Tiempo restante: {tiempo_restante:.1f} segundos')
                    
                    if proceso_detenido:
                        limpiar_interfaz()
                        print("Proceso detenido por el usuario")
                        break

            # Habilitar el botón "Agregar Video" después de finalizar el procesamiento
            agregar_video_button.config(state="active")
            stop_button.config(state="disabled")
            proceso_detenido = False

            # abrir el notepad con el archivo de texto
            descargar_subtitulos()

            print(f'Los subtítulos se han guardado en {output_file}')

    processing_thread = threading.Thread(target=procesar)
    processing_thread.start()

def descargar_subtitulos():
    # Abre el archivo de subtítulos en el visor de texto predeterminado
    import os
    os.system("notepad.exe temp/subtitulos.txt")

def limpiar_interfaz():
    progress_var.set(0.0)  # Reinicia la barra de progreso
    estimado_var.set("")  # Limpia el texto del tiempo restante estimado
    estimado_label.config(text="")  # Limpia el Label
    agregar_video_button.config(state="active")  # Habilita el botón "Agregar Video"
    stop_button.config(state="disabled")  # Deshabilita el botón "Stop"

def stop_proceso():
    global proceso_detenido
    proceso_detenido = True  # Establece la variable de control en True para detener el proceso
    

# Crear la ventana de la aplicación
app = tk.Tk()

app.iconbitmap("logo.ico") # Establece el icono
app.geometry("400x400")  # Ajustar el tamaño de la ventana
app.title("Procesador de Video")

titulo = tk.Label(app,font='sans 14 bold',text="\n EXTRAER TEXTO DE UN VIDEO")
titulo.pack(pady=10) 
etiqueta = tk.Label(app,font='sans 9',text="Agregue el archivo y aguarde a que se abra un archivo txt \n\n  (Puede detener el proceso presionando STOP) ")
etiqueta.pack(pady=10) 

# Crear un marco para centrar los botones y la ProgressBar
frame = tk.Frame(app)
frame.pack(expand=True)

# Crear un marco para los botones
button_frame = tk.Frame(frame)
button_frame.pack()

# Agregar botones con margen
agregar_video_button = tk.Button(button_frame, text="  Agregar Video  ", overrelief="flat", font='sans 14 bold',activeforeground="#bc69bb",fg="#bc69bb", command=procesar_video)
agregar_video_button.grid(row=0, column=0, pady=13, padx=(10, 0))  # Agregar margen en el eje Y y espaciado en el eje X

# Agregar un botón para detener el proceso
stop_button = tk.Button(button_frame, text=" Stop ", font='sans 14 bold', compound='center', overrelief="flat",activeforeground="red",foreground="red",  command=stop_proceso, state="disabled")
stop_button.grid(row=0, column=1, pady=13, padx=(0, 10))  # Agregar margen en el eje Y y espaciado en el eje X

# Agregar una ProgressBar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, length=300)
progress_bar.pack(pady=10)  # Agregar margen en el eje Y

# Etiqueta para mostrar el tiempo restante estimado
estimado_var = tk.StringVar()
estimado_label = tk.Label(frame, textvariable=estimado_var)
estimado_label.pack(pady=5)

# Iniciar la aplicación
app.mainloop()
