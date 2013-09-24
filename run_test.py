import sys
import os
import glob

test_file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(test_file_path)

for files in glob.glob("test_dir*test.py):
	# use subprocess module to run tests in parallel or series. 
	
if status == SUCCESSFUL:
	print "Test Passed Successfully!!\n"
else:
	print "Testing Failed\n"


