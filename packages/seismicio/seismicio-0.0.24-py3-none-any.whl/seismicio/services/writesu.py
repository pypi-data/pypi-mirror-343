from ..Models.InOutSuModel import InOutSu

def writesu(file_path, traces_data, hdr):
	# Write a binary file in .su format
	with open(file_path, 'wb') as file:
		InOutSu.pack_and_save_su(file, traces_data, hdr)
	pass
