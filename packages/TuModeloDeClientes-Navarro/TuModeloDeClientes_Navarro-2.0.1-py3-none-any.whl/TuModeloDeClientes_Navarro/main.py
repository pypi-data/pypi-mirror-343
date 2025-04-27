from paquete1.modulo1 import Cliente, ClientePremium
from paquete1.modulo2 import menu



def gestionar_cliente():#aca podemos harcodear un cliente para hacer pruebas

    cliente1 = Cliente("Juan", 24, "juan@hotmail.com", "netbook, tecnologia")
    cliente1.agregar_al_carrito("libro", 2)
    cliente1.ver_carrito()
    cliente1.comprar("Amazon")
    print(cliente1)

def gestionar_cliente_premium():#aca podemos harcodear un cliente premium para hacer pruebas
    cliente_premium = ClientePremium("Maria", 30, "maria@hotmail.com", "ropa, comida", 0.2)
    cliente_premium.agregar_al_carrito("zapatos", 1)
    cliente_premium.ver_carrito()
    cliente_premium.comprar("eBay", 300)
    print(cliente_premium)



def main():# o menu_pruebas
    while True:
        print("--------------------------")
        print("--- MENÚ DE PRUEBAS ---")
        print("--------------------------")
        print("1. Gestionar Cliente")
        print("2. Gestionar Usuarios")
        print("3. Cliente Premium")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_cliente()
        elif opcion == "2":
            menu()#los usuarios son tratados como clientes
        elif opcion == "3":
            gestionar_cliente_premium()
        elif opcion == "4":
            print("👋 Saliendo...")
            break
        else:
            print("❌⚠️ Opción inválida. Intente nuevamente.❌⚠️")

# Ejecutar
main()
