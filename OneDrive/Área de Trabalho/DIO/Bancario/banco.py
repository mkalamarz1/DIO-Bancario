from datetime import datetime

def ler_numero(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número.")

def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um inteiro.")

def listar_clientes():
    print("\n=== LISTA DE CLIENTES ===")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for cliente in clientes:
        print(f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Contas: {len(cliente.contas)}")

def listar_contas():
    print("\n=== LISTA DE CONTAS ===")
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for numero in sorted(contas_dict.keys()):
        conta = contas_dict[numero]
        print(f"Nº {numero} ({conta.agencia}) - {conta.cliente.nome} | Saldo: R$ {conta.saldo:.2f}")

# ===== TRANSACOES =====
class Transacao:
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ===== HISTORICO =====
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })


# ===== CONTA =====
class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente!")
            return False
        elif valor <= 0:
            print("Valor inválido!")
            return False

        self.saldo -= valor
        print("Saque realizado!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido!")
            return False

        self.saldo += valor
        print("Depósito realizado!")
        return True


# ===== CLIENTE =====
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# ===== PESSOA FISICA =====
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ===== SISTEMA =====
clientes = []
contas = []

clientes_dict = {}
contas_dict = {}


def criar_cliente():
    cpf = input("CPF: ")
    if buscar_cliente(cpf):
        print("CPF já cadastrado!")
        return
    nome = input("Nome: ")
    data = input("Data de nascimento: ")
    endereco = input("Endereço: ")

    cliente = PessoaFisica(nome, cpf, data, endereco)
    clientes.append(cliente)
    clientes_dict[cpf] = cliente

    print("Cliente criado!")


def buscar_cliente(cpf):
    return clientes_dict.get(cpf)


def criar_conta():
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(cpf)

    if cliente:
        numero = len(contas) + 1
        conta = Conta(numero, cliente)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        contas_dict[numero] = conta
        print("Conta criada!")
    else:
        print("Cliente não encontrado!")


def depositar():
    numero = ler_inteiro("Número da conta: ")
    valor = ler_numero("Valor do depósito: ")

    conta = contas_dict.get(numero)
    if not conta:
        print("Conta não encontrada!")
        return
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)


def sacar():
    numero = ler_inteiro("Número da conta: ")
    valor = ler_numero("Valor do saque: ")

    conta = contas_dict.get(numero)
    if not conta:
        print("Conta não encontrada!")
        return
    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)


def extrato():
    numero = ler_inteiro("Número da conta: ")

    conta = contas_dict.get(numero)
    if not conta:
        print("Conta não encontrada!")
        return
    print("\n=== EXTRATO ===")
    print(f"Agência/Conta: {conta.agencia}/{conta.numero}")
    print(f"Titular: {conta.cliente.nome}")
    for t in conta.historico.transacoes:
        print(f"{t['tipo']}: R$ {t['valor']:.2f} em {t['data']}")
    print(f"Saldo: R$ {conta.saldo:.2f}")


def menu():
    while True:
        print("""
1 - Criar cliente
2 - Criar conta
3 - Depositar
4 - Sacar
5 - Extrato
6 - Listar clientes
7 - Listar contas
0 - Sair
        """)

        opcao = input("Escolha: ")

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            extrato()
        elif opcao == "6":
            listar_clientes()
        elif opcao == "7":
            listar_contas()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


menu()
