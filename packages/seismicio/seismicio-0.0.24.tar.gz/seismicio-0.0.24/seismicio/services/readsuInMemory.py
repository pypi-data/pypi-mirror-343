from ..Models.InOutSuModel import InOutSu

def readsuInMemory(mem_fs, file_path):
	# Read a binary file in .su format
	# from in-memory temporary file system
	with mem_fs.open(file_path, 'rb') as file:
		return InOutSu.unpack_su(file)
