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
		# PINs Used
		self._pin_usage = {}

	def setup_data_file (self, file_name="AVSL_ADC_SPI.RAW"):
		self._raw_file = open (file_name, "w")
		self._file_lock = True

	def close_data_file (self):
		if self._file_lock:
			self._raw_file.close()
		else:
			print "Data File not initiated"
	# Hardcode since each pin needs to be initialized differently
	def _init_pin (self, pin, function, params):
		if (function == "PWM"):
			duty = params[0]
			freq = params[1]
			polarity = params[2]
			PWM.start (pin, duty, freq, polarity)			
			self._pin_usage[pin] = "PWM"
		elif (function == "GPIO"):
			direction = params[0]
			GPIO.setup(pin, direction)
		elif (function == "
			
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

	def setup_adc_clock (self, adc_clk_pin = "P9_14", adc_clk_freq = -1):
		if verbose:
			print "Setting up ADC clock"
		if (adc_clk_freq < 0):
			adc_clk_freq = self._adc.msh
		PWM.start(adc_clk_pin, 50, adc_clk_freq, 0) # clock signal to ADC with 0 polarity and 50%duty cycle
	
	def raw_read_value (self, address):
		addr["0"] = [address]
		return self.adc.xfer(addr["0"])[0]

	def read_till_stop(self, pin = "P8_14"):
		# Setup input control pin if it wasn't setup before
		if (not (pin in self._pin_setup) or (self._pin_setup[pin] is False)):
			GPIO.setup(pin, GPIO.IN)
			self._pin_setup[pin] = True
		
		print "Press and hold record button to record"
		GPIO.wait_for_edge(pin, GPIO.RISING)		# wait for button press
		
		# Setup Loopback timer
		GPIO.setup ("P8_15", GPIO.IN)
		PWM.start ("P8_13", 50, 8000, 0)
		# Setup output file
		self._data_file = open("data.sample", "w") 
		GPIO.add_event_detect(pin, GPIO.FALLING)
		i = 0
		addr = {}
		print "Reading Audio Data"
		# Write to output file until user input
		while (not GPIO.event_detected(pin)):		# Stop if released
			addr["{0}".format(i)] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			for value in self._adc.xfer(addr[str(i)]):
				self._data_file.write (chr(value))
			i = i+1
		
		# Cleanup GPIO and file handling
		self._data_file.close()
		GPIO.cleanup()
		
	def event_detect(self, pin = "P8_14"):
		# Setup input control pin if it wasn't setup before
		if (not (pin in self._pin_setup) or (self._pin_setup[pin] is False)):
			GPIO.setup(pin, GPIO.IN)
			self._pin_setup[pin] = True
		print "Sampling Ambient Noise Levels"
		ambient_addr = {}
		value = self._adc.xfer([0])
		for i in range(1000):
			addr["{0}".format(i)] = [0]
			value = (value + self._adc.xfer(addr[str(i)])[0]) / 2
		print "Ambient Noise: %f" % value
		
		print "Press and hold record button to start edge detect"
		GPIO.wait_for_edge(pin, GPIO.RISING)		# wait for button press
		
		# Setup Loopback timer
		GPIO.setup ("P8_15", GPIO.IN)
		PWM.start ("P8_13", 50, 8000, 0)
		# Setup output file
		GPIO.add_event_detect(pin, GPIO.FALLING)
		i = 0
		status = 0
		addr = {}
		# Write to output file until user input
		while (not GPIO.event_detected(pin)):		# Stop if released
			addr["{0}".format(i)] = [0]
			if ((self._adc.xfer(addr[str(i)])[0] - value)/value > 0.1):
				status = 1
				break
			i = i+1
		
		if status: 
			print "Event Detected."
		else:
			print "Nothing Detected."
			
		# Cleanup GPIO 
		GPIO.cleanup()
