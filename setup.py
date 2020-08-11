from setuptools import setup, find_packages

version = "1.0.1"

setup(
    name="senaite.panic",
    version=version,
    description="Panic level alerts for SENAITE",
    long_description=open("README.rst").read() + "\n" +
    open("CHANGES.rst").read() + "\n",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords=['senaite', 'lims', 'opensource'],
    author="RIDING BYTES & NARALABS",
    author_email="senaite@senaite.com",
    url="https://github.com/senaite/senaite.panic",
    license="GPLv2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "senaite.lims>=1.3.4",
        "requests",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "Products.SecureMailHost",
            "plone.app.testing",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
