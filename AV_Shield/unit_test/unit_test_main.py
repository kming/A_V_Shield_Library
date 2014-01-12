import sys 
import os
import glob
import subprocess

list_of_tests = ["audio_wav_file", "generic", "setup"]

SUCCESSFUL = 0
FAIL = 1

def run_all_test():
	verbose = 1 # use a hardcode for now, implement getopt later
	status = SUCCESSFUL

	# Go through all unit test and call the unit test file
	for module in list_of_tests:
		print "Running %s" % module 
		# Call the module's main test 
		unit_test_str = "AV_Shield.unit_test.unit_test_" + module
		m_obj = __import__ (unit_test_str)
		print dir(m_obj)
		status = getattr(m_obj, 'main')()
		
	
		# Check testing results
		if status == SUCCESSFUL:
			print "  - Passed" 
		else:
			print "  - Failed" 
	return status
