from collections import UserDict
import re

class Field ():
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    # 09042023
    def __repr__(self) -> str:
        return str(self)
    # *** 
  

class Name (Field):
    # def __init__(self, name) -> None:
    #     self.name = name
    
    # def __str__(self) -> str:
    #     return str(self.name)    
    pass
    
class Phone (Field):
    pass
    # def __init__(self, phone) -> None:
    #     self.phone = phone

    # def normal_phone(self, value:Field):
    #    if not re.match(r"^\+[\d]{12}$", value):
    #     raise ValueError("Invalid phone number")

    # def __str__(self) -> str:
    #     return str(self.phone)    

class Record ():
    def __init__(self, name:Name, phone:Phone = None):
        self.name = name
        self.phones = [phone] if phone else [] 
    
    # Добавление телефона из адресной книги
    def add_phone(self, phone:Phone):
        self.phones.append(phone)

    # Удаление телефона из адресной книги
    def remove_record(self, phone:Phone):
        # self.phones.remove(phone)
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                self.phones.pop(i)
                return f"Phone {phone} deleted successfully"
        return f'Contact has no phone {phone}'  
    
    # Изменение телефона в адресной книги
    def change_phone(self, old_phone:Phone, new_phone:Phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[i] = new_phone
                return f'Phone {old_phone} change to {new_phone}'
        return f'Contact has no phone {old_phone}'   
    
    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
        return f"{self.name}: {phones}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record


user_contacts = AddressBook()

def user_help ():
   return """
          Phone book commands:
          1. hello
          2. add 'Name' 'phone number" (Igor +380989709609)
          3. change 'Name' 'phone number1' 'phone number1' (Igor +380989709609 +380990509393)
          4. phone 'Name'
          5. remove 'Name' 'phone number' (Igor +380989709609') 
          6. show all
          7. good bye
          8. close
          9. exit
          """
 
# Decorator input errors
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return f"This contact {' '.join(args)} doesn't exist in the phone book"
        except ValueError:
            return "The entered name and phone number do not match the given parameter. For help, type 'help'"
        except IndexError:
            return "Type all params for command. For help, type 'help'"

    return wrapper

# Greetings
@input_error
def user_hello(*args):
    return "How can I help you?"

# Add добавление номера в адресную книгу
@input_error
def user_add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    
    if not re.match(r"^\+[\d]{12}$", phone.value):
        raise ValueError
    
    # 09042023
    rec:Record = user_contacts.get(name.value)
    
    if not rec:
        rec = Record(name, phone)
        user_contacts.add_record(rec)
        return f"{name} : {phone} has been added to the phone book"    
    
    rec.add_phone(phone)
    return f"Phone {phone} add to contact {name}"
    #  ****

# Change  изменение номера в адресной книги
@input_error
def user_change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    
    rec = user_contacts.get(name.value)
    
    if rec:
        return rec.change_phone(old_phone, new_phone)
    
    return f'Phone book has no contact {name}'

    
# Contact phone number
@input_error
def user_phone(*args):
    name = Name(args[0])
    record = user_contacts[name.value]
    
    # 09042023 
    # not_user_phone(name)
    # ***

    return f"The phone number for {name} is {record.phones}"
    

# Show all  вся адресная книга
@input_error
def user_show_all(*args):
    
    all = ""
    
    if len(user_contacts) == 0:
        return "Phone book is empty"
    else:
        for name, phone in user_contacts.items():
            all += f"{name}: {phone}\n"
        return all
# 
@input_error
def remove_phone(*args):
    
    name = Name(args[0])
    phone = Phone(args[1])
    
    rec:Record = user_contacts[name.value]
    return rec.remove_record(phone) 
    
    # 09042023
    # not_user = not_user_phone(name.value)

    # if not_user:
    #     rec = Record(name, phone)
    #     user_contacts.remove_record(rec)
    # ****

#09042023  
# def not_user_phone(name):
#     for i in user_contacts.keys():
#         print(i, type(i))
    
#     if name == "":
#         print("Try again. Enter contact name.")
#         return False
#     if name not in user_contacts.keys():
#         print(f'Contact {name} is not in phone book.')
#         return False
#     return True
# ****

# Exit
def user_exit(*args): 
    return "Good bye!\n"

COMMANDS = {
    'hello': user_hello, # приветствие
    'add': user_add, # Добавление
    'change': user_change, # Изменение
    'phone': user_phone, # Телефон
    'show all': user_show_all, # Список контактов
    "remove": remove_phone, # удаление из адресной книги
    'good bye': user_exit, # выход
    'close': user_exit,
    'exit': user_exit,
    'help': user_help, # помощь
}
 
# Command processing
def command_handler(user_input: str):
    for cmd in COMMANDS:
        if user_input.startswith(cmd):
            return COMMANDS[cmd], user_input.replace(cmd, '').strip().split()
    return None, []

# ********
def main():
    
    print(user_help())

    while True:
        user_input = input("Enter a command: ")
        command, data = command_handler(user_input)

        if command == user_exit:
            break

        if not command:
            print("Command is not supported. Try again.")
            continue
        
        print(command(*data))


if __name__ == "__main__":
    main()
