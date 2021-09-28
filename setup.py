# Classification (U)

"""Program:  setup.py

    Description:  A setuptools based setup module.

"""

# Libraries and Global Variables

# Standard
import os
import setuptools

# Third-party

# Local
import version


# Read in long description from README file.
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f_hdlr:
    LONG_DESCRIPTION = f_hdlr.read()

setuptools.setup(
    name="Mail_RabbitMQ",
    description="Process an email message and send it to the RabbitMQ queue",
    author="Mark Pernot",
    author_email="Mark.J.Pernot@coe.ic.gov",
    url="https://sc.appdev.proj.coe.ic.gov/JAC-DSXD/mail-rabbitmq",
    version=version.__version__,
    platforms=["Linux"],
    long_description=LONG_DESCRIPTION,

    classifiers=[
        # Common Values:
        #  1 - Pre-Alpha
        #  2 - Alpha
        #  3 - Beta
        #  4 - Field
        #  5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Linux",
        "Operating System :: Linux :: Centos",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Message",
        "Topic :: Message :: RabbitMQ",
        "Topic :: Message :: RabbitMQ :: 3.6.6",
        "Topic :: Message :: RabbitMQ :: 3.8.2",
        "Topic :: Server",
        "Topic :: Server :: Mail"])
