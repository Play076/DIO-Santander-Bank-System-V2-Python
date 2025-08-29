userDatabase = []
accountDatabase = []

AGENCY_NUMBER = "0001"
WITHDRAWAL_LIMIT = 500
WITHDRAWAL_LIMIT_PER_DAY = 3

def menu():
    menu = """

        [n] Novo Cliente
        [c] Criar Conta
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

        => """
    
    return menu

def createNewAccount(cpf):
    newAccount = {}

    if not userDatabase:
        print("Nenhum usuário cadastrado.")
    elif not accountDatabase:
        newAccount["cpf"] = cpf
        newAccount["agency"] = AGENCY_NUMBER
        newAccount["account_number"] = len(accountDatabase) + 1
        newAccount["balance"] = 0.0
        newAccount["withdrawls"] = 0
        newAccount["deposits"] = 0
        newAccount['limit_withdrawls'] = 0

        accountDatabase.append(newAccount)
        print("Nova conta criada com sucesso!")
        print(f"Seus dados: agência {AGENCY_NUMBER}, número da conta {newAccount['account_number']}")
        print("Por favor, guarde esses dados para futuras operações.")
        return
    else:
        for account in accountDatabase:
            if cpfFilter(cpf):
                if account["cpf"] == cpf:
                    print("Já existe uma conta vinculada a esse CPF!")
                    return
                else:
                    newAccount["cpf"] = cpf
                    newAccount["agency"] = AGENCY_NUMBER
                    newAccount["account_number"] = len(accountDatabase) + 1
                    newAccount["balance"] = 0.0
                    newAccount["withdrawls"] = 0
                    newAccount["deposits"] = 0
                    newAccount['limit_withdrawls'] = 0

                    accountDatabase.append(newAccount)
                    print("Nova conta criada com sucesso!")
                    print(f"Seus dados: agência {AGENCY_NUMBER}, número da conta {newAccount['account_number']}")
                    print("Por favor, guarde esses dados para futuras operações.")
                    return
            else:
                print("Esse cpf não está cadastrado.")

def cpfFilter(cpf):
    if not userDatabase:
        print("Nenhum usuário cadastrado.")
    else:
        for user in userDatabase:
            if user["cpf"] == cpf:
                return True, user["cpf"]
        return False

def newClient(user):
    newUser = {}

    for key, value in user.items():
        if key not in newUser:
            newUser[key] = value

    if not userDatabase:
        userDatabase.append(newUser)
        print("Novo usuário cadastrado com sucesso!")
    else:
        for exsitingUser in userDatabase:
            if exsitingUser["cpf"] == newUser["cpf"]:
                print("Esse usuário já está cadastrado!")
            else:
                userDatabase.append(newUser)
                print("Novo usuário cadastrado com sucesso!")

def depositOperation(balance, amount):
    if amount > 0:
        balance += amount
        print(f"Depósito realizado com sucesso! Novo balance: R$ {balance:.2f}")
    else:
        print("Operação falhou! O valor do depósito deve ser positivo.")
    return balance

def withdrawOperation(balance, amount, limit_account, withdrawal_limit):
    if limit_account < WITHDRAWAL_LIMIT_PER_DAY:
        if amount > balance:
            print("Operação falhou! você não tem saldo o suficiente.")
            return balance, limit_account
        elif amount > withdrawal_limit:
            print("Operação falhou! O valor do saque excede o limite.")
            return balance, limit_account
        else:
            balance -= amount
            limit_account += 1
            print(f"Saque realizado com sucesso! Novo saldo: R$ {balance:.2f}")
            return balance, limit_account
    else:
        print("Operação falhou! Número máximo de saques excedido.")
        return balance, limit_account

def statementAccounts(cpf, /, *, agency, accountNumber):

    if not accountDatabase or not userDatabase:
        print("Nenhuma conta ou usuário cadastrado.")
    else:
        if cpfFilter(cpf):
            for account in accountDatabase:
                if account["cpf"] == cpf and account["agency"] == agency and account["account_number"] == accountNumber:
                    print(f"Extrato da conta:\n Número e agência: {accountNumber} / {agency}")
                    print(f"Saldo: R$ {account['balance']:.2f}")
                    print(f"Total de depósitos: {account['deposits']}")
                    print(f"Total de saques: {account['withdrawls']}")
                    print(f"Limite de saques diários: {account['limit_withdrawls']}/{WITHDRAWAL_LIMIT_PER_DAY}")
                    return
                else:
                    print("Operação falhou! Conta não encontrada nesse CPF.")
        else:
            print("Operação falhou! CPF não encontrado.")

def main():
    while True:
        opcao = input(menu())

        if opcao == "n":
            
            print("Olá novo cliente, bem-vindo ao nosso sistema bancário\n Por favor informe seus dados abaixo para cadastrá-lo")

            newUser = {
                "cpf": int(input("Informe o seu CPF (somente os números): ")),
                "name": input("Informe o seu nome: "),
                "birth_date": input("Informe a sua data de nascimento (dd-mm-aaaa): "),
                "address": {
                    "street": input("Informe a sua rua: "),
                    "number": input("Informe o seu número: "),
                    "neighborhood": input("Informe o seu bairro: "),
                    "city/state": input("Informe a sua cidade e seu estado (Sigla da unidade federativa): ")
                }
            }

            newClient(newUser)
        elif opcao == "c":
            cpf = int(input("Informe o CPF do cliente: "))
            createNewAccount(cpf)

        elif opcao == "d":
            cpf = int(input("Informe o CPF do cliente: "))

            if cpfFilter(cpf):
                for account in accountDatabase:
                    if account["cpf"] == cpf:
                        valor = float(input("Informe o valor do depósito: "))
                        account["balance"] = depositOperation(balance=account["balance"], amount=valor)
                        account["deposits"] += 1
                    else:
                        print("Operação falhou! CPF não vinculado a nenhuma conta.")
            else:
                print("Operação falhou! CPF não encontrado.")

        elif opcao == "s":
            cpf = int(input("Informe o CPF do cliente: "))
            
            if cpfFilter(cpf):
                for account in accountDatabase:
                    if account["cpf"] == cpf:
                        valor = float(input("Informe o valor do saque: "))
                        account["balance"], account["limit_withdrawls"] = withdrawOperation(balance=account["balance"], amount=valor, limit_account=account["limit_withdrawls"], withdrawal_limit=WITHDRAWAL_LIMIT)
                        account["withdrawls"] += 1
                    else:
                        print("Operação falhou! CPF não vinculado a nenhuma conta.")
            else:
                print("Operação falhou! CPF não encontrado.")

        elif opcao == "e":
            cpf = int(input("Informe o CPF do cliente: "))
            agency = input("Informe a agência: ")
            accountNumber = int(input("Informe o número da conta: "))
            statementAccounts(cpf, agency=agency, accountNumber=accountNumber)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()