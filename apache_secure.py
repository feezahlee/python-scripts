import subprocess
import os

ssl_certificate_path = "/etc/ssl/certs/apache-selfsigned.crt"
ssl_certificate_key_path = "/etc/ssl/private/apache-selfsigned.key"
server_name = "192.0.2.3"

def run_command(command, check=True):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr.decode()}")
        return None, e.stderr.decode()

def install_apache_and_openssl():
    print("Installing Apache and OpenSSL...")
    stdout, stderr = run_command('sudo apt-get update')
    print(stdout, stderr)
    stdout, stderr = run_command('sudo apt-get install -y apache2 openssl')
    print(stdout, stderr)

def enable_ssl_module():
    print("Enabling SSL module in Apache...")
    stdout, stderr = run_command('sudo a2enmod ssl')
    print(stdout, stderr)

def create_directory(path, mode):
    print(f"Creating directory {path} with mode {oct(mode)}...")
    os.makedirs(path, mode=mode, exist_ok=True)

def generate_ssl_certificate():
    print("Generating a self-signed SSL certificate...")
    command = (
        f"sudo openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 "
        f"-keyout {ssl_certificate_key_path} -out {ssl_certificate_path} "
        f'-subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN={server_name}"'
    )
    stdout, stderr = run_command(command)
    print(stdout, stderr)

def configure_apache_port():
    print("Configuring Apache to listen on port 443...")
    ports_conf_path = "/etc/apache2/ports.conf"
    run_command(f"sudo sed -i 's/^#?Listen 443/Listen 443/' {ports_conf_path}")

def create_ssl_virtual_host():
    print("Creating SSL Virtual Host file...")
    virtual_host_content = f"""
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        DocumentRoot /var/www/html
        DirectoryIndex testing.html
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
    run_command(f"sudo cp default-ssl.conf {config_path}")
    os.remove("default-ssl.conf")

def enable_ssl_virtual_host():
    print("Enabling SSL Virtual Host...")
    stdout, stderr = run_command("sudo a2ensite default-ssl.conf")
    print(stdout, stderr)

def restart_apache():
    print("Restarting Apache server...")
    stdout, stderr = run_command("sudo systemctl restart apache2")
    print(stdout, stderr)

def copy_testing_html():
    print("Copying testing.html to the Apache document root...")
    run_command("sudo cp testing.html /var/www/html/")

def remove_default_index_html():
    print("Removing default index.html if it exists...")
    run_command("sudo rm -f /var/www/html/index.html")

def set_permissions():
    print("Setting correct permissions for testing.html...")
    run_command("sudo chmod 644 /var/www/html/testing.html")
    run_command("sudo chown www-data:www-data /var/www/html/testing.html")

def main():
    install_apache_and_openssl()
    enable_ssl_module()
    create_directory("/etc/ssl/certs", 0o755)
    create_directory("/etc/ssl/private", 0o700)
    generate_ssl_certificate()
    configure_apache_port()
    create_ssl_virtual_host()
    enable_ssl_virtual_host()
    remove_default_index_html()
    copy_testing_html()
    set_permissions()
    restart_apache()
    print("Apache server with SSL has been configured successfully and testing.html is available.")

if __name__ == "__main__":
    main()
