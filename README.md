# InvoiceSplitter
A short script for splitting and saving invoice files.

This script was designed to split files that contain multiple invoices and save each invoice as a separate file. This task was becoming tedious to do by hand, so I decided to automate it. I'm not sure that this will be useful to anyone else, but if it is, feel free to use it!

The program requires [PyPDF2](https://github.com/mstamy2/PyPDF2) to run. You can install it from the command line by running `pip install PyPDF2`.

You will need to pass the file to be split into the program as an argument. For ease of use, I recommend creating a shortcut in the context menu. If you're on Windows, [this post on StackOverflow](https://stackoverflow.com/questions/8570288/run-python-script-on-selected-file) might be helpful. I'm not sure how to do this on Mac or Linux, unfortunately.

Also note that this script was designed specifically for the invoice template used at a particular company, so it probably won't work out-of-the-box for everyone. Assuming that your invoices are in PDF format and have both an invoice number and a page number, compatibility should be achievable by editing the regex values. Additionally, with a bit of tweaking it should work for any large file that needs to be split by page number, title, etc.
