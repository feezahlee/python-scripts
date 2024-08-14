import subprocess

def run_command_in_container(command):
    """Execute a shell command in the Apache server Docker container and print its output."""
    full_command = f"sudo docker exec clab-firstlab-apache-server {command}"
    try:
        result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command '{full_command}' failed with error: {e.stderr}")

def copy_file(source, destination):
    """Copy a file from source to destination inside the Docker container."""
    command = f"cp {source} {destination}"
    run_command_in_container(command)

def update_httpd_ssl_conf():
    """Update the httpd-ssl.conf with SSL settings inside the Docker container."""
    ssl_settings = """
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
    command = f'echo "{ssl_settings}" > /usr/local/apache2/conf/extra/httpd-ssl.conf'
    run_command_in_container(command)

def update_httpd_conf():
    """Update the main httpd.conf file to include the SSL configuration and load modules inside the Docker container."""
    httpd_conf_path = "/usr/local/apache2/conf/httpd.conf"
    ssl_include = "Include conf/extra/httpd-ssl.conf\n"
    ssl_modules = "LoadModule ssl_module modules/mod_ssl.so\nLoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n"

    # Appending SSL configurations to the main httpd.conf file
    run_command_in_container(f'echo "{ssl_include}" >> {httpd_conf_path}')
    run_command_in_container(f'echo "{ssl_modules}" >> {httpd_conf_path}')

def restart_apache():
    """Restart the Apache server to apply changes inside the Docker container."""
    run_command_in_container("apachectl restart")

def configure_apache_ssl():
    """Main function to configure SSL on Apache inside the Docker container."""
    print("Configuring SSL on Apache Server...")
    copy_file("/usr/local/apache2/conf/ssl/apache.crt", "/usr/local/apache2/conf/server.crt")
    copy_file("/usr/local/apache2/conf/ssl/apache.key", "/usr/local/apache2/conf/server.key")
    update_httpd_ssl_conf()
    update_httpd_conf()
    restart_apache()

if __name__ == "__main__":
    configure_apache_ssl()
