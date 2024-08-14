Started by user admin
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/apache python
[Pipeline] {
[Pipeline] stage
[Pipeline] { (checkout)
[Pipeline] checkout
The recommended git tool is: NONE
No credentials specified
 > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/apache python/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/feezahlee/python-scripts.git # timeout=10
Fetching upstream changes from https://github.com/feezahlee/python-scripts.git
 > git --version # timeout=10
 > git --version # 'git version 2.25.1'
 > git fetch --tags --force --progress -- https://github.com/feezahlee/python-scripts.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision f1bdd7daef2ea3663e3cb4d7776940e930372092 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f f1bdd7daef2ea3663e3cb4d7776940e930372092 # timeout=10
Commit message: "Update apache_secure2.py"
 > git rev-list --no-walk 59a4a8fb835cb1572eaf5ba01918ac6aa663ee44 # timeout=10
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (build)
[Pipeline] git
The recommended git tool is: NONE
No credentials specified
 > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/apache python/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/feezahlee/python-scripts.git # timeout=10
Fetching upstream changes from https://github.com/feezahlee/python-scripts.git
 > git --version # timeout=10
 > git --version # 'git version 2.25.1'
 > git fetch --tags --force --progress -- https://github.com/feezahlee/python-scripts.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision f1bdd7daef2ea3663e3cb4d7776940e930372092 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f f1bdd7daef2ea3663e3cb4d7776940e930372092 # timeout=10
 > git branch -a -v --no-abbrev # timeout=10
 > git branch -D main # timeout=10
 > git checkout -b main f1bdd7daef2ea3663e3cb4d7776940e930372092 # timeout=10
Commit message: "Update apache_secure2.py"
[Pipeline] sh
+ python3 apache_secure2.py
Configuring SSL on Apache Server...


Command 'sudo docker exec clab-firstlab-apache-server echo "
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
" > /usr/local/apache2/conf/extra/httpd-ssl.conf' failed with error: /bin/sh: 1: cannot create /usr/local/apache2/conf/extra/httpd-ssl.conf: Directory nonexistent

Command 'sudo docker exec clab-firstlab-apache-server echo "Include conf/extra/httpd-ssl.conf
" >> /usr/local/apache2/conf/httpd.conf' failed with error: /bin/sh: 1: cannot create /usr/local/apache2/conf/httpd.conf: Directory nonexistent

Command 'sudo docker exec clab-firstlab-apache-server echo "LoadModule ssl_module modules/mod_ssl.so
LoadModule socache_shmcb_module modules/mod_socache_shmcb.so
" >> /usr/local/apache2/conf/httpd.conf' failed with error: /bin/sh: 1: cannot create /usr/local/apache2/conf/httpd.conf: Directory nonexistent

Command 'sudo docker exec clab-firstlab-apache-server apachectl restart' failed with error: [Wed Aug 14 03:55:12.428876 2024] [so:warn] [pid 1241:tid 1241] AH01574: module ssl_module is already loaded, skipping
[Wed Aug 14 03:55:12.428912 2024] [so:warn] [pid 1241:tid 1241] AH01574: module socache_shmcb_module is already loaded, skipping
AH00534: httpd: Configuration error: No MPM loaded.

[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Test)
[Pipeline] echo
the job has been tested
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
