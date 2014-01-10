# Import test python module
from ..lib import setup

def main():
	# Debugging Output
	print "Testing setup..."

	# Test each individual function within the python module
	print " - Testing general_setup"
	assert (0 == setup.general_setup)

	print " - Testing video_setup"
	assert (0 == setup.video_setup)

	print " - Testing audio_setup"
	assert (0 == setup.audio_setup)

	print " - Testing setup"
	assert (0 == setup.setup)

	# Test End
	print "'setup' module test passed"
	
	return 0

