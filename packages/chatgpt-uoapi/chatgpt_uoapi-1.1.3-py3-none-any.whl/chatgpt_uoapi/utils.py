import os
import sys
import yaml

CONFIG_PATH = os.path.abspath('config.yaml')



def get_chrome_profile_path():
    """Creates a new profile (directory) and returns the its path (Chrome profile path) based on the OS.
    """
    if sys.platform.startswith("win"):
        base_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data")
    elif sys.platform.startswith("darwin"):  # macOS
        base_path = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif sys.platform.startswith("linux"):
        base_path = os.path.expanduser("~/.config/google-chrome")
    else:
        raise OSError("Unsupported operating system")

    try:
        path = os.path.join(base_path, 'chatgpt-api')
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print('Failed to create new profile directory under chrome profiles. Error: {e}')
        
    return path


def update_config() -> bool:
    path = get_chrome_profile_path()
    config = {
        'PROFILE_PATH': path
    }

    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file)


def load_config() -> dict:
    with open(CONFIG_PATH, 'r') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    update_config()