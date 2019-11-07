import setuptools

with open("gateway_package/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gateway-pkg-CGF",
    version="0.0.1",
    license="MIT",
    author="Matthew Ashley",
    author_email="matthewashley@verntechnologies.com",
    description="A package for connecting to and accessing information on BehrTech's gateway computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/matthewashley1/gateway-apis/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
