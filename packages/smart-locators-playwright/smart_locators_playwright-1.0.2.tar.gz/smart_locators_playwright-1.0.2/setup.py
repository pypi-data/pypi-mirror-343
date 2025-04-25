from setuptools import setup, find_packages

setup(
    name='smart-locators-playwright', 
    version='1.0.2',              
    packages=find_packages(),     
    install_requires=[
        'playwright',
    ],
    author='Manikandan Baskaran',  # Author's name
    author_email='manikandan.baskaran.15@gmail.com',  # Author's email
    description='A simplified Python-playwright utility that provides more flexible locator strategies which is easier for users.',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/thereal-manish/smart-locators-playwright/', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3'
)
