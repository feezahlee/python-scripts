import subprocess

def install_packages(packages):
    for package in packages:
        subprocess.run(['sudo', 'apt-get', 'install', '-y', package], check=True)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def main():
    # List of packages to install
    packages = ['net-tools', 'iputils-ping', 'iproute2', 'wget', 'vim']

    # Install required packages
    install_packages(packages)

    # Remove old IP address from eth1
    run_command("ip addr del 192.168.2.4/24 dev eth1")

    # Configure IP address on eth1
    run_command("ip addr add 192.168.2.2/24 dev eth1")

    # Add route to Linux client subnet
    run_command("ip route add 192.168.1.0/24 dev eth1")

if __name__ == "__main__":
    main()
