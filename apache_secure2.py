import subprocess
import os

ssl_certificate_path = "/etc/ssl/certs/apache-selfsigned.crt"
ssl_certificate_key_path = "/etc/ssl/private/apache-selfsigned.key"
server_name = "192.168.2.2"
container_name = "clab-firstlab-apache-server"

def run_command(command, check=True):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr.decode()}")
        return None, e.stderr.decode()

def install_apache_and_openssl():
    print("Installing Apache and OpenSSL...")
    stdout, stderr = run_command(f'docker exec {container_name} apt-get update')
    print(stdout, stderr)
    stdout, stderr = run_command(f'docker exec {container_name} apt-get install -y apache2 openssl')
    print(stdout, stderr)

def enable_ssl_module():
    print("Enabling SSL module in Apache...")
    stdout, stderr = run_command(f'docker exec {container_name} a2enmod ssl')
    print(stdout, stderr)

def create_directory(path, mode):
    print(f"Creating directory {path} with mode {mode}...")
    run_command(f'docker exec {container_name} mkdir -p {path}')
    run_command(f'docker exec {container_name} chmod {mode} {path}')

def generate_ssl_certificate():
    print("Generating a self-signed SSL certificate...")
    command = (
        f"docker exec {container_name} openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 "
        f"-keyout {ssl_certificate_key_path} -out {ssl_certificate_path} "
        f'-subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN={server_name}"'
    )
    stdout, stderr = run_command(command)
    print(stdout, stderr)

def configure_apache_ports():
    print("Configuring Apache to listen on ports 80 and 443...")
    ports_conf_path = "/etc/apache2/ports.conf"
    run_command(f"docker exec {container_name} sed -i 's/^#?Listen 80/Listen 80/' {ports_conf_path}")
    run_command(f"docker exec {container_name} sed -i 's/^#?Listen 443/Listen 443/' {ports_conf_path}")

def create_ssl_virtual_host():
    print("Creating SSL Virtual Host file...")
    ssl_virtual_host_content = f"""
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        DocumentRoot /usr/local/apache2/htdocs
        DirectoryIndex index2.html
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
    ssl_config_path = "/etc/apache2/sites-available/default-ssl.conf"
    with open("default-ssl.conf", 'w') as file:
        file.write(ssl_virtual_host_content)
    run_command(f"docker cp default-ssl.conf {container_name}:{ssl_config_path}")
    os.remove("default-ssl.conf")

def create_http_virtual_host():
    print("Creating HTTP Virtual Host file...")
    http_virtual_host_content = f"""
<VirtualHost *:80>
    DocumentRoot /usr/local/apache2/htdocs
    DirectoryIndex index2.html
    <Directory /usr/local/apache2/htdocs/>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""
    http_config_path = "/etc/apache2/sites-available/000-default.conf"
    with open("000-default.conf", 'w') as file:
        file.write(http_virtual_host_content)
    run_command(f"docker cp 000-default.conf {container_name}:{http_config_path}")
    os.remove("000-default.conf")

def enable_ssl_virtual_host():
    print("Enabling SSL Virtual Host...")
    stdout, stderr = run_command(f"docker exec {container_name} a2ensite default-ssl.conf")
    print(stdout, stderr)

def restart_apache():
    print("Restarting Apache server...")
    stdout, stderr = run_command(f"sudo docker exec {container_name} systemctl restart apache2")
    print(stdout, stderr)

def copy_testing_html():
    print("Copying index2.html to the Apache document root...")
    run_command(f"docker cp index2.html {container_name}:/usr/local/apache2/htdocs/")

def remove_default_index_html():
    print("Removing default index.html if it exists...")
    run_command(f"docker exec {container_name} rm -f /usr/local/apache2/htdocs/index.html")

def set_permissions():
    print("Setting correct permissions for index2.html...")
    run_command(f"docker exec {container_name} chmod 644 /usr/local/apache2/htdocs/index2.html")
    run_command(f"docker exec {container_name} chown www-data:www-data /usr/local/apache2/htdocs/index2.html")

def main():
    print("Entering Docker container clab-firstlab-apache-server...")
    run_command(f'sudo docker exec -it {container_name} bash -c')  # Ensure we're using the correct shell environment
    print("Entered Docker container clab-firstlab-apache-server.")
    install_apache_and_openssl()
    enable_ssl_module()
    create_directory("/etc/ssl/certs", "755")
    create_directory("/etc/ssl/private", "700")
    generate_ssl_certificate()
    configure_apache_ports()
    create_ssl_virtual_host()
    create_http_virtual_host()
    enable_ssl_virtual_host()
    remove_default_index_html()
    copy_testing_html()
    set_permissions()
    restart_apache()
    print("Apache server with SSL has been configured successfully and testing.html is available.")

if __name__ == "__main__":
    main()
