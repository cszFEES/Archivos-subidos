import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QFileDialog, QMessageBox, QSizePolicy) ### CAMBIO: Importar QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtCore import Qt, QSize ### CAMBIO: Importar QSize

TAM_CASILLA_MIN = 40 ### CAMBIO: Definir un tamaño mínimo para las casillas

class LabelImagenConGrid(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_original = None
        self.filas = 6
        self.columnas = 6
        ### CAMBIO: Establecer política de tamaño expansible
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setPixmap(self, pixmap):
        self.pixmap_original = pixmap
        self.resizeEvent(None) # Reescalar inmediatamente al cargar
    
    def get_scaled_pixmap(self):
        """Retorna el pixmap reescalado al tamaño actual del label."""
        if self.pixmap_original is None:
            return None
        return self.pixmap_original.scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

    def paintEvent(self, event):
        ### CAMBIO: Usar el pixmap escalado en lugar del original
        pixmap_escalado = self.get_scaled_pixmap()
        if not pixmap_escalado:
            super().paintEvent(event)
            return
        
        # Centrar el pixmap escalado
        w_esc = pixmap_escalado.width()
        h_esc = pixmap_escalado.height()
        offset_x = (self.width() - w_esc) // 2
        offset_y = (self.height() - h_esc) // 2
        
        painter = QPainter(self)
        painter.drawPixmap(offset_x, offset_y, pixmap_escalado)
        
        pen = QPen(Qt.red)
        pen.setWidth(1)
        painter.setPen(pen)

        # Dibujar la cuadrícula sobre el pixmap escalado
        w = w_esc
        h = h_esc
        
        if self.columnas > 0 and self.filas > 0:
            ancho_celda = w / self.columnas
            alto_celda = h / self.filas
        
            for c in range(self.columnas + 1):
                x = offset_x + int(c * ancho_celda)
                painter.drawLine(x, offset_y, x, offset_y + h)
            for f in range(self.filas + 1):
                y = offset_y + int(f * alto_celda)
                painter.drawLine(offset_x, y, offset_x + w, y)

    def resizeEvent(self, event):
        """Reimplementar para actualizar la visualización de la imagen al reescalar."""
        if self.pixmap_original:
            pixmap_escalado = self.get_scaled_pixmap()
            if pixmap_escalado:
                super().setPixmap(pixmap_escalado)
                # Forzar repintado para dibujar el grid en la nueva posición/tamaño
                self.update() 
        else:
            super().resizeEvent(event)

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
        self.setMinimumSize(400, 300) ### CAMBIO: Establecer un tamaño mínimo

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
                ### CAMBIO: Usar un tamaño mínimo y política de expansión
                boton.setMinimumSize(TAM_CASILLA_MIN, TAM_CASILLA_MIN)
                boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                boton.setStyleSheet("margin: 0px; padding: 0px;")
                boton.clicked.connect(self.clicCasilla)
                self.grid.addWidget(boton, f, c)
                fila_casillas.append(boton)
            self.casillas.append(fila_casillas)
        
        ### CAMBIO: Envolver el grid en un widget para controlar su expansión
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid)
        grid_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_principal.addWidget(grid_widget)

        layout_derecha = QVBoxLayout()
        ### CAMBIO: Fijar el tamaño del layout derecho (o usar QSizePolicy.Fixed/Preferred) para que no se estire demasiado, o simplemente no darle la política Expanding.

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
        ### CAMBIO: Eliminar setFixedSize y usar setMinimumSize
        self.label_imagen.setMinimumSize(TAM_CASILLA_MIN*4, TAM_CASILLA_MIN*4) 
        self.label_imagen.setStyleSheet("border: 1px solid black;")
        self.label_imagen.setAlignment(Qt.AlignCenter) ### CAMBIO: Centrar la imagen en el QLabel
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
        
    def resizeEvent(self, event):
        """Reimplementar para reescalar los íconos de las casillas al redimensionar."""
        super().resizeEvent(event)
        self.reescalarIconosCasillas()

    def reescalarIconosCasillas(self):
        """Actualiza el tamaño de los íconos de las casillas según el tamaño actual de los botones."""
        if not self.pixmap_imagen:
            return
        
        # Asumiendo que todas las casillas tienen el mismo tamaño, usamos la primera para obtener las dimensiones
        if self.casillas and self.casillas[0]:
            btn_width = self.casillas[0][0].width()
            btn_height = self.casillas[0][0].height()
        else:
            return
            
        filas_img = self.grid_img_filas
        columnas_img = self.grid_img_columnas
        
        ancho_celda_img = int(self.pixmap_imagen.width() / columnas_img)
        alto_celda_img = int(self.pixmap_imagen.height() / filas_img)
        
        for f in range(self.filas):
            for c in range(self.columnas):
                val = self.indice_mosaico_casillas[f][c]
                if val is not None:
                    # val es (fila_imagen, columna_imagen)
                    top = val[0] * alto_celda_img
                    left = val[1] * ancho_celda_img
                    
                    seleccionado = self.pixmap_imagen.copy(left, top, ancho_celda_img, alto_celda_img)
                    
                    # Reescalar al tamaño actual del botón
                    pixmap_escalado = seleccionado.scaled(
                        btn_width, btn_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                    )
                    
                    self.casillas[f][c].setIcon(QIcon(pixmap_escalado))
                    self.casillas[f][c].setIconSize(pixmap_escalado.size())


    def aplicarTamanoGrid(self):
        try:
            f = int(self.input_filas.text())
            c = int(self.input_columnas.text())
            if f <= 0 or c <= 0:
                raise ValueError("El número de filas y columnas debe ser positivo.")
            self.ajustarDimension(f, c)
            self.reescalarIconosCasillas() ### CAMBIO: Reescalar después de ajustar dimensión
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
                self.reescalarIconosCasillas() ### CAMBIO: Reescalar los iconos al cambiar el grid de la imagen
        except Exception as e:
            QMessageBox.warning(self, "Entrada inválida", str(e))

    def ajustarDimension(self, filas_nuevas, columnas_nuevas):
        # ... (La lógica de agregar/quitar botones es la misma, solo se modificó el tamaño de los botones)
        
        # Eliminar filas/columnas existentes
        while len(self.casillas) > filas_nuevas:
            fila_eliminar = self.casillas.pop()
            for btn in fila_eliminar:
                self.grid.removeWidget(btn)
                btn.deleteLater()
            self.indice_mosaico_casillas.pop()

        for f in range(len(self.casillas)):
            fila = self.casillas[f]
            # Eliminar columnas
            while len(fila) > columnas_nuevas:
                btn = fila.pop()
                self.grid.removeWidget(btn)
                btn.deleteLater()
                self.indice_mosaico_casillas[f].pop()
            # Agregar columnas
            while len(fila) < columnas_nuevas:
                c = len(fila)
                btn = QPushButton("")
                btn.setMinimumSize(TAM_CASILLA_MIN, TAM_CASILLA_MIN) ### CAMBIO: Mínimo
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) ### CAMBIO: Política
                btn.setStyleSheet("margin: 0px; padding: 0px;")
                btn.clicked.connect(self.clicCasilla)
                self.grid.addWidget(btn, f, c)
                fila.append(btn)
                self.indice_mosaico_casillas[f].append(None)
                
        # Agregar filas
        while len(self.casillas) < filas_nuevas:
            fila_nueva = []
            f = len(self.casillas)
            for c in range(columnas_nuevas):
                btn = QPushButton("")
                btn.setMinimumSize(TAM_CASILLA_MIN, TAM_CASILLA_MIN) ### CAMBIO: Mínimo
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) ### CAMBIO: Política
                btn.setStyleSheet("margin: 0px; padding: 0px;")
                btn.clicked.connect(self.clicCasilla)
                self.grid.addWidget(btn, f, c)
                fila_nueva.append(btn)
            self.casillas.append(fila_nueva)
            self.indice_mosaico_casillas.append([None]*columnas_nuevas)


        self.filas = filas_nuevas
        self.columnas = columnas_nuevas
        
        # Asegurar que el layout se reajuste
        self.grid.invalidate()
        self.adjustSize()
        self.update()


    def clicCasilla(self, *args): ### CAMBIO: Ignorar argumentos si se usa solo con self.sender()
        boton = self.sender()
        pos = self.obtenerPosicion(boton)
        if not pos:
            return
        f, c = pos
        
        # Obtener el tamaño actual del botón
        btn_width = boton.width()
        btn_height = boton.height()
        
        if self.pixmap_seleccionado:
            ### CAMBIO: Escalar al tamaño actual del botón
            pixmap_ajustada = self.pixmap_seleccionado.scaled(
                btn_width, btn_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
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
            
            ### CAMBIO: Ya no se escala aquí. LabelImagenConGrid se encarga de reescalar al tamaño de la etiqueta
            self.label_imagen.setPixmap(pixmap) 
            
            self.label_imagen.filas = self.grid_img_filas
            self.label_imagen.columnas = self.grid_img_columnas
            self.pixmap_seleccionado = None
            ancho_celda = int(pixmap.width() / self.grid_img_columnas)
            alto_celda = int(pixmap.height() / self.grid_img_filas)
            self.label_tamano_grid.setText(f"Tamaño cuadrícula imagen: {ancho_celda} x {alto_celda} px")
            self.reescalarIconosCasillas() ### CAMBIO: Reescalar los iconos con la nueva imagen

    def seleccionarParteImagen(self, event):
        if not self.pixmap_imagen:
            return
        
        pos = event.pos()
        pixmap_actual = self.label_imagen.get_scaled_pixmap() ### CAMBIO: Obtener el pixmap escalado
        if not pixmap_actual:
            return
            
        # Calcular los offsets y tamaños del pixmap centrado en el QLabel
        w_esc = pixmap_actual.width()
        h_esc = pixmap_actual.height()
        offset_x = (self.label_imagen.width() - w_esc) // 2
        offset_y = (self.label_imagen.height() - h_esc) // 2
            
        x = pos.x() - offset_x ### CAMBIO: Ajustar la posición al offset del pixmap
        y = pos.y() - offset_y ### CAMBIO: Ajustar la posición al offset del pixmap
        
        # Verificar que el clic esté dentro del área del pixmap escalado
        if x < 0 or y < 0 or x >= w_esc or y >= h_esc:
            self.pixmap_seleccionado = None
            return

        orig_w = self.pixmap_imagen.width()
        orig_h = self.pixmap_imagen.height()
        
        # Mapear las coordenadas escaladas a las coordenadas originales
        orig_x = int(x * orig_w / w_esc) 
        orig_y = int(y * orig_h / h_esc)
        
        ancho_celda_img = orig_w / self.label_imagen.columnas
        alto_celda_img = orig_h / self.label_imagen.filas
        
        col_sel = int(orig_x // ancho_celda_img)
        fila_sel = int(orig_y // alto_celda_img)
        
        left = int(col_sel * ancho_celda_img)
        top = int(fila_sel * alto_celda_img)
        
        # Asegurar que los anchos/altos sean enteros para la copia
        ancho_celda = int(ancho_celda_img)
        alto_celda = int(alto_celda_img)
        
        seleccionado = self.pixmap_imagen.copy(left, top, ancho_celda, alto_celda)
        self.pixmap_seleccionado = seleccionado
        self.sel_fila_imagen = fila_sel
        self.sel_col_imagen = col_sel

    def guardarConfiguracion(self):
        # ... (Sin cambios funcionales en guardar)
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar configuración JSON", "configuracion_mosaico.json", "Archivos JSON (*.json)")
        if not ruta:
            return
        try:
            data = {
                "imagen_ruta": self.ruta_imagen_cargada,
                "imagen_nombre": self.nombre_imagen_cargada,
                "tam_casilla_min": TAM_CASILLA_MIN, ### CAMBIO: Guardar el tamaño mínimo
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
            # TAM_CASILLA_MIN es global, no es necesario cambiarlo, pero lo cargamos por si acaso
            # tam_casilla = data.get("tam_casilla_min", TAM_CASILLA_MIN) 
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
                    ### CAMBIO: setPixmap usa el pixmap original, LabelImagenConGrid lo escala
                    self.label_imagen.setPixmap(pixmap) 
                    self.label_imagen.filas = filas_img
                    self.label_imagen.columnas = columnas_img
                    self.label_tamano_grid.setText(f"Tamaño cuadrícula imagen: "
                                                     f"{pixmap.width() // columnas_img} x {pixmap.height() // filas_img} px")
            else:
                self.pixmap_imagen = None
                self.label_imagen.clear()
                self.label_tamano_grid.setText("Tamaño cuadrícula imagen: -")


            for f, fila in enumerate(casillas_data):
                for c, val in enumerate(fila):
                    if val is None:
                        self.casillas[f][c].setIcon(QIcon())
                        self.indice_mosaico_casillas[f][c] = None
                    else:
                        self.indice_mosaico_casillas[f][c] = tuple(val)
                        # El reescalado de los iconos se hará al final de la carga o en el resizeEvent.
                        
            # Finalmente, reescalar todos los íconos de las casillas cargados
            self.reescalarIconosCasillas()
            
            self.label_ruta_guardado.setText(f"Cargado de: {ruta}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo cargar la configuración: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = EditorDeMosaicos()
    sys.exit(app.exec())