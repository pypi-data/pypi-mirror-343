from setuptools import setup, find_packages
setup(
    name='mlflow_log_module',
    version='1.0.0',
    packages=find_packages(),
    description='A package to log the params, metrics and artifacts to mlflow ui.',
    author='Radhika Menon',
    author_email='Radhika.Menon@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)