import csv
import os

CSV = "catalogo.csv"

#validaciones 

def normalizar_titulo(t: str) -> str:
    return " ".join(t.strip().lower().split())

def titulo_valido(t: str)->bool:
    
    return normalizar_titulo(t) != ""


def pedir_titulo(msg: str) -> str:
    while True:
        titulo = input(msg).strip()
        if titulo_valido(titulo):
            return " ".join(titulo.strip().split())
        print(" Título inválido. Intente nuevamente.")

def pedir_entero_no_negativo(msg: str) -> int:
    while True:
        valor = input(msg).strip()
        if valor.isdigit():
            numero = int(valor)
            if numero >= 0:
                return numero
        print("Ingrese un número entero mayor o igual a 0.")



#PERSISTENCIA EN EL CSV

def cargar_catalogo_desde_csv() -> list[dict]:
    catalogo = []
    if not os.path.exists(CSV):
        return catalogo
    with open(CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                titulo = fila["TITULO"].strip()
                cantidad = int(fila["CANTIDAD"])
                catalogo.append({"TITULO": titulo, "CANTIDAD": cantidad})
            except (KeyError, ValueError):
                continue
    return catalogo


def guardar_catalogo_a_csv(catalogo: list[dict]) -> None:
    with open(CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["TITULO", "CANTIDAD"])
        writer.writeheader()
        writer.writerows(catalogo)


#BUSQUEDAS Y REGLAS DEL NEGOCIO

def buscar_indice_por_titulo(catalogo: list[dict], titulo_busqueda: str) -> int:
    titulo_norm = normalizar_titulo(titulo_busqueda)
    for i, libro in enumerate(catalogo):
        if normalizar_titulo(libro["TITULO"]) == titulo_norm:
            return i
    return -1

def existe_titulo(catalogo: list[dict], titulo: str) -> bool:
    return buscar_indice_por_titulo(catalogo, titulo) != -1

#OPERACIONES PRINCIPALES

def ingresar_titulos(catalogo: list[dict]) -> list[dict]:
    n = pedir_entero_no_negativo("¿Cuántos títulos desea ingresar? ")
    for i in range(n):
        while True:
            titulo = pedir_titulo("Título: ")
            if not existe_titulo(catalogo, titulo):
                break
            print("Ese título ya existe.")
        cantidad = pedir_entero_no_negativo("Cantidad de ejemplares: ")
        catalogo.append({"TITULO": titulo, "CANTIDAD": cantidad})
    guardar_catalogo_a_csv(catalogo)
    print(" Títulos agregados correctamente.")
    return catalogo


def mostrar_catalogo(catalogo: list[dict]) -> None:
    if not catalogo:
        print("El catálogo está vacío.")
        return
    print("\nCATÁLOGO COMPLETO:")
    for libro in catalogo:
        print(f"- {libro['TITULO']} ({libro['CANTIDAD']} ejemplares)")


def ingresar_ejemplares(catalogo: list[dict]) -> list[dict]:
    titulo = pedir_titulo("Título al que agregar ejemplares: ")
    indice = buscar_indice_por_titulo(catalogo, titulo)
    if indice == -1:
        print(" Título no encontrado.")
        return catalogo
    cantidad = pedir_entero_no_negativo("Cantidad a agregar: ")
    catalogo[indice]["CANTIDAD"] += cantidad
    guardar_catalogo_a_csv(catalogo)
    print(" Ejemplares actualizados.")
    return catalogo

def consultar_disponibilidad(catalogo: list[dict]) -> None:
    titulo = pedir_titulo("Ingrese el título a consultar: ")
    indice = buscar_indice_por_titulo(catalogo, titulo)
    if indice == -1:
        print(" Título no encontrado.")
    else:
        print(f"El libro: {catalogo[indice]['TITULO']}, tiene  {catalogo[indice]['CANTIDAD']} ejemplares disponibles.")

def listar_agotados(catalogo: list[dict]) -> None:
    agotados = [lib for lib in catalogo if lib["CANTIDAD"] == 0]
    if not agotados:
        print(" No hay títulos agotados.")
    else:
        print(" Títulos agotados:")
        for libro in agotados:
            print(f"- {libro['TITULO']}")

def agregar_titulo(catalogo: list[dict]) -> list[dict]:
    titulo = pedir_titulo("Título nuevo: ")
    if existe_titulo(catalogo, titulo):
        print(" El título ya existe.")
        return catalogo
    cantidad = pedir_entero_no_negativo("Cantidad inicial: ")
    catalogo.append({"TITULO": titulo, "CANTIDAD": cantidad})
    guardar_catalogo_a_csv(catalogo)
    print(" Título agregado.")
    return catalogo

def actualizar_ejemplares_prestamo_devolucion(catalogo: list[dict]) -> list[dict]:
    titulo = pedir_titulo("Título: ")
    indice = buscar_indice_por_titulo(catalogo, titulo)
    if indice == -1:
        print(" No se encontró el título.")
        return catalogo

    accion = input("¿Préstamo (P) o Devolución (D)? ").strip().lower()
    if accion == "p":
        if catalogo[indice]["CANTIDAD"] > 0:
            catalogo[indice]["CANTIDAD"] -= 1
            print(" Préstamo registrado.")
        else:
            print(" No hay ejemplares disponibles.")
    elif accion == "d":
        catalogo[indice]["CANTIDAD"] += 1
        print(" Devolución registrada.")
    else:
        print(" Opción inválida.")

    guardar_catalogo_a_csv(catalogo)
    return catalogo





#MENU

def mostrar_menu() -> None:
    print("1 - Ingresar títulos (múltiples)")
    print("2 - Ingresar ejemplares")
    print("3 - Mostrar catálogo" )
    print("4 - Consultar disponibilidad" )
    print("5 - Listar agotados")
    print("6 - Agregar título" )
    print("7 - Actualizar ejemplares (Préstamo/Devolución)" )
    print("8 - Salir")


def main() -> None:
    print(" Iniciando sistema de Biblioteca…")
    catalogo: list[dict] = cargar_catalogo_desde_csv()
    if len(catalogo) == 0:
        print("Catálogo vacío o CSV no encontrado.")
    else:
        print(f"Catálogo cargado. {len(catalogo)} título(s).")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                catalogo = ingresar_titulos(catalogo)
            case "2":
                catalogo = ingresar_ejemplares(catalogo)
            case "3":
                mostrar_catalogo(catalogo)
            case "4":
                consultar_disponibilidad(catalogo)
            case "5":
                listar_agotados(catalogo)
            case "6":
                catalogo = agregar_titulo(catalogo)
            case "7":
                catalogo = actualizar_ejemplares_prestamo_devolucion(catalogo)
            case "8":
                print(" Saliendo. ¡Hasta luego!")
                break
            case _:
                print(" Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()





