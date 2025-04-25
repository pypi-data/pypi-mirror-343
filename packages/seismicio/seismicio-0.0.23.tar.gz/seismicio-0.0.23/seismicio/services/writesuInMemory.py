from ..Models.InOutSuModel import InOutSu

def writesuInMemory(mem_fs, file_path, traces_data, hdr):
	# Write a binary file in .su format
	# at in-memory temporary file system
	with mem_fs.open(file_path, 'wb') as file:
		InOutSu.pack_and_save_su(file, traces_data, hdr)
	pass
