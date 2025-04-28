from setuptools import setup, find_packages
from setuptools.command.install import install
import os

# Custom install class to trigger `update_config()` automatically after install
class PostInstallCommand(install):
    def run(self):
        # Call the original install process
        install.run(self)
        # Now that the package is installed, call the setup function
        from chatgpt_uoapi.utils import update_config
        update_config()
        print("Post-install setup completed!")

setup(
    name='chatgpt_uoapi',
    version='1.1.1',
    packages=['chatgpt_uoapi'],
    include_package_data=True,
    install_requires=[
        "selenium>=4.29.0",
        "undetected_chromedriver>=3.5.5",
        "webdriver_manager>=4.0.2",
        "pyperclip>=1.9.0",
        "setuptools>=75.8.2",
        "pyyaml>=6.0.2"
    ],
    cmdclass={
        'install': PostInstallCommand,  # Register the custom command
    },
    entry_points={
        'console_scripts': [
            # Any other command-line scripts if needed
        ],
    },
)
