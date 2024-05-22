def mostrar_pedidos(self):
        respuesta = ""
        if not self.pedidos:
            return "No hay pedidos."
        for pedido in self.pedidos:
            respuesta += str(pedido) + "\n"
        respuesta += f"Total de pedidos: ${self.calcular_total_pedidos():.2f}\n"
        return respuesta