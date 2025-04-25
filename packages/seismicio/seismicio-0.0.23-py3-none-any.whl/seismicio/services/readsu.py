from ..Models.InOutSuModel import InOutSu

def readsu(file_path, gather_keyword=None):
	# Read a binary file in .su format
	with open(file_path, 'rb') as file:
		return InOutSu.unpack_su(file, gather_keyword)
