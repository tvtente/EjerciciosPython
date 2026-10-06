"""Control de eventos con PySide6.

Ejecutar: python3 control_eventos_pyside6.py
Comparte asistentes.json con los ejemplos anteriores.
"""
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox, QFileDialog, QDialog, QPlainTextEdit, QDialogButtonBox,
)


ARCHIVO = Path(__file__).with_name("asistentes.json")
CATEGORIAS = ("General", "VIP", "Prensa", "Ponente", "Organización")
CAMPOS = ("id", "nombre", "apellidos", "correo", "categoria", "hora_entrada")


@dataclass
class Persona:
    """Un asistente del evento. dataclass genera el constructor __init__."""

    id: int
    nombre: str
    apellidos: str
    correo: str
    categoria: str
    hora_entrada: str

    def a_diccionario(self):
        """JSON necesita datos simples: convertimos el objeto a diccionario."""
        return asdict(self)

    def a_fila(self):
        """Valores en el mismo orden que las columnas de la tabla."""
        return (self.id, self.nombre, self.apellidos, self.correo,
                self.categoria, self.hora_entrada)

    @classmethod
    def desde_diccionario(cls, registro):
        """Valida un registro leído del JSON y construye una Persona."""
        if not isinstance(registro, dict) or not all(c in registro for c in CAMPOS):
            raise ValueError("Hay un registro incompleto en el JSON.")
        if type(registro["id"]) is not int or registro["id"] < 1:
            raise ValueError("El identificador debe ser un entero positivo.")
        if not all(isinstance(registro[c], str) for c in CAMPOS[1:]):
            raise ValueError("Los campos del asistente deben contener texto.")
        return cls(
            id=registro["id"],
            nombre=registro["nombre"],
            apellidos=registro["apellidos"],
            correo=registro["correo"],
            categoria=registro["categoria"],
            hora_entrada=registro["hora_entrada"],
        )


def cargar_datos(ruta):
    if not ruta.exists():
        return []
    registros = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(registros, list):
        raise ValueError("El JSON debe contener una lista de asistentes.")
    personas = []
    ids = set()
    for registro in registros:
        persona = Persona.desde_diccionario(registro)
        if persona.id in ids:
            raise ValueError("Los identificadores deben ser únicos.")
        ids.add(persona.id)
        personas.append(persona)
    return personas


def convertir_a_json(personas):
    registros = [persona.a_diccionario() for persona in personas]
    return json.dumps(registros, ensure_ascii=False, indent=2)


def guardar_datos(ruta, personas):
    # Primero escribimos un temporal y después reemplazamos el archivo completo.
    temporal = ruta.with_name(ruta.name + ".tmp")
    registros = [persona.a_diccionario() for persona in personas]
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    temporal.replace(ruta)


