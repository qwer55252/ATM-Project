class Bank:
    def __init__(self):
        self.bank_data = {}
    
    def add_entry(self, card_num: str, pin: str, account: str, amt: int):
        self.bank_data[card_num] = {"pin":pin, "account":{account:amt}}
    
    def add_account(self, card_num: str, pin: str, account: str):
        # 이미 존재하는 계좌인지 확인
        if self.check_account(card_num, account):
            print(f'{account} 계좌는 이미 {card_num} 카드에 존재하는 계좌입니다.')
        else:
            self.bank_data[card_num]["account"][account] = 0
    
    def check_cardnum(self, card_num: str):
        if card_num in self.bank_data.keys():
            return True
        else:
            return False
    
    def check_pin(self, card_num: str, entered_pin: str):
        if self.bank_data[card_num]["pin"] == entered_pin: # 카드 번호와 핀번호 일치하면
            return True
        else:
            return False
    def check_account(self, card_num: str, account: str):
        if account in self.bank_data[card_num]["account"].keys():
            return True
        else:
            return False
    
    def get_account(self, card_num: str, entered_pin: str): # card_num의 pin 번호와 일치하는지 확인
        if self.check_cardnum(card_num) and self.check_pin(card_num, entered_pin):
            return self.bank_data[card_num]["account"] # 카드의 계좌 반환
        else:
            return None
        
    def update_account(self, card_num: str, entered_pin: str, account: str, amt: int): # card_num 카드의 account 계좌 금액을 amt 로 update 해주는 메서드
        # 카드가 존재하고, 핀번호가 같고, 계좌가 존재하면 업데이트 해주자
        if self.check_cardnum(card_num) and self.check_pin(card_num, entered_pin) and self.check_account(card_num, account):
            self.bank_data[card_num]["account"][account] = amt
            print(f'거래 후 {card_num} 카드의 {account} 계좌 잔액 : {amt}')
        else:
            print(f'카드번호 또는 핀번호, 또는 계좌를 다시 확인해주세요')
            
    
    def print_bank(self):
        print(f'{self.bank_data}\n')
        

class Controller:
    def __init__(self, bank: Bank, cash_bin: int):
        self.bank = bank
        self.accounts = None # 이 변수가 왜 필요할까? 한번 인증하고 Controller 에서 계속 쓰기 위해?
        self.cash_bin = cash_bin
    
    def swipe(self, card_num: str, entered_pin: str): # self.accounts 에 변수 받아오기 위한 메서드
        self.accounts = self.bank.get_account(card_num, entered_pin)
        if self.accounts:
            pass
        else:
            print("카드 정보 혹은 핀 번호가 올바르지 않습니다. 다시 시도해주세요.")

    def account_action(self, card_num: str, entered_pin: str, account: str, action: tuple):
        # 이 메서드는 card_num, entered_pin, account 확인이 이루어진 후 불러집니다.
        if action[0] == "See Balance":
            balance = self.accounts[account]
            print(f'카드 번호 : {card_num}')
            print(f'계좌 번호 : {account}')
            print(f'잔액 조회 : {balance}')
            return self.accounts[account], 1
        elif action[0] == "Withdraw":
            amt = action[1]
            if self.accounts[account] < amt:
                print(f'계좌 잔액 : {self.accounts[account]}')
                print('계좌 잔액이 부족합니다!')
                return self.accounts[account], 0
            if self.cash_bin < amt:
                print(f'현금통 잔액 : {self.cash_bin}')
                print('현금통에 돈이 없습니다!')
                return self.accounts[account], 0
            else:
                new_balance = self.accounts[account] - amt
                self.cash_bin -= amt
                self.accounts[account] -= new_balance
                self.bank.update_account(card_num, entered_pin, account, new_balance)
                print(f'{card_num} 카드의 {account} 계좌에서 {amt} 달러 출금을 완료했습니다.')
                return self.accounts[account], 1
                
        elif action[0] == "Deposit":
            amt = action[1]
            new_balance = self.accounts[account] + amt
            self.cash_bin += amt
            self.accounts[account] = new_balance
            self.bank.update_account(card_num, entered_pin, account, new_balance)
            print(f'{card_num} 카드의 {account} 계좌에서 {amt} 달러 입금을 완료했습니다.')
            return self.accounts[account], 1
        else:
            print(f'{action}은 존재하지 않는 action 입니다!')
            return self.accounts[account], 2
    
    def __call__(self, card_num: str, entered_pin: str, account: str, action: tuple):
        # 전체적으로 점검
        if not self.bank.check_cardnum(card_num):
            print('존재하지 않는 카드 번호입니다.')
            print(f'조회하려는 카드 : {card_num}')
            print(f'은행 현황 : {self.bank.bank_data}\n')
            return "Invalid Card!\n"
        if not self.bank.check_pin(card_num, entered_pin):
            print('핀번호가 일치하지 않습니다.\n')
            print(f'은행 현황 : {self.bank.bank_data}\n')
            return "Invalid Pin!\n"
        if not self.bank.check_account(card_num, account):
            print('존재하지 않는 계좌입니다.')
            print(f'조회하려는 계좌 : {account}')
            print(f'해당 카드의 계좌 현황 : {self.bank.bank_data[card_num]["account"]}\n')
            return "Invalid Account!\n"
        
        # [card_num, pin, account] check complete
        self.swipe(card_num, entered_pin)
        self.account_action(card_num, entered_pin, account, action)
        print()
        
        

if __name__ == "__main__":
    
    # Bank 클래스 테스트
    print('------------- Start Bank Class Test -------------')
    bank1 = Bank()
    bank1.add_entry("1234-1234-1234-1234", "1234", "111111-11-111111", 1000)        # test case 1 : add_entry
    bank1.print_bank()
    print('test case 1 Done\n')
    bank1.add_account("1234-1234-1234-1234", "1234", "111111-11-111111")            # test case 2 : To create an existing account
    bank1.print_bank()
    print('test case 2 Done\n')
    bank1.add_account("1234-1234-1234-1234", "1234", "222222-22-222222")            # test case 3 : add_account
    bank1.print_bank()
    print('test case 3 Done\n')
    bank1.update_account("1234-1234-1234-1234", "1234", "111111-11-111111", 2000)   # test case 4 : 카드에 새로운 계좌 생성
    bank1.print_bank()
    print('test case 4 Done\n')
    bank1.add_entry("4321-4321-4321-4321", "4321", "444444-44-444444", 1000)
    bank1.print_bank()
    print('------------- End Bank Class Test -------------')

    # Controller 클래스 테스트
    print('------------- Start Controller Class Test -------------')
    atm1 = Controller(bank1, 500)
    action1 = ("See Balance", 0)
    action2 = ("Withdraw", 1000)
    action3 = ("Deposit", 100)
    action4 = ("Withdraw", 300)
    
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action1)    # test case 1 : See Balance function
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action2)    # test case 2 : cash bin insufficient
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action1)
    
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action3)    # test case 3 : See Deposit function
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action1)
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action4)    # test case 4 : Withdraw function 2
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action1)
    
    atm1("1234-1234-1234-1234", "5678", "111111-11-111111", action1)    # test case 5 : Wrong pin number
    atm1("5678-5678-5678-5678", "1234", "111111-11-111111", action1)    # test case 6 : Wrong card number
    atm1("1234-1234-1234-1234", "1234", "333333-33-333333", action1)    # test case 7 : Wrong account number
    
    action5 = ("Withdraw", 100000)                                      # test case 8 : Account balance insufficient
    atm1("1234-1234-1234-1234", "1234", "111111-11-111111", action5)
    print('------------- End Controller Class Test -------------')
        