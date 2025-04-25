import os

import pandas as pd
import glob #To read the files of specific format...
from  fpdf import FPDF
import pathlib


def generate(invoices_path,pdfs_path,image_path,product_id,product_name,
             amount_purchased,price_per_unit,total_price):
    """
    This function converts the invoices Excel files into PDF invoices!!
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f'{invoices_path}/*.xlsx')
    # print(filepaths)
    for filepath in filepaths:

        pdf = FPDF(orientation="p", unit="mm", format="A4")
        pdf.add_page()

        filename = pathlib.Path(filepath).stem
        Invoice_no,date = filename.split('-')
        # Actual_invoice_no = Invoice_no[0]
        # date = Invoice_no[1]

        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=50, h=8, txt=f"Invoice no: {Invoice_no}",ln=1)
        pdf.cell(w=50, h=8, txt=f"Date: {date} ",ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        #Add a Header like productid,product name etc(not in loop as this header needs to be printed once only)
        columns = df.columns
        columns =  [item.replace('_',' ').title() for item in columns]
        pdf.set_font(family="Times", size=12,style="B")
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=52, h=8, txt=columns[1], border=1)
        pdf.cell(w=52, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows into the table
        for index, row in df.iterrows():
            if row.isnull().all():
                continue  # skip this row

            pdf.set_font(family="Times", size=12)
            pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
            pdf.cell(w=52, h=8, txt=str(row["product_name"]), border=1)
            pdf.cell(w=52, h=8, txt=str(row["amount_purchased"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

        #Writing total price to the pdf
        total_price = df["total_price"].sum()
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=52, h=8, txt="", border=1)
        pdf.cell(w=52, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_price), border=1, ln=1)

        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30,h=12,txt=f"The total price is sum: {total_price}", ln=1)
        pdf.cell(w=30,h=12,txt=f"Python how")
        pdf.image(f"{image_path}",w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")