class ControlEventos(QMainWindow):
    def __init__(self, datos, archivo=ARCHIVO):
        super().__init__()
        self.datos = datos  # Lista de objetos Persona.
        self.archivo = Path(archivo)
        self.setWindowTitle("Control de Acceso a Eventos — PySide6")
        self.resize(960, 650)
        self.setMinimumSize(820, 560)

        central = QWidget()
        self.setCentralWidget(central)
        # QVBoxLayout distribuye los elementos de arriba hacia abajo.
        contenido = QVBoxLayout(central)
        contenido.setContentsMargins(20, 20, 20, 20)
        contenido.setSpacing(16)
        titulo = QLabel("Control de Entrada a Evento")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenido.addWidget(titulo)

        formulario = QGroupBox("Registrar Nuevo Asistente")
        contenido.addWidget(formulario)
        # QGridLayout coloca los campos en filas y columnas.
        rejilla = QGridLayout(formulario)
        rejilla.setContentsMargins(15, 25, 15, 15)
        rejilla.setSpacing(12)
        self.campos = {}
        for indice, (campo, texto) in enumerate([
            ("nombre", "Nombre:"), ("apellidos", "Apellidos:"),
            ("correo", "Correo:"), ("categoria", "Categoría:"),
        ]):
            fila, pareja = divmod(indice, 2)
            etiqueta = QLabel(texto)
            rejilla.addWidget(etiqueta, fila, pareja * 2)
            if campo == "categoria":
                entrada = QComboBox()
                entrada.addItems(CATEGORIAS)
            else:
                entrada = QLineEdit()
            entrada.setObjectName(campo)
            etiqueta.setBuddy(entrada)
            self.campos[campo] = entrada
            rejilla.addWidget(entrada, fila, pareja * 2 + 1)
        rejilla.setColumnStretch(1, 1)
        rejilla.setColumnStretch(3, 1)
        self.boton_registrar = QPushButton("Registrar Entrada")
        self.boton_registrar.setObjectName("registrar")
        # Las señales de Qt conectan acciones del usuario con métodos Python.
        self.boton_registrar.clicked.connect(self.registrar_asistente)
        rejilla.addWidget(self.boton_registrar, 2, 0, 1, 4)

        filtros = QHBoxLayout()
        filtros.addWidget(QLabel("Buscar:"))
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Nombre, correo, categoría…")
        self.busqueda.setMaximumWidth(320)
        self.busqueda.textChanged.connect(self.actualizar_tabla)
        filtros.addWidget(self.busqueda)
        filtros.addStretch()
        self.total = QLabel()
        filtros.addWidget(self.total)
        contenido.addLayout(filtros)

        self.tabla = QTableWidget(0, len(CAMPOS))
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellidos", "Correo", "Categoría", "Hora de entrada"
        ])
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().hide()
        cabecera = self.tabla.horizontalHeader()
        cabecera.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        contenido.addWidget(self.tabla, 1)

        acciones = QHBoxLayout()
        self.boton_json = QPushButton("Ver JSON")
        self.boton_json.clicked.connect(self.ver_json)
        acciones.addWidget(self.boton_json)
        self.boton_exportar = QPushButton("Exportar JSON…")
        self.boton_exportar.clicked.connect(self.exportar)
        acciones.addWidget(self.boton_exportar)
        acciones.addStretch()
        contenido.addLayout(acciones)
        self.estado = QLabel(f"Guardado automático: {self.archivo.name}")
        self.estado.setWordWrap(True)
        contenido.addWidget(self.estado)
        self.setStyleSheet("""
            QWidget { font-size: 13px; color: #263746; }
            QMainWindow, QDialog { background: #ffffff; }
            QLabel#titulo { font-size: 24px; font-weight: bold; }
            QGroupBox { border: 1px solid #3498db; border-radius: 4px;
                        margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px;
                                color: #217dbb; padding: 0 5px; }
            QLineEdit, QComboBox { background: white; border: 1px solid #cbd5df;
                                    padding: 7px; border-radius: 3px; }
            QPushButton { background: #e8f2f8; border: 1px solid #b9d7ea;
                            padding: 9px 16px; border-radius: 3px; }
            QPushButton:hover { background: #d2e9f5; }
            QPushButton#registrar { background: #16a085; color: white;
                                    border: none; }
            QPushButton#registrar:hover { background: #138a72; }
            QHeaderView::section { background: #3498db; color: white;
                                    padding: 8px; border: none; }
            QTableWidget { background: white; alternate-background-color: #f0f6fa;
                            gridline-color: #e3e9ef; selection-background-color: #d3eafa;
                            selection-color: #182a38; }
            QPlainTextEdit { background: white; color: #263746; }
        """)
        self.actualizar_tabla()
        self.campos["nombre"].setFocus()

    def registrar_asistente(self):
        valores = {campo: self.campos[campo].text().strip()
                for campo in ("nombre", "apellidos", "correo")}
        valores["categoria"] = self.campos["categoria"].currentText()
        if not all(valores.values()):
            QMessageBox.warning(self, "Faltan datos", "Completa todos los campos.")
            return
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valores["correo"]):
            QMessageBox.warning(self, "Correo incorrecto", "Escribe un correo como nombre@ejemplo.com.")
            return
        persona = Persona(
            id=max((p.id for p in self.datos), default=0) + 1,
            nombre=valores["nombre"], apellidos=valores["apellidos"],
            correo=valores["correo"], categoria=valores["categoria"],
            hora_entrada=datetime.now().astimezone().isoformat(timespec="seconds"),
        )
        nuevos = self.datos + [persona]
        try:
            guardar_datos(self.archivo, nuevos)
        except OSError as error:
            QMessageBox.critical(self, "No se pudo guardar", str(error))
            return
        self.datos = nuevos
        for campo in ("nombre", "apellidos", "correo"):
            self.campos[campo].clear()
        self.campos["categoria"].setCurrentText("General")
        self.busqueda.clear()
        self.actualizar_tabla()
        self.estado.setText(f"Entrada de {persona.nombre} guardada en {self.archivo.name}.")
        self.campos["nombre"].setFocus()

    def actualizar_tabla(self):
        consulta = self.busqueda.text().strip().casefold()
        visibles = [p for p in self.datos
                    if consulta in " ".join(str(v) for v in p.a_fila()).casefold()]
        self.tabla.setRowCount(len(visibles))
        for fila, persona in enumerate(visibles):
            for columna, valor in enumerate(persona.a_fila()):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        self.total.setText(f"Total asistentes: {len(self.datos)} | Mostrados: {len(visibles)}")

    def ver_json(self):
        visor = QDialog(self)
        visor.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        visor.setWindowTitle("Datos guardados en JSON")
        visor.resize(760, 480)
        contenido = QVBoxLayout(visor)
        texto = QPlainTextEdit()
        texto.setReadOnly(True)
        texto.setPlainText(convertir_a_json(self.datos))
        contenido.addWidget(texto)
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        botones.rejected.connect(visor.close)
        contenido.addWidget(botones)
        visor.show()

    def exportar(self):
        dialogo = QFileDialog(self, "Exportar todos los asistentes")
        dialogo.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialogo.setNameFilter("Archivo JSON (*.json)")
        dialogo.setDefaultSuffix("json")
        dialogo.selectFile("asistentes_exportados.json")
        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return
        destino = Path(dialogo.selectedFiles()[0])
        try:
            guardar_datos(destino, self.datos)
        except OSError as error:
            QMessageBox.critical(self, "Error al exportar", str(error))
            return
        self.estado.setText(f"JSON exportado en: {destino}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    try:
        datos = cargar_datos(ARCHIVO)
    except (OSError, ValueError) as error:
        QMessageBox.critical(None, "No se pudo leer asistentes.json",
                    f"El archivo se conserva sin cambios.\n\n{error}")
        return 1
    ventana = ControlEventos(datos)
    ventana.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
