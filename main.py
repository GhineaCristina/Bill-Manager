import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import PdfReport, FileSharer, Fields
import webbrowser
import os
import yagmail
from personal_email import my_email, my_password


Builder.load_file('frontend.kv')


class BillsScreen(Screen):
    """Represents a screen in the application for entering bill information.

    Attributes:
        manager (ScreenManager): The screen manager responsible for handling screen transitions.
    """

    def calculate(self):
        #  Calculate the total amount of the bill based on the entered rent
        #and utilities. Then, transitions to the 'create_pdf' screen.
        try:
            rent = float(self.ids.rent_id.text)
            utilities = float(self.ids.utilities_id.text)
            amount = rent + utilities
            self.manager.amount = amount
            self.manager.current = 'create_pdf'

        except ValueError:
            print("Enter valid numbers for rent and utilities!")


class CreatePdf(Screen):
    """Represents a screen in the application for generating PDF bills and performing related actions.

        Attributes:
            manager (ScreenManager): The screen manager responsible for handling screen transitions.
            url (str): The URL of the shared PDF file.
        """

    def on_enter(self, *args):
        # Callback method invoked when the screen is entered.
        # Calls the 'total' and 'date' methods to update displayed information.
        self.total()
        self.date()

    def total(self):
        # Update the displayed total bill amount on the screen.
        self.ids.bills.text = f'Total Bill: ${self.manager.amount:.2f}'

    def date(self):
        # Update the displayed current date on the screen.
        current_time = time.strftime('%Y-%m-%d')
        self.ids.date.text = f'Date: {current_time}'

    def generate_pdf(self):
        # Generate a PDF bill report, share it, and update the link on the screen
        fields = Fields(self.manager, self.manager.amount)
        current_date = time.strftime('%Y-%m-%d')
        filename = f"{current_date}.pdf"
        filepath = os.path.join("files", filename)  # Ensures the path is built correctly for all OS

        pdf_report = PdfReport(filename=filename, fields=fields)
        pdf_report.generate()

        filesharer = FileSharer(filepath=filepath)
        self.url = filesharer.share()  # Share the file and get the URL
        self.ids.link.text = self.url  # Display the URL

    def open_link(self):
        # Open link with default browser
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = "Create a PDF first!"

    def send_email(self):
        # Send the PDF bill report via email to the specified recipient.
        recipient_email = self.ids.mail_id.text
        filename = f"files/{time.strftime('%Y-%m-%d')}.pdf"

        yag = yagmail.SMTP(my_email, my_password)  # Set up the yagmail SMTP server
        subject = 'Bill Report'
        contents = 'Please find attached the bill report.'

        # Attach the PDF file
        try:
            yag.send(to=recipient_email, subject=subject, contents=contents, attachments=filename)
            self.ids.link_email.text = "Email sent successfully."
        except Exception as e:
            self.ids.link_email.text = "Enter a valid email address!"
            print(f"Error sending email: {e}")


class RootWidget(ScreenManager):
    """
       Represents the root widget of the application,
    responsible for managing screens and screen transitions.
    """
    pass


class MainApp(App):
    """Represents the main application class responsible for
    running the application.
    """

    def build(self):
        return RootWidget()

# Run the application
MainApp().run()
