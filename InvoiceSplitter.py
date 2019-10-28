# Invoice Splitter
# Copyright (C) 2019 Sophie Garrett

# This program takes an invoice file and renames it as its invoice number.

# If there are multiple invoices in the file, it separates them and saves each
# as a separate file.

# If an invoice has multiple pages, it saves each page as a separate file.

import sys
import os
import re
import PyPDF2
import configparser

def main():
    # Load configuration file
    config = loadConfig()
    regInvNum = config.get('main', 'invoicenum')
    regPageNum = config.get('main', 'pagenum')
    
    # Open the file and determine the number of pages
    pdfFileObj = open(sys.argv[1], 'rb')
    pdfFileName = pdfFileObj.name
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.getNumPages()

    # Split each page in the file
    count = 0
    while (count < numPages):
        splitInvoice(pdfReader, count, regInvNum, regPageNum)
        count = count + 1

    # Close the file to prevent errors
    pdfFileObj.close()

# Split an invoice from the file
def splitInvoice(reader, pageNum, regInvNum, regPageNum):
    # Extract text from the first page
    pageObj = reader.getPage(pageNum)
    pageText = pageObj.extractText()

    # Search the text for an invoice number
    invoiceNumber = getInvoiceNumber(pageText, regInvNum)

    # Check that an invoice number was found; if false, add an error flag
    if not invoiceNumber:
        invoiceNumber = 'error' + str(pageNum)

    # Search the text for a page number
    pageNumber = getPageNumber(pageText, regPageNum)

    # Check that a page number was found; if false, add an error flag
    if not pageNumber:
        pageNumber = 'noPg'

    # Add file extension to invoice number
    if pageNumber == '1':
        newFileName = invoiceNumber + '.pdf'
    else:
        newFileName = invoiceNumber + ' (' + pageNumber + ').pdf'

    # Create a new PDF writer and add the page to it
    pdfWriter = PyPDF2.PdfFileWriter()
    pdfWriter.addPage(pageObj)

    # Create a new invoice file
    with open(newFileName, 'wb') as outputFile:
        pdfWriter.write(outputFile)

# Get invoice number from page text
def getInvoiceNumber(pageText, regInvNum):
    # Search the text for an invoice number
    try:
        invoiceNumber = re.search(regInvNum, pageText).group(1)
    except AttributeError:
        # No invoice number found
        invoiceNumber = ''

    # Return the invoice number
    return invoiceNumber;

# Get page number from page text
def getPageNumber(pageText, regPageNum):
    # Search the text for a page number
    try:
        pageNumber = re.search(regPageNum, pageText).group(1)
    except AttributeError:
        # No page number found
        pageNumber = ''

    # Return the page number
    return pageNumber;

# Load configuration file
def loadConfig():
    config = configparser.ConfigParser()
    scriptdir = os.path.dirname(__file__)
    configpath = os.path.join(scriptdir, 'config.ini')

    # Check if configuration file exists. If not, create it.
    if not os.path.exists(configpath):
        config['main'] = {'invoicenum': 'Number: (.+?)Page', 'pagenum': 'Page (.+?) of'}
        config.write(open(configpath, 'w'))
    else:
        config.read(configpath)

    return config

if __name__== "__main__":
  main()
