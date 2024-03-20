import os
from fpdf import FPDF
from filestack import Client
from datetime import datetime


class Fields:
    """Represents the fields necessary for generating a PDF report.

        Attributes:
            manager: The manager responsible for managing screens in the application.
            total_bill: The total bill amount.
            renter: The name of the renter.
            owner: The name of the owner.
            period: The period of the bill.
            additional_info: Additional information related to the bill.
        """
    def __init__(self, manager, total_bill):
        self.manager = manager  # The manager responsible for managing screens in the application.
        self.renter = self.manager.get_screen('bills_screen').ids.rent_name.text
        self.owner = self.manager.get_screen('bills_screen').ids.owner_name.text
        self.period = self.manager.get_screen('bills_screen').ids.period_id.text
        self.additional_info = self.manager.get_screen('bills_screen').ids.information.text
        self.total_bill = total_bill


class PdfReport:
    """Creates a PDF file containing bill-related data.
    """
    def __init__(self, filename, fields):
        self.filename = filename  # The name of the PDF file.
        self.fields = fields  # The Fields object containing bill-related data.

    def generate(self):
        # Generates the PDF report.
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()
        pdf.image(name="files/house.png", x=10, y=8, w=30, h=30)  # Add icon

        # Insert title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Bill Manager", border=0, align="C", ln=1)

        # Insert values
        self.insert_field(pdf, "Date:", datetime.now().strftime('%Y-%m-%d'))
        self.insert_field(pdf, "Renter:", self.fields.renter)
        self.insert_field(pdf, "Owner:", self.fields.owner)
        self.insert_field(pdf, "Total Bill:", str(self.fields.total_bill))
        self.insert_field(pdf, "Period:", self.fields.period)
        self.insert_field(pdf, "Additional Info:", self.fields.additional_info)

        pdf.output(os.path.join("files", self.filename))

    def insert_field(self, pdf, field_name, field_value):
        # Inserts fields into the PDF report.
        pdf.set_font(family="Times", size=14, style='B')
        pdf.cell(w=100, h=50, txt=field_name, border=0)
        pdf.cell(w=150, h=50, txt=field_value, border=0, ln=1)


class FileSharer:
    """Provides functionality for sharing files.
        """
    def __init__(self, filepath, api_key='AFYXWYRlBS0ercmZeBvBcz'):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        # Shares the file and returns the URL.
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
