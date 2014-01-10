###############################################################
#
#	audio_wav_object.py -- wav object and handling functions
#
#	By: Kei-Ming Kwong 2013
#
###############################################################
import array as ArrayType


class chunk:
	_id = ''		# id of the chunk
	_size = 0		# Aligned data size (not sync with actual data size)
	_data = 0		# Data Array
	_dirty = False		# Determines if chunk has been written to
	_align = False		# Aligned mode, which pads '0' data if uneven size
	_type = 0		# Stores the type of the chunk
	# Define a chunk with a specific ID
	def __init__ (self, a_id, a_align_mode=True, a_type='c'):
		self._id = a_id
		self._align = a_align_mode	#defaults to aligned mode
		self._data = ArrayType.array (a_type)
		self._type = a_type
	
	# Get Chunk ID
	def get_id (self):
		return self._id
	
	# Data Modification Related Functions
	def append_value (self, a_data, a_size=1, a_big_endian=False):
		assert (a_size >= 1)		
		if (a_size==1):
			self._data.append (a_data)
		else:
			# Assumes Little Endian if passing in a value			
			byte_list = [ str(chr((a_data >> i) & 0xff)) for i in range (0, 8*a_size, 8)]
			if (a_big_endian):
				byte_list.reverse()
			#print " - Byte Order: Value(0x%x) Byte Size(%d)" % (a_data, a_size)
			#print byte_list
			self.append_list(byte_list)
		self._dirty = True

	def append_list (self, a_list):
		# First value is first, etc
		self._data.fromlist(a_list)
		self._dirty = True

	def append_array (self, a_array):
		self._data.extend(a_array)
		self._dirty = True

	def append_string (self, a_string):
		# First Character is first byte, etc. 
		self.append_list (list(a_string))

	# Output Data as String
	def data_to_string (self):	
		data_string = self._data.tostring()
		self._update_size()
		# Null padding added to output string, but data not modified 
		# since chunk may be continually modified and accessed
		if (self._align and (self._size%2 != 0)):
			data_string += "\0"
		return data_string

	# Output Data as List
	def data_to_list (self):	
		data_list = self._data.tolist()
		self._update_size()
		# Null padding added to output string, but data not modified 
		# since chunk may be continually modified and accessed
		if (self._align and (self._size%2 != 0)):
			data_list.append("\0")
		return data_list
	
	# Update Data Size (Internal function)
	def _update_size(self):
		if self._dirty:
			# determine actual data size and modify if needs to be aligned
			self._size = self._data.buffer_info()[1] * self._data.itemsize
			if (self._align and (self._size%2 != 0)):
				self._size += 1			
			self._dirty = False
	
	# Determine size of data
	def get_data_size (self):
		self._update_size()
		output_size = self._size
		return output_size
	
	def get_total_size (self):
		# add 4 bytes for Chunk ID and Chunk Size
		return 4 + 4 + self.get_data_size()
	# Clear Data
	def clear_data (self):
		for i in range (0, self._data.buffer_info()[1]):
			self._data.pop()
	

	
