from setuptools import setup, find_packages

setup(
    name='leoambrose',  # Your package name
    version='0.1.0',  # Version number (we will update this as needed)
    packages=find_packages(where='src'),  # Assuming your code is inside the 'src' folder
    package_dir={'': 'src'},
    install_requires=[
        # Add any external dependencies here, for example:
        # 'numpy',
    ],
    author="vijaysharonl",  # Replace with your name
    author_email="vijaysharonl2005@gmail.com",  # Replace with your email
    description="Hehe Enjoy Mate",
    long_description=open('README.md').read(),  # Your README file will be included
    long_description_content_type="text/markdown",
    url="https://github.com/vijaysharonl/leo",  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        # Add more if necessary
    ],
    python_requires='>=3.7',  # Minimum Python version
)
