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
    stdout, stderr = run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt')
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    stdout, stderr = run_command(f'docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key')
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

def update_httpd_ssl_conf():
    print("Updating httpd-ssl.conf with SSL settings...")
    ssl_conf_content = """
ServerName 192.168.2.2
<IfModule ssl_module>
    Listen 443
    SSLPassPhraseDialog builtin
    SSLSessionCache shmcb:/usr/local/apache2/logs/ssl_scache(512000)
    SSLSessionCacheTimeout 300
    SSLCertificateFile "/usr/local/apache2/conf/server.crt"
    SSLCertificateKeyFile "/usr/local/apache2/conf/server.key"
    <VirtualHost _default_:443>
        ServerAdmin webmaster@localhost
        DocumentRoot "/usr/local/apache2/htdocs"
        ErrorLog "logs/ssl_error_log"
        SSLEngine on
    </VirtualHost>
</IfModule>
"""
    with open("httpd-ssl.conf", 'w') as file:
        file.write(ssl_conf_content)
    stdout, stderr = run_command(f"docker cp httpd-ssl.conf {container_name}:/usr/local/apache2/conf/extra/httpd-ssl.conf")
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    stdout, stderr = run_command(f"rm httpd-ssl.conf")
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

def include_ssl_conf():
    print("Including httpd-ssl.conf in main configuration...")
    stdout, stderr = run_command(f"docker exec {container_name} sh -c 'echo \"Include conf/extra/httpd-ssl.conf\" >> /usr/local/apache2/conf/httpd.conf'")
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

def load_ssl_modules():
    print("Loading SSL, socache_shmcb, and MPM modules...")
    # Check if modules are already present
    modules_line = (
        "LoadModule ssl_module modules/mod_ssl.so\n"
        "LoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n"
        "LoadModule mpm_prefork_module modules/mod_mpm_prefork.so"
    )
    
    # Append the lines only if they are not already present
    current_conf, _ = run_command(f"docker exec {container_name} cat /usr/local/apache2/conf/httpd.conf")
    
    if not all(module in current_conf for module in modules_line.splitlines()):
        stdout, stderr = run_command(f"docker exec {container_name} sh -c 'echo \"{modules_line}\" >> /usr/local/apache2/conf/httpd.conf'")
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
    else:
        print("Modules are already loaded in httpd.conf")


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
