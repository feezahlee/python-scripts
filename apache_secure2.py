import subprocess

def run_command(command):
    """Function to run shell commands."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{command}' executed successfully.")
    else:
        print(f"Error executing '{command}': {result.stderr}")
        raise Exception(result.stderr)

def configure_ssl_on_apache():
    """Configure SSL on Apache server."""
    # Rename and move SSL certificate
    run_command("docker exec clab-firstlab-apache-server cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")

    # Rename and move SSL key
    run_command("docker exec clab-firstlab-apache-server cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")

    # Update httpd-ssl.conf with SSL settings
    ssl_conf_path = "/usr/local/apache2/conf/extra/httpd-ssl.conf"
    ssl_conf_content = """
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
"""

    # Append SSL configuration to httpd-ssl.conf
    with open("httpd-ssl.conf", "w") as ssl_conf_file:
        ssl_conf_file.write(ssl_conf_content)

    run_command("docker cp httpd-ssl.conf clab-firstlab-apache-server:/usr/local/apache2/conf/extra/httpd-ssl.conf")

    # Include httpd-ssl.conf in main configuration if not already included
    httpd_conf_path = "/usr/local/apache2/conf/httpd.conf"
    include_directive = "Include conf/extra/httpd-ssl.conf"
    
    with open("httpd.conf", "r+") as httpd_conf_file:
        lines = httpd_conf_file.readlines()
        if include_directive not in lines:
            httpd_conf_file.write(f"\n{include_directive}\n")
    
    run_command("docker cp httpd.conf clab-firstlab-apache-server:/usr/local/apache2/conf/httpd.conf")

    # Load SSL and socache_shmcb modules if not already loaded
    ssl_module = "LoadModule ssl_module modules/mod_ssl.so"
    socache_module = "LoadModule socache_shmcb_module modules/mod_socache_shmcb.so"
    
    with open("httpd.conf", "r+") as httpd_conf_file:
        lines = httpd_conf_file.readlines()
        if ssl_module not in lines:
            httpd_conf_file.write(f"\n{ssl_module}\n")
        if socache_module not in lines:
            httpd_conf_file.write(f"{socache_module}\n")

    run_command("docker cp httpd.conf clab-firstlab-apache-server:/usr/local/apache2/conf/httpd.conf")

    # Update index.html content
    index_html_path = "/usr/local/apache2/htdocs/index.html"
    index_html_content = """
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
"""

    # Write new content to index.html
    with open("index.html", "w") as index_html_file:
        index_html_file.write(index_html_content)

    run_command("docker cp index.html clab-firstlab-apache-server:/usr/local/apache2/htdocs/index.html")

    # Restart Apache to apply changes
    run_command("docker exec clab-firstlab-apache-server apachectl restart")

def execute_script_in_container():
    """Function to execute the Python script inside the Docker container."""
    container_name = "clab-firstlab-apache-server"
    script_path = "/root/configure_ssl.py"
    
    # Copy the script into the container
    run_command(f"docker cp configure_ssl.py {container_name}:{script_path}")
    
    # Execute the script inside the container
    run_command(f"docker exec {container_name} python3 {script_path}")

if __name__ == "__main__":
    configure_ssl_on_apache()
    execute_script_in_container()
