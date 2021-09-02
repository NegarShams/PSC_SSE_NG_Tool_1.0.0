REM
REM #######################################################################################################################
REM ###										SSE Missing Packages Installer                                              ###
REM ###		Script sets up Python on SSE machines for use with PSSE and the scripts produced by PSC                     ###
REM ###			                                                                                                        ###
REM ###		These packages will be installed in a sub directory <local_packages> of the directory the batch file is run ###
REM ###     in and so should be located somewhere with suitable write permissions so that                               ###
REM ###     administrative privileges if the batch file is located in the users directory. The package 		            ###
REM ###     installation is completed using python 2.7 and pip, since sometimes the PSSE installation does not  	    ###
REM ###     have pip installed it is provided as part of this package.                                           	    ###
REM ###									                                                                                ###
REM ###		Also, since python is not defined as an environment variable as part of the standard installation the file  ###
REM ###		will search for python 2.7 installation on the C drive.  If a different drive is necessary then the         ###
REM ###		user will need to change the search path                                                                    ###
REM ###															                                                        ###
REM ###		Code developed by David Mills (david.mills@PSCconsulting.com, +44 7899 984158) as part of PSC 		        ###
REM ###		project JK7938 - SHEPD - studies and automation                                                								###
REM ###															                                                        ###
REM #######################################################################################################################
REM """

REM Required inputs are python.exe, location of python wheels, target installation location

@echo off
REM The following lines ensure all outputs are saved to a log file
echo "Defining target directories for python package installation and finding python executable"
REM define variables for current directory and target directory for the packages to be installed in
set python_exe=%1
set package_dir=%2
set target_dir=%3

echo %python_exe%
echo %package_dir%
echo %target_dir%

echo "Python wheels should be located here: "%package_dir%
echo "Python packages will be installed here: "%target_dir%

REM If the target directory for the new scripts does not exist then this will be created
if not exist %target_dir% mkdir %target_dir%

REM Break command to exit for loop once python file has been found to avoid continuing to search
echo "Python installation here to be used: ""%pythonpath%

REM Define pip executable file which will be used to install all the wheels
set pip_execute=%package_dir%\pip-19.2.3-py2.py3-none-any.whl/pip

REM Install each of the defined wheel files in the local directory, forcing a replacement if they already exist
REM and avoiding the downloading of dependencies.  Therefore all dependencies will need to be installed manually in
REM here.
REM Output turned on so progress of installation can be monitored
echo on
echo "Any errors mean a package did not install and should be investigated further"
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\setuptools-44.1.1-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\six-1.12.0-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\python_dateutil-2.8.1-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\pytz-2019.3-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\et_xmlfile-1.0.1-cp27-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\numpy-1.16.5-cp27-cp27m-win32.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\pandas-0.24.2-cp27-cp27m-win32.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\XlsxWriter-1.2.9-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\dill-0.3.3-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\xlrd-1.2.0-py2.py3-none-any.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\scipy-1.2.3-cp27-cp27m-win32.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\MarkupSafe-1.1.1-cp37-cp37m-win32.whl
%python_exe% %pip_execute% install --no-deps --target=%target_dir% --upgrade --force-reinstall %package_dir%\Jinja2-2.11.2-py2.py3-none-any.whl


echo "All python packages have been installed."
exit
