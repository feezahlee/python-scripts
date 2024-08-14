import subprocess

container_name = "clab-firstlab-apache-server"

def run_command(command, check=True):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr.decode()}")
        return None, e.stderr.decode()

def rename_and_move_certificates():
    print("Renaming and moving SSL certificate and key...")
    run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt')
    run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key')

def update_httpd_ssl_conf():
    print("Updating httpd-ssl.conf with SSL settings...")
    ssl_conf_content = f"""
ServerName 192.168.2.2
<IfModule ssl_module>
    Listen 443
    SSLPassPhraseDialog builtin
    SSLSessionCache shmcb:/usr/local/apache2/logs/ssl_scache(512000)
    SSLSessionCacheTimeout 300
    SSLMutex file:/usr/local/apache2/logs/ssl_mutex
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
    with open("httpd-ssl.conf", 'w') as file:
        file.write(ssl_conf_content)
    run_command(f"docker cp httpd-ssl.conf {container_name}:/usr/local/apache2/conf/extra/httpd-ssl.conf")
    run_command(f"rm httpd-ssl.conf")

def include_ssl_conf():
    print("Including httpd-ssl.conf in main configuration...")
    run_command(f"docker exec {container_name} sh -c 'echo \"Include conf/extra/httpd-ssl.conf\" >> /usr/local/apache2/conf/httpd.conf'")

def load_ssl_modules():
    print("Loading SSL and socache_shmcb modules...")
    ssl_modules_line = "LoadModule ssl_module modules/mod_ssl.so\nLoadModule socache_shmcb_module modules/mod_socache_shmcb.so"
    run_command(f"docker exec {container_name} sh -c 'echo \"{ssl_modules_line}\" >> /usr/local/apache2/conf/httpd.conf'")

def restart_apache():
    print("Restarting Apache server...")
    stdout, stderr = run_command(f"docker exec {container_name} apachectl restart")
    print(stdout, stderr)

def main():
    rename_and_move_certificates()
    update_httpd_ssl_conf()
    include_ssl_conf()
    load_ssl_modules()
    restart_apache()
    print("Apache server with SSL has been configured successfully.")

if __name__ == "__main__":
    main()
