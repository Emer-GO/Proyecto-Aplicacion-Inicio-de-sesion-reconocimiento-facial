import sys
import cv2
import threading
import time
from PySide6.QtWidgets import QFrame,QMessageBox, QApplication, QWidget
from PySide6.QtWidgets import QFileDialog , QGridLayout, QPushButton, QLabel
from PySide6.QtWidgets import QLineEdit, QVBoxLayout,QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QImage, QPixmap
import sqlite3
import os
import imutils
import numpy as np
import cv2.data

rutaData = ""

def conexion():
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contra TEXT NOT NULL,
            archivo TEXT 
        )          
        ''')
    return conn

class Ventana_usuario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

        form_layout = QGridLayout()

        self.btn_admin = QPushButton("ADMIN")
        self.btn_admin.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.btn_admin.clicked.connect(self.cambiar_admin)

        self.label_usuario = QLabel("Usuario:")
        self.label_usuario.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.input_usuario = QLineEdit()
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.input_usuario.setPlaceholderText("Ingrese su nombre de usuario")

        self.label_contraseña = QLabel("Contraseña:")
        self.label_contraseña.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.input_contraseña = QLineEdit()
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.input_contraseña.setPlaceholderText("Ingrese su contraseña")

        self.boton_login = QPushButton("Iniciar sesión")
        self.boton_login.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.boton_login.clicked.connect(self.ingresar)

        self.label_mensaje = QLabel("")
        self.label_mensaje.setStyleSheet("color: red;")

        form_layout.addWidget(self.btn_admin,0,0)
        form_layout.addWidget(self.label_usuario,1,0)
        form_layout.addWidget(self.input_usuario,1,1)

        form_layout.addWidget(self.label_contraseña,2,0)
        form_layout.addWidget(self.input_contraseña,2,1)

        form_layout.addWidget(self.boton_login, 3, 0, 1, 2)
        form_layout.addWidget(self.label_mensaje, 4, 0, 1, 2)

        main_layout.addLayout(form_layout)

        self.texto_registro = QLabel("<a href='#'>¿No tienes una cuenta? Regístrate aquí.</a>")
        self.texto_registro.setOpenExternalLinks(False)
        self.texto_registro.setAlignment(Qt.AlignCenter)
        self.texto_registro.setStyleSheet("color: blue; text-decoration: underline;")
        self.texto_registro.linkActivated.connect(self.cambiar_registro)

        main_layout.addWidget(self.texto_registro)

        self.setLayout(main_layout)
    
    def ingresar(self):
        nombre = self.input_usuario.text()
        contra = self.input_contraseña.text()

        conn = conexion()

        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM usuarios WHERE nombre = ? AND contra = ?
        ''', (nombre, contra))

        user = cursor.fetchone()

        if user:
            self.ventana_confirmacion = Ventana_confirmacion(nombre)
            screen_geometry = app.primaryScreen().geometry()

            x = (screen_geometry.width() - self.ventana_confirmacion.width()) // 2
            y = (screen_geometry.height() - self.ventana_confirmacion.height()) // 2

            self.ventana_confirmacion.move(x, y)
            self.ventana_confirmacion.show()
            self.close()
        else:
            self.label_mensaje.setText("Usuario o Contraseña equivocados")
        
        conn.close()

    def cambiar_registro(self):
        self.ventana_registro = Ventana_registro()
        screen_geometry = app.primaryScreen().geometry()

        x = (screen_geometry.width() - self.ventana_registro.width()) // 2
        y = (screen_geometry.height() - self.ventana_registro.height()) // 2

        self.ventana_registro.move(x, y)
        self.ventana_registro.show()
        self.close()

    def cambiar_admin(self):
        self.ventana_admin = Ventana_admin()
        screen_geometry = app.primaryScreen().geometry()

        x = (screen_geometry.width() - self.ventana_admin.width()) // 2
        y = (screen_geometry.height() - self.ventana_admin.height()) // 2

        self.ventana_admin.move(x, y)
        self.ventana_admin.show()
        self.close()

