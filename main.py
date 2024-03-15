import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import FileSharer



Builder.load_file('frontend.kv')

class BillsScreen(Screen):
    def calculate(self):
        try:
            rent = float(self.ids.rent_id.text)
            utilities = float(self.ids.utilities_id.text)
            amount = rent + utilities
            self.manager.amount = amount
            self.manager.current = 'create_pdf'

        except ValueError:
            print("Enter valid numbers for rent and utilities!")

class CreatePdf(Screen):

    def on_enter(self, *args):
        # Call the total() method to update the label when the screen is entered.
        self.total()
        self.date()

    def total(self):
        # Access the amount using self.manager.amount
        self.ids.bills.text = f'Total Bill: ${self.manager.amount:.2f}'

    def date(self):
        current_time = time.strftime('%Y-%m-%d')
        self.ids.date.text = f'Date: {current_time}'

    def generate(self):
        pass

    def open_link(self):
        pass

    def send_email(self):
        pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()