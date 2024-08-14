import subprocess

def run_command(command):
    """Execute a shell command and print its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr}")

def copy_file(source, destination):
    """Copy a file from source to destination."""
    command = f"cp {source} {destination}"
    run_command(command)

def update_httpd_ssl_conf():
    """Update the httpd-ssl.conf with SSL settings."""
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
    with open("/usr/local/apache2/conf/extra/httpd-ssl.conf", "w") as file:
        file.write(ssl_settings)

def update_httpd_conf():
    """Update the main httpd.conf file to include the SSL configuration and load modules."""
    httpd_conf_path = "/usr/local/apache2/conf/httpd.conf"
    ssl_include = "Include conf/extra/httpd-ssl.conf\n"
    ssl_modules = "LoadModule ssl_module modules/mod_ssl.so\nLoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n"

    with open(httpd_conf_path, "a") as file:
        file.write(ssl_include)
        file.write(ssl_modules)

def restart_apache():
    """Restart the Apache server to apply changes."""
    run_command("apachectl restart")

def configure_apache_ssl():
    """Main function to configure SSL on Apache."""
    print("Configuring SSL on Apache Server...")
    copy_file("/usr/local/apache2/conf/ssl/apache.crt", "/usr/local/apache2/conf/server.crt")
    copy_file("/usr/local/apache2/conf/ssl/apache.key", "/usr/local/apache2/conf/server.key")
    update_httpd_ssl_conf()
    update_httpd_conf()
    restart_apache()

if __name__ == "__main__":
    configure_apache_ssl()
