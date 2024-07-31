# extract_invoices

A simple script to extract and save pdf files from the local filestore, bypassing Odoo itself.

The script checks all PDF files (invoices, vendor bills, etc.) from the filestore one by one and matches them with documents from the Odoo database, and then saves them locally in the destination location in separate directories for each Odoo company.
All you need to do is import the Odoo database locally and have local access to the filestore. No Odoo instance or source code needed. Just run the script and wait. During extraction, the number of processed files and their total number are given, but the total applies to all files, not only PDF. Maybe I'll fix it later.

Config:
- credentials to the local Odoo postgres db
- path to the log file
- path to the source filestore directory
- path to the target directory for copied invoices

What else?

Python and Postgres in PATH, but you probably have it.
If you have freshly installed python, you will probably have to run this line:
pip install psycopg2-binary


On my computer with the power of a larger potato, about 200k PDF files were copied from the filestore in about 1 hour.

If anything, please contact me: luk.jasin at gmail.com