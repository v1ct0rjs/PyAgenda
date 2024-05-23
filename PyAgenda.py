import os
import json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class Tarea:
    """
    Clase que representa una tarea pendiente.

    Atributos:
        descripcion (str): Descripción de la tarea.
        estado (bool): Indica si la tarea está completada (True) o pendiente (False).
        creado_en (str): Hora de creación de la tarea (formato ISO 8601).
        realizada_en (str): Hora de marcado como completada de la tarea (formato ISO 8601).
        fecha_realizar (str): Fecha y hora de cuando se debe realizar la tarea (formato ISO 8601).
    """

    def __init__(self, descripcion, fecha_realizar=None, creado_en=None, realizada_en=None):
        self.descripcion = descripcion
        self.estado = False
        self.creado_en = creado_en
        self.realizada_en = realizada_en
        self.fecha_realizar = fecha_realizar

    def __str__(self):
        estado_str = f"{Fore.RED}Pendiente{Style.RESET_ALL}" if not self.estado else f"{Fore.GREEN}Completada{Style.RESET_ALL}"
        return f"- {self.descripcion} ({estado_str}) - Realizar en: {Fore.BLUE}{self.fecha_realizar}{Style.RESET_ALL}"


class GestorTareas:
    """
    Clase que gestiona la lista de tareas pendientes.

    Atributos:
        tareas (list): Lista de objetos Tarea.
        archivo (str): Ruta del archivo JSON donde se guardan las tareas.
    """

    def __init__(self, archivo):
        self.tareas = []
        self.archivo = archivo

        try:
            self.cargar_tareas()
        except FileNotFoundError:
            pass

    def cargar_tareas(self):
        """Carga las tareas del archivo JSON."""
        with open(self.archivo, "r") as archivo:
            datos = json.load(archivo)
            for tarea_data in datos:
                tarea = Tarea(tarea_data["descripcion"], tarea_data["fecha_realizar"], tarea_data["creado_en"], tarea_data["realizada_en"])
                tarea.estado = tarea_data["estado"]
                self.tareas.append(tarea)

    def guardar_tareas(self):
        """Guarda las tareas en el archivo JSON."""
        datos = []
        for tarea in self.tareas:
            tarea_data = {
                "descripcion": tarea.descripcion,
                "estado": tarea.estado,
                "creado_en": tarea.creado_en,
                "realizada_en": tarea.realizada_en,
                "fecha_realizar": tarea.fecha_realizar
            }
            datos.append(tarea_data)

        with open(self.archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def agregar_tarea(self, descripcion):
        """Agrega una nueva tarea a la lista."""
        ahora = datetime.now().isoformat()
        fecha_realizar = input("Ingrese la fecha y hora de realizar la tarea: ")
        nueva_tarea = Tarea(descripcion, fecha_realizar, creado_en=ahora)
        self.tareas.append(nueva_tarea)
        self.guardar_tareas()

    def marcar_completada(self, posicion):
        """Marca una tarea como completada en la posición indicada."""
        try:
            tarea = self.tareas[posicion - 1]
            tarea.estado = True
            tarea.realizada_en = datetime.now().isoformat()
            self.guardar_tareas()
        except IndexError:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} La posición {posicion} no existe.")

    def mostrar_tareas(self):
        """Muestra todas las tareas en pantalla."""
        if not self.tareas:
            print("No hay tareas pendientes.")
            return

        for i, tarea in enumerate(self.tareas, start=1):
            print(f"{i}. {tarea}")

    def eliminar_tarea(self, posicion):
        """Elimina una tarea de la lista en la posición indicada."""
        try:
            del self.tareas[posicion - 1]
            self.guardar_tareas()
        except IndexError:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} La posición {posicion} no existe.")


def mostrar_portada():
    """Muestra la portada ASCII."""
    print(Fore.GREEN + """
 ____           _                        _       
|  _ \ _   _   / \   __ _  ___ _ __   __| | __ _ 
| |_) | | | | / _ \ / _` |/ _ \ '_ \ / _` |/ _` |
|  __/| |_| |/ ___ \ (_| |  __/ | | | (_| | (_| |
|_|    \__, /_/   \_\__, |\___|_| |_|\__,_|\__,_|
       |___/        |___/                        

                                                      """)

    print(Fore.CYAN + "          Realizado por Víctor Jiménez\n" + Style.RESET_ALL)

def main():
    """Función principal del programa."""
    os.system('clear')
    mostrar_portada()
    gestor = GestorTareas("tareas.json")

    while True:
        print("\nMenú:")
        print(f"{Fore.YELLOW}1. {Fore.BLUE}Agregar tarea")
        print(f"{Fore.YELLOW}2. {Fore.BLUE}Marcar como completada")
        print(f"{Fore.YELLOW}3. {Fore.BLUE}Mostrar tareas")
        print(f"{Fore.YELLOW}4. {Fore.BLUE}Eliminar tarea")
        print(f"{Fore.YELLOW}5. {Fore.BLUE}Salir{Style.RESET_ALL}")

        opcion = input(f"{Fore.YELLOW}Ingrese una opción: {Style.RESET_ALL}")

        os.system('clear')

        if opcion == "1":
            mostrar_portada()
            descripcion = input("Descripción de la tarea: ")
            gestor.agregar_tarea(descripcion)
        elif opcion == "2":
            mostrar_portada()
            gestor.mostrar_tareas()
            posicion = int(input("Ingrese la posición de la tarea a marcar: "))
            gestor.marcar_completada(posicion)
        elif opcion == "3":
            mostrar_portada()
            gestor.mostrar_tareas()
        elif opcion == "4":
            mostrar_portada()
            gestor.mostrar_tareas()
            posicion = int(input("Ingrese la posición de la tarea a eliminar: "))
            gestor.eliminar_tarea(posicion)
        elif opcion == "5":
            break
        else:
            print(f"{Fore.RED}Opción no válida.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

