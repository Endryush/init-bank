import textwrap

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
  return input(menu)


def deposit (balance, value, bank_statement, /) : # / informa que params será passado por posição
  if value <= 0:
    print("Valor inválido! Por favor informe um valor maior que zero para fazer um depósito")
  else:
    balance +=value
    bank_statement += f'Depósito de R$ {value} realizado com sucesso!\n'
    print('\nDepósito realizado com sucesso')
  
  return balance, bank_statement

def draft (*, balance, value, bank_statement, daily_limit, bank_daily_draft, draft_limit) : # * informa que params serão nomeados
  invalid_draft = value > balance
  invalid_value = value > daily_limit
  drafted_today_exceeded = bank_daily_draft >= draft_limit

  if invalid_draft:
    print('Saldo insuficiente!')
  
  elif invalid_value:
    print(f'O valor do saque é maior do que {daily_limit}')

  elif drafted_today_exceeded:
    print ('Limite diário atingido. Não pode sacar mais.')

  elif value <= 0:
    print ("Valor inválido!")

  else :
    balance -= value
    message = f'Saque no valor de R${value:.2f} realizado com sucesso!\n'
    bank_daily_draft += 1
    bank_statement += message
    print(message)

  return balance, bank_statement

def show_bank_statement (balance, /, *, bank_statement) :
  print('===================== EXTRATO BANCÁRIO =========================')
  print('Não foram realizadas movimentações bancárias!' if not bank_statement else bank_statement)
  print(f'Saldo atual: R$ {balance:.2f}\n')
  print('===================== EXTRATO BANCÁRIO =========================')

def create_user (users) :
  cpf = input('Informe o número do CPF: ')
  user = filter_user(cpf, users)

  if user:
    print('Já existe cadastro com esse número de CPF')
    return
  
  name = input('Informe o nome completo: ')
  birth_date = input('Informe a data de nascimento (dd-mm-aaaa): ')
  address = input('Informe o endereço (rua, número - bairro - cidade/sigla estado): ')

  users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})

  print("=== Usuário criado com sucesso! ===")

def filter_user (cpf, users) :
  filtered_user = [user for user in users if user['cpf'] == cpf]

  return filtered_user[0] if filtered_user else None

def create_account (agency, account_number, users) :
  cpf = input("Informe o CPF do usuário: ")
  user = filter_user(cpf, users)

  if user:
      print("\n=== Conta criada com sucesso! ===")
      return {"agency": agency, "account_number": account_number, "user": user}

  print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def list_accounts (accounts) : 
  for account in accounts:
    linha = f"""\
        Agência:\t{account['agency']}
        C/C:\t\t{account['account_number']}
        Titular:\t{account['user']['name']}
    """
    print("=" * 100)
    print(textwrap.dedent(linha))


def main () :
  DRAFT_LIMIT = 3
  AGENCY = '0001'

  balance = 0
  daily_limit = 500
  bank_statement = ''
  bank_daily_draft = 0
  users = []
  accounts = []

  while True:
    option = menu()

    if option == 'd':
      value = float(input('Informe o valor para depositar:'))

      balance, bank_statement = deposit(balance, value, bank_statement)

    elif option == 's':
      value = float(input('Informe o valor do saque:'))

      balance, bank_statement = draft (
        balance = balance,
        value = value,
        bank_statement = bank_statement,
        daily_limit = daily_limit,
        bank_daily_draft = bank_daily_draft,
        draft_limit = DRAFT_LIMIT
      )

    elif option == 'e':
      show_bank_statement(balance, bank_statement = bank_statement)

    elif option == 'nu':
      create_user(users)

    elif option == 'nc':
      account_number=len(accounts)
      account = create_account(AGENCY, account_number, users)

      if account:
        accounts.append(account)

    elif option == 'lc':
      list_accounts(accounts)
    
    elif option == 'q':
      break
    else: 
      print('operação inválida')




main()