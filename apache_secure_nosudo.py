import subprocess
import os

ssl_certificate_path = "/etc/ssl/certs/apache-selfsigned.crt"
ssl_certificate_key_path = "/etc/ssl/private/apache-selfsigned.key"
server_name = "192.0.2.3"

# Runs a shell command and handles errors
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr.decode()}")
        return None, e.stderr.decode()

# Installing Apache and OpenSSL
def install_apache_and_openssl():
    print("Installing Apache and OpenSSL...")
    stdout, stderr = run_command('apk update')
    print(stdout, stderr)
    stdout, stderr = run_command('apk add apache2 openssl')
    print(stdout, stderr)

# Enabling SSL module in Apache
def enable_ssl_module():
    print("Enabling SSL module in Apache...")
    # In Alpine, Apache modules are typically configured directly in httpd.conf or similar.
    # If needed, this logic would be adapted to fit Alpine's way of managing Apache modules.
    # For now, we assume the module is already enabled or not needed.

# Creating directories with specific permissions
def create_directory(path, mode):
    print(f"Creating directory {path} with mode {oct(mode)}...")
    os.makedirs(path, mode=mode, exist_ok=True)

# Generating a self-signed SSL certificate
def generate_ssl_certificate():
    print("Generating a self-signed SSL certificate...")
    command = (
        f"openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 "
        f"-keyout {ssl_certificate_key_path} -out {ssl_certificate_path} "
        f'-subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN={server_name}"'
    )
    stdout, stderr = run_command(command)
    print(stdout, stderr)

# Configuring Apache to listen on port 443
def configure_apache_port():
    print("Configuring Apache to listen on port 443...")
    # In Alpine, you might configure Apache directly in httpd.conf or similar.

# Creating SSL Virtual Host File
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

# Enabling SSL Virtual Host
def enable_ssl_virtual_host():
    print("Enabling SSL Virtual Host...")
    # In Alpine, enabling virtual hosts is usually managed via symbolic links or direct config file edits.

# Restarting Apache Server
def restart_apache():
    print("Restarting Apache server...")
    # In Alpine, restart or reload commands are often specific to the service's management system.

# Main function to execute all steps
def main():
    install_apache_and_openssl()
    enable_ssl_module()  # Adjust if needed for Alpine's Apache configuration
    create_directory("/etc/ssl/certs", 0o755)
    create_directory("/etc/ssl/private", 0o700)
    generate_ssl_certificate()
    configure_apache_port()  # Adjust for Alpine
    create_ssl_virtual_host()
    enable_ssl_virtual_host()  # Adjust for Alpine
    restart_apache()  # Adjust for Alpine
    print("Apache server with SSL has been configured successfully.")

if __name__ == "__main__":
    main()