class Ventana_registro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear cuenta")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()
        form_layout = QGridLayout()

        self.btn_admin = QPushButton("ADMIN")
        self.btn_admin.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.btn_admin.clicked.connect(self.cambiar_admin)

        self.label_usuario = QLabel("Nuevo Usuario:")
        self.label_usuario.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.input_usuario = QLineEdit()
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.input_usuario.setPlaceholderText("Ingrese su nombre de usuario")

        self.label_contraseña = QLabel("Contraseña:")
        self.label_contraseña.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.input_contraseña = QLineEdit()
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.input_contraseña.setPlaceholderText("Ingrese su contraseña")

        self.label_confirmar = QLabel("Confirmar Contraseña:")
        self.label_confirmar.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.input_confirmar = QLineEdit()
        self.input_confirmar.setEchoMode(QLineEdit.Password)
        self.input_confirmar.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.input_confirmar.setPlaceholderText("Confirme su contraseña")

        self.btn_crear = QPushButton("Crear cuenta")
        self.btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.btn_crear.clicked.connect(self.creacion)

        self.label_mensaje = QLabel("")
        self.label_mensaje.setStyleSheet("color: red;")

        form_layout.addWidget(self.btn_admin,0,0)
        form_layout.addWidget(self.label_usuario,1,0)
        form_layout.addWidget(self.input_usuario,1,1)
        form_layout.addWidget(self.label_contraseña,2,0)
        form_layout.addWidget(self.input_contraseña,2,1)
        form_layout.addWidget(self.label_confirmar,3,0)
        form_layout.addWidget(self.input_confirmar,3,1)
        form_layout.addWidget(self.btn_crear,4,0,1,2)
        form_layout.addWidget(self.label_mensaje,5,0,1,2)

        main_layout.addLayout(form_layout)

        # Establecer el layout principal
        self.setLayout(main_layout)

    def creacion(self):
        nombre = self.input_usuario.text()
        contra = self.input_contraseña.text()
        contra2 = self.input_confirmar.text()

        if contra == contra2:

            self.ventana_guardado = Ventana_guardado(nombre,contra)
            screen_geometry = app.primaryScreen().geometry()

            x = (screen_geometry.width() - self.ventana_guardado.width()) // 2
            y = (screen_geometry.height() - self.ventana_guardado.height()) // 2

            self.ventana_guardado.move(x, y)
            self.ventana_guardado.show()
            self.close()

        else:
            self.label_mensaje.setText("Las Contrseñas son diferentes")
    def cambiar_admin(self):
        self.ventana_admin = Ventana_admin()
        screen_geometry = app.primaryScreen().geometry()

        x = (screen_geometry.width() - self.ventana_admin.width()) // 2
        y = (screen_geometry.height() - self.ventana_admin.height()) // 2

        self.ventana_admin.move(x, y)
        self.ventana_admin.show()
        self.close()

