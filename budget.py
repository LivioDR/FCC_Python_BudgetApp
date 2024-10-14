class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def check_funds(self, amount):
        balance = 0
        for items in self.ledger:
            balance += items["amount"]
        if (amount > balance):
            return False
        else:
            return True

    def withdraw(self, amount, description=""):
        if (self.check_funds(amount)):
            amount = -amount
            self.ledger.append({"amount": amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for items in self.ledger:
            balance += items["amount"]
        return balance

    def transfer(self, amount, category):
        if (self.check_funds(amount)):
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False

    def __str__(self):

        # Creo el string final para ir incorporando cada item
        string_final = ""

        # Creo el string de categoria
        titulo = ""
        largo = len(self.category)
        largo_asteriscos = int(15 - largo / 2)
        titulo += "*" * largo_asteriscos
        titulo = titulo + str(self.category) + titulo

        # Agrego el título al string final
        string_final = titulo

        # Creo ahora el string para cada item y a la par voy sumando el total
        total = 0.0
        for items in self.ledger:
            # Creo la columna izq de 23 caracteres para la descripcion
            count_descr = len(items['description'])
            if count_descr > 23:
                descr_final = items['description'][0:23]
            else:
                descr_final = items['description'] + " " * (23 - count_descr)

            # Creo una variable string para manipular el monto de la columna derecha
            text_amount = str(items['amount'] * 1.00)
            count_price = len(text_amount)

            # Corrijo problema de ceros en el string
            if text_amount[count_price - 1] == "0":
                if text_amount[count_price - 2] == ".":
                    text_amount += "0"
                    count_price += 1

            # Chequeo cant de caracteres del monto y lo ajusto a 7 right-justified
            if count_price > 7:
                price_final = text_amount[0:7]
            else:
                price_final = " " * (7 - count_price) + text_amount

            # Sumo el monto del item al monto final
            total += items['amount']

            # Creo la linea del item y la agrego al string que se va a retornar
            line_item = descr_final + price_final
            string_final += "\n" + line_item
        # Una vez creados el titulo y los items, creo la linea del total y la devuelvo
        string_final += "\n" + "Total: " + str(total)

        return string_final


def create_spend_chart(categories):

    final_string = "Percentage spent by category" + "\n"

    number_of_categories = len(categories)

    spenditure = []
    aux_spend = 0.0
    categ_name = []

    # Cargo los nombres de las categorias y sus respectivos gastos
    for items in categories:
        categ_name.append(items.category)
        for amounts in items.ledger:
            if amounts['amount'] < 0:
                aux_spend += amounts["amount"]
        spenditure.append(aux_spend)
        aux_spend = 0

    # Calculo el gasto total y el porcentaje por categoria redondeado al 10% mas cercano
    gasto_total = 0.0
    for gastos in spenditure:
        gasto_total += gastos

    percentage = []
    for gastos in spenditure:
        percentage.append(gastos / gasto_total * 100)

    # Comienzo ahora a armar cada renglon de valores y luego armare la referencia
    valores = []
    aux_valores = ""
    max = 100
    while max >= 0:
        for valor_categoria in percentage:
            if valor_categoria >= max:
                aux_valores += " o "
            else:
                aux_valores += "   "
        max -= 10
        valores.append(aux_valores)
        aux_valores = ""

    # Creo ahora el eje y le voy incorporando cada valor segun corresponda
    maximo = 100
    eje_y_valores = ""
    for numeros in valores:
        if maximo == 100:
            eje_y_valores += str(maximo) + "|" + numeros + ' \n'
            maximo -= 10
        elif maximo == 0:
            eje_y_valores += "  " + str(maximo) + "|" + numeros + ' \n'
            maximo -= 10
        else:
            eje_y_valores += " " + str(maximo) + "|" + numeros + ' \n'
            maximo -= 10

    # Incorporo el gráfico al string final antes de crear las categorias
    final_string += eje_y_valores

    # Creo ahora el eje horizontal de guiones
    guiones = "---" * number_of_categories + "-"
    final_string += "    " + guiones + '\n'

    # Comienzo ahora a crear las categorías respetando los espacios
    # Creo una prueba para el caso en que el nombre sea más corto
    mas_largo = 0
    for names in categ_name:
        if len(names) > mas_largo:
            mas_largo = len(names)

    indice = 0

    while indice < mas_largo:
        final_string += "    "
        for names in categ_name:
            try:
                final_string += " " + names[indice] + " "
            except:
                final_string += "   "
        indice += 1
        if indice == mas_largo:
          final_string += " "
        else:
          final_string += ' \n'

    return final_string
