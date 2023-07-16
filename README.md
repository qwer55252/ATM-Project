# ATM-Project
Simple ATM Implementation Code


## Execute

Verify the output by running the following command.

python3 controller.py

## Class Description

### Class Bank

Stores the information from the bank in the bank_data which is instance variable of bank class. Here is an example of bank_data.

```json
"account": {
   '1234-1234-1234-1234': {
        'pin': '1234', 
        'account': {
            '111111-11-111111': 2000, 
            '222222-22-222222': 0
        }
    }, 
    '4321-4321-4321-4321': {
        'pin': '4321', 
        'account': {
            '444444-44-444444': 1000
        }
    }
}
```

- add_entry : Create (card_num, pin, account) account of amt balance
- add_account : create account on card_num card
- check_card_num : Check if it is a card number that exists in the bank
- check_pin : Check if the card matches the entered pin number
- check_account : check if the account exists on the card
- get_account : Import all accounts on the card
- update_account : Update balance in account
- print_bank : bank status output
### Class Controller
- sweep : Gets the account information using the card number and the entered pin number and saves it in the instance variable.
- account_action : Executes an action on the card's account.
- \_\_call\_\_: Check the card number, pin number, and account and execute the action using the account_action method.
### \_\_main\_\_
: You can run various test cases and check the output. It consists of two tests: the Bank Class test and the Controller Class test. Annotation describes which test case.