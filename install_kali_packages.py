import subprocess

def install_kali_packages():
    try:
        # Update the package list
        print("Updating package list...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)

        # Upgrade existing packages
        print("Upgrading existing packages...")
        subprocess.run(["sudo", "apt-get", "upgrade", "-y"], check=True)

        # Install Kali Linux's metapackages
        print("Installing Kali Linux dependencies and tools...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "kali-linux-all"], check=True)

        print("All dependencies and tools have been installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have sufficient disk space, network connectivity, and proper permissions.")

if __name__ == "__main__":
    install_kali_packages()