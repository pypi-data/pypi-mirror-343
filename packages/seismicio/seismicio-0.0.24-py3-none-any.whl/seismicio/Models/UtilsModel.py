import numpy as np
from io import SEEK_END
from ..constants.TRACE_HEADER_SIZE import TRACE_HEADER_SIZE

class Utils():
	@staticmethod
	def get_header_position(index, trace_data_size):
		return (TRACE_HEADER_SIZE + trace_data_size) * index

	@staticmethod
	def get_data_position(index, trace_data_size):
		return (TRACE_HEADER_SIZE + trace_data_size) * index + TRACE_HEADER_SIZE
	
	@staticmethod
	def get_file_size(file):
		file.seek(0, SEEK_END)
		return file.tell()

	@staticmethod
	def new_empty_header(traces_amount):
		header = {
			'tracl': np.zeros(traces_amount, dtype=np.int32),
			'tracr': np.zeros(traces_amount, dtype=np.int32),
			'fldr': np.zeros(traces_amount, dtype=np.int32),
			'tracf': np.zeros(traces_amount, dtype=np.int32),
			'ep': np.zeros(traces_amount, dtype=np.int32),
			'cdp': np.zeros(traces_amount, dtype=np.int32),
			'cdpt': np.zeros(traces_amount, dtype=np.int32),
			'trid': np.zeros(traces_amount, dtype=np.int16),
			'nvs': np.zeros(traces_amount, dtype=np.int16),
			'nhs': np.zeros(traces_amount, dtype=np.int16),
			'duse': np.zeros(traces_amount, dtype=np.int16),
			'offset': np.zeros(traces_amount, dtype=np.int32),
			'gelev': np.zeros(traces_amount, dtype=np.int32),
			'selev': np.zeros(traces_amount, dtype=np.int32),
			'sdepth': np.zeros(traces_amount, dtype=np.int32),
			'gdel': np.zeros(traces_amount, dtype=np.int32),
			'sdel': np.zeros(traces_amount, dtype=np.int32),
			'swdep': np.zeros(traces_amount, dtype=np.int32),
			'gwdep': np.zeros(traces_amount, dtype=np.int32),
			'scalel': np.zeros(traces_amount, dtype=np.int16),
			'scalco': np.zeros(traces_amount, dtype=np.int16),
			'sx': np.zeros(traces_amount, dtype=np.int32),
			'sy': np.zeros(traces_amount, dtype=np.int32),
			'gx': np.zeros(traces_amount, dtype=np.int32),
			'gy': np.zeros(traces_amount, dtype=np.int32),
			'counit': np.zeros(traces_amount, dtype=np.int16),
			'wevel': np.zeros(traces_amount, dtype=np.int16),
			'swevel': np.zeros(traces_amount, dtype=np.int16),
			'sut': np.zeros(traces_amount, dtype=np.int16),
			'gut': np.zeros(traces_amount, dtype=np.int16),
			'sstat': np.zeros(traces_amount, dtype=np.int16),
			'gstat': np.zeros(traces_amount, dtype=np.int16),
			'tstat': np.zeros(traces_amount, dtype=np.int16),
			'laga': np.zeros(traces_amount, dtype=np.int16),
			'lagb': np.zeros(traces_amount, dtype=np.int16),
			'delrt': np.zeros(traces_amount, dtype=np.int16),
			'muts': np.zeros(traces_amount, dtype=np.int16),
			'mute': np.zeros(traces_amount, dtype=np.int16),
			'ns': np.zeros(traces_amount, dtype=np.uint16),
			'dt': np.zeros(traces_amount, dtype=np.uint16),
			'gain': np.zeros(traces_amount, dtype=np.int16),
			'igc': np.zeros(traces_amount, dtype=np.int16),
			'igi': np.zeros(traces_amount, dtype=np.int16),
			'corr': np.zeros(traces_amount, dtype=np.int16),
			'sfs': np.zeros(traces_amount, dtype=np.int16),
			'sfe': np.zeros(traces_amount, dtype=np.int16),
			'slen': np.zeros(traces_amount, dtype=np.int16),
			'styp': np.zeros(traces_amount, dtype=np.int16),
			'stas': np.zeros(traces_amount, dtype=np.int16),
			'stae': np.zeros(traces_amount, dtype=np.int16),
			'tatyp': np.zeros(traces_amount, dtype=np.int16),
			'afilf': np.zeros(traces_amount, dtype=np.int16),
			'afils': np.zeros(traces_amount, dtype=np.int16),
			'nofilf': np.zeros(traces_amount, dtype=np.int16),
			'nofils': np.zeros(traces_amount, dtype=np.int16),
			'lcf': np.zeros(traces_amount, dtype=np.int16),
			'hcf': np.zeros(traces_amount, dtype=np.int16),
			'lcs': np.zeros(traces_amount, dtype=np.int16),
			'hcs': np.zeros(traces_amount, dtype=np.int16),
			'year': np.zeros(traces_amount, dtype=np.int16),
			'day': np.zeros(traces_amount, dtype=np.int16),
			'hour': np.zeros(traces_amount, dtype=np.int16),
			'minute': np.zeros(traces_amount, dtype=np.int16),
			'sec': np.zeros(traces_amount, dtype=np.int16),
			'timbas': np.zeros(traces_amount, dtype=np.int16),
			'trwf': np.zeros(traces_amount, dtype=np.int16),
			'grnors': np.zeros(traces_amount, dtype=np.int16),
			'grnofr': np.zeros(traces_amount, dtype=np.int16),
			'grnlof': np.zeros(traces_amount, dtype=np.int16),
			'gaps': np.zeros(traces_amount, dtype=np.int16),
			'otrav': np.zeros(traces_amount, dtype=np.int16),
			'd1': np.zeros(traces_amount, dtype=np.float32),
			'f1': np.zeros(traces_amount, dtype=np.float32),
			'd2': np.zeros(traces_amount, dtype=np.float32),
			'f2': np.zeros(traces_amount, dtype=np.float32),
			'ungpow': np.zeros(traces_amount, dtype=np.float32),
			'unscale': np.zeros(traces_amount, dtype=np.float32),
			'ntr': np.zeros(traces_amount, dtype=np.int32),
			'mark': np.zeros(traces_amount, dtype=np.int16),
			'shortpad': np.zeros(traces_amount, dtype=np.int16)
		}

		return header
