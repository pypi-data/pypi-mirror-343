from setuptools import setup

VERSION = '0.1.0'  # The initial release version
DESCRIPTION = 'Email sending functionality package'
LONG_DESCRIPTION = 'A package that allows sending emails via smtp from within a python application.'

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="email-stuff",
    url="https://github.com/george-oconnor/email-stuff",
    version=VERSION,
    author="george.oconnor (George O' Connor)",
    author_email="<george@georgeoc.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["email_stuff"],
    package_dir={'': 'src'},
    install_requires=[],
    keywords=['python', 'email', 'outlook', 'send email', 'email attachments', 'mail', 'gmail', 'smtp'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)