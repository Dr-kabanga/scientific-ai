from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from cryptography.fernet import Fernet
import os

class BankingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Labels and text inputs for bank details
        self.add_widget(Label(text='Bank Name:'))
        self.bank_name = TextInput(hint_text="Enter your bank name")
        self.add_widget(self.bank_name)

        self.add_widget(Label(text='Account Type:'))
        self.account_type = TextInput(hint_text="Enter your account type")
        self.add_widget(self.account_type)

        self.add_widget(Label(text='Account Number:'))
        self.account_number = TextInput(hint_text="Enter your account number", password=True)
        self.add_widget(self.account_number)

        self.add_widget(Label(text='Email:'))
        self.email = TextInput(hint_text="Enter your email")
        self.add_widget(self.email)

        self.add_widget(Label(text='Mobile Number:'))
        self.mobile = TextInput(hint_text="Enter your mobile number")
        self.add_widget(self.mobile)

        # Save Button
        save_button = Button(text="Save Details")
        save_button.bind(on_press=self.save_details)
        self.add_widget(save_button)

        # Display message area
        self.message = Label()
        self.add_widget(self.message)

    def save_details(self, instance):
        # Generate or load an encryption key
        key_file = 'secret.key'
        if not os.path.exists(key_file):
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        else:
            with open(key_file, 'rb') as f:
                key = f.read()

        cipher = Fernet(key)

        # Encrypt and save details to a file
        details = {
            'Bank Name': self.bank_name.text,
            'Account Type': self.account_type.text,
            'Account Number': self.account_number.text,
            'Email': self.email.text,
            'Mobile': self.mobile.text
        }

        encrypted_details = cipher.encrypt(str(details).encode())

        with open('bank_details.txt', 'wb') as f:
            f.write(encrypted_details)

        self.message.text = "Details saved securely!"

class BankingAppMain(App):
    def build(self):
        return BankingApp()

if __name__ == '__main__':
    BankingAppMain().run()