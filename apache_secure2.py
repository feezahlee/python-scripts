import subprocess

def run_command(command):
    """Function to run shell commands inside the Docker container."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{command}' executed successfully.")
    else:
        print(f"Error executing '{command}': {result.stderr}")
        raise Exception(result.stderr)

def configure_ssl_certificates(container_name):
    # Rename and move SSL certificate
    run_command(f"docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")

    # Rename and move SSL key
    run_command(f"docker exec {container_name} cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")


def configure_ssl_on_apache():
    container_name = "clab-firstlab-apache-server"
    httpd_conf_path = "/usr/local/apache2/conf/httpd.conf"
    ssl_conf_path = "/usr/local/apache2/conf/extra/httpd-ssl.conf"
    index_html_path = "/usr/local/apache2/htdocs/index.html"

    # Define the necessary modules and settings
    mpm_module = "LoadModule mpm_event_module modules/mod_mpm_event.so"
    ssl_module = "LoadModule ssl_module modules/mod_ssl.so"
    socache_module = "LoadModule socache_shmcb_module modules/mod_socache_shmcb.so"
    include_directive = "Include conf/extra/httpd-ssl.conf"
    
    # Generate httpd.conf content
    httpd_conf_content = f"""
{mpm_module}
{ssl_module}
{socache_module}
{include_directive}
"""

    # Write the generated content to httpd.conf
    with open("httpd.conf", "w") as httpd_conf_file:
        httpd_conf_file.write(httpd_conf_content)
    
    run_command(f"docker cp httpd.conf {container_name}:{httpd_conf_path}")

    # Write SSL configuration
    with open("httpd-ssl.conf", "w") as ssl_conf_file:
        ssl_conf_file.write("""
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
""")
    run_command(f"docker cp httpd-ssl.conf {container_name}:{ssl_conf_path}")

    # Update index.html content
    with open("index.html", "w") as index_html_file:
        index_html_file.write("""
<html>
  <body>
    <h1>Hello I am Yan Yan :))</h1>
    <h2 style="font-family: Arial, sans-serif;">The previous 'It works!' has been changed to this!</h2>
    <h3 style="color: blue;">This webpage has been changed by running Ansible Playbooks from Jenkins.</h3>
    <br><br><br>
    <p>Image:</p>
    <img src="https://www.tp.edu.sg/ecerts/images/banner.jpg" alt="Dog Image" width="500" height="300">
    <br><br><br>
    <p>Video:</p>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/gGcubGOqDHE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <br><br><br>
    <p>All images and videos used are free of copyright and available for public use.</p>
  </body>
</html>
""")
    run_command(f"docker cp index.html {container_name}:{index_html_path}")

    # Restart Apache to apply changes
    run_command(f"docker exec {container_name} apachectl restart")

if __name__ == "__main__":
    configure_ssl_on_apache()

    configure_ssl_certificates(container_name)
