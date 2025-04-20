import subprocess
import os

def clone_repository(repo_url, clone_dir):
    """
    Clones a GitHub repository to a specified directory.

    Parameters:
    - repo_url (str): The URL of the GitHub repository to clone.
    - clone_dir (str): The directory where the repository will be cloned.
    """
    try:
        print(f"Cloning repository from {repo_url} to {clone_dir}...")
        # Run the git clone command
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        print("Repository cloned successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while cloning the repository: {e}")

if __name__ == "__main__":
    # Replace with your repository URL
    repo_url = "https://github.com/dr-kabanga/scientific-AI.git"
    
    # Replace with your desired clone directory
    clone_dir = os.path.join(os.getcwd(), "scientific-AI")
    
    # Clone the repository
    clone_repository(repo_url, clone_dir)