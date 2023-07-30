import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QListWidget, QStyledItemDelegate, QVBoxLayout, QWidget
from PySide2.QtWidgets import QLineEdit, QLabel, QAbstractItemView, QListView, QPushButton, QCheckBox, QProgressBar
from PySide2.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QListWidgetItem, QFileDialog, QFrame, QMessageBox
from PySide2.QtGui import QIcon, QColor
from PySide2.QtCore import Qt, QSize
from PySide2 import QtCore

from controladores.db import manager_db

################################################################################
# Interfaz
################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.icon_size = QSize(25, 25)
        # self.setupUi(self)
    
    def setupUi(self, Nuke_Render):
        if not Nuke_Render.objectName():
            Nuke_Render.setObjectName("Render all!")

        # Icono de la ventana
        icon = QIcon("./recursos/logo_s.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Render all!")

        # Obtener el tamaño de la pantalla actual
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry(self)
        
        # Establecer el tamaño de la ventana relativo a la pantalla
        window_width = screen_geometry.width() * 0.5 
        window_height = screen_geometry.height() * 0.5 
        self.setGeometry(screen_geometry.x(), screen_geometry.y(), window_width, window_height)

        #Establecer las propiedades de estilo personalizadas
        self.setStyleSheet("""
                           
                QMainWindow {
                    font: 10pt "Verdana";
                    color:rgb(180, 180, 180);
                }
                            
                QWidget {
                    font: 10pt "Verdana";
                    alignment: 'AlignTop';
                    border-radius: 10px;
                    background-color: rgba(200, 200, 200, 8);
                    color:rgb(180, 180, 180);
                }              
                
                QLabel {
                    font: 10pt "Verdana";
                    min-height: 15px;
                    qproperty-alignment: 'AlignVCenter';
                    padding: 5px;            
                }
                
                QLineEdit { padding: 10px }
                           
                QCheckBox { padding: 10px }

                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }

                QCheckBox::indicator:unchecked {
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                }

                QCheckBox::indicator:checked {
                    background-color: #3498db;
                    border: 2px solid #3498db;
                    border-radius: 5px;
                }
          
                QFrame {
                    background-color: rgb(20, 25, 35);
                    border-radius: 10px;
                }

                QPushButton:hover {
                    background-color: rgb(40, 45, 60); 
                }
                           
                                 
                QPushButton:pressed { 
                    background-color: rgb(50, 55, 70);
                }

                QPushButton {
                    font-size: 18px;
                    min-height: 30px; 
                    font-weight: bold;
                    padding: 10px;                         
                }
                           
                QMessageBox {
                    background-color: rgb(20, 25, 35);
                    font: 10pt "Verdana";
                }
                           
                QMessageBox QPushButton {
                    font-weight: bold;
                    padding: 10px;
                }
                           
                CustomTitleBar {
                    background-color: #2f2f2f; /* Color de fondo personalizado */
                    border-bottom: 1px solid #1f1f1f; /* Borde inferior */
                }

        """)

        self.center_window()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Variables para el manejo del arrastre y redimensionamiento
        self.draggable = False
        self.last_pos = None
        self.resize_offset = None

        #-------------------------------Crear-------------------------------
        # Crear el layout principal y el widget central
        frame = QFrame(self)
        self.setCentralWidget(frame)
        frame_layout = QVBoxLayout() 
        frame.setLayout(frame_layout)
        
        # Definir layout para el titulo
        title_widget = CustomTitleBar(self)
        frame_layout.addWidget(title_widget)
        frame_layout.setAlignment(Qt.AlignTop)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Definir layout para el cuerpo
        central_widget = QWidget(self)
        layout = QVBoxLayout()  
        central_widget.setLayout(layout)
        frame_layout.addWidget(central_widget)
        
        # Layouts para el cuerpo
        division_label_check = QHBoxLayout()
        division_H_layout1 = QHBoxLayout()
        division_H_layout2 = QHBoxLayout()
        division_H_layout3 = QHBoxLayout()
        division_H_layout4 = QHBoxLayout()
        division_H_layout5 = QHBoxLayout()
        division_H_layout6 = QHBoxLayout()

        # Crear las divisiones secundarias (vertical)
        sub_division_layout1 = QVBoxLayout()
        sub_division_layout2 = QVBoxLayout()
        sub_division_layout3 = QVBoxLayout()
        sub_division_layout4 = QVBoxLayout()

        #-------------------------Agregar-------------------------------

        # Agregar las divisiones secundarias a las divisiones principales
        division_H_layout1.addLayout(sub_division_layout1)
        division_H_layout2.addLayout(sub_division_layout2)
        division_H_layout6.addLayout(sub_division_layout3)
        division_H_layout6.addLayout(sub_division_layout4)

        #Definir un espacio
        spacer = QSpacerItem(0, 25, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Agregar las divisiones principales al layout principal
        layout.addItem(spacer)
        layout.addLayout(division_H_layout1)
        layout.addItem(spacer)
        layout.addLayout(division_label_check)
        layout.addLayout(division_H_layout2)
        layout.addLayout(division_H_layout3)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout4)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout5)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout6)
        layout.addItem(spacer)

        #-------------------------Crear los widgets, botones, etc---------------------------
        # Crear botones y asignar colores de fondo y estilo redondeado
        self.nuke_dir = QLineEdit()
        self.nuke_dir.setPlaceholderText(r'C:\Program Files\Nuke14.0v4\Nuke14.0.exe')
        self.nuke_dir.setToolTip('Nuke executable file location')
        sub_division_layout1.addWidget(self.nuke_dir)

        #para introducir el nombre del script
        self.input_write = QLineEdit()
        self.input_write.setPlaceholderText('Write1')
        self.input_write.setToolTip('Name of the Write node to render')
        self.input_write.setAlignment(Qt.AlignLeft)
        sub_division_layout1.addWidget(self.input_write)
        
        #etiqueta de la lista
        label_lista = QLabel("Drag and drop the scripts to render:")
        label_lista.setStyleSheet("max-width: 800px; min-width: 400px;")
        label_lista.setAlignment(Qt.AlignLeft)
        division_label_check.addWidget(label_lista)

        #checkbox open in folder
        division_label_check.addStretch(1)
        self.goto_folder = QCheckBox("Open in folder after render")
        self.goto_folder .setStyleSheet("max-width: 800px; min-width: 400px;")
        division_label_check.addWidget(self.goto_folder)

        #checkbox Shutdown after render
        self.checkbox = QCheckBox('Shutdown after render')
        self.checkbox .setStyleSheet("max-width: 800px; min-width: 400px;")
        division_label_check.addWidget(self.checkbox)

        # Agregar la lista
        self.lista = FileListWidget(self)
        sub_division_layout2.addWidget(self.lista)

        #Agregar botones de add
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.agregar_archivo)
        # agregamos un icono al boton
        icon_path_add = "./recursos/plus.png"
        icon_add = QIcon(icon_path_add)
        pixmap_add = icon_add.pixmap(self.icon_size)
        scaled_icon_add = QIcon(pixmap_add)
        self.add_button.setIcon(scaled_icon_add)

        self.add_button.setStyleSheet("QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                "QPushButton { font-size: 18px; font-weight: bold; }")
        division_H_layout3.addWidget(self.add_button)

        #Agregar botones de eliminar 
        remove_button = QPushButton()
        remove_button.clicked.connect(self.lista.remove_item)
        # agregamos un icono al boton
        icon_path_minus = "./recursos/minus.png"
        icon_minus = QIcon(icon_path_minus)
        pixmap_minus = icon_minus.pixmap(self.icon_size)
        scaled_icon_minus = QIcon(pixmap_minus)
        remove_button.setIcon(scaled_icon_minus)
        remove_button.setStyleSheet("QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                    "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                    "QPushButton { font-size: 18px; font-weight: bold; }")
        division_H_layout3.addWidget(remove_button)
        
        #boton para cargar datos de la DB
        size_db = QSize(80, 80)
        self.load_db = QPushButton("   Load from DB")
        self.load_db.clicked.connect(self.load_from_db)
        # agregamos un icono al boton
        icon_path_db = "./recursos/database.png"
        icon_db = QIcon(icon_path_db)
        pixmap_db = icon_db.pixmap(size_db)
        scaled_icon_db = QIcon(pixmap_db)
        self.load_db.setIcon(scaled_icon_db)
        self.load_db.setStyleSheet("QPushButton:hover { background-color: rgb(70, 80, 90); }"
                                "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                "QPushButton { font-size: 18px; font-weight: bold; }")
        division_H_layout3.addWidget(self.load_db)

        # Agregar el boton de render
        division_H_layout4.addStretch(1)
        self.render_button = QPushButton("   Render")
        self.render_button.setMinimumWidth(800)
        self.render_button.setMaximumWidth(1000)
        # agregamos un icono al boton
        icon_path_render = "./recursos/play.png"
        icon_render = QIcon(icon_path_render)
        pixmap_render = icon_render.pixmap(self.icon_size)
        scaled_icon_render = QIcon(pixmap_render)
        self.render_button.setIcon(scaled_icon_render)
        self.render_button.setStyleSheet("QPushButton { background-color: rgb(30, 120, 90); }"
                     "QPushButton:hover { background-color: rgb(40, 150, 100); }"
                     "QPushButton:pressed { background-color:rgb(10, 150, 120); }"
                     "QPushButton { font-size: 18px; font-weight: bold; }")
        division_H_layout4.addWidget(self.render_button)

        # Boton de stop
        self.button_stop = QPushButton("   Stop")
        self.button_stop.setMinimumWidth(800)
        self.button_stop.setMaximumWidth(1000)
        # agregamos un icono al boton
        icon_path_stop = "./recursos/stop.png"
        icon_stop = QIcon(icon_path_stop)
        pixmap_stop = icon_stop.pixmap(self.icon_size)
        scaled_icon_stop = QIcon(pixmap_stop)
        self.button_stop .setIcon(scaled_icon_stop)
        self.button_stop.setStyleSheet("QPushButton { background-color: rgb(70, 80, 90); }"
                                        "QPushButton:hover { background-color: rgb(100, 60, 60); }"
                                        "QPushButton:pressed { background-color:rgb(120, 60, 60); }"
                                        "QPushButton { font-size: 18px; font-weight: bold; }")
        division_H_layout4.addWidget(self.button_stop)
        division_H_layout4.addStretch(1)

        # Agregar la barra de progreso
        self.progressBar = QProgressBar()
        self.progressBar.setObjectName("progressBar")
        style = """
        QProgressBar { min-height: 50px; border-radius: 5px; }
        QProgressBar::chunk {
            background-color: rgb(30, 120, 90);
            border-radius: 5px;
        }
        """
        self.progressBar.setStyleSheet(style)
        self.progressBar.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        division_H_layout5.addWidget(self.progressBar)

        #Label del status
        self.status = QLabel("Status:")
        self.status.setStyleSheet("QLabel { min-height: 40px;}")
        self.status.setAlignment(Qt.AlignLeft)
        sub_division_layout3.addWidget(self.status)

        #Label de la descripcion del render
        self.descripcion = QLabel("-")
        self.descripcion.setStyleSheet("QLabel { min-height: 40px;}")
        self.descripcion.setAlignment(Qt.AlignLeft)
        self.descripcion.setStyleSheet("font-size: 7pt; color: rgb(90, 90, 90);")
        sub_division_layout3.addWidget(self.descripcion)

        #Label del tiempo total de render
        self.tiempo = QLabel("Render time:")
        self.tiempo.setStyleSheet("QLabel { min-height: 40px;}")
        self.tiempo.setAlignment(Qt.AlignLeft)
        sub_division_layout4.addWidget(self.tiempo)

        #Label del tiempo estimado de render
        self.tiempo_restante = QLabel("-")
        self.tiempo_restante.setStyleSheet("QLabel { min-height: 40px;}")
        self.tiempo_restante.setAlignment(Qt.AlignLeft)
        sub_division_layout4.addWidget(self.tiempo_restante)

    def center_window(self):
        # Obtener el tamaño de la pantalla y el tamaño de la ventana
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # Calcular la posición central de la ventana
        center_x = screen_geometry.center().x() - window_geometry.width() / 2
        center_y = screen_geometry.center().y() - window_geometry.height() / 2

        # Establecer la posición de la ventana
        self.move(center_x, center_y)

    def agregar_archivo(self):
        # Abrir el explorador de archivos y obtener la ubicación del archivo seleccionado
        file_dialog = QFileDialog()
        archivo_seleccionado, _ = file_dialog.getOpenFileName(self, 'Select File', '', 'Nuke script (*.nk)')

        if archivo_seleccionado: 
            self.lista.agregar_elemento(archivo_seleccionado)           

    def load_from_db(self):
        db = manager_db()
        resultado = db.leer_datos()
        
        if len(resultado) > 0:
            for item in resultado:
                self.lista.agregar_elemento(item)
        else:
            print('No elements in DB')
            return

    def CustomMessageBox(self, titulo, mensaje):
        handler = CustomMessageBox()
        handler.question_message(titulo, mensaje)

    def mousePressEvent(self, event):
        # Capturar el evento de clic del ratón para iniciar el arrastre o redimensionamiento
        if event.button() == Qt.LeftButton:
            if event.y() <= 30:
                self.draggable = True
                self.click_pos = event.globalPos() - self.pos()
            else:
                self.click_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        # Capturar el evento de movimiento del ratón para mover o redimensionar la ventana
        if self.draggable:
            if event.buttons() == Qt.LeftButton:
                self.move(event.globalPos() - self.click_pos)

    def mouseReleaseEvent(self, event):
        # Liberar el arrastre o redimensionamiento al soltar el botón del ratón
        if event.button() == Qt.LeftButton:
            self.draggable = False

############################################################

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.isMaximized = False
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear el botón de cerrar
        close_button = QPushButton()
        close_button.setStyleSheet("QPushButton { background-color: transparent; padding: 20px }"
                                        "QPushButton:hover { background-color: rgb(100, 60, 60); }"
                                        "QPushButton:pressed { background-color:rgb(120, 60, 60); }"
                                        "QPushButton { font-size: 15px; font-weight: bold; border-radius: 5px; }"
                                        )
        close_button.clicked.connect(self.parent().close)

        icon_size = QSize(15, 15)
        # agregamos un icono al boton
        icon_path_close = "./recursos/close.png"
        icon_close = QIcon(icon_path_close)
        pixmap_close = icon_close.pixmap(icon_size)
        scaled_icon_close = QIcon(pixmap_close)
        close_button.setIcon(scaled_icon_close)


        # Crear el botón de minimizar
        minimize_button = QPushButton()
        minimize_button.setStyleSheet("QPushButton { background-color: transparent; padding: 20px }"
                                        "QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                        "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                        "QPushButton { font-size: 15px; font-weight: bold; border-radius: 5px; }"
                                        )
        minimize_button.clicked.connect(self.parent().showMinimized)

        # agregamos un icono al boton
        icon_path_mini = "./recursos/minus.png"
        icon_mini = QIcon(icon_path_mini)
        pixmap_mini = icon_mini.pixmap(icon_size)
        scaled_icon_mini = QIcon(pixmap_mini)
        minimize_button.setIcon(scaled_icon_mini)

        # Crear el botón de maximizar/restaurar
        maximize_restore_button = QPushButton()
        maximize_restore_button.setStyleSheet("QPushButton { background-color: transparent; padding: 20px }"
                                        "QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                        "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                        "QPushButton { font-size: 15px; font-weight: bold; border-radius: 5px; }"
                                        )
        maximize_restore_button.clicked.connect(self.toggle_maximize_restore)

        # agregamos un icono al boton
        icon_path_maxi = "./recursos/maximize.png"
        icon_maxi = QIcon(icon_path_maxi)
        pixmap_maxi = icon_maxi.pixmap(icon_size)
        scaled_icon_maxi = QIcon(pixmap_maxi)
        maximize_restore_button.setIcon(scaled_icon_maxi)

        # Crear la barra de título personalizada
        app_name_label = QLabel("Render All!", self)
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("font-size: 12pt; color: rgb(90, 90, 90); font-weight: bold")

        close_button.setGeometry(QtCore.QRect(10, 10, 100, 25))
        minimize_button.setGeometry(QtCore.QRect(120, 10, 100, 25))
        maximize_restore_button.setGeometry(QtCore.QRect(230, 10, 100, 25))

        # Agregar los widgets al layout
        layout.addWidget(app_name_label)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(maximize_restore_button)
        layout.addWidget(close_button)       

    def toggle_maximize_restore(self):
        if self.isMaximized:
            print('maximized')
            self.window().showNormal()
            self.isMaximized = False
        else:
            print('no maximized')
            self.window().showMaximized()
            self.isMaximized = True

############################################################

class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(1)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setViewMode(QListView.ListMode)
        self.setItemDelegate(AlternatingColorDelegate()) 

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                self.agregar_elemento(file_path)

    def remove_item(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            self.takeItem(self.row(item))

    def agregar_elemento(self, nombre):

        item = QListWidgetItem(self)
        elemento_widget = QWidget()
        elemento_widget.setStyleSheet("QWidget { background-color: transparent; }")
        layout = QHBoxLayout()
        self.nombre_label = QLabel(nombre)
        self.nombre_label.setAlignment(Qt.AlignLeft)
        self.nombre_label.setStyleSheet("QLabel { background-color: transparent; }")

        # Agregar la barra de progreso
        self.mini_progressBar = QProgressBar()
        self.mini_progressBar.setObjectName("mini_progressBar")
        style = """
        QProgressBar { border-radius: 5px; }
        QProgressBar::chunk {
            background-color: rgb(30, 120, 90);
            border-radius: 5px;
        }
        """
        self.mini_progressBar.setStyleSheet(style)
        self.mini_progressBar.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Establecemos las políticas de tamaño para los widgets
        self.nombre_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mini_progressBar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Establecemos los tamaños mínimos y máximos para los widgets
        self.mini_progressBar.setMaximumWidth(200)

        layout.addWidget(self.nombre_label)
        layout.addWidget(self.mini_progressBar)

        elemento_widget.setLayout(layout)
        item.setSizeHint(elemento_widget.sizeHint())
        self.setItemWidget(item, elemento_widget)
        item.setData(1, self.nombre_label)



class CustomMessageBox(QMessageBox):
    def __init__(self):
        super(CustomMessageBox, self).__init__()
        self.setStyleSheet("""
           
            QWidget {
                font: 10pt "Verdana";
                alignment: 'AlignTop';
                border-radius: 10px;
                background-color: rgba(200, 200, 200, 8);
                color:rgb(180, 180, 180);
                padding: 10px;
            } 
                            
            QMessageBox {
                background-color: rgb(20, 25, 35);      
                font: 10pt "Verdana";
            }

            QPushButton:hover {
                background-color: rgb(40, 45, 60); 
            }
                                                     
            QPushButton:pressed { 
                background-color: rgb(50, 55, 70);
            }

        """)
        
    def question_message(self, titulo, mensaje):
        respuesta = QMessageBox.question(self, titulo, mensaje, QMessageBox.Ok)


################################################################################

class AlternatingColorDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.row() % 2 == 0:
            option.backgroundBrush = QColor(25, 28, 38)  # Color para filas pares
        else:
            option.backgroundBrush = QColor(25, 30, 40)  # Color para filas impares

################################################################################
# ejecutar
################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())