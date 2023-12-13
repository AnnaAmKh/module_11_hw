from collections import UserDict
from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.validate_phone(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value

class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid birthday format")
        self._value = new_value

    def days_to_birthday(self):
        if self._value:
            dob = datetime.strptime(self._value, '%Y-%m-%d')
            today = datetime.now()
            next_birthday = datetime(today.year, dob.month, dob.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, dob.month, dob.day)
            return (next_birthday - today).days
        else:
            return None

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if new_phone.value not in [p.value for p in self.phones]:
            self.phones.append(new_phone)
            print(f"Phone number {new_phone.value} has been added to the contact.")
        else:
            print("Phone number already exists for this contact.")

    def remove_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
                break

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)

        found = False
        for i, stored_phone in enumerate(self.phones):
            if stored_phone.value == old_phone_obj.value:
                found = True
                if new_phone_obj.value != old_phone_obj.value and new_phone_obj.value not in [p.value for p in self.phones]:
                    self.phones[i] = new_phone_obj
                    print(f"Phone number {old_phone_obj.value} has been updated to {new_phone_obj.value}.")
                else:
                    print("New phone number already exists for this contact or is the same as the old one.")
                break

        if not found:
            raise ValueError("Phone number not found for this contact.")

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone

    def __str__(self):
        phone_list = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_list}"

    def days_to_birthday(self):
        return self.birthday.days_to_birthday() if self.birthday else None

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
            print(f"Record for {record.name.value} has been added to the address book.")
        else:
            print(f"Record for {record.name.value} already exists in the address book.")

    def find(self, name):
        if name in self.data:
            print(f"Record for {name} found in the address book.")
            return self.data[name]
        else:
            print(f"Record for {name} not found in the address book.")
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Record for {name} has been deleted from the address book.")
        else:
            print(f"Record for {name} not found in the address book.")
    def iterator(self, batch_size):
        keys = list(self.data.keys())
        for i in range(0, len(keys), batch_size):
            yield [self.data[key] for key in keys[i:i+batch_size]]