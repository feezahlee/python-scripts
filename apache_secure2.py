import subprocess
import os

ssl_certificate_path = "/usr/local/apache2/conf/server.crt"
ssl_certificate_key_path = "/usr/local/apache2/conf/server.key"
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

def create_directories_and_copy_certificates():
    print("Creating directories and copying SSL certificates...")
    run_command(f'docker exec {container_name} mkdir -p /usr/local/apache2/conf/ssl')
    run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/csr.crt /usr/local/apache2/conf/ssl/server.crt')
    run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/csr.key /usr/local/apache2/conf/ssl/server.key')

def update_httpd_ssl_conf():
    print("Updating httpd-ssl.conf with SSL settings...")
    ssl_conf_content = f"""
<IfModule ssl_module>
    Listen 443
    SSLPassPhraseDialog builtin
    SSLSessionCache shmcb:/usr/local/apache2/logs/ssl_scache(512000)
    SSLSessionCacheTimeout 300
    SSLMutex file:/usr/local/apache2/logs/ssl_mutex
    SSLCertificateFile "{ssl_certificate_path}"
    SSLCertificateKeyFile "{ssl_certificate_key_path}"
    <VirtualHost _default_:443>
        ServerAdmin webmaster@localhost
        DocumentRoot "/usr/local/apache2/htdocs"
        ErrorLog "logs/ssl_error_log"
        CustomLog "logs/ssl_access_log" common
        SSLEngine on
    </VirtualHost>
</IfModule>
"""
    ssl_conf_path = "/usr/local/apache2/conf/extra/httpd-ssl.conf"
    with open("httpd-ssl.conf", 'w') as file:
        file.write(ssl_conf_content)
    run_command(f"docker cp httpd-ssl.conf {container_name}:{ssl_conf_path}")
    os.remove("httpd-ssl.conf")

def include_ssl_conf():
    print("Including httpd-ssl.conf in main configuration...")
    run_command(f"docker exec {container_name} sh -c 'echo \"Include conf/extra/httpd-ssl.conf\" >> /usr/local/apache2/conf/httpd.conf'")

def load_ssl_modules():
    print("Loading SSL and socache_shmcb modules...")
    modules_line = "LoadModule ssl_module modules/mod_ssl.so\nLoadModule socache_shmcb_module modules/mod_socache_shmcb.so"
    with open("httpd-modules.conf", 'w') as file:
        file.write(modules_line)
    run_command(f"docker cp httpd-modules.conf {container_name}:/usr/local/apache2/conf/httpd.conf")
    os.remove("httpd-modules.conf")

def restart_apache():
    print("Restarting Apache server...")
    stdout, stderr = run_command(f"docker exec {container_name} apachectl restart")
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
    install_apache_and_openssl()
    create_directories_and_copy_certificates()
    update_httpd_ssl_conf()
    include_ssl_conf()
    load_ssl_modules()
    restart_apache()
    remove_default_index_html()
    copy_testing_html()
    set_permissions()
    print("Apache server with SSL has been configured successfully.")

if __name__ == "__main__":
    main()