class wav_object:
	# Initialize class object	
	def __init__ (self):
			# Initialize class variables
			# class fmt variables
			self._w_fmt_key = ['Audio_Format', 'Num_Channels', 'Sample_Rate', 'Byte_Rate', 'Block_Align', 'Bits_per_Sample']
			self._w_fmt_value = [None, None, None, None, None, None]
			self._w_fmt_size = [2,2,4,4,2,2]
			self._w_fmt_dirty = False

			# Initialize Header Chunk
			self.w_header = chunk("RIFF") # "RIFF"(0x52494646) Header ID
			self.w_header.append_string("WAVE") # Initialize Header Data to "WAVE" to indicate wav RIFF file
			
			# Initialize fmt Chunk
			self.w_format = chunk("fmt ") # "fmt "(0x666D7420) format ID 
			self.change_basic_fmt()

			# Initialize data Chunk
			self.w_data = chunk("data") 	# "data"(0x64617461) data ID

	# Change fmt parameters for wav file	
	def change_basic_fmt (self, a_fmt=1, a_num_chan=1, a_samp_rate=8000, a_bits_per_sample=8):
		self._w_fmt_value [1] = a_num_chan
		self._w_fmt_value [0] = a_fmt
		self._w_fmt_value [2] = a_samp_rate
		self._w_fmt_value [3] = a_samp_rate * a_num_chan * (a_bits_per_sample/8)
		self._w_fmt_value [4] = a_num_chan * (a_bits_per_sample/8)
		self._w_fmt_value [5] = a_bits_per_sample
		self._w_fmt_dirty = True
	
	# Adding Extra Format Params (Not a correct implementation)
	def add_extra_fmt (self, a_fmt_name, a_fmt_value, a_fmt_size):
		self._w_fmt_key.append(a_fmt_name)
		self._w_fmt_value.append(a_fmt_value) 
		self._w_fmt_size(a_fmt_size)
		self._w_fmt_dirty = True

	def _update_fmt_chunk (self):
		if self._w_fmt_dirty:		
			for key, value, size in zip(self._w_fmt_key, self._w_fmt_value, self._w_fmt_size):
				self.w_format.append_value (value, size)
		#self._print_fmt_debug_info()

	def _print_fmt_debug_info(self):		
		print "\n\nDEBUG INFORMATION: FMT"		
		print " - Key"
		print self._w_fmt_key
		print " - Byte Size"
		print self._w_fmt_size
		print " - Value(wav)"
		print self._w_fmt_value
		print " - Value(Chunk)"
		print self.w_format.data_to_list()
		print " - Chunk Data Size"
		print self.w_format.get_data_size()
		
		
	# Adding and removing data for wav file 
	def append_data_value (self, a_data, a_size=0, a_big_endian=False):
		if a_size == 0:
			a_size = (self._w_fmt_value[5] / 8) 		# Assumes default value byte size unless specified
		self.w_data.append_value(a_data, a_size, a_big_endian) 

	def clear_data (self):
		self.w_data.clear_data()

	def _print_data_debug_info(self):		
		print "\n\nDEBUG INFORMATION: DATA"	
		print " - Value(Chunk)"
		print self.w_data.data_to_list()
		print " - Chunk Data Size"
		print self.w_data.get_data_size()	
	
	# export to file
	def export_to_file (self, full_file_path):
		# Update fmt 		
		self._update_fmt_chunk()
		# Check file name/path
		f = open(full_file_path, 'w')
		# Compile File String
		total_data_size = self.w_header.get_total_size() + self.w_format.get_data_size() + self.w_data.get_data_size()

		# The Sizes are converted to a list to ensure little Endian format
		file_list = list (self.w_header.get_id())
		file_list += [str(chr((total_data_size >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_header.data_to_list()

		file_list += list (self.w_format.get_id())
		file_list += [str(chr((self.w_format.get_data_size() >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_format.data_to_list()

		file_list += list(self.w_data.get_id())
		file_list += [str(chr((self.w_data.get_data_size() >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_data.data_to_list()
		
		f.write (''.join(file_list))		
		f.close()

	# read from file
	def import_from_file (self, full_file_path):
		
		# Check file name/path
		f = open(full_file_path, 'r')	
		file_string = f.read()
		f.close()
		
		# Separate different chunk information
		(header_string, fmt_data_string) = file_string.split("fmt ", 1)
		(fmt_string, data_string) = fmt_data_string.split("data", 1)		
		# Ensure it is a RIFF WAVE File 		
		if "WAVE" not in header_string:
			print " - NOT a WAV File Format"
			return 0
		
		# Determine Fmt Data Values from raw string
		# Remove First four bytes --> Size Byte	
		self._w_fmt_value = self._fmt_raw_to_list (fmt_string[4:])
		self._w_fmt_dirty = True

		# Copy the data portion
		self.w_data.append_string(data_string[4:])
		
		return 0

	# Converts the raw fmt string to actual values
	def _fmt_raw_to_list (self, a_str):
		return_list = []
		index = 0
		for key, size in zip(self._w_fmt_key, self._w_fmt_size):
			return_list.append(self._raw_to_value(a_str[index:(index + size)], size))
			index += size
		return return_list

	# Converts raw string to value given string and size
	def _raw_to_value (self, a_str, a_size, a_big_endian=False):
		return_value = 0
		for i in range(a_size):
			char_value = ord(a_str[i])
			if (a_big_endian):
				char_value = char_value>>(8*(a_size-i-1))
			else:
				char_value = char_value<<(8*i)
			return_value += char_value
		return return_value
		
		
