import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import PdfReport, FileSharer, Fields
import webbrowser
import os


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

    def generate_pdf(self):
        fields = Fields(self.manager, self.manager.amount)
        current_date = time.strftime('%Y-%m-%d')
        filename = f"{current_date}.pdf"
        filepath = os.path.join("files", filename)  # This ensures the path is built correctly for all OS

        # Create an instance of PdfReport with the correct file path
        pdf_report = PdfReport(filename=filename, fields=fields)

        # Generate the PDF report
        pdf_report.generate()

        # Create an instance of FileSharer with the filepath
        filesharer = FileSharer(filepath=filepath)

        # Share the file and get the URL
        self.url = filesharer.share()

        # Display the URL
        self.ids.link.text = self.url

    def open_link(self):
        """Open link with default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message

    def send_email(self):
        pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()