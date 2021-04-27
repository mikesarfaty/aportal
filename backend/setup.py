import setuptools

setuptools.setup(
    name="APortal Server",
    version="0.0.1",
    author="Mike Sarfaty",
    author_email="mike.sarfaty (at) gmail",
    description="back end academic portal for HZ Beta Theta Pi",
    url="https://github.com/mikesarfaty/hzportal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['PyJWT==2.0.1',
                      'PyMySQL==1.0.2',
                      'Flask==1.1.2',
                      'bcrypt==3.2.0']
)
