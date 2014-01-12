###############################################################
#
#	audio_wav_file.py -- wav file classes
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

###### IMPORT LIBRARIES ######
import array as ArrayType
import generic as generic

###### CLASS DEFINITIONS ######
# Chunk Class:
#       RIFF File Type Chunk, Composed of the following parts
# 		ID: 4 byte Value(Big Endian) ID of the chunk
#		Size: 4 byte Value(Little Endian) Size of all following data in bytes
#		Data Bytes: Array of all Data Bytes
# 	get_id: Returns the ID set in the creation
# 	append_value: Appends a value of a certain size to the char array given a value.  Can be converted to little endian or big 
# 	append_list: Appends the list given entirely to the data, User is responsible for ensuring little endian or big endian
# 	append_array: Same as append_list, require user to ensure correctness,but takes in an "array" type
# 	append_string: Same as append_list, require user to ensure correctness,but takes in an "string" type 
# 	data_to_string: Returnss the data Array as a string
# 	data_to_list: Returns the data Array as a list
# 	clear_data: Clears out the data Array
#	get_data_size: Gets the total size of the data array in bytes (this may or may not include the 1 byte null padding if it is aligned)
# 	get_total_size: Gets the total size of the data array in bytes + size of ID/Size in bytes
class chunk:
	# Chunk Initialization
	def __init__ (self, a_id, a_align_mode=True, a_type='c'):
		self._id = a_id				# id of the chunk (String Typically)
		self._size = 0				# Aligned data size (not sync with actual data size)
		self._data = ArrayType.array (a_type)	# Data Array (Byte Array is the default, but can be changed accordingly)
		self._dirty = False			# Determines if chunk has been written to
		self._align = a_align_mode		# Aligned mode, which pads '0' data if uneven size
		self._type = a_type			# Stores the type of the chunk

	
	# Returns chunk ID set
	def get_id (self):
		return self._id
	
	# Append value to data (finer granular control on "endian-ness" and size)
	def append_value (self, a_data, a_size=1, a_big_endian=False):
		assert (a_size >= 1)		
		if (a_size==1):
			self._data.append (a_data)
		else:
			# Create a little Endian Byte Array from the value		
			byte_list = [ str(chr((a_data >> i) & 0xff)) for i in range (0, 8*a_size, 8)]
			if (a_big_endian):
				byte_list.reverse() 	# Convert to Big Endian byte array
			self.append_list(byte_list)
		self._dirty = True
	# Generic Appending functions (Require user to ensure correctness)
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

	# Output Raw Data (adds a null padding if required)
	def data_to_string (self):	
		data_string = self._data.tostring()
		self._update_size()
		# Null padding added to output string, but data not modified 
		# since chunk may be continually modified and accessed
		if (self._align and (self._size%2 != 0)):
			data_string += "\0"
		return data_string

	def data_to_list (self):	
		data_list = self._data.tolist()
		self._update_size()
		# Null padding added to output string, but data not modified 
		# since chunk may be continually modified and accessed
		if (self._align and (self._size%2 != 0)):
			data_list.append("\0")
		return data_list
	
	# Private Function: Update Data Size --> Only calculate size when necessary, not everytime data is written. 
	def _update_size(self):
		if self._dirty:
			# determine actual data size and modify if needs to be aligned
			self._size = self._data.buffer_info()[1] * self._data.itemsize
			if (self._align and (self._size%2 != 0)):
				self._size += 1			
			self._dirty = False
	
	# Determine size of data Array in Bytes
	def get_data_size (self):
		self._update_size()
		output_size = self._size
		return output_size
	def get_total_size (self):
		# add 4 bytes for Chunk ID and Chunk Size
		return 4 + 4 + self.get_data_size()

	# Clear Data Array
	def clear_data (self):
		for i in range (0, self._data.buffer_info()[1]):
			self._data.pop()
	

