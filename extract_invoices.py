import os
import shutil
import psycopg2
import logging

# logger
log_file_path = 'C:\\path_to\\logfile.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# db connection
conn = psycopg2.connect(
    dbname='your_odoo_db',
    user='postgres',
    password='postgres_password',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# filestore
filestore_path = 'C:\\path_to\\filestore'

# query
cur.execute("""
    SELECT ir.store_fname, ir.name, res_partner.name AS company_name
    FROM ir_attachment ir
    JOIN account_move am ON ir.res_id = am.id
    JOIN res_company res_partner ON am.company_id = res_partner.id
    WHERE ir.res_model = 'account.move'
""")
rows = cur.fetchall()

# invoice dest path
base_destination_path = 'C:\\path_to\\invoices'

# directory check
if not os.path.exists(base_destination_path):
    os.makedirs(base_destination_path)

# counters
processed_files_count = 0
failed_files_count = 0

# copy files
for row in rows:
    store_fname, name, company_name = row
    # pdf check
    if name.lower().endswith('.pdf'):
        # compant name normalization
        sanitized_company_name = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in company_name)
        company_folder_path = os.path.join(base_destination_path, sanitized_company_name)

        # company directory check
        if not os.path.exists(company_folder_path):
            os.makedirs(company_folder_path)

        # source path
        src_path = os.path.normpath(os.path.join(filestore_path, store_fname))
        # add company name
        dest_name = f"{name}"
        dest_path = os.path.join(company_folder_path, dest_name)

        # source file check
        if os.path.exists(src_path):
            shutil.copyfile(src_path, dest_path)
            processed_files_count += 1
            log_message = f"{processed_files_count}/{len(rows)}, dir: {sanitized_company_name}, file: {dest_name}"
            print(log_message)
            logging.info(log_message)
        else:
            log_message = f"File not found: {src_path}"
            print(log_message)
            logging.warning(log_message)

# close db conection
cur.close()
conn.close()

# final logs
final_message = f"Total number of files processed: {processed_files_count}, errors: {failed_files_count}."
print(final_message)
logging.info(final_message)