class Ventana_admin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Admin")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

        form_layout = QGridLayout()

        self.btn_inicio = QPushButton("INICIO")
        self.btn_inicio.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)

        self.btn_inicio.clicked.connect(self.inicio)

        self.lbl_admin = QLabel("Bienvenido,Admin")
        self.lbl_admin.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.lbl_admin.setAlignment(Qt.AlignCenter)
        self.lbl_admin.setFixedHeight(20)

        self.btn_ruta = QPushButton("Cargar ruta")
        self.btn_ruta.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.btn_ruta.clicked.connect(self.cargar_ruta)

        self.lbl_ruta = QLabel(rutaData)
        self.lbl_ruta.setStyleSheet("font-size: 10px; font-weight: bold; color: #333;")
        self.frame_Usuario = QFrame()
        self.frame_Usuario.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self.frame_Usuario)
        self.tabla = QTableWidget(self)
        layout.addWidget(self.tabla)


        form_layout.addWidget(self.btn_inicio,0,0)
        form_layout.addWidget(self.lbl_admin,1,0,1,2)
        form_layout.addWidget(self.btn_ruta,2,0)
        form_layout.addWidget(self.lbl_ruta,2,1)
        form_layout.addWidget(self.frame_Usuario,3,0,1,2)

        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)
        
        self.cargar_datos()

    def cargar_ruta(self):
        global rutaData
        rutaData=QFileDialog.getExistingDirectory(self,"Selecciona la ruta para cargar archivos")
        if rutaData:
            self.lbl_ruta.setText(rutaData)
            if rutaData != "No se a seleccionado ruta":
                carpeta = "data"
                nueva_carpeta = os.path.join(rutaData,carpeta)
            if os.path.exists(nueva_carpeta):
                print(f"Error: Ya existe una carpeta con el nombre '{nueva_carpeta}'.")
            else:
                # Crear la carpeta si no existe
                try:
                    os.makedirs(nueva_carpeta, exist_ok=True)
                    print(f"Carpeta '{nueva_carpeta}' creada en: {nueva_carpeta}")
                except Exception as e:
                    print(f"Error al crear la carpeta: {e}")
        else:
            self.lbl_ruta.setText("No se a seleccionado ruta")

    def cargar_datos(self):
        conn =conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios")
        rows= cursor.fetchall()

        if rows:
            # Establecer el número de filas y columnas
            self.tabla.setRowCount(len(rows))
            self.tabla.setColumnCount(len(rows[0]))

            # Establecer los encabezados de la tabla (columnas)
            self.tabla.setHorizontalHeaderLabels(["ID", "Usuario", "Contraseña","Archivo"])  # Ajusta los nombres de las columnas

            # Insertar los datos en el QTableWidget
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        else:
            # Si no hay datos
            self.tabla.setRowCount(0)
        conn.close()
    
    def inicio(self):
        self.ventana_usuario = Ventana_usuario()
        screen_geometry = app.primaryScreen().geometry()

        x = (screen_geometry.width() - self.ventana_usuario.width()) // 2
        y = (screen_geometry.height() - self.ventana_usuario.height()) // 2

        self.ventana_usuario.move(x, y)
        self.ventana_usuario.show()
        self.close()

