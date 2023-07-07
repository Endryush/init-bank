
MENU = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair 


"""

balance = 0
daily_limit = 500
bank_statement = ''
bank_daily_draft = 0
DRAFT_LIMIT = 3

while True:
    option = input(MENU)

    if option == 'd':
      value = float(input('Informe o valor para depositar:'))
      if value <= 0:
         print("Valor inválido! Por favor informe um valor maior que zero para fazer um depósito")
      
      balance +=value
      bank_statement += f'Depósito de R$ {value} realizado com sucesso!\n'

    elif option == 's':
      value = float(input('Informe o valor do saque:'))

      invalid_draft = value > balance
      invalid_value = value > daily_limit
      drafted_today_exceeded = bank_daily_draft >= DRAFT_LIMIT

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
    elif option == 'e':
        print('===================== EXTRATO BANCÁRIO =========================')
        print('Não foram realizadas movimentações bancárias!' if not bank_statement else bank_statement)
        print(f'Saldo atual: R$ {balance:.2f}\n')
        print('===================== EXTRATO BANCÁRIO =========================')
    elif option == 'q':
      break
    else: 
      print('operação inválida')


