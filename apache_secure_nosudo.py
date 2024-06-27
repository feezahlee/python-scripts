import subprocess
import os

ssl_certificate_path = "/etc/ssl/certs/apache-selfsigned.crt"
ssl_certificate_key_path = "/etc/ssl/private/apache-selfsigned.key"
server_name = "192.0.2.3"

# Runs a shell command and it will handle errors that might occur during execution
def run_command(command, check=True):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr.decode()}")
        return None, e.stderr.decode()

# Installing Apache and OpenSSL
def install_apache_and_openssl():
    print("Installing Apache and OpenSSL...")
    stdout, stderr = run_command('apt-get update')
    print(stdout, stderr)
    stdout, stderr = run_command('apt-get install -y apache2 openssl')
    print(stdout, stderr)


# This is to make sure that it enables the SSL module in the Apache
def enable_ssl_module():
    print("Enabling SSL module in Apache...")
    stdout, stderr = run_command('a2enmod ssl')
    print(stdout, stderr)

# creating a directory with a specific permissions, it is to make sure that the directory exists with specific permissions
# before performing further operation.
def create_directory(path, mode):
    print(f"Creating directory {path} with mode {oct(mode)}...")
    os.makedirs(path, mode=mode, exist_ok=True)

# This is to create a self-signed SSL certificate for the Apache Server.
def generate_ssl_certificate():

    print("Generating a self-signed SSL certificate...")
    command = (
        f"sudo openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 "
        f"-keyout {ssl_certificate_key_path} -out {ssl_certificate_path} "
        f'-subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN={server_name}"'
    )
    stdout, stderr = run_command(command)
    print(stdout, stderr)


# To configure the Apache to listen on port 443 (HTTPS) instead of port 80.
def configure_apache_port():
    print("Configuring Apache to listen on port 443...")
    ports_conf_path = "/etc/apache2/ports.conf"
    run_command(f"sed -i 's/^#?Listen 443/Listen 443/' {ports_conf_path}")

# To create SSL Virtual Host File which includes the ssl certicate and key.
def create_ssl_virtual_host():
    print("Creating SSL Virtual Host file...")
    virtual_host_content = f"""
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        DocumentRoot /var/www/html
        SSLEngine on
        SSLCertificateFile {ssl_certificate_path}
        SSLCertificateKeyFile {ssl_certificate_key_path}
        <FilesMatch "\\.(cgi|shtml|phtml|php)$">
            SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
            SSLOptions +StdEnvVars
        </Directory>
        BrowserMatch "MSIE [2-6]" nokeepalive ssl-unclean-shutdown downgrade-1.0 force-response-1.0
    </VirtualHost>
</IfModule>
"""
    config_path = "/etc/apache2/sites-available/default-ssl.conf"
    with open("default-ssl.conf", 'w') as file:
        file.write(virtual_host_content)
    run_command(f"cp default-ssl.conf {config_path}")
    os.remove("default-ssl.conf")

# To enable the SSL Virtual Host where the Apache can use.
def enable_ssl_virtual_host():
    print("Enabling SSL Virtual Host...")
    stdout, stderr = run_command("a2ensite default-ssl.conf")
    print(stdout, stderr)

# To restart the Apache Server after changes are made.
def restart_apache():
    print("Restarting Apache server...")
    stdout, stderr = run_command("systemctl restart apache2")
    print(stdout, stderr)

# To call the fuctions.
def main():
    install_apache_and_openssl()
    enable_ssl_module()
    create_directory("/etc/ssl/certs", 0o755)
    create_directory("/etc/ssl/private", 0o700)
    generate_ssl_certificate()
    configure_apache_port()
    create_ssl_virtual_host()
    enable_ssl_virtual_host()
    restart_apache()
    print("Apache server with SSL has been configured successfully.")

if __name__ == "__main__":
    main()
