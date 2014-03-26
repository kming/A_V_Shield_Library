###############################################################
#
#	bbb_adc.py -- BBB specific code to enable 
#			  the use of the ADC 
#	By: Kei-Ming Kwong 2013
#
###############################################################

#Import Needed Libraries
import generic as generic
import Adafruit_BBIO.ADC as ADC 
import Adafruit_BBIO.SPI as SPI
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time as time
verbose = 0
# class to interact with ADC
class adc:
	def __init__ (self, spi_bus=0, spi_device=0):	
		# Flag to indicate this isn't machine specific code -- 
		self.MACHINE_SPECIFIC = False
		# File for storage of raw data, needs to be setup prior to write
		self._data_file = ""
		self._file_lock = False
		# pins Used
		self._pin_usage = {}
		# Setup ADC
		ADC.setup()
		
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
			elif (function == "ADC"):
				self._pin_usage[pin] = "ADC"
			else:
				print "No Such Function %s" % function
	
	# Read a single value assuming infrequent reads
	def read_single_value (self, adc_pin = "P4_40"):
		return ADC.read(adc_pin)

	def read_till_stop(self, ctrl_pin = "P8_14"):
		# Setup input control pin 
		self._init_pin (ctrl_pin, GPIO.IN)
		
		# Setup output file
		self.setup_data_file()
		
		# Add a detection event for when the input will fall.
		GPIO.add_event_detect(ctrl_pin, GPIO.FALLING)
			
		# Setup Loopback timer
		GPIO.setup ("P8_15", GPIO.IN)
		PWM.start ("P8_13", 50, 8000, 0)	
			
		# Starts when initiated by input
		print "Press and hold record button to record"
		GPIO.wait_for_edge(ctrl_pin, GPIO.RISING)		# wait for button press
		
		i = 0
		addr = {}
		print "Reading Audio Data"
		# Write to output file until user input
		while (not GPIO.event_detected(ctrl_pin)):
			GPIO.wait_for_edge("P8_15", GPIO.RISING) # Records every time a rising edge is hit. 	
			self._data_file.write (self.read_single_value())
		
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
