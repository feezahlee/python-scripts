import subprocess

def docker_exec(command):
    try:
        subprocess.run(f"docker exec clab-firstlab-linux-client bash -c '{command}'", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def add_google_signing_key():
    docker_exec("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")

def install_packages(packages):
    for package in packages:
        docker_exec(f"apt-get update && apt-get install -y {package}")

def main():
    # Add Google Linux signing key
    add_google_signing_key()

    # List of packages to install
    packages = ['net-tools', 'iproute2', 'wget', 'python3']

    # Install required packages inside the container
    install_packages(packages)

    # Configure IP address on eth1
    docker_exec("ip addr add 192.168.1.100/24 dev eth1")

    # Add route to Apache server subnet
    docker_exec("ip route add 192.168.2.0/24 dev eth1")

if __name__ == "__main__":
    main()
