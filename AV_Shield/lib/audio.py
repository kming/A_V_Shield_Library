###############################################################
#
#	audio.py -- common audio functionality --> Setup in setup.py
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#import Adafruit_BBIO.ADC as ADC
import generic as generic
def raw_adc_input(pin_name):
	## PINS FOR ADC/AUDIO
	#"AIN4", "P9_33"
	#"AIN6", "P9_35"
	#"AIN5", "P9_36"
	#"AIN2", "P9_37"
	#"AIN3", "P9_38"
	#"AIN0", "P9_39"
	#"AIN1", "P9_40"
	#return ADC.read(pin_name)
	pass
	

# mu law encoding is a way 	
def mu_law_encode_value (original_value, signed=true, reference_value=0):
	return_value = 0
	# Encoding to change the original value to the mu_law equivalent
	assert (isinstance(original_value, int))
	
	# If the value isn't signed, then convert it to a signed integer
	if (signed == False) and (original_value > 0): 
		# Convert to signed using reference level 
		# Check reference_value 
		pass

	# mu_law Algorithm steps
	# Good Article on basis of mu_law http://www.cypress.com/?docID=38075
	# Save Sign bit = 0
	# Ex 0010 1110 1001 1011 
	# clip magnitude to 2^15 --> 16bit number 1 sign bit, 15bit data. -2^15 to 2^15
	# Add a bias of 132 to magnitude ensures a 1 will always appear in the exponent region 
	# Ex 0010 1110 1001 1011  + 1000 0100 = 0010 1111 0001 1111 
	# Exp region = 8bits to the right of the sign bit. the left most 1 in the EXP region = P, and the four bits to the right are the mantissa. 
	# 0010 1111 0001 1111 
	# 00PM MMM1 0001 1111 
	# Since 0P000000 --> 6th position --> 110 in binary = PPP
	# 8 bit encoding = SPPP MMMM
	
	return return_value	
