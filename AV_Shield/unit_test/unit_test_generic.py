# Import test python module
from ..lib import generic

def main():

	# Debugging Output
	print "Testing Generic Module..."

	# Test each individual function within the python module
	print " - Testing vprint:"
	assert (1 == generic.vprint ("test_print_ok", 1))
	assert (0 == generic.vprint ("test_print_fail", 0))

	# Test End
	print "'generic' module test passed"
	
	return 0
