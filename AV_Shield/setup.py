###############################################################
#
#	setup.py -- common setup functions initializes all required
#				pins and environment needed for AV Shield
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

import generic
import generic.vprint as vprint

OK = 0
ERROR = 1

def setup(verbose=0):
	# Generic main setup function
	vprint("Initializing Setup Procedure...", verbose)
	status = OK
	
	# Call sub setup functions
	status = general_setup (verbose)
	generic.status_check ("general_setup", status)
	status = audio_setup (verbose)
	generic.status_check ("audio_setup", status)
	status = video_setup (verbose)
	generic.status_check ("video_setup", status)
	
	vprint ("Initial Setup Complete.", verbose)
	return status
			
def general_setup(verbose=0):
	# Setup generic information needed for the beaglebone black
	return OK
def audio_setup(verbose=0):
	# Setup Audio related pins and environment
	return OK
	
def video_setup(verbose=0):
	return OK
