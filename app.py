import subprocess
import os
import sys
import time
import re
import signal
import os
import psutil

from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QApplication, QMessageBox, QProgressBar
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QTime, QUrl

from ui.master_ui import MainWindow
from controladores.conversor import convertir_segundos

##################################################################################
#Clases de la interfaz
##################################################################################

class MainWindows(MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = None
        self.stop_rendering = False
        self.iteracion = 0
        
        # Setear el boton de render
        self.render_in_progress = False
        self.render_button.clicked.connect(self.renderizar)
        self.button_stop.clicked.connect(self.stop_render)
        self.render_button.clicked.connect(self.renderizar)

        notify_path = './recursos/notify.mp3'
        self.media_player = QMediaPlayer()
        media_content = QMediaContent(QUrl.fromLocalFile(notify_path))
        self.media_player.setMedia(media_content)
  
    def renderizar(self):
        self.iteracion = 0
        self.render_parado = False
        # Si el render esta en progreso no se ejecuta el resto
        if self.render_in_progress:
            return
        
        # setear el nombre del write
        input_write = self.input_write.text()

        # setear el la ubicacion del archivo de nuke
        self.nuke_executable = self.nuke_dir.text()

        # Si se dejo el campo vacio la opcion por defecto se define:
        if self.nuke_executable == "":
            self.nuke_executable = r'C:\Program Files\Nuke14.0v4\Nuke14.0.exe'

        # Si la ubicacion del archivo de nuke no es real se lanza un mensaje de alerta  
        if not os.path.exists(self.nuke_executable):
            self.CustomMessageBox('Warning', 'Nuke.exe location not exists')
            return
        
        # Se agregan comillas dobles para evitar problemas
        self.nuke_version = self.nuke_executable
        self.nuke_executable = '"' + self.nuke_executable + '"'

        # Inicar la lista que contiene los archivos de nuke a renderizar
        self.comando = list()

        # Definir el codigo de python que se guardara en un archivo temporal
        execute = '''

import nuke

print('Iniciando execute.py')

########################################
# raiz del proyecto
root_node = nuke.root()

# Obtiene el primer y ultimo fotograma
first_frame = int(root_node['first_frame'].value())
last_frame = int(root_node['last_frame'].value())
frame_range = last_frame - first_frame

print('last frame:', frame_range)

# Obtener el nombre del script
shot_name = nuke.tcl('file rootname [file tail [value root.name]]')
print('shot name:', shot_name)

######################################
#Renderizar
node_name = "Write1"
if nuke.exists(node_name):
    write_node = nuke.toNode(node_name)
    render_path = nuke.filename(write_node)
    print('render_path is:', render_path)
    nuke.execute(write_node, continueOnError = True)
else:
    print(f"El nodo {node_name} no existe")

#################
quit()
        '''

        # Modificar el valor de la variable en execute.py
        if not input_write == "":
            execute = execute.replace('node_name = "Write1"', f'node_name = "{input_write}"')

        # Guardar el contenido modificado en un archivo temporal
        execute_temp = './temp/execute_temp.py'
        with open(execute_temp, 'w') as file:
            file.write(execute)

        #Crear una lista con los archivos a renderizar
        for index in range(self.lista.count()):
            item = self.lista.item(index)
            nombre_label = item.data(1)
            self.script = nombre_label.text()
            print('script name:', self.script)
            self.script = '"' + self.script + '"'
            linea = self.nuke_executable + ' -ti -V2 '+ self.script +' < ' + execute_temp
            self.comando.append(linea)

        #Se inicia la clase RenderThread para que la interfaz no se pare mientras se renderiza
        self.thread = RenderThread()
        
        #Se conectan las señales y lo que ejecutaran  
        self.thread.shot_porcentaje.connect(self.update_progress)
        self.thread.descripcion.connect(self.update_descripcion)
        self.thread.current_shot.connect(self.update_shot)
        self.thread.render_path.connect(self.update_render_path)
        self.thread.finished.connect(self.rendering_finished)
        self.thread.tiempo_restante.connect(self.update_rest_time)
        self.thread.not_node.connect(self.not_node)
        self.thread.consola.connect(self.update_console)
        self.thread.iteracion.connect(self.update_iteracion)
        
        #Se inicia el metodo que inicia el render
        self.thread.start_rendering(self.comando)

        #Se establece el status como render in progress
        self.render_button.setEnabled(False) 
        self.render_in_progress = True 
        self.status.setText("Starting")
        self.progressBar.setValue(0)

        #comienza a contar los miniutos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.start_time = QTime.currentTime()

    def stop_render(self):
        if self.thread:
            self.thread.stop_rendering = True 
            self.render_parado = True
            self.thread.stop(self.nuke_version)
            self.thread.wait() 
            self.thread = None 
            self.render_button.setEnabled(True)
            self.render_in_progress = False 
            self.tiempo_restante.setText('-')
            self.status.setText("Render stop")

    def not_node(self):
        self.CustomMessageBox('Warning', 'The node not exist')

    #Actualiza el nombre del archivo de nuke que se esta renderizando
    def update_shot(self, current_shot):
        self.status.setText(f'Rendering: {current_shot}')

    def update_console(self, consola):
        pass

    def update_iteracion(self, iteracion):
        self.iteracion = iteracion
        print('self iteracion funcion:', self.iteracion)

    #Actualiza la barra de progresso durante el render
    def update_progress(self, shot_porcentaje):
        shot_name, porcentaje = shot_porcentaje
        porcentaje = int(porcentaje)
        print('shot:', shot_name)
        numero_renders = self.lista.count()
        porcentaje_por_render = 100/numero_renders
        iniciar_en = self.iteracion*porcentaje_por_render
        porcentaje_total = (porcentaje/numero_renders) + iniciar_en
        print('total progress:', porcentaje_total)
        self.progressBar.setValue(porcentaje_total)

        for index in range(self.lista.count()):
            item = self.lista.item(index)
            elemento_widget = self.lista.itemWidget(item)
            nombre_label = item.data(1)
            nombre_label = nombre_label.text()
            nombre_label = os.path.splitext(os.path.basename(nombre_label))[0]
            print('label_name:', nombre_label)

            if nombre_label == shot_name:
                progress_bar = elemento_widget.findChild(QProgressBar)
                progress_bar.setValue(porcentaje)

    #Actualiza la descripcion de lo que se esta renderizando
    def update_descripcion(self, descripcion):
        self.descripcion.setText(descripcion)
    
    #Actualiza el tiempo restante de render
    def update_rest_time(self, tiempo_restante):
        tiempo_restante = round(abs(tiempo_restante), 1)
        tiempo_restante = int(tiempo_restante)
        tiempo_restante = convertir_segundos(tiempo_restante)
        self.tiempo_restante.setText(f'Render ETA: {tiempo_restante}')

    # Abre el folder donde se aloja el render
    def update_render_path(self, render_path):
        if self.goto_folder.isChecked():
            render_path = str(render_path)
            render_path = os.path.dirname(render_path)
            render_path = os.path.normpath(render_path)
            print('render_path:', render_path)
            if render_path:
                if os.path.exists(render_path):
                    if os.path.isdir(render_path):
                        if sys.platform.startswith("darwin"):  # macOS
                            os.system("open '{}'".format(render_path))
                        elif sys.platform.startswith("win32"):  # Windows
                            os.startfile(render_path)
                        elif sys.platform.startswith("linux"):  # Linux
                            os.system("xdg-open '{}'".format(render_path))
                    else:
                        print("The path is not a folder.")
                else:
                    print("The folder does not exist.")
            

    #Se activa una vez el render haya terminado
    def rendering_finished(self):
        self.timer.stop()
        self.status.setText("Render completed")
        self.render_button.setEnabled(True)
        self.render_in_progress = False  
        self.tiempo_restante.setText('-')
        self.media_player.play()
        if self.checkbox.isChecked() and self.render_parado is False:
            self.autoapagado()

    # Actualizar tiempo total de render
    def update_time(self):
        current_time = QTime.currentTime()
        elapsed_seconds = self.start_time.secsTo(current_time)
        elapsed_seconds = convertir_segundos(elapsed_seconds)
        self.tiempo.setText(f"Render time: {elapsed_seconds}")

    def autoapagado(self):
        # Realizar el apagado
        comando_apagado = "shutdown /s /t 600"
        os.system(comando_apagado)
        respuesta = QMessageBox.question(self, "Warning!", "It will shutdown in 10 minutes. Do you want to continue?",
                                         QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if respuesta == QMessageBox.Cancel:
            # Si el usuario selecciona "Cancelar", cancela el apagado
            os.system("shutdown /a")

    def closeEvent(self, event):
        respuesta = QMessageBox.question(self, "Confirm", "Are you sure you want to close the application?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            print("Ejecutando función de cerrado...")
            self.stop_render()
            event.accept()
        else:
            event.ignore()

##################################################################################


class RenderThread(QtCore.QThread):
    shot_porcentaje = QtCore.Signal(object)
    tiempo_restante = QtCore.Signal(float)
    current_shot = QtCore.Signal(str)
    render_path = QtCore.Signal(str)
    descripcion = QtCore.Signal(str)
    finished = QtCore.Signal()
    tiempo = QtCore.Signal(int)
    not_node = QtCore.Signal()
    consola = QtCore.Signal(object)
    iteracion = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.stop_rendering = False

    def start_rendering(self, instrucciones):
        self.command = instrucciones
        self.start()

    def run(self):
        print(self.command)
        self.start_time = time.time()
        iteracion = 0
        render_path = None
        for comando in self.command:
            if self.stop_rendering is True:
                break
            count = 0
            with subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True) as self.proceso:
                self.pid = self.proceso.pid
                print('Subprocess id:', self.pid)

                while True:
                    if self.stop_rendering: 
                        break
                    linea = self.proceso.stdout.readline()
                    print(linea)
                    self.consola.emit(linea)
                    if not linea:
                        break
                    if 'last frame:' in linea:
                        frame_range = linea.split()
                        frame_range = frame_range[-1]
                        frame_range = int(frame_range)

                    if 'shot name:' in linea:
                        shot_name = linea.split()
                        shot_name = shot_name[-1]
                        shot_name = str(shot_name)
                        self.current_shot.emit(shot_name)

                    if 'render_path is:' in linea:
                        inicio = "render_path is: "

                        # Utilizamos la función find() para obtener el índice donde empieza el texto después de render_path is:
                        indice_inicio = linea.find(inicio)

                        # Verificamos si se encontró la cadena inicial
                        if indice_inicio != -1:
                        # Obtenemos los caracteres después de render_path is:
                            render_path = linea[indice_inicio + len(inicio):]
                            print(render_path)
                        else:
                            print("Not found")
                        render_path = str(render_path)
                        
                    if 'Writing ' in linea:
                        count = count + 1
                        frame_actual = count/2
                        porcentaje = (frame_actual / frame_range) *100
                        porcentaje = int(porcentaje)
                        shot_porcentaje = (shot_name, porcentaje) 
                        self.shot_porcentaje.emit(shot_porcentaje)
                        
                        end_time = time.time()
                        frames_restantes = frame_range - frame_actual
                        tiempo = end_time - self.start_time
                        time_per_frame = tiempo/frame_actual
                        tiempo_restante = time_per_frame * frames_restantes
                        self.tiempo_restante.emit(tiempo_restante)

                        actual = linea.split()
                        actual = actual[0:-3]
                        actual = ' '.join(actual)
                        self.descripcion.emit(actual)

                    if linea.startswith('Total render time:'):
                        self.descripcion.emit(linea)
                    
                    if 'no existe' in linea:
                        patron = r"(El nodo.*)"
                        nombre_del_nodo = re.search(patron, linea)

                        if nombre_del_nodo:
                            nombre_del_nodo = nombre_del_nodo.group(1).strip()
                        
                        # Enviamos la informacion y las señales
                        self.descripcion.emit(nombre_del_nodo)
                        self.not_node.emit()

                    end_time = time.time()
                    tiempo = end_time - self.start_time
                    tiempo = int(tiempo)
                    self.tiempo.emit(tiempo)

                # Ejecutar al terminar el render de cada shot
                if render_path is not None:    
                    self.render_path.emit(render_path)

            iteracion += 1
            print('iteracion', iteracion)
            self.iteracion.emit(iteracion)

        # Cuando se llega aqui es por que el proceso de render terminó       
        if self.stop_rendering:
            self.finished.emit()

    def stop(self, exe_path):
        if self.proceso.poll() is None:
            self.stop_rendering = True

            nombre_archivo = os.path.basename(exe_path)
            nuke_process = None
            for proc in psutil.process_iter(['pid', 'name']):
                print(proc.info['name'])
                if proc.info['name'] == nombre_archivo:
                    nuke_process = proc
                    break
            self.nuke_pid = nuke_process.info['pid'] if nuke_process else None
            print('Nuke subprocesss id is:', self.nuke_pid)
            os.kill(self.nuke_pid, signal.SIGTERM)

#################################################################################
#ejecutable
#################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())