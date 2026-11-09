class Endereco:
    def __init__(self, cidade, cep):
        self._cidade = cidade
        self._cep = cep

    def cidade(self):
        return self._cidade

    def cep_valido(self):
        return len(self._cep) == 8 and self._cep.isdigit()

class Pessoa:
    def __init__(self, nome, endereco, cpf, email):
        self._nome = nome
        self._endereco = endereco
        self._cpf = cpf
        self._email = email

    def nome(self):
        return self._nome

    def cidade(self):
        return self._endereco.cidade()

    def cpf_valido(self):
        return len(self._cpf) == 11 and self._cpf.isdigit()

    def email_valido(self):
        return "@" in self._email and "." in self._email

    def cep_valido(self):
        return self._endereco.cep_valido()

    def descrever(self):
        return f"{self._nome} - {self.cidade()}"

class TipoNormal:
    def desconto_sobre(self, valor):
        return 0

class TipoVip:
    def desconto_sobre(self, valor):
        return valor * 0.10

class TipoFuncionario:
    def desconto_sobre(self, valor):
        return valor * 0.20

class Cliente:
    def __init__(self, pessoa, tipo):
        self._pessoa = pessoa
        self._tipo = tipo

    def descrever(self):
        return self._pessoa.descrever()

    def desconto_sobre(self, valor):
        return self._tipo.desconto_sobre(valor)

    def problema(self):
        if not self._pessoa.cpf_valido():
            return "cpf invalido"
        if not self._pessoa.email_valido():
            return "email invalido"
        if not self._pessoa.cep_valido():
            return "cep invalido"
        return ""

class Produto:
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def nome(self):
        return self._nome

    def preco(self):
        return self._preco

class StatusAberto:
    def nome(self):
        return "aberto"

    def pode_pagar(self):
        return True

    def pode_cancelar(self):
        return True

class StatusPago:
    def nome(self):
        return "pago"

    def pode_pagar(self):
        return False

    def pode_cancelar(self):
        return False

class StatusCancelado:
    def nome(self):
        return "cancelado"

    def pode_pagar(self):
        return False

    def pode_cancelar(self):
        return False

class Pedido:
    def __init__(self, numero, cliente, itens):
        self._numero = numero
        self._cliente = cliente
        self._itens = itens
        self._status = StatusAberto()

    def numero(self):
        return self._numero

    def tem_itens(self):
        return len(self._itens) > 0

    def total(self):
        total = 0
        for item in self._itens:
            total = total + item.preco()
        return total

    def desconto(self):
        return self._cliente.desconto_sobre(self.total())

    def a_pagar(self):
        return self.total() - self.desconto()

    def esta_aberto(self):
        return self._status.pode_cancelar()

    def esta_pago(self):
        return self._status.nome() == "pago"

    def esta_cancelado(self):
        return self._status.nome() == "cancelado"

    def pagar(self):
        if not self._status.pode_pagar():
            return False
        if not self.tem_itens():
            return False
        self._status = StatusPago()
        return True

    def cancelar(self):
        if not self._status.pode_cancelar():
            return False
        self._status = StatusCancelado()
        return True

    def linhas_itens(self):
        contagem = {}
        ordem = []
        for item in self._itens:
            nome = item.nome()
            if nome not in contagem:
                contagem[nome] = [0, 0]
                ordem.append(nome)
            contagem[nome][0] = contagem[nome][0] + 1
            contagem[nome][1] = contagem[nome][1] + item.preco()
        linhas = []
        for nome in ordem:
            qtd = contagem[nome][0]
            soma = contagem[nome][1]
            linhas.append(f"  {qtd} x {nome} = R$ {soma:.2f}")
        return linhas

    def descrever(self):
        linhas = []
        linhas.append(f"Pedido {self._numero} - {self._cliente.descrever()}")
        linhas.append(f"  status: {self._status.nome()}")
        if self.esta_cancelado():
            return "\n".join(linhas)
        for linha in self.linhas_itens():
            linhas.append(linha)
        linhas.append(f"  total: R$ {self.total():.2f} | desconto: R$ {self.desconto():.2f} | a pagar: R$ {self.a_pagar():.2f}")
        return "\n".join(linhas)

def arrecadado(pedidos):
    total = 0
    for pedido in pedidos:
        total = total + valor_pago(pedido)
    return total

def valor_pago(pedido):
    if not pedido.esta_pago():
        return 0
    return pedido.a_pagar()

def qtd_abertos(pedidos):
    total = 0
    for pedido in pedidos:
        total = total + eh_aberto(pedido)
    return total

def eh_aberto(pedido):
    if not pedido.esta_aberto():
        return 0
    return 1

def tentar_criar(pedidos, numero, cliente, itens):
    problema = cliente.problema()
    if problema != "":
        print(f"pedido {numero} recusado: {problema}")
        return
    pedidos.append(Pedido(numero, cliente, itens))

# --- Roteiro final - Passo 9 ---
ana = Cliente(Pessoa("Ana Souza", Endereco("Sorocaba", "18000000"), "12345678901", "ana@email.com"), TipoVip())
bruno_cpf = Cliente(Pessoa("Bruno", Endereco("Atibaia", "12900000"), "123", "bruno@email.com"), TipoNormal())
carla_email = Cliente(Pessoa("Carla", Endereco("Atibaia", "12900000"), "12345678901", "carla-sem-arroba"), TipoVip())
diego = Cliente(Pessoa("Diego Rocha", Endereco("Itu", "13300000"), "12345678901", "diego@email.com"), TipoVip())
eva = Cliente(Pessoa("Eva Nunes", Endereco("Itu", "13300000"), "12345678901", "eva@email.com"), TipoFuncionario())
bruno_cep = Cliente(Pessoa("Bruno", Endereco("Atibaia", "123"), "12345678901", "bruno@email.com"), TipoNormal())
gil = Cliente(Pessoa("Gil Alves", Endereco("Sorocaba", "18000000"), "12345678901", "gil@email.com"), TipoNormal())

caderno = Produto("Caderno", 15.50)
caneta = Produto("Caneta", 2.50)
livro = Produto("Livro", 89.50)
fone = Produto("Fone", 60.00)

pedidos = []
tentar_criar(pedidos, 1, ana, [caderno, caderno, caneta, caneta, caneta, caneta, caneta])
tentar_criar(pedidos, 2, bruno_cpf, [livro])
tentar_criar(pedidos, 3, ana, [livro])
tentar_criar(pedidos, 4, carla_email, [fone])
tentar_criar(pedidos, 5, diego, [])
tentar_criar(pedidos, 6, eva, [fone])
tentar_criar(pedidos, 7, bruno_cep, [fone])
tentar_criar(pedidos, 8, gil, [fone, fone])

por_numero = {}
for pedido in pedidos:
    por_numero[pedido.numero()] = pedido

print(f"pagar 1: {por_numero[1].pagar()}")
print(f"pagar 3: {por_numero[3].pagar()}")
print(f"pagar 5: {por_numero[5].pagar()}")
print(f"pagar 6: {por_numero[6].pagar()}")
print(f"cancelar 5: {por_numero[5].cancelar()}")
print(f"cancelar 1: {por_numero[1].cancelar()}")

for pedido in pedidos:
    print(pedido.descrever())
print(f"arrecadado: R$ {arrecadado(pedidos):.2f}")
print(f"abertos: {qtd_abertos(pedidos)}")