import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Customer:
  def __init__ (self, address):
    self.address = address
    self.accounts = []

  def do_transaction (self, account, transaction):
    transaction.register(account)

  def add_account (self, account):
    self.accounts.append(account)

class PhysicalPerson (Customer):
  def __init__ (self, name, birth_date, cpf, address):
    super().__init__(address)
    self.name = name
    self.birth_date = birth_date
    self.cpf = cpf

class Account:
  def __init__ (self, number, customer):
    self._balance = 0
    self._number = number
    self._agency = "0001"
    self._customer = customer
    self._historic = Historic()

  @classmethod
  def new_account (cls, customer, number):
    return cls (number, customer)

  @property
  def balance (self):
    return self._balance
  
  @property
  def number (self):
    return self._number
  
  @property
  def agency (self):
    return self._agency
  
  @property
  def historic (self):
    return self._historic
  
  def draft (self, value):
    try:
      balance = self.balance
      exceeded_balance = value > balance

      if exceeded_balance:
        print('\n Operação falhou! Não possui saldo o suficiente para realizar esta operação')
      elif value > 0:
        self._balance -= value
        print("\n Saque realizado com sucesso!")
        return True
      else:
        print("\n Operação falhou! O valor informado é inválido! ")

      return False
    except Exception as error:
      print(error)

  def deposit (self, value):
    try:
      if value > 0:
        self._balance += value
        print("\n Depósito realizado com sucesso!")
      else:
        print("\n Operação falhou! Valor de depósito deve ser positivo")
        return False
      
      return True

    except Exception as error:
      print(error)
    
class CheckingAccount (Account):
  def __init__(self, number, customer, limit=500, draft_limit=3):
    super().__init__(number, customer)
    self.limit = limit
    self.draft_limit = draft_limit
  
  def draft (self, value):
    try:
      draft_count = len([transaction for transaction in self.historic.transactions if transaction['type'] == Draft.__name__ ])
      exceeded_limit = value > self.limit
      exceeded_draft = draft_count > self.draft_limit

      if exceeded_limit:
        print(f'\n Operação falhou! O valor do saque excede o limite de {self.limit} reais por dia')
      elif exceeded_draft:
        print(f'\n Operação falhou! O número de saques por dia excede o limite de {self.limit} saques  por dia')
      else:
        return super().draft(value)
      
      return False

    except Exception as error:
      print(error)

  def __str__(self):
      return f"""\
          Agência:\t{self.agency}
          C/C:\t\t{self.number}
          Titular:\t{self._customer.name}
      """
  
class Historic:
  def __init__ (self):
    self._transactions = []

  @property
  def transactions (self):
    return self._transactions

  def add_transaction (self, transaction):
    self.transactions.append({
      'date': datetime.now(),
      'type': transaction.__class__.__name__,
      'value': transaction.value
    })

class Transaction (ABC):
  @property
  @abstractproperty
  def value(self):
      pass

  @abstractclassmethod
  def register(self, account):
    pass


class Draft (Transaction):
  def __init__ (self, value):
    self._value = value

  @property
  def value (self):
    return self._value
  
  def register (self, account):
    transaction_success = account.draft(self.value)

    if transaction_success:
      account.historic.add_transaction(self)

class Deposit (Transaction):
  def __init__ (self, value):
    self._value = value
    
  @property
  def value (self):
    return self._value
  
  def register (self, account):
    transaction_success = account.deposit(self.value)
    if transaction_success:
      account.historic.add_transaction(self)


def menu ():
  menu = """
    =================================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair 
    =================================
    """
  return input(textwrap.dedent(menu))

def filter_customer (cpf, customers):
  try:
    filtered_customers = [customer for customer in customers if customer.cpf == cpf]
  
    return filtered_customers[0] if filtered_customers else None
  except Exception as error:
      print(error)

def get_customer_account (customer):
  if not customer.accounts:
    print('\n Cliente não possui conta')
    return
  
  return customer.accounts[0]


def deposit (customers):
  try:
    cpf = input("Informe o CPF do cliente: ")
    customer = filter_customer(cpf, customers)

    if not customer:
      print("\n Cliente não encontrado! ")
      return
    
    value = float(input("Informe o valor do depósito: "))
    transaction = Deposit(value)
    account = get_customer_account(customer)

    if not account:
      return
    
    customer.do_transaction(account, transaction)
  except Exception as error:
        print(error)

def draft (customers):
  try:
    cpf = input("Informe o CPF do cliente: ")
    customer = filter_customer(cpf, customers)

    if not customer:
      print("\n Cliente não encontrado! ")
      return
    
    value = float(input("Informe o valor do saque: "))
    transaction = Draft(value)
    account = get_customer_account(customer)

    if not account:
      return
    
    customer.do_transaction(account, transaction)
  except Exception as error:
        print(error)

def show_bank_statement (customers):
  try:
    cpf = input("Informe o CPF do cliente: ")
    customer = filter_customer(cpf, customers)

    if not customer:
      print("\n Cliente não encontrado! ")
      return
    
    account = get_customer_account(customer)

    if not account:
      return
    
    print("\n================ EXTRATO ================")
    transactions = account.historic.transactions
    
    statement = ''

    if not transactions:
      statement = "Não foram realizadas transações bancárias"
    else:
      for transaction in transactions:
        statement += f"\n{transaction['type']}:\n\tR$ {transaction['value']:.2f}"

    print(statement)
    print(f"\nSaldo:\n\tR$ {account.balance:.2f}")
    print("==========================================")
  except Exception as error:
        print(error)


def create_customer (customers):
  try:
    cpf = input("Informe o CPF (somente número): ")
    customer = filter_customer(cpf, customers)

    if customer:
      print('Já existe conta para este usuário')
      return
    
    name = input('Informe o nome completo: ')
    birth_date = input('Informe a data de nascimento (dd-mm-aaaa): ')
    address = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    customer = PhysicalPerson (name=name, birth_date=birth_date, cpf=cpf, address=address)

    customers.append(customer)

    print('Cliente cadastrado com sucesso!')
  except Exception as error:
    print(error)

def create_account (account_number, customers, accounts):
  try:
    cpf = input("Informe o CPF (somente número): ")
    customer = filter_customer(cpf, customers)

    if not customer:
      print('\nCliente não encontrado!')
      return
    
    account = CheckingAccount(account_number, customer)
    accounts.append(account)
    customer.accounts.append(account)

    print('\n Conta criada com sucesso!')

  except Exception as error:
    print(error)

def list_accounts (accounts):
  try:
    for account in accounts:
      print('=' * 100)
      print(textwrap.dedent(str(account)))
  except Exception as error:
    print(error)

def main():
    customers = []
    accounts = []

    while True:
      opcao = menu()

      if opcao == "d":
        deposit(customers)

      elif opcao == "s":
        draft(customers)

      elif opcao == "e":
        show_bank_statement(customers)

      elif opcao == "nu":
        create_customer(customers)

      elif opcao == "nc":
        numero_conta = len(accounts) + 1
        create_account(numero_conta, customers, accounts)

      elif opcao == "lc":
        list_accounts(accounts)

      elif opcao == "q":
        break

      else:
        print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()