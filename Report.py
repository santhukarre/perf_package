import pandas as pd
from vincent.colors import brews
import smtplib
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
report_file_name = "Androbench_Report.xlsx"

sender_email = "santhoshkarre956@gmail.com"
receiver_email = "santhoshkarre956@gmail.com"

def generateAndrobenchReport():
    global report_file_name
    # Some sample data to plot.
    iteration_1 = {'seq_read': 10, 'seq_write': 32, 'rand_read': 21, 'rand_write': 13, 'sql_insert': 18}
    iteration_2 = {'seq_read': 15, 'seq_write': 43, 'rand_read': 17, 'rand_write': 10, 'sql_insert': 22}
    iteration_3 = {'seq_read': 6, 'seq_write': 24, 'rand_read': 22, 'rand_write': 16, 'sql_insert': 30}
    iteration_4 = {'seq_read': 12, 'seq_write': 30, 'rand_read': 15, 'rand_write': 9, 'sql_insert': 15}
    data = [iteration_1, iteration_2, iteration_3, iteration_4]
    index = ['Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4']
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data, index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Sheet1'
    writer = pd.ExcelWriter(report_file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})
    # Configure the series of the chart from the dataframedata.
    for col_num in range(1, len(iteration_1) + 1):
        chart.add_series({
            'name':       ['Sheet1', 0, col_num],
            'categories': ['Sheet1', 1, 0, 4, 0],
            'values':     ['Sheet1', 1, col_num, 4, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10,})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Score'})
    chart.set_y_axis({'name': 'Iterations', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def sendPlainMail():
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "santhoshkarre956@gmail.com"
    receiver_email = "santhoshkarre956@gmail.com"
    #password = input("Type your password and press enter:")
    password = ""
    message = """\
    Subject: Micon Xindus Test Report

    Please find the attached Micron Xindus Test Report."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def sendReportThroughMail():
    global report_file_name
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    password = ""
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # Open PDF file in binary mode
    with open(report_file_name, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {report_file_name}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
#sendMail()
generateAndrobenchReport()
sendReportThroughMail()
