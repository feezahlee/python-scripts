import shutil
import os
import sys

def rename_and_move_certificates():
    # Define source and destination paths for the certificate and key
    src_crt = os.path.expanduser('~/vrnetlab/csr/ssl/apache.crt')
    dest_crt = '/usr/local/apache2/conf/server.crt'
    src_key = os.path.expanduser('~/vrnetlab/csr/ssl/apache.key')
    dest_key = '/usr/local/apache2/conf/server.key'

    # Check if the source files exist
    if not os.path.isfile(src_crt):
        print(f"Error: Source certificate file does not exist: {src_crt}")
        sys.exit(1)
    if not os.path.isfile(src_key):
        print(f"Error: Source key file does not exist: {src_key}")
        sys.exit(1)

    # Copy the certificate and key to the new locations
    try:
        shutil.copy(src_crt, dest_crt)
        print(f"Certificate copied from {src_crt} to {dest_crt}")
    except Exception as e:
        print(f"Error copying certificate: {e}")
        sys.exit(1)

    try:
        shutil.copy(src_key, dest_key)
        print(f"Key copied from {src_key} to {dest_key}")
    except Exception as e:
        print(f"Error copying key: {e}")
        sys.exit(1)

if __name__ == "__main__":
    rename_and_move_certificates()
