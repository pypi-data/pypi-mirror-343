from setuptools import setup,find_packages

setup(
    name='DhapLu-STT',
    version='0.1',
    author='Subhadip Sarkar',
    author_email='subhadip021@gmail.com',
    description='this is speech to text package created by subhadip sarkar'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_msnsger'
]