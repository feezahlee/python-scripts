import subprocess

def docker_exec(command):
    try:
        subprocess.run(f"docker exec clab-firstlab-apache-server bash -c '{command}'", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def install_packages(packages):
    for package in packages:
        docker_exec(f"apt-get update && apt-get install -y {package}")

def main():
    # List of packages to install
    packages = ['net-tools', 'iputils-ping', 'iproute2', 'wget', 'vim']

    # Install required packages inside the container
    install_packages(packages)
    
    # Configure IP address on eth1
    docker_exec("ip addr add 192.168.2.2/24 dev eth1")

    # Add route to Linux client subnet
    docker_exec("ip route add 192.168.1.0/24 dev eth1")

if __name__ == "__main__":
    main()
