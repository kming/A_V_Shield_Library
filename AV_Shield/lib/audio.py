###############################################################
#
#	audio.py -- common audio functionality --> Setup in setup.py
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#import Adafruit_BBIO.ADC as ADC
import generic as generic
import Adafruit_BBIO.SPI as SPI
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

# Constant Definition
verbose = True

# class to interact with ADC.  Assumes a default mode of using SPI protocol
class adc:
	_adc = ""
	_data_file = ""
	_file_lock = False
	_pin_setup = {}
	_xfer_protocol = ""
	def __init__ (self, protocol = "SPI"):
		if (protocol == "SPI"):
			self._adc = SPI.SPI(0,0)		# Use SPI0 as the main protocol to communicate with the ADC			
		self._xfer_protocol = protocol
		self._data_file = "" 		
		
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
		
		# Setup output file
		self._data_file = open("data.sample", "w") 
		GPIO.add_event_detect(pin, GPIO.FALLING)
		i = 0
		addr = {}
		print "Reading Audio Data"
		# Write to output file until user input
		while (not GPIO.event_detected(pin)):		# Stop if released
			addr["{0}".format(i)] = [0]
			self._data_file.write(str(self._adc.xfer(addr[str(i)])[0]))	
			i = i+1
			
		
		# Cleanup GPIO and file handling
		self._data_file.close()
		GPIO.cleanup()
		
		
		
		
	
	
	
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
	
# Need to do: write WAV Header, write WAV Data
def read_wav_file (full_file_path):

	return

