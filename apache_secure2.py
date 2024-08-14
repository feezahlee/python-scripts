import sys
import os
import subprocess
import fileinput
import shutil


def rename_and_move_certificates():
    # Define source and destination paths for the certificate and key
    src_crt = '/usr/local/apache2/conf/ssl/apache.crt'
    dest_crt = '/usr/local/apache2/conf/server.crt'
    src_key = '/usr/local/apache2/conf/ssl/apache.key'
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
def update_httpd_ssl_conf():
    block = """
ServerName 192.168.2.2
<IfModule ssl_module>
  Listen 443
  SSLPassPhraseDialog  builtin
  SSLSessionCache       shmcb:/usr/local/apache2/logs/ssl_scache(512000)
  SSLSessionCacheTimeout  300
  SSLMutex  file:/usr/local/apache2/logs/ssl_mutex
  SSLCertificateFile "/usr/local/apache2/conf/server.crt"
  SSLCertificateKeyFile "/usr/local/apache2/conf/server.key"
  <VirtualHost _default_:443>
    ServerAdmin webmaster@localhost
    DocumentRoot "/usr/local/apache2/htdocs"
    ErrorLog "logs/ssl_error_log"
    CustomLog "logs/ssl_access_log" common
    SSLEngine on
  </VirtualHost>
</IfModule>
"""
    with open('/usr/local/apache2/conf/extra/httpd-ssl.conf', 'a') as f:
        f.write(block)

def include_httpd_ssl_conf():
    with open('/usr/local/apache2/conf/httpd.conf', 'a') as f:
        f.write('\nInclude conf/extra/httpd-ssl.conf\n')

def load_modules():
    with open('/usr/local/apache2/conf/httpd.conf', 'a') as f:
        f.write('\nLoadModule ssl_module modules/mod_ssl.so\n')
        f.write('LoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n')

def restart_apache():
    subprocess.run(['apachectl', 'restart'])

def configure_ssl_on_apache():
    rename_and_move_certificates()
    update_httpd_ssl_conf()
    include_httpd_ssl_conf()
    load_modules()
    restart_apache()

if __name__ == "__main__":
    configure_ssl_on_apache()
