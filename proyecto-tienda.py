# Importación de los widgets necesarios de PySide6
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QGridLayout, QMessageBox, QScrollArea, QLineEdit,
    QSpinBox, QHBoxLayout
)

# Importación del validador para campos numéricos decimales
from PySide6.QtGui import QDoubleValidator

# Módulo para interactuar con argumentos del sistema y cerrar la app
import sys


# Clase Menu: representa la ventana del menú de productos
class Menu(QWidget):
    def __init__(self, parent=None):  # Constructor de la clase Menu
        super().__init__(parent)  # Llama al constructor del QWidget padre
        self.setWindowTitle("Menú de la tienda")  # Título de la ventana
        self.resize(500, 500)  # Tamaño inicial de la ventana

        layout = QVBoxLayout()  # Crea un layout vertical para organizar los widgets

        self.label_menu = QLabel("Productos")  # Etiqueta principal
        self.label_menu.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")  # Estilo
        layout.addWidget(self.label_menu)  # Añade la etiqueta al layout

        self.search_input = QLineEdit()  # Campo de texto para buscar productos
        self.search_input.setPlaceholderText("Buscar producto...")  # Texto de ayuda
        self.search_input.textChanged.connect(self.filtrar_productos)  # Filtra al escribir
        layout.addWidget(self.search_input)  # Añade el buscador al layout

        # Lista de productos con sus precios
        self.menu_items = [
            ("Pachito", 2500), ("Pachito de queso", 3000), ("Bolo", 100), ("Barrilete", 300),
            ("Bianchi", 100), ("Jabón líder", 2400), ("Jabón oro", 2000), ("Pan coco", 500),
            ("Galleta choco", 1500), ("Refresco cola", 1200), ("Empanada pollo", 3500),
            ("Arepa queso", 2000), ("Café", 1800), ("Té", 1500), ("Torta de chocolate", 4500),
            ("Sándwich", 3200), ("Hamburguesa", 5000), ("Papas fritas", 2500),
            ("Jugo natural", 2200), ("Helado", 3000), ("Pizza", 6000), ("Hot Dog", 3500),
            ("Churros", 2700), ("Empanada carne", 3400), ("Arepa huevo", 2300),
            ("Croissant", 2800), ("Tostadas", 2600), ("Muffin", 2400),
            ("Brownie", 3100), ("Batido", 2900)
        ]

        self.estado_seleccion = {}  # Almacena cada spinbox de producto
        self.cantidades = {}  # Guarda las cantidades elegidas
        self.total_pedido = 0  # Total del pedido inicializado en cero

        self.scroll_area = QScrollArea()  # Área con scroll para productos
        self.scroll_widget = QWidget()  # Widget que contendrá los productos
        self.grid_layout = QGridLayout(self.scroll_widget)  # Layout de grilla para colocar productos

        self.actualizar_productos()  # Llama a la función para mostrar productos

        self.scroll_widget.setLayout(self.grid_layout)  # Establece el layout del widget
        self.scroll_area.setWidget(self.scroll_widget)  # Inserta el widget en la scroll area
        self.scroll_area.setWidgetResizable(True)  # Permite que el área sea redimensionable
        layout.addWidget(self.scroll_area)  # Añade la scroll area al layout principal

        self.btn_pedido = QPushButton("Realizar Pedido")  # Botón para procesar el pedido
        self.btn_pedido.clicked.connect(self.mostrar_pedido)  # Conecta a la función que muestra el pedido
        layout.addWidget(self.btn_pedido)  # Añade botón al layout

        self.btn_limpiar = QPushButton("Limpiar Selección")  # Botón para borrar selección
        self.btn_limpiar.clicked.connect(self.limpiar_seleccion)  # Conecta al método limpiar
        layout.addWidget(self.btn_limpiar)  # Añade botón al layout

        self.label_pago = QLabel("Ingrese el dinero recibido:")  # Etiqueta del campo de pago
        layout.addWidget(self.label_pago)  # Añade etiqueta al layout

        self.input_pago = QLineEdit()  # Campo para ingresar dinero recibido
        self.input_pago.setValidator(QDoubleValidator(0.0, 999999.0, 2))  # Solo permite números válidos
        layout.addWidget(self.input_pago)  # Añade campo al layout

        self.btn_calcular_vuelta = QPushButton("Calcular Vuelta")  # Botón para calcular el cambio
        self.btn_calcular_vuelta.clicked.connect(self.calcular_vuelta)  # Conecta a la función de cálculo
        layout.addWidget(self.btn_calcular_vuelta)  # Añade botón al layout

        self.setLayout(layout)  # Establece el layout como principal del widget

    def actualizar_productos(self, filtro=""):  # Actualiza los productos en pantalla, opcionalmente filtra
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)  # Elimina widgets anteriores del layout

        for i, (producto, precio) in enumerate(self.menu_items):  # Itera por todos los productos
            if filtro.lower() in producto.lower():  # Si el producto coincide con el filtro (búsqueda)
                label = QLabel(f"{producto} - ${precio:,.0f}".replace(",", "."))  # Muestra nombre y precio
                spin_box = QSpinBox()  # Crea un selector de cantidad
                spin_box.setRange(0, 10)  # Cantidades entre 0 y 10
                spin_box.setValue(self.cantidades.get(producto, 0))  # Establece cantidad previa si existe
                spin_box.valueChanged.connect(lambda value, p=producto: self.guardar_cantidad(p, value))  # Guarda cantidad al cambiar

                self.grid_layout.addWidget(label, i, 0)  # Coloca el nombre
                self.grid_layout.addWidget(spin_box, i, 1)  # Coloca el spinbox
                self.estado_seleccion[producto] = spin_box  # Guarda referencia al spinbox

    def guardar_cantidad(self, producto, cantidad):  # Guarda cuántos se eligieron de cada producto
        self.cantidades[producto] = cantidad

    def limpiar_seleccion(self):  # Restaura todos los spinbox a 0
        for producto in self.estado_seleccion:
            self.estado_seleccion[producto].setValue(0)  # Reinicia a 0
        self.cantidades.clear()  # Limpia el diccionario de cantidades
        self.total_pedido = 0  # Reinicia total

    def filtrar_productos(self):  # Filtra los productos usando el texto ingresado
        filtro = self.search_input.text()  # Obtiene el texto actual del buscador
        self.actualizar_productos(filtro)  # Actualiza lista de productos filtrados

    def calcular_total_pedido(self):  # Calcula el total del pedido sumando precio * cantidad
        self.total_pedido = sum(
            cantidad * precio for producto, cantidad in self.cantidades.items()
            for p, precio in self.menu_items if p == producto
        )

    def mostrar_pedido(self):  # Muestra los productos seleccionados y el total
        self.calcular_total_pedido()  # Calcula el total actual
        pedido = []  # Lista para líneas del resumen

        for producto, cantidad in self.cantidades.items():  # Itera por productos seleccionados
            if cantidad > 0:
                precio = next(p[1] for p in self.menu_items if p[0] == producto)
                subtotal = precio * cantidad
                pedido.append(f"{producto} x{cantidad} - ${subtotal:,.0f}".replace(",", "."))  # Agrega línea del producto

        if not pedido:
            QMessageBox.warning(self, "Pedido vacío", "No has seleccionado ningún producto.")  # Alerta si está vacío
            return

        mensaje_pedido = "\n".join(pedido)  # Combina todo en una sola cadena
        QMessageBox.information(self, "Pedido Realizado",  # Muestra el resumen
            f"Has pedido:\n{mensaje_pedido}\n\nTotal a pagar: ${self.total_pedido:,.0f}".replace(",", "."))

    def calcular_vuelta(self):  # Calcula el cambio a devolver al cliente
        self.calcular_total_pedido()  # Asegura que el total esté actualizado
        try:
            dinero_recibido = float(self.input_pago.text())  # Toma el valor ingresado
            if dinero_recibido < self.total_pedido:
                QMessageBox.warning(self, "Pago insuficiente", "El dinero recibido es menor al total a pagar.")  # Si es insuficiente
            else:
                vuelta = dinero_recibido - self.total_pedido  # Resta el total al dinero recibido
                QMessageBox.information(self, "Vuelta", f"El cambio a devolver es: ${vuelta:,.0f}".replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Entrada inválida", "Por favor, ingrese un valor numérico válido.")  # Error si no es número


# Clase MainWindow: representa la ventana principal de bienvenida
class MainWindow(QMainWindow):
    def __init__(self):  # Constructor de la ventana principal
        super().__init__()  # Inicializa la QMainWindow
        self.setWindowTitle("TIENDA - Bienvenido")  # Título de la ventana
        self.resize(600, 400)  # Tamaño inicial

        layout = QVBoxLayout()  # Layout principal

        self.label_bienvenida = QLabel("¡Bienvenido a la tienda de Heli!")  # Mensaje de bienvenida
        self.label_bienvenida.setStyleSheet("font-size: 29px; font-weight: bold;")  # Estilo
        layout.addWidget(self.label_bienvenida)  # Añade etiqueta al layout

        self.btn_menu = QPushButton("Ver Menú")  # Botón para abrir el menú
        self.btn_menu.clicked.connect(self.abrir_menu)  # Conecta al método abrir_menu
        layout.addWidget(self.btn_menu)  # Añade botón al layout

        container = QWidget()  # Crea contenedor principal
        container.setLayout(layout)  # Asigna el layout al contenedor
        self.setCentralWidget(container)  # Establece el contenedor como central

        self.menu_window = None  # Almacena la instancia de la ventana del menú

    def abrir_menu(self):  # Abre la ventana del menú si no está abierta
        if self.menu_window is None or not self.menu_window.isVisible():
            self.menu_window = Menu(self)  # Crea nueva ventana de menú
            self.menu_window.show()  # La muestra


# Punto de entrada del programa
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea la aplicación Qt
    window = MainWindow()  # Instancia la ventana principal
    window.show()  # Muestra la ventana
    sys.exit(app.exec())  # Ejecuta el bucle principal y espera cierre