class Ventana_confirmacion(QWidget):
    def __init__(self,nombre):
        super().__init__()
        self.nombre = nombre
        self.setWindowTitle("Dejemee escanear su cara")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.layout = QGridLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label,0,0)

        self.time_label = QLabel("Tiempo de detección: 0 segundos", self)
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.time_label,1,0)

        self.setLayout(self.layout)

        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print("Error al abrir la cámara.")
            sys.exit()

        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        ruta_data=os.path.join(rutaData,"data")
        ruta_persona =os.path.join(ruta_data,self.nombre)
        self.model_name = f"modelo_{self.nombre}.yml"
        ruta_modelo=os.path.join(ruta_persona,self.model_name)

        self.face_recognizer.read(ruta_modelo)

        self.face_detected_time = None
        self.detection_duration = 5  # Tiempo de detección en segundos (5 segundos)
        self.new_window_open = False  # Control para abrir la nueva ventana solo una vez

        # Temporizador para actualizar la imagen cada 30 ms (aproximadamente 30 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.face_detected = False
    
    def update_frame(self):
        # Capturar un fotograma de la cámara
        ret, frame = self.cap.read()
        if not ret:
            print("No se pudo obtener un fotograma.")
            return

        # Convertir la imagen BGR a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        # Detectar las caras en el fotograma
        faces = self.faceClassif.detectMultiScale(gray, 1.3, 5)

        face_detected = False  # Variable para saber si se detectó alguna cara

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

            # Realizar la predicción del rostro
            result = self.face_recognizer.predict(rostro)

            # Si la predicción tiene una distancia pequeña, mostramos el nombre
            if result[1] < 70:
                cv2.putText(frame, '{}'.format(self.nombre), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face_detected = True
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Si se detecta una cara, marcar el tiempo
        if face_detected:
            if self.face_detected_time is None:
                self.face_detected_time = cv2.getTickCount()  # Marca el tiempo cuando se detecta la cara
        else:
            # Si no se detecta una cara, reiniciar el temporizador
            self.face_detected_time = None

        # Si ha pasado más de 5 segundos desde la última detección de cara, cambiar a otra ventana
        if self.face_detected_time is not None:
            elapsed_time = (cv2.getTickCount() - self.face_detected_time) / cv2.getTickFrequency()
            elapsed_seconds = round(elapsed_time)  # Redondear el tiempo a segundos

            if elapsed_seconds >= self.detection_duration and not self.new_window_open:
                self.face_detected = True
                self.open_new_window()
                return

            # Actualizar el label con el tiempo transcurrido de detección de la cara en segundos
            self.time_label.setText(f"Tiempo de detección: {elapsed_seconds} segundos")

        # Convertir la imagen de BGR a RGB para usar con PySide6
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Crear un QPixmap a partir de QImage
        pixmap = QPixmap.fromImage(q_image)

        # Mostrar la imagen en el QLabel
        self.image_label.setPixmap(pixmap)

    def open_new_window(self):
        self.timer.stop()       
        self.cap.release() 
        self.cap = None

        self.new_window = Ventana_principal(self.nombre)
        screen_geometry = app.primaryScreen().geometry()
        x = (screen_geometry.width() - self.new_window.width()) // 2
        y = (screen_geometry.height() - self.new_window.height()) // 2
        self.new_window.move(x, y)
        self.new_window.show()
        self.new_window_open = True
        self.close()

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("✔️ Cámara liberada en closeEvent")
        event.accept()

class Ventana_guardado(QWidget):
    cambio_a_inicio = Signal()

    def __init__(self, nombre, contra):
        super().__init__()

        self.cambio_a_inicio.connect(self.cambiar_inicio)
        self.nombre = nombre
        self.contra = contra

        self.setWindowTitle("Creador de cuenta")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.layout = QGridLayout()

        self.lbl_bienvenida = QLabel(f"Bienvenido {self.nombre},Dejenos capturar su rostro")
        self.lbl_bienvenida.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.lbl_bienvenida,0,0)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label,1,0)

        self.capture_button = QPushButton('Iniciar Cuenta Regresiva', self)
        self.capture_button.clicked.connect(self.start_countdown)
        self.capture_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.layout.addWidget(self.capture_button,2,0)

        self.countdown_label = QLabel(self)
        self.countdown_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.countdown_label,3,0)

        self.setLayout(self.layout)
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            print("Error cargando el clasificador de rostros.")
            sys.exit()
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error al acceder a la cámara")
            sys.exit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.is_counting_down = False
        self.countdown = 5  # Tiempo de cuenta regresiva en segundos
        self.photos_taken = 0

        carpeta = "data"
        nueva_carpeta = os.path.join(rutaData,carpeta)
        self.output_dir = os.path.join(nueva_carpeta,nombre)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def update_frame(self):
        ret,frame = self.cap.read()
        if ret:
            # Convertir la imagen de BGR (OpenCV) a RGB (Qt)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
            faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 4)  # Detectar rostros

            # Dibujar un cuadro verde alrededor de cada rostro detectado
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rectángulo verde

            # Convertir la imagen con el cuadro verde de BGR (OpenCV) a RGB (Qt)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            # Ajustar la imagen para que cubra todo el área de la cámara, manteniendo la relación de aspecto
            pixmap = pixmap.scaled(700, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Establecer la imagen en el QLabel
            self.image_label.setPixmap(pixmap)

    def start_countdown(self):
        if not self.is_counting_down:
            self.is_counting_down = True
            self.capture_button.setEnabled(False)
            self.countdown_label.setText(f"Cuenta regresiva: {self.countdown}s")
            self.countdown_timer = QTimer(self)
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)  # Actualizar cada segundo

            # Crear y lanzar un hilo para iniciar el proceso de captura después de la cuenta regresiva
            self.capture_thread = threading.Thread(target=self.capture_photos)
            self.capture_thread.start()

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown -= 1
            self.countdown_label.setText(f"Cuenta regresiva: {self.countdown}s")
        else:
            self.countdown_label.setText("¡Comienza a tomar fotos!")
            self.countdown_timer.stop()

    def capture_photos(self):
        time.sleep(self.countdown)
        self.photos_taken = 0

        while self.photos_taken < 300:
            ret, frame = self.cap.read()
            if ret:
                # Detectar rostro en la imagen antes de guardar la foto
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
                faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 4)  # Detectar rostros

                # Si se detecta al menos un rostro, capturamos la imagen
                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        # Recortamos el rostro de la imagen
                        face = frame[y:y + h, x:x + w]
                        
                        # Guardamos solo el rostro detectado
                        photo_path = os.path.join(self.output_dir, f"foto_{self.photos_taken + 1}.jpg")
                        cv2.imwrite(photo_path, face)
                        self.photos_taken += 1
                        self.countdown_label.setText(f"Foto {self.photos_taken} tomada.")
                        time.sleep(0.05)  # Pequeña espera entre fotos

        print("300 fotos tomadas, proceso terminado.")
        
        # Ahora que tenemos las fotos, entrenamos el modelo con las fotos tomadas
        self.train_face_recognizer(self.output_dir)  # Llamamos a la función de entrenamiento con el directorio de fotos
        self.capture_button.setEnabled(True)
        self.is_counting_down = False
    
    def train_face_recognizer(self, image_folder):
        faces = []
        labels = []
        label = 0

        # Recorremos las imágenes en la carpeta
        for filename in os.listdir(image_folder):
            if filename.endswith('.jpg'):
                image_path = os.path.join(image_folder, filename)
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Leer la imagen en escala de grises
                
                # Redimensionar la imagen a un tamaño fijo (por ejemplo, 200x200)
                img = cv2.resize(img, (200, 200))  # Redimensionar la imagen
                
                faces.append(img)
                labels.append(label)
                label += 1  # Incrementar la etiqueta para cada rostro nuevo

        # Convertir las listas a arrays de numpy
        faces = np.array(faces)
        labels = np.array(labels)

        # Crear el objeto LBPHFaceRecognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Entrenar el modelo
        recognizer.train(faces, labels)

        # Guardar el modelo entrenado
        self.model_name = f"modelo_{self.nombre}.yml"
        model_path = os.path.join(image_folder,self.model_name)
        recognizer.save(model_path)
        print(f"Modelo entrenado y guardado en {model_path}")

        for filename in os.listdir(image_folder):
            if filename.endswith('.jpg'):
                ruta_img = os.path.join(image_folder,filename)
                os.remove(ruta_img)
            else:
                print("este es el modelo")

        self.guardar_usuario(self.model_name)
    
    def guardar_usuario(self, model_name):
        if self.nombre and self.contra and model_name:
            conn = conexion()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO usuarios (nombre, contra, archivo)
                VALUES (?, ?, ?)
            ''', (self.nombre, self.contra, model_name))
            
            conn.commit()
            conn.close()
            print("aqui se guardo el usuario")

        # Emitir señal para cambiar de pestaña desde hilo principal
        self.cambio_a_inicio.emit()

    def cambiar_inicio(self):
        print("aqui se cambio de pestaña")
        self.ventana_usuario = Ventana_usuario()
        screen_geometry = app.primaryScreen().geometry()

        x = (screen_geometry.width() - self.ventana_usuario.width()) // 2
        y = (screen_geometry.height() - self.ventana_usuario.height()) // 2

        self.ventana_usuario.move(x, y)
        self.ventana_usuario.show()
        self.close()

class Ventana_principal(QWidget): 
    def __init__(self, nombre):  
        super().__init__()
        self.nombre = nombre

        self.setWindowTitle('Inicio de Sesion Correcto')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.layout = QGridLayout()
        self.btn_inicio = QPushButton("Regresar")
        self.btn_inicio.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.btn_inicio.clicked.connect(self.inicio)

        self.lbl_sesion = QLabel(f"Bienvenido {nombre}")
        self.lbl_sesion.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.lbl_sesion.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.btn_inicio, 0, 0)
        self.layout.addWidget(self.lbl_sesion, 1, 0, 1, 3)

        self.setLayout(self.layout)

    def inicio(self):
        self.ventana_usuario = Ventana_usuario()
        screen_geometry = app.primaryScreen().geometry()
        x = (screen_geometry.width() - self.ventana_usuario.width()) // 2
        y = (screen_geometry.height() - self.ventana_usuario.height()) // 2
        self.ventana_usuario.move(x, y)
        self.ventana_usuario.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana_usuario()

    screen_geometry = app.primaryScreen().geometry()

    x = (screen_geometry.width() - ventana.width()) // 2
    y = (screen_geometry.height() - ventana.height()) // 2

    ventana.move(x, y)
    ventana.show()
    sys.exit(app.exec())