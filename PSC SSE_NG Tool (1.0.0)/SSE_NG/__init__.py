import os
import sys
import time
import subprocess
import shutil

local_packages = os.path.join(os.path.dirname(__file__), 'local_packages')
# Won't be searched unless it exists when added to system path

if not os.path.exists(local_packages):
	os.makedirs(local_packages)
# Insert local_packages to start of path for fault studies
sys.path.insert(0, local_packages)

def find_python_executable():
	"""
		Function finds the python executable that is being used to run this code
	:return str python_exe_path:  Path string to the python executable
	"""
	# Find python executable
	python_exe_path = 'ERROR NO FILE FOUND'
	for dirpath, dirnames, filenames in os.walk(sys.exec_prefix):
		for filename in filenames:
			if filename == 'python.exe':
				python_exe_path = os.path.join(dirpath, filename)
				break

	return python_exe_path

def create_local_packages():
	"""
		Function creates the local packages folder in the very first run of the tool
	:return:
	"""

	# Install local packages time starting
	t0 = time.time()

	package_wheels = os.path.join(os.path.dirname(__file__), 'package_wheels')
	# Confirm wheels actually exist or fail at this point
	if os.path.isdir(package_wheels):
		print(
			'The script will now install '
			'the packages locally which will result in some pop-ups and may take some time, please be patient!!\n\n'
		)
	else:
		print(
			(
				'The directory {} does not exist which is needed to install the python packages, the script '
				'cannot continue.  Please check the original source of this code'
			).format(package_wheels)
		)
		raise ImportError('Python Package Wheels Directory Missing')

	# Wait 500ms and then create a new folder, 500 ms to allow time for deleting to take place
	time.sleep(0.5)
	os.makedirs(local_packages)

	# Find python executable
	python_exe = find_python_executable()

	# Path to batch file that will install the missing packages
	batch_path = os.path.join(os.path.dirname(__file__), 'JK7938_SSE_NG_Missing_Packages.bat')
	# Text files produced when batch file run to control output messages
	batch_install_errors = os.path.join(local_packages, 'batch_install_errors.log')
	batch_log_messages = os.path.join(local_packages, 'batch_install_progress.log')

	print(
		(
			'The following batch file will be run to install the packages: {} to the folder {}.  \n\t'
			'Any error messages during the installation will be recorded in the file: {}\n\t'
			'All log messaged during the installation will be recorded in the file: {}'
		).format(batch_path, local_packages, batch_install_errors, batch_log_messages)
	)
	# Adjusted to use an additional try block to capture if an error occurs
	try:
		# Open file to store errors into
		with open(batch_install_errors, 'w') as f:
			# Now checks whether an error status is returned
			subprocess.check_output(
				[batch_path, python_exe, package_wheels, local_packages, '>' + batch_log_messages],
				stderr=f
			)
		print('Installation of packages completed in  {:.2f} seconds'.format(time.time() - t0))
	except subprocess.CalledProcessError:
		print(
			'Installation of packages failed, check the errors reported in the file {}'.format(
				batch_install_errors)
		)
		raise EnvironmentError('Unable to install python packages')
	return None


# Installs local packages when there is no local packages folder which means that it is the very first installation
if not os.path.isdir(local_packages):
	create_local_packages()
	inst = 'Local packages installed as part of the very first run of the tool'

# Package imports
try:
	# #
	import SSE_NG.common_functions as common_functions
	import SSE_NG.GSP_assigner_function as GSP_assigner_function
	import SSE_NG.BB_assigner_function as BB_assigner_function
	import SSE_NG.aggregator_function as aggregator

except ImportError:
	t0 = time.time()

	package_wheels = os.path.join(os.path.dirname(__file__), 'package_wheels')
	# Confirm wheels actually exist or fail at this point
	if os.path.isdir(package_wheels):
		print(
			'Unable to import some packages because they may not have been installed, the script will now install '
			'the missing packages locally which will result in some pop-ups and may take some time, please be patient!!\n\n'
			'This should only happen once for each machine / PSSE version'
		)
	else:
		print(
			(
				'The directory {} does not exist which is needed to install the missing python packages, the script '
				'cannot continue.  Please check the original source of this code'
			).format(package_wheels)
		)
		raise ImportError('Python Package Wheels Directory Missing')

	# Remove any already installed local_packages as they will all be re-installed.
	if os.path.isdir(local_packages):
		shutil.rmtree(local_packages)

	# Wait 500ms and then create a new folder, 500 ms to allow time for deleting to take place
	time.sleep(0.5)
	os.makedirs(local_packages)

	# Find python executable
	python_exe = find_python_executable()

	# Path to batch file that will install the missing packages
	batch_path = os.path.join(os.path.dirname(__file__), 'JK7938_SSE_NG_Missing_Packages.bat')

	# Text files produced when batch file run to control output messages
	batch_install_errors = os.path.join(local_packages, 'batch_install_errors.log')
	batch_log_messages = os.path.join(local_packages, 'batch_install_progress.log')

	print(
		(
			'The following batch file will be run to install the packages: {} to the folder {}.  \n\t'
			'Any error messages during the installation will be recorded in the file: {}\n\t'
			'All log messaged during the installation will be recorded in the file: {}'
		).format(batch_path, local_packages, batch_install_errors, batch_log_messages)
	)
	# Adjusted to use an additional try block to capture if an error occurs
	try:
		# Open file to store errors into
		with open(batch_install_errors, 'w') as f:
			# Now checks whether an error status is returned
			subprocess.check_output(
				[batch_path, python_exe, package_wheels, local_packages, '>'+batch_log_messages],
				stderr=f
			)
		print('Installation of missing packages completed in  {:.2f} seconds'.format(time.time()-t0))
	except subprocess.CalledProcessError:
		print(
			'Installation of missing packages failed, check the errors reported in the file {}'.format(batch_install_errors)
		)
		raise EnvironmentError('Unable to install missing python packages')


	import SSE_NG.common_functions as common_functions
	import SSE_NG.GSP_assigner_function as GSP_assigner_function
	import SSE_NG.BB_assigner_function as BB_assigner_function
	import SSE_NG.aggregator_function as aggregator
	print('All modules now imported correctly')