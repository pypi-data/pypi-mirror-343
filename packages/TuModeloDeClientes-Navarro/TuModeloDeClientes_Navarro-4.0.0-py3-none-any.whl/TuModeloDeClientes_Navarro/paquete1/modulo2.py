# Autor: [Juan Navarro]
# Fecha de entrega: [lunes 14 de abril de 2025]

from .modulo1 import Cliente

USUARIOS = {}

def pausa():
    input("Precione ENTER para continuar...")

def salir():
    print("👋 Saliendo...")
    exit()

#funcion registrar usuario

def registrar_usuario():
    print("--------------------")
    print("Registro de Usuario")
    print("--------------------")
    nombre = input("Ingrese su nombre de usuario: ").strip()#saca los espacios en blanco al principio y al final
    if nombre == "":
        print("❌ El nombre de usuario no puede estar vacío.")
        pausa()
        return
    if nombre in USUARIOS:
        print("❌ El nombre de usuario ya existe. Intente con otro.")
        pausa()
        return

    password = input("Ingrese su contraseña: ").strip()
    if password == "":
        print("❌ La contraseña no puede estar vacía.")
        pausa()
        return

    USUARIOS[nombre] = password
    print("✅ Usuario registrado con éxito.")
    pausa()


#funcion para mostrar todos los usuarios registrados

def mostrar_usuarios():
    print("--------------------")
    print("Usuarios Registrados")
    print("--------------------")
    if not USUARIOS:
        print("No hay usuarios registrados.")
    else:
        for usuario in USUARIOS:
            print(f"👤Usuario: {usuario}")
    pausa()


#funcion login

def login():
    print("--------------------")
    print("Iniciar Sesión")
    print("--------------------")
    nombre = input("Ingrese su nombre de usuario: ")
    if nombre not in USUARIOS:
        print("❌ Usuario no encontrado.")
        pausa()
        return None
    password = input("Ingrese su contraseña: ")
    if USUARIOS[nombre] == password:
        print("✅Inicio de sesión exitoso.")
        pausa()
        return nombre  
    else:
        print("❌ Contraseña incorrecta.")
        pausa()
        return None

#funcion para mostrar el menu de opciones
def menu():
    while True:
        print("--------------------------")
        print("---   MENÚ PRINCIPAL   ---")
        print("--------------------------")
        print("1. Registrar Usuario")
        print("2. Mostrar Usuarios Registrados")
        print("3. Iniciar Sesión")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            usuario_logueado = login()
            if usuario_logueado:
                menu_cliente(usuario_logueado)
        elif opcion == "4":
            salir()
        else:
            print("❌⚠️ Opción inválida. Intente nuevamente.❌⚠️")





def menu_cliente(nombre_usuario):
    print(f"🙋‍ Bienvenido {nombre_usuario}!")
    edad = int(input("Ingrese su edad: "))
    email = input("Ingrese su email: ")
    gustos = input("Ingrese sus gustos separados por coma (ejemplo: ropa , comida, tecnologia): ")
    print(gustos)
    cliente = Cliente(nombre_usuario, edad, email, gustos)
    #.SPLIT() separa los gustos por comas y los convierte en una lista


    while True:
        print("--------------------------")
        print("--- 🙋‍ MENÚ CLIENTE   ---")
        print("--------------------------")
        print("1. Agregar al carrito 🛒")
        print("2. Ver carrito 🛒")
        print("3. Comprar")
        print("4. Cerrar sesión")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            producto = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad: "))
            cliente.agregar_al_carrito(producto, cantidad)
        elif opcion == "2":
            cliente.ver_carrito()
        elif opcion == "3":
            tienda = input("Ingrese el nombre de la tienda: ")
            cliente.comprar(tienda)
        elif opcion == "4":
            print("👋 Cerrando sesión...")
            break
        elif opcion == "5":
            salir()
        else:
            print("❌⚠️ Opción inválida. Intente nuevamente.❌⚠️")



#condicion especial de python para que no se ejecute el modulo si no es llamado desde otro modulo
#asi no me molesta en el menu de pruebas
if __name__ == "__main__":
    menu()
