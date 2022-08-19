# Software-for-determing-pacient-s-diagnosis
Application that helps doctors to determine pacient's diagnosis.

**
About this project
**

    This project was completed in 2019, as a final project for Grade 3 of high school.
    
**
How to create a Python 3 virtual environment in Windows 10
**

    ---------------------------------------------------------------------
    Creating a virtual environment on Windows 10 with Python3 venv module
    ---------------------------------------------------------------------

    Once you had completed the installation of Python 3 on Windows 10, you will be ready to create the virtual environment for your application. In order to do so, open up a command prompt window and type the following command:

    python -m venv %systemdrive%%homepath%\my-venv

    After the command completes, you will find the my-venv directory inside your home directory. Inside the my-venv, you will find the Python artefacts for your isolated virtual environment.

    ----------------------------------------------------------
    Activating your Python 3 virtual environment on Windows 10
    ----------------------------------------------------------

    Before you can run your Python 3 application inside of your Python 3 virtual environment, you will need to activate it. In order to activate your virtual environment, you will need to run the activate.bat script located inside your virtual environment directory.

    For example, to activate the virtual environment inside my-venv, you can run the following command in your command prompt window:

    %systemdrive%%homepath%\my-venv\Scripts\activate.bat

    After the activate.bat script had ran, you will see the prompt appended with (my-venv)

    -------------------------------------------------------------------------------------
    Installing Python 3 dependencies into your Python 3 virtual environment on Windows 10
    -------------------------------------------------------------------------------------

    When you had activated your virtual environment, you can then install your Python 3 dependencies into your Python 3 virtual environment on Windows 10. For example, you can install the requests library for your Python 3 application to download a file from a HTTP server or upload a file to a HTTP server:

    pip install -r requirements.txt

    ----------------------------------------------------------------------------------------
    Running your Python 3 application inside your Python 3 virtual environment on Windows 10
    ----------------------------------------------------------------------------------------

    Subsequently, when you had installed all the needed dependencies, you can then run your Python 3 application with the python binary:

    python a_python_application.py

    ------------------------------------------------------------
    Deactivating your Python 3 virtual environment on Windows 10
    ------------------------------------------------------------

    When you want to get out of your Python 3 virtual environment on Windows 10, you can simply run the following command:

    deactivate

    After the virtual environment is deactivated, your command prompt will switch to the global Python 3 environment. In addition, those Python 3 dependencies that you had installed in your virtual environment will not be available.

**
How to run this application
**

	Source point is SODP.py file. You need to have Python installed on your PC (https://www.python.org/downloads/).
	
