from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
setup(
    name="py-solanautil",          
    version="2.1.5",                  
    description="Python Solana Util for Humans",   
    long_description=readme, 
    long_description_content_type="text/markdown", 
    author="Gusarich Tede",
    author_email="danielsedovzzz@gmail.com",
    url="",   
    packages=find_packages(where="src"),   
    package_dir={"": "src"},  
    include_package_data=True,  
    package_data={
        'sol': ['*.so', '*.pyd'],  
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  
    install_requires=[       
        "construct>=2.10.68",
        "PyNaCl>=1.5.0",
        "base58>=2.1.1",
        "requests>=2.32.3",
        "aiohttp>=3.11.12",
        "pycryptodome",
    ],
)
