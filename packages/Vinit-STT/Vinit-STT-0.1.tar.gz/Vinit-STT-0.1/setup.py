from setuptools import setup,find_packages 

setup(
    name= 'Vinit-STT',
    version='0.1',
    author='Vinit Kumar Jha',
    author_email='vinitjha2712@gmail.com',
    description='This is a speech to text package created by Vinit Kumar Jha',
)
packages = find_packages()
install_requirement = [
    'selenium',
    'webdriver_manager',

]
