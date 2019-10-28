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

def main():
    # Open the file and determine the number of pages
    pdfFileObj = open(sys.argv[1], 'rb')
    pdfFileName = pdfFileObj.name
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.getNumPages()

    # Split each page in the file
    count = 0
    while (count < numPages):
        splitInvoice(pdfReader, count)
        count = count + 1

    # Close the file to prevent errors
    pdfFileObj.close()

# Split an invoice from the file
def splitInvoice(reader, pageNum):
    # Extract text from the first page
    pageObj = reader.getPage(pageNum)
    pageText = pageObj.extractText()

    # Search the text for an invoice number
    invoiceNumber = getInvoiceNumber(pageText)

    # Check that an invoice number was found; if false, add an error flag
    if not invoiceNumber:
        invoiceNumber = 'error' + pageNum

    # Search the text for a page number
    pageNumber = getPageNumber(pageText)

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
def getInvoiceNumber(pageText):
    # Search the text for an invoice number
    try:
        invoiceNumber = re.search('Number: (.+?)Page', pageText).group(1)
    except AttributeError:
        # No invoice number found
        invoiceNumber = ''

    # Return the invoice number
    return invoiceNumber;

# Get page number from page text
def getPageNumber(pageText):
    # Search the text for a page number
    try:
        pageNumber = re.search('Page (.+?) of', pageText).group(1)
    except AttributeError:
        # No page number found
        pageNumber = ''

    # Return the page number
    return pageNumber;

if __name__== "__main__":
  main()
