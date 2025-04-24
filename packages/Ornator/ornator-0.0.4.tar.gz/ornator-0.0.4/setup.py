from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()
    
#print(load_requirements("requirements.txt"))

setup(
    name='Ornator',
    version='0.0.4',
    description="""This library provides a robust set of decorators for enhancing Python code functionality. It includes:
 *Base decorator classes for extensibility *Monitoring and logging capabilities *Validation and security features *Caching and performance optimization *Support for both functions and classes""",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Conectar Wali SAS',
    author_email='dev@conectarwalisas.com.co',
    url='https://github.com/ConectarWali/Ornator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license_files=['LICENSE'],
    python_requires='>=3.9',
)
