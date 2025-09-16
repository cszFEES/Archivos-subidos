import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtCore import Qt

TAM_CASILLA = 40

class LabelImagenConGrid(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_original = None
        self.filas = 6
        self.columnas = 6

    def setPixmap(self, pixmap):
        self.pixmap_original = pixmap
        super().setPixmap(pixmap)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap_original:
            return

        painter = QPainter(self)
        pen = QPen(Qt.red)
        pen.setWidth(1)
        painter.setPen(pen)

        w = self.pixmap().width()
        h = self.pixmap().height()

        offset_x = 0
        offset_y = 0

        ancho_celda = w / self.columnas
        alto_celda = h / self.filas

        for c in range(self.columnas + 1):
            x = offset_x + int(c * ancho_celda)
            painter.drawLine(x, offset_y, x, offset_y + h)
        for f in range(self.filas + 1):
            y = offset_y + int(f * alto_celda)
            painter.drawLine(offset_x, y, offset_x + w, y)

class EditorDeMosaicos(QWidget):
    def __init__(self, filas=5, columnas=5):
        super().__init__()
        self.filas = filas
        self.columnas = columnas

        self.indice_mosaico_casillas = [[None]*columnas for _ in range(filas)]

        self.pixmap_seleccionado = None
        self.pixmap_imagen = None
        self.ruta_imagen_cargada = ""
        self.nombre_imagen_cargada = ""

        self.grid_img_filas = 6
        self.grid_img_columnas = 6

        self.iniciarUI()

    def iniciarUI(self):
        self.setWindowTitle("Editor de Mosaicos")

        layout_principal = QHBoxLayout()

        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(1)
        self.grid.setVerticalSpacing(1)
        self.grid.setContentsMargins(1,1,1,1)

        self.casillas = []
        for f in range(self.filas):
            fila_casillas = []
            for c in range(self.columnas):
                boton = QPushButton("")
                boton.setFixedSize(TAM_CASILLA, TAM_CASILLA)
                boton.setStyleSheet("margin: 0px; padding: 0px;")
                boton.clicked.connect(self.clicCasilla)
                self.grid.addWidget(boton, f, c)
                fila_casillas.append(boton)
            self.casillas.append(fila_casillas)
        layout_principal.addLayout(self.grid)

        layout_derecha = QVBoxLayout()

        layout_2columnas = QGridLayout()
        layout_2columnas.addWidget(QLabel("Filas casillas:"), 0, 0)
        self.input_filas = QLineEdit(str(self.filas))
        self.input_filas.setFixedWidth(40)
        layout_2columnas.addWidget(self.input_filas, 0, 1)

        layout_2columnas.addWidget(QLabel("Columnas casillas:"), 0, 2)
        self.input_columnas = QLineEdit(str(self.columnas))
        self.input_columnas.setFixedWidth(40)
        layout_2columnas.addWidget(self.input_columnas, 0, 3)

        layout_2columnas.addWidget(QLabel("Filas grid imagen:"), 1, 0)
        self.input_grid_img_filas = QLineEdit(str(self.grid_img_filas))
        self.input_grid_img_filas.setFixedWidth(40)
        layout_2columnas.addWidget(self.input_grid_img_filas, 1, 1)

        layout_2columnas.addWidget(QLabel("Columnas grid imagen:"), 1, 2)
        self.input_grid_img_columnas = QLineEdit(str(self.grid_img_columnas))
        self.input_grid_img_columnas.setFixedWidth(40)
        layout_2columnas.addWidget(self.input_grid_img_columnas, 1, 3)

        layout_derecha.addLayout(layout_2columnas)

        layout_botones = QHBoxLayout()
        boton_aplicar = QPushButton("Aplicar tamaño casillas")
        boton_aplicar.clicked.connect(self.aplicarTamanoGrid)
        layout_botones.addWidget(boton_aplicar)

        boton_aplicar_grid = QPushButton("Aplicar grid imagen")
        boton_aplicar_grid.clicked.connect(self.aplicarGridImagen)
        layout_botones.addWidget(boton_aplicar_grid)
        layout_derecha.addLayout(layout_botones)

        boton_cargar = QPushButton("Cargar Imagen")
        boton_cargar.clicked.connect(self.cargarImagen)
        layout_derecha.addWidget(boton_cargar)

        self.label_imagen = LabelImagenConGrid()
        self.label_imagen.setFixedSize(TAM_CASILLA*6, TAM_CASILLA*6)
        self.label_imagen.setStyleSheet("border: 1px solid black;")
        self.label_imagen.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout_derecha.addWidget(self.label_imagen)

        self.label_tamano_grid = QLabel("Tamaño cuadrícula imagen: -")
        layout_derecha.addWidget(self.label_tamano_grid)

        layout_guardar_cargar = QHBoxLayout()
        boton_cargar_config = QPushButton("Cargar Configuración JSON")
        boton_cargar_config.clicked.connect(self.cargarConfiguracion)
        layout_guardar_cargar.addWidget(boton_cargar_config)

        boton_guardar = QPushButton("Guardar Configuración JSON")
        boton_guardar.clicked.connect(self.guardarConfiguracion)
        layout_guardar_cargar.addWidget(boton_guardar)
        layout_derecha.addLayout(layout_guardar_cargar)

        self.label_ruta_guardado = QLabel("No se ha guardado aún")
        layout_derecha.addWidget(self.label_ruta_guardado)

        layout_derecha.addStretch()

        layout_principal.addLayout(layout_derecha)

        self.setLayout(layout_principal)

        self.label_imagen.mousePressEvent = self.seleccionarParteImagen

        self.show()

    def aplicarTamanoGrid(self):
        try:
            f = int(self.input_filas.text())
            c = int(self.input_columnas.text())
            if f <= 0 or c <= 0:
                raise ValueError("El número de filas y columnas debe ser positivo.")
            self.ajustarDimension(f, c)
        except Exception as e:
            QMessageBox.warning(self, "Entrada inválida", str(e))

    def aplicarGridImagen(self):
        try:
            f = int(self.input_grid_img_filas.text())
            c = int(self.input_grid_img_columnas.text())
            if f <= 0 or c <= 0:
                raise ValueError("El tamaño de filas y columnas del grid de la imagen debe ser positivo.")
            self.grid_img_filas = f
            self.grid_img_columnas = c
            if self.pixmap_imagen:
                self.label_imagen.filas = f
                self.label_imagen.columnas = c
                self.label_imagen.update()
                ancho_celda = int(self.pixmap_imagen.width() / c)
                alto_celda = int(self.pixmap_imagen.height() / f)
                self.label_tamano_grid.setText(f"Tamaño cuadrícula imagen: {ancho_celda} x {alto_celda} px")
        except Exception as e:
            QMessageBox.warning(self, "Entrada inválida", str(e))

    def ajustarDimension(self, filas_nuevas, columnas_nuevas):
        while len(self.casillas) < filas_nuevas:
            fila_nueva = []
            f = len(self.casillas)
            for c in range(self.columnas):
                btn = QPushButton("")
                btn.setFixedSize(TAM_CASILLA, TAM_CASILLA)
                btn.setStyleSheet("margin: 0px; padding: 0px;")
                btn.clicked.connect(self.clicCasilla)
                self.grid.addWidget(btn, f, c)
                fila_nueva.append(btn)
            self.casillas.append(fila_nueva)
            self.indice_mosaico_casillas.append([None]*self.columnas)

        while len(self.casillas) > filas_nuevas:
            fila_eliminar = self.casillas.pop()
            for btn in fila_eliminar:
                self.grid.removeWidget(btn)
                btn.deleteLater()
            self.indice_mosaico_casillas.pop()

        for f in range(len(self.casillas)):
            fila = self.casillas[f]
            while len(fila) < columnas_nuevas:
                c = len(fila)
                btn = QPushButton("")
                btn.setFixedSize(TAM_CASILLA, TAM_CASILLA)
                btn.setStyleSheet("margin: 0px; padding: 0px;")
                btn.clicked.connect(self.clicCasilla)
                self.grid.addWidget(btn, f, c)
                fila.append(btn)
                self.indice_mosaico_casillas[f].append(None)

            while len(fila) > columnas_nuevas:
                btn = fila.pop()
                self.grid.removeWidget(btn)
                btn.deleteLater()
                self.indice_mosaico_casillas[f].pop()

        self.filas = filas_nuevas
        self.columnas = columnas_nuevas

    def clicCasilla(self):
        boton = self.sender()
        pos = self.obtenerPosicion(boton)
        if not pos:
            return
        f, c = pos
        if self.pixmap_seleccionado:
            pixmap_ajustada = self.pixmap_seleccionado.scaled(
                TAM_CASILLA, TAM_CASILLA, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
            icono = QIcon(pixmap_ajustada)
            boton.setIcon(icono)
            boton.setIconSize(pixmap_ajustada.size())
            self.indice_mosaico_casillas[f][c] = (self.sel_fila_imagen, self.sel_col_imagen)
        else:
            boton.setIcon(QIcon())
            boton.setStyleSheet("background-color: white; margin: 0px; padding: 0px;")
            self.indice_mosaico_casillas[f][c] = None

    def obtenerPosicion(self, boton):
        for f, fila in enumerate(self.casillas):
            for c, btn in enumerate(fila):
                if btn == boton:
                    return f, c
        return None

    def cargarImagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir imagen", "", "Archivos de imagen (*.png *.jpg *.bmp)")
        if ruta:
            pixmap = QPixmap(ruta)
            if pixmap.isNull():
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen.")
                return
            self.pixmap_imagen = pixmap
            self.ruta_imagen_cargada = ruta
            self.nombre_imagen_cargada = os.path.basename(ruta)
            pixmap_esc = pixmap.scaled(self.label_imagen.width(), self.label_imagen.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_imagen.setPixmap(pixmap_esc)
            self.label_imagen.filas = self.grid_img_filas
            self.label_imagen.columnas = self.grid_img_columnas
            self.pixmap_seleccionado = None
            ancho_celda = int(pixmap.width() / self.grid_img_columnas)
            alto_celda = int(pixmap.height() / self.grid_img_filas)
            self.label_tamano_grid.setText(f"Tamaño cuadrícula imagen: {ancho_celda} x {alto_celda} px")

    def seleccionarParteImagen(self, event):
        if not self.pixmap_imagen:
            return
        pos = event.pos()
        pixmap_actual = self.label_imagen.pixmap()
        if not pixmap_actual:
            return
        pixmap_size = pixmap_actual.size()
        x = pos.x()
        y = pos.y()
        if x < 0 or y < 0 or x >= pixmap_size.width() or y >= pixmap_size.height():
            return
        orig_w = self.pixmap_imagen.width()
        orig_h = self.pixmap_imagen.height()
        orig_x = int(x * orig_w / pixmap_size.width())
        orig_y = int(y * orig_h / pixmap_size.height())
        ancho_celda_img = orig_w / self.label_imagen.columnas
        alto_celda_img = orig_h / self.label_imagen.filas
        col_sel = int(orig_x // ancho_celda_img)
        fila_sel = int(orig_y // alto_celda_img)
        left = int(col_sel * ancho_celda_img)
        top = int(fila_sel * alto_celda_img)
        ancho_celda = int(ancho_celda_img)
        alto_celda = int(alto_celda_img)
        seleccionado = self.pixmap_imagen.copy(left, top, ancho_celda, alto_celda)
        self.pixmap_seleccionado = seleccionado
        self.sel_fila_imagen = fila_sel
        self.sel_col_imagen = col_sel

    def guardarConfiguracion(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar configuración JSON", "configuracion_mosaico.json", "Archivos JSON (*.json)")
        if not ruta:
            return
        try:
            data = {
                "imagen_ruta": self.ruta_imagen_cargada,
                "imagen_nombre": self.nombre_imagen_cargada,
                "tam_casilla": TAM_CASILLA,
                "grid_imagen": {
                    "filas": self.grid_img_filas,
                    "columnas": self.grid_img_columnas
                },
                "casillas": self.indice_mosaico_casillas
            }
            with open(ruta, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.label_ruta_guardado.setText(f"Guardado en: {ruta}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {e}")

    def cargarConfiguracion(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar configuración JSON", "", "Archivos JSON (*.json)")
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding='utf-8') as f:
                data = json.load(f)
            self.ruta_imagen_cargada = data.get("imagen_ruta", "")
            self.nombre_imagen_cargada = data.get("imagen_nombre", "")
            tam_casilla = data.get("tam_casilla", TAM_CASILLA)
            grid_img = data.get("grid_imagen", {})
            filas_img = grid_img.get("filas", 6)
            columnas_img = grid_img.get("columnas", 6)
            casillas_data = data.get("casillas", [])

            self.grid_img_filas = filas_img
            self.grid_img_columnas = columnas_img

            self.input_filas.setText(str(len(casillas_data)))
            self.input_columnas.setText(str(len(casillas_data[0]) if casillas_data else 0))
            self.input_grid_img_filas.setText(str(filas_img))
            self.input_grid_img_columnas.setText(str(columnas_img))

            self.ajustarDimension(len(casillas_data), len(casillas_data[0]) if casillas_data else 0)

            if self.ruta_imagen_cargada:
                pixmap = QPixmap(self.ruta_imagen_cargada)
                if pixmap.isNull():
                    QMessageBox.warning(self, "Error", "No se pudo cargar la imagen de la configuración.")
                    self.pixmap_imagen = None
                    self.label_imagen.clear()
                else:
                    self.pixmap_imagen = pixmap
                    pixmap_esc = pixmap.scaled(self.label_imagen.width(), self.label_imagen.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.label_imagen.setPixmap(pixmap_esc)
                    self.label_imagen.filas = filas_img
                    self.label_imagen.columnas = columnas_img
                    self.label_tamano_grid.setText(f"Tamaño cuadrícula imagen: "
                                                  f"{pixmap.width() // columnas_img} x {pixmap.height() // filas_img} px")
            else:
                self.pixmap_imagen = None
                self.label_imagen.clear()

            for f, fila in enumerate(casillas_data):
                for c, val in enumerate(fila):
                    if val is None:
                        self.casillas[f][c].setIcon(QIcon())
                        self.indice_mosaico_casillas[f][c] = None
                    else:
                        self.indice_mosaico_casillas[f][c] = tuple(val)
                        if self.pixmap_imagen:
                            ancho_celda = int(self.pixmap_imagen.width() / columnas_img)
                            alto_celda = int(self.pixmap_imagen.height() / filas_img)
                            left = val[1] * ancho_celda
                            top = val[0] * alto_celda
                            seleccionado = self.pixmap_imagen.copy(left, top, ancho_celda, alto_celda)
                            pixmap_escalado = seleccionado.scaled(TAM_CASILLA, TAM_CASILLA, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                            self.casillas[f][c].setIcon(QIcon(pixmap_escalado))
                            self.casillas[f][c].setIconSize(pixmap_escalado.size())
                        else:
                            self.casillas[f][c].setIcon(QIcon())

            self.label_ruta_guardado.setText(f"Cargado de: {ruta}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo cargar la configuración: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = EditorDeMosaicos()
    sys.exit(app.exec())
