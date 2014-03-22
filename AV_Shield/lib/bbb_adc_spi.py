###############################################################
#
#	bbb_adc_spi.py -- BBB specific code to enable 
#			  the use of the ADC under the SPI 
# 			  protocol
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#Import Needed Libraries
import generic as generic
import Adafruit_BBIO.SPI as SPI
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time as time
verbose = 0
# class to interact with ADC
class adc_spi:

	def __init__ (self, spi_bus=0, spi_device=0):	
		# Flag to indicate machine specific code
		self.MACHINE_SPECIFIC = True
		# Initialize an SPI communication process using the SPI protocol. 
		self._adc = SPI.SPI(spi_bus, spi_device)
		# File for storage of raw data, needs to be setup prior to write
		self._data_file = ""
		self._file_lock = False
		# pins Used
		self._pin_usage = {}
		
	# Uses a software lock to ensure it is only outputing to one file and running one procedure at a time. 
	def setup_data_file (self, file_name="AVSL_ADC_SPI.RAW"):
		self._raw_file = open (file_name, "w")
		self._file_lock = True

	def close_data_file (self):
		if self._file_lock:
			self._raw_file.close()
		else:
			print "Data File not initiated"
			
	# Hardcode setup of pins needed to be initialized differently
	def _init_pin (self, pin, function, params):
		if ((pin in self._pin_usage) and (self._pin_usage[pin] != function):
			print "Pin is defined already"
		else:			
			if (function == "PWM"):
				duty = params[0]
				freq = params[1]
				polarity = params[2]
				PWM.start (pin, duty, freq, polarity)			
				self._pin_usage[pin] = "PWM"
			elif (function == "GPIO"):
				direction = params[0]
				GPIO.setup(pin, direction)		
				self._pin_usage[pin] = "GPIO"
			else:
				print "No Such Function %s" % function
	
	# setup spi protocol, assumes default values unless otherwise specified. 
	def setup_spi_protocol (self, max_freq, bpw=8, cs_high=False, threewire=False, loopback=False, mode=0):
		self._adc.msh = max_freq
		self._adc.bpw = bpw
		self._adc.cshigh = cs_high
		self._adc.threewire = threewire
		self._adc.loop = loopback
		self._adc.mode = mode
		if verbose:
			print "bpw\t{0}".format(self._adc.bpw)
			print "msh\t{0}".format(self._adc.msh)
			print "cshigh\t{0}".format(self._adc.cshigh)
			print "threewire\t{0}".format(self._adc.threewire)
			print "loop\t{0}".format(self._adc.loop)
			print "mode\t{0}".format(self._adc.mode)

	# setup ADC external clock -- assumes same frequency as SPI unless specified. 
	def setup_adc_clock (self, adc_clk_pin = "P9_14", adc_clk_freq = -1):
		if (adc_clk_freq < 0):
			adc_clk_freq = self._adc.msh
		self._init_pin (adc_clk_pin, "PWM", [50, adc_clk_freq, 0]) # clock signal to ADC with 0 polarity and 50%duty cycle
	
	# Read a single value assuming infrequent reads
	def read_single_value (self, address):
		addr["0"] = [address]
		return self.adc.xfer(addr["0"])[0]

	def read_till_stop(self, ctrl_pin = "P8_14"):
		# Setup input control pin 
		self._init_pin (ctrl_pin, GPIO.IN)
		
		# Setup output file
		self.setup_data_file()
		
		# Add a detection event for when the input will fall.
		GPIO.add_event_detect(ctrl_pin, GPIO.FALLING)
		
		# Starts when initiated by input
		print "Press and hold record button to record"
		GPIO.wait_for_edge(ctrl_pin, GPIO.RISING)		# wait for button press
		
		# Setup Loopback timer
		# GPIO.setup ("P8_15", GPIO.IN)
		# PWM.start ("P8_13", 50, 8000, 0)
		
		i = 0
		addr = {}
		print "Reading Audio Data"
		# Write to output file until user input
		while (not GPIO.event_detected(ctrl_pin)):		# Stop if released
			addr["{0}".format(i)] = [0]
			for value in self._adc.xfer(addr[str(i)]):
				self._data_file.write (chr(value))
			i = i+1
		
		# Cleanup event detection and close data file
		self.close_data_file()
		GPIO.remove_event_detect(ctrl_pin)
	
	# Absolute Difference Variance Calculation
	def event_detect_one_input(self, pin = "P8_14"):
		# Setup input control pin 
		self._init_pin (ctrl_pin, GPIO.IN)
		
		# Setup output file
		self.setup_data_file()
		
		# Determine the average input for ADC quiet environment
		print "Sampling Ambient Noise Levels"
		ambient_addr = {}
		amb_noise = self._adc.xfer([0])
		for i in range(1000):
			addr["{0}".format(i)] = [0]
			amb_noise = (amb_noise + self._adc.xfer(addr[str(i)])[0]) / 2
		print "Ambient Noise: %f" % amb_noise
		
		print "Press and hold record button to start event detect"
		GPIO.add_event_detect(pin, GPIO.FALLING)
		GPIO.wait_for_edge(pin, GPIO.RISING)		# wait for button press
		
		i = 0
		status = 0
		addr = {}
		# Write to output file until user input
		prev_abs_diff = 0
		while (not GPIO.event_detected(pin)):		# Stop if released
			addr["{0}".format(i)] = [0]
			new_adc_value = self._adc.xfer(addr[str(i)])[0]
			new_abs_diff = abs(new_adc_value - amb_noise)
			print new_abs_diff
			if (new_abs_diff > prev_abs_diff + 60):
				# too big of a jump from prev abs value, ignore. 
				prev_abs_diff = new_abs_diff
				continue 
			elif (new_abs_diff > 50):
				#consistently large abs diff
				status = 1 
				break
			prev_abs_diff = new_abs_diff
			i = i+1
		
		if status: 
			print "Event Detected."
		else:
			print "Nothing Detected."
			
		# Cleanup event detection and close data file
		self.close_data_file()
		GPIO.remove_event_detect(ctrl_pin)	
		
	# Running Variance Calculation http://www.johndcook.com/standard_deviation.html
	def event_detect_one_input_var(self, pin = "P8_14"):
		# Setup input control pin 
		self._init_pin (ctrl_pin, GPIO.IN)
		
		# Setup output file
		self.setup_data_file()
		
		print "Press and hold record button to start event detect"
		GPIO.add_event_detect(pin, GPIO.FALLING)
		GPIO.wait_for_edge(pin, GPIO.RISING)		# wait for button press
		
		i = 2
		status = 0
		count = 0
		addr = {}
		init_addr = [0]
		# initialize running mean
		S = 0
		M = self._adc.xfer(init_addr)[0]
		while (not GPIO.event_detected(pin)):		# Stop if released
			addr["{0}".format(i)] = [0]
			new_adc_value = self._adc.xfer(addr[str(i)])[0]
			
			M_new = M + (new_adc_value - M)/i #save to another variable to not overwrite M
			S = S + (new_adc_value - M)*(new_adc_value - M_new)
			M = M_new
			print S
			if (count > 20):
				count = 0
				
			count = count + 1
			i = i+1
		
		if status: 
			print "Event Detected."
		else:
			print "Nothing Detected."
			
		# Cleanup event detection and close data file
		self.close_data_file()
		GPIO.remove_event_detect(ctrl_pin)
