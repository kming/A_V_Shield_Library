###############################################################
#
#	audio.py -- common audio functionality --> Setup in setup.py
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#import Adafruit_BBIO.ADC as ADC
import generic as generic
import array as array
# Constant Definition
verbose = False

# Mu Law Constant Def
MU_LAW_Initialized = 0
MU_LAW_BIT_DEPTH = 0 
MU_LAW_BIAS = 0
MU_LAW_MAX_VALUE = 0
MU_LAW_CLIP_LIMIT = 0
# Mu law Exp Region Lookup Table
MU_LAW_P_ENCODING = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]


# Set Mu Law constants, allows for recofiguration of mu law to work with different bit depth inputs. 
def set_mu_law_constant (bit_depth):
	# To make sure we are changing global (module) scope constants
	global MU_LAW_BIT_DEPTH, MU_LAW_BIAS, MU_LAW_MAX_VALUE, MU_LAW_CLIP_LIMIT

	
	if (bit_depth < 8):
		bit_depth = 8 # it is really stored as a byte in memory anyways, so assume it is 8bits in size.

	MU_LAW_BIT_DEPTH = bit_depth # defines mu law bit depth  
	MU_LAW_BIAS = 1 << (MU_LAW_BIT_DEPTH-7) # smallest bias to ensure a "1" in exponent region (LEFT 8 BITS OF SIGN)
	MU_LAW_MAX_VALUE = (1<<(MU_LAW_BIT_DEPTH-1))-1 # 2's compliment ranges from -2^(n-1) to (2^(n-1)-1) n = bitdepth
	MU_LAW_CLIP_LIMIT = MU_LAW_MAX_VALUE - MU_LAW_BIAS # Want to remove bias from limit since bias will be added on later
	# Error Checking
	output_string = "Mu Law Constants Setup\n - bit_depth: %d\n - bias: %d\n - Max_value: %d\n - Clip_limit: %d\n" %(MU_LAW_BIT_DEPTH, MU_LAW_BIAS, MU_LAW_MAX_VALUE, MU_LAW_CLIP_LIMIT)
	generic.vprint(output_string, verbose);
	return 

# mu law encoding algorithm 
def mu_law_encode_value (original_value, signed=True, reference_value=0, bit_depth=16):
	return_value = 0

	# Encoding to change the original value to the mu_law equivalent
	assert (isinstance(original_value, int))

	# Set the parameters of mu_law encoding if it isn't already 
	if (not MU_LAW_Initialized):
		set_mu_law_constant(bit_depth)

	# If the value isn't signed, then convert it to a signed integer
	if (signed == False) and (original_value > 0): 
		# Convert to signed using reference level 
		# Check reference_value 
		pass

	# mu_law Algorithm steps
	# Good Article on basis of mu_law http://www.cypress.com/?docID=38075
	# 1. Save Sign bit for a number of a certain BIT_DEPTH, default is 16. 
	# 	Ex. 0010 1110 1001 1011 Sign Bit = 0
	# 2. Clip magnitude to maximum positive value subtract bias 
	# 	Assuming 16 bit #, bias = 128, then clip value to 2^15-128 if greater
	# 3. Add a bias to ensures a 1 will always appear in the most significant 8 bits left of the sign bit
	# 	Ex. 0010 1110 1001 1011  + 1000 0100 = 0010 1111 0001 1111 
	# 4. Determine Exponent and Mantissa Region 
	#	Exp region = 8bits to the right of the sign bit. 
	# 	Most significant 1 in EXP region = P,next four bits to the right = Mantissa Region. 
	# 	Ex. 0010 1111 0001 1111 
	# 	    00PM MMM1 0001 1111 
	# 5. Create 8bit encoding. 
	# 	Sign Bit = most Significant bit
	# 	Mantissa Region = least significant 4 bits
	# 	Numerical Position of P in 3 bit Binary ecoding = the remaining bits
	# 	Ex. 0P000000 --> 6th position --> 110 in binary = PPP
	# 	    Final 8 bit encoding = SPPP MMMM = 01100111

	generic.vprint ("Mu_Law Debugging Constants:", verbose)

	# Stage 1 - Save and remove sign from value
	sign = (original_value&(1<<(MU_LAW_BIT_DEPTH-1)) != 0)
	return_value = original_value^(1<<(MU_LAW_BIT_DEPTH-1)) #Erases sign bit
	
	# Debugging Statements
	output_string = " - Original_Value(INT): %d\n - Originial_Value(Bin): %s\n - Sign(bit at bit_depth specified): %s\n - After_Sign_Stage_Value(Bin): %s" % (original_value, bin(original_value), sign, bin(return_value))
	generic.vprint (output_string, verbose)

	# Stage 2 - Clip 
	return_value = original_value^(1<<(MU_LAW_BIT_DEPTH-1))
	if (return_value >= MU_LAW_CLIP_LIMIT):
		return_value = MU_LAW_CLIP_LIMIT
	# Debugging Statements
	output_string = " - Clip Limit: %d\n - After_Clip_Stage_Value: %d" %(MU_LAW_CLIP_LIMIT, return_value)
	generic.vprint (output_string, verbose)

	# Stage 3 - Add Bias
	return_value = return_value + int(MU_LAW_BIAS)
	# Debugging Statements
	output_string = " - Bias: %d\n - After_Biasing_Stage_Value(INT): %d\n - After_Biasing_Stage_Value (Binary): %s" %(MU_LAW_BIAS , return_value, bin(return_value))
	generic.vprint (output_string, verbose)

	# Stage 4 - Saves EXP region and mantissa region
	exp_region = (return_value >> (MU_LAW_BIT_DEPTH - 9))&0xFF # 1 for sign bit, 8 for exp region
	p_encoding = MU_LAW_P_ENCODING[exp_region-1]
	man_region = (return_value >> (MU_LAW_BIT_DEPTH - (13 - p_encoding))) & 0x0F # Bit_Depth - sign bit - (relative position of p) - (4 bits for mantissa) = (bit_depth - 1 - (8-p) - 4) = bit depth - (13-p)
	# Debugging Statements
	output_string = " - Exp Region: %s\n - Mantissa Region: %s" % (bin(exp_region), bin(man_region))
	generic.vprint (output_string, verbose)

	# Stage 5
	return_value = ((sign << 7) + (p_encoding << 4) + man_region) 
	# Debugging Statements
	output_string = " - Sign: %s\n - P_encoding: %s\n - Mantissa Region: %s\n - Encoded Value: %s\n" % (bin(sign), bin(p_encoding), bin(man_region), bin(return_value))
	generic.vprint (output_string, verbose)

	return return_value
		
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

def write_wav_file_header (full_file_path, bit_depth=8, compression=False):

	return

