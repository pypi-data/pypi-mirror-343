from setuptools import setup, find_packages

setup(
    name='wasengine',  # PyPI name (must be unique)
    version='1.0.4',
    description='Blizzard API Simulation Engine for Lua Addon Testing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='chadricksoup@gmail.com',
    url='https://github.com/WAStudios/WASEngine',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'lupa',
        'gdown'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
