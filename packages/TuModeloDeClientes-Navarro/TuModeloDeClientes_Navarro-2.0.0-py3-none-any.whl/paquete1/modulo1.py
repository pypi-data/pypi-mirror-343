

class Cliente:
    def __init__(self, nombre, edad, email, gustos=None):
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.gustos = gustos
        if gustos is None:
            self.gustos = []

        self.carrito = []

    def __str__(self):
        return f"Cliente(nombre={self.nombre}, edad={self.edad}, email={self.email}, gustos={self.gustos}, carrito={self.carrito})"
    
    def agregar_al_carrito(self, producto, cantidad=1):#si no le pasan nada se le asigna 1 por defecto
        self.carrito.append({"producto": producto, "cantidad": cantidad})
        print(f"{self.nombre} agregó {cantidad} {producto}(s) al carrito.")

    def ver_carrito(self):
        if not self.carrito:
            print("🛒 El carrito está vacío.")
        else:
            print("🛒 Carrito actual:")
            for item in self.carrito:
                print(f"- {item['cantidad']} x {item['producto']}")

    def comprar(self, tienda):
        if not self.carrito:
            print(f"{self.nombre} no tiene productos en el carrito para comprar.")
        else:
            print(f"{self.nombre} ha comprado los siguientes productos en {tienda}:")
            for item in self.carrito:
                print(f"- {item['cantidad']} x {item['producto']}")
            self.carrito.clear()







class ClientePremium(Cliente):
    def __init__(self, nombre, edad, email, gustos=None, descuento=0.1):
        super().__init__(nombre, edad, email, gustos)
        self.descuento = descuento

    def comprar(self, tienda, precio):
        if not self.carrito:
            print(f"{self.nombre} no tiene productos en el carrito para comprar.")
        else:
            total = sum(item["cantidad"] for item in self.carrito) * precio
            total_con_descuento = total - (total * self.descuento)
            print(f"{self.nombre} ha comprado los siguientes productos en {tienda}:")
            for item in self.carrito:
                print(f"- {item['cantidad']} x {item['producto']}")
            print(f"Total a pagar (con descuento del {self.descuento * 100}%): ${total_con_descuento:.2f}")
            self.carrito.clear()

        