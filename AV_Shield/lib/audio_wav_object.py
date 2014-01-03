###############################################################
#
#	audio_wav_object.py -- wav object and handling functions
#
#	By: Kei-Ming Kwong 2013
#
###############################################################
import array as array

class chunk:
	_id = 0			# id of the chunk
	_output_size = 0	# total chunk size
	_data = array ('c')	# Data Array
	_dirty = False		# Determines if chunk has been written to
	_align = False		# Aligned mode, which pads '0' data if uneven size
	
	# Define a chunk with a specific ID
	def _init_ (self, a_id, a_align_mode=True):
		self._id = a_id
		self._aligned = a_align_mode	#defaults to aligned mode
			
	# Write data to chunk
	def append_value (self, a_data):
		self._data.append (a_data)
		self._dirty = True

	def append_list (self, a_list):
		self._data.fromlist(a_list)
		self._dirty = True

	def append_array (self, a_array):
		self._data.extend(a_array)
		self._dirty = True

	# output chunk data as string
	def data_to_string (self):	
		data_string = self._data.tostring()
		# determine size
		size = _data.buffer_info()[1] * _data.itemsize

		if self._dirty:
			_dirty = false
		
		if (_aligned and (_size%2 not 0)):
			# needs to be aligned but not aligned
			_size += 1
			
		
	def get_total_size
		
class wav_object:
	w_header = None
	w_format = None
	w_data = None
	w_size = 0
	# Initialize class object	
	def _init_ (self):
			self.header = chunk(0x52494646) # RIFF(0x52494646) Header ID
			self.format = chunk(0x666D7420) # fmt(0x666D7420) format ID 
			self.data = chunk(0x64617461) 	# data(0x64617461) data ID
	# Writing functions to wav_object
	# Reading functions to wav_object
	# export to file
	# read from file


