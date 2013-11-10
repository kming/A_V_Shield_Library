###############################################################
#
#	generic.py -- generic library functions needed for most modules
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#prints if verbose flag is set
def vprint (output_string, verbose = 0):
	if verbose:
		print output_string
	return verbose

#checks the return status of the function name 	
def status_check (function_name, status):
	if status != 0:
		error_string =  "%s Errored with Error code %d" % (function_name, status)
		raise RuntimeError(error_string)
	return status
 

#convert a value to signed from unsigned
def convert_to_signed_int (value, reference):
	return value-reference
