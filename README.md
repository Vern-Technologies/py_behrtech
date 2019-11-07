# Gateway APIs

A custom Python package for interfacing with BehrTech's gateway computers to build applications

___

## Information

To import the package into your local code editor you will need to host the package on a private package 
repository on your machine. This is a private proprietary Python package and is prohibited from being
uploaded to a public Python package repository.  

___

## Private Package Repository Setup Instructions

#### Install PyPI Server

1. Install virtualenv if it's not already installed.

    ```bash
    pip install virtualenv
    ```

2. Create a new directory name packages which will be used to hold the Python package. Create a new virtual environment 
called **venv** inside this directory, then activate.

    ```bash
    mkdir ~/packages
    cd packages
    virtualenv venv
    source venv/bin/activate
    ``` 
   
3. Download PyPI Server through pip in the newly created virtual environment.

    ```bash
    pip install pypiserver
    ```

4. Move both files from the dist directory into the create packages directory.

    ```bash
    mv <python package repo path>/dist/gateway-pkg-CGF-0.0.1.tar.gz <packages dirctory path>/
    mv <python package repo path>/dist/gateway_pkg_CGF-0.0.1-py3-none-any.whl <packages dirctory path>/
    ```
   
5. Launch the server.

    ```bash
    pypi-server -p 8080 <packages directory path>/
    ```
   
___

## Example PyCharm setup

#### Installing package into PyCharm

1. Select PyCharm -> Preferences -> Project Interpreter -> + -> Manage Repositories -> + and add your private 
package repository address and then select ok. Example repository address: http://localhost:8080/simple/

2. Select Ok on the Manage Repositories window and then refresh the Available Packages window.

3. Now you should be able to search for the Gateway APIs package in the Available Packages window with gateway-pkg-CGF.

4. Find the correct package and select Install Package.

5. Once package is install you can start using it to build your applications. Remember to close your running PyPI 
Server by closing your terminal.

---

## Updating To New Package Version

1. To implement a new version of the Gateway APIs package, you just need to replace to file in your packages directory
with the new file from the dist directory in the repo and relaunch your PyPI server.

2. Then re-install the package in PyCharm and your good to go.