# wav Class:
#       WAVE RIFF File Type, Composed of the following parts
# 		ID Chunk: Identifier for the RIFF filetype as WAV
#		Format Chunk: Stores settings of the WAV type
#		Data Chunk: Sonic Data
# 	change_basic_fmt: Changes the fundamental settings (Data_format(compression scheme etc), num_of_channels, sampling_rate, bits_per_sample)
# 	add_extra_fmt: Adds extra fmt parameters
# 	append_data_value: Appends the data value, defaults to size as described in "fmt string", or unless specified
# 	clear_data: Removes all sonic data, fmt is not reset. 
# 	export_to_file: Exports raw wav file
# 	import_from_file: Imports raw wav file
class wav:
	# WAV File initialization	
	def __init__ (self):
		# Basic Formatting Values
		#'Audio_Format', 'Num_Channels', 'Sample_Rate', 'Byte_Rate', 'Block_Align', 'Bits_per_Sample'
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

	# Used to change the basic format settings
	# returns True if successful, False if failed
	def change_basic_fmt (self, a_fmt=1, a_num_chan=1, a_samp_rate=8000, a_bits_per_sample=8):
		if (a_bits_per_sample%8 != 0):
			print " - Bits per sample needs to be a factor of 8"			
			return False 
		bytes_per_sample = a_bits_per_sample/8

		# The values in order: 'Audio_Format', 'Num_Channels', 'Sample_Rate', 'Byte_Rate', 'Block_Align', 'Bits_per_Sample'
		self._w_fmt_value [0] = a_fmt
		self._w_fmt_value [1] = a_num_chan
		self._w_fmt_value [2] = a_samp_rate
		self._w_fmt_value [3] = a_samp_rate * a_num_chan * bytes_per_sample
		self._w_fmt_value [4] = a_num_chan * bytes_per_sample
		self._w_fmt_value [5] = a_bits_per_sample
		
		# Sets the fmt dirty bit
		self._w_fmt_dirty = True
		return True
	
	# Adding Extra Format Params (Not a correct implementation, needs to be added to later.)
	def add_extra_fmt (self, _fmt_value, a_fmt_size):
		self._w_fmt_value.append(a_fmt_value) 
		self._w_fmt_size(a_fmt_size)
		self._w_fmt_dirty = True

	# Updating fmt chunk (This method should be faster since updating chunk takes longer due to varying size values of fmt) 
	def _update_fmt_chunk (self):
		if self._w_fmt_dirty:		
			for value, size in zip(self._w_fmt_value, self._w_fmt_size):
				self.w_format.append_value (value, size)
		#self._print_fmt_debug_info()

	def _print_fmt_debug_info(self):		
		print "\n\nDEBUG INFORMATION: FMT"		
		print " - 'Audio_Format', 'Num_Channels', 'Sample_Rate', 'Byte_Rate', 'Block_Align', 'Bits_per_Sample'"
		print " - Byte Size"
		print self._w_fmt_size
		print " - Value(wav)"
		print self._w_fmt_value
		print " - Value(Chunk)"
		print self.w_format.data_to_list()
		print " - Chunk Data Size"
		print self.w_format.get_data_size()
		
		
	# Appending Sonic Data (No Verification to ensure correctness with the fmt of the wav file)
	def append_data_value (self, a_data, a_size=0, a_big_endian=False):
		if a_size == 0:
			a_size = (self._w_fmt_value[5] / 8) 		# Assumes default value byte size from fmt unless specified
		# if two channels, then we will expect two value for left and right
		if (self._w_fmt_value[1] == 2):	
			self.w_data.append_value(a_data[1], a_size, a_big_endian)
		self.w_data.append_value(a_data[0], a_size, a_big_endian) 

	# Clearing Sonic Data
	def clear_data (self):
		self.w_data.clear_data()

	def _print_data_debug_info(self):		
		print "\n\nDEBUG INFORMATION: DATA"	
		print " - Value(Chunk)"
		print self.w_data.data_to_list()
		print " - Chunk Data Size"
		print self.w_data.get_data_size()	
	
	# Export to a WAV file 
	def export_to_file (self, full_file_path):
		# Ensure fmt chunk is updated	
		self._update_fmt_chunk()

		# Calculate total size 
		total_data_size = self.w_header.get_data_size() + self.w_format.get_total_size() + self.w_data.get_total_size()

		# Write Header Chunk to string with total size in Little Endian Format
		file_list = list (self.w_header.get_id())
		file_list += [str(chr((total_data_size >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_header.data_to_list()

		# Write format Chunk to string with format string size in Little Endian Format
		file_list += list (self.w_format.get_id())
		file_list += [str(chr((self.w_format.get_data_size() >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_format.data_to_list()

		# Write data Chunk to string with sonic data string size in Little Endian Format
		file_list += list(self.w_data.get_id())
		file_list += [str(chr((self.w_data.get_data_size() >> i) & 0xff)) for i in (0,8,16,24)]
		file_list += self.w_data.data_to_list()
		

		# Write to file
		f = open(full_file_path, 'w')
		f.write (''.join(file_list))		
		f.close()

	# Import a wav file to the object
	def import_from_file (self, full_file_path):
		
		# Read File Data
		f = open(full_file_path, 'r')	
		file_string = f.read()
		f.close()
		
		# Separate different chunk information (Header, Format, Data)
		(header_string, fmt_data_string) = file_string.split("fmt ", 1)
		(fmt_string, data_string) = fmt_data_string.split("data", 1)		
		# Ensure it is a RIFF WAVE File 		
		if "WAVE" not in header_string:
			print " - NOT a WAV File Format"
			return 0
		
		# Determine Format settings from raw format string
		# First four bytes of raw format string(first 4 characters) are size--> Remove
		self._w_fmt_value = self._fmt_raw_to_list (fmt_string[4:])
		self._w_fmt_dirty = True

		# Import Data as is. 
		self.w_data.append_string(data_string[4:])
		
		return 0

	# Given Raw Fmt string, extract all basic fmt values in list. 
	def _fmt_raw_to_list (self, a_str):
		return_list = []
		index = 0
		for size in self._w_fmt_size:
			return_list.append(self._raw_to_value(a_str[index:(index + size)], size))
			index += size
		return return_list

	# Converts a Raw File String to a numeric value (Given size in bytes, and Endian-ness)
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
			
		
		
