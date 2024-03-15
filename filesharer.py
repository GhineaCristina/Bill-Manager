import os
from fpdf import FPDF
from filestack import Client
from datetime import datetime

class Fields:
    def __init__(self, manager, total_bill):
        self.manager = manager
        self.renter = self.manager.get_screen('bills_screen').ids.rent_name.text
        self.owner = self.manager.get_screen('bills_screen').ids.owner_name.text
        self.period = self.manager.get_screen('bills_screen').ids.period_id.text
        self.additional_info = self.manager.get_screen('bills_screen').ids.information.text
        self.total_bill = total_bill

class PdfReport:
    """
    Creates a Pdf file that contains data, such as their names, their due amount,
    and the period of the bill.
    """
    def __init__(self, filename, fields):
        self.filename = filename
        self.fields = fields

    def generate(self):
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()
        # Add icon
        pdf.image(name="files/house.png", x=10, y=8, w=30, h=30)

        # Insert title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Bill Manager", border=0, align="C", ln=1)

        # Insert values
        self.insert_field(pdf, "Date:", datetime.now().strftime('%Y-%m-%d'))
        self.insert_field(pdf, "Renter:", self.fields.renter)
        self.insert_field(pdf, "Owner:", self.fields.owner)
        self.insert_field(pdf, "Total Bill:", str(self.fields.total_bill))
        self.insert_field(pdf, "Period:", self.fields.period)
        self.insert_field(pdf, "Additional Information:", self.fields.additional_info)

        pdf.output(os.path.join("files", self.filename))

    def insert_field(self, pdf, field_name, field_value):
        pdf.set_font(family="Times", size=14, style='B')
        pdf.cell(w=100, h=40, txt=field_name, border=0)
        pdf.cell(w=150, h=40, txt=field_value, border=0, ln=1)

class FileSharer:
    def __init__(self, filepath, api_key='AFYXWYRlBS0ercmZeBvBcz'):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
