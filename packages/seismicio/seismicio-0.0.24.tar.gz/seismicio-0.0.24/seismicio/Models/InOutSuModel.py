import struct
import numpy as np
import pandas as pd

from .UtilsModel import Utils
from .SuDataModel import SuFile, Header
from ..constants.HEADER_FORMAT_STRING import HEADER_FORMAT_STRING
from ..constants.TRACE_HEADER_SIZE import TRACE_HEADER_SIZE
from ..constants.HEADER_KEYS import HEADER_KEYS

# https://docs.python.org/3/library/struct.html#format-strings
class InOutSu():
    @staticmethod
    def unpack_su(file, gather_keyword=None):
        # Read number of samples (how many values a trace has)
        file.seek(114)  # change stream position to byte 114
        bytes_to_unpack = file.read(2)  # read 2 bytes
        trace_samples_amount = struct.unpack('<H', bytes_to_unpack)[0]

        file_size = Utils.get_file_size(file)

        # Compute number of traces
        trace_data_size = trace_samples_amount * 4
        traces_amount = file_size // (trace_data_size + TRACE_HEADER_SIZE)

        traces_data = np.zeros(shape=(trace_samples_amount, traces_amount), dtype=np.float32)
        headers = Utils.new_empty_header(traces_amount)

        data_format_string = f'{trace_samples_amount}f'
        file.seek(0)
        for index in range(traces_amount):
            # Read trace header
            header_bytes = file.read(TRACE_HEADER_SIZE)
            header_values = struct.unpack_from(HEADER_FORMAT_STRING, header_bytes)

            for key, value in zip(HEADER_KEYS, header_values):
                headers[key][index] = value

            # Read data trace
            data_bytes = file.read(trace_data_size)
            traces_data[:, index] = np.array(
                struct.unpack(data_format_string, data_bytes),
                dtype=np.float32
            )
        return SuFile(traces_data, Header(**headers), gather_keyword)
    
    @staticmethod
    def pack_and_save_su(file, traces_data, hdr):
        n_samples, n_traces = traces_data.shape
        trace_data_size = n_samples * 4
        data_format = f'{n_samples}f'

        print(f'Number of samples: {n_samples}')
        print(f'Number of traces: {n_traces}')

        for i in range(n_traces):
            # Write trace header
            file.seek(Utils.get_header_position(i, trace_data_size))
            header_bytes = struct.pack(
                HEADER_FORMAT_STRING, hdr.tracl[i], hdr.tracr[i], hdr.fldr[i],
                hdr.tracf[i], hdr.ep[i], hdr.cdp[i], hdr.cdpt[i], hdr.trid[i],
                hdr.nvs[i], hdr.nhs[i], hdr.duse[i], hdr.offset[i],
                hdr.gelev[i], hdr.selev[i], hdr.sdepth[i], hdr.gdel[i],
                hdr.sdel[i], hdr.swdep[i], hdr.gwdep[i], hdr.scalel[i],
                hdr.scalco[i], hdr.sx[i], hdr.sy[i], hdr.gx[i], hdr.gy[i],
                hdr.counit[i], hdr.wevel[i], hdr.swevel[i], hdr.sut[i],
                hdr.gut[i], hdr.sstat[i], hdr.gstat[i], hdr.tstat[i],
                hdr.laga[i], hdr.lagb[i], hdr.delrt[i], hdr.muts[i],
                hdr.mute[i], hdr.ns[i], hdr.dt[i], hdr.gain[i], hdr.igc[i],
                hdr.igi[i], hdr.corr[i], hdr.sfs[i], hdr.sfe[i], hdr.slen[i],
                hdr.styp[i], hdr.stas[i], hdr.stae[i], hdr.tatyp[i],
                hdr.afilf[i], hdr.afils[i], hdr.nofilf[i], hdr.nofils[i],
                hdr.lcf[i], hdr.hcf[i], hdr.lcs[i], hdr.hcs[i], hdr.year[i],
                hdr.day[i], hdr.hour[i], hdr.minute[i], hdr.sec[i],
                hdr.timbas[i], hdr.trwf[i], hdr.grnors[i], hdr.grnofr[i],
                hdr.grnlof[i], hdr.gaps[i], hdr.otrav[i], hdr.d1[i], hdr.f1[i],
                hdr.d2[i], hdr.f2[i], hdr.ungpow[i], hdr.unscale[i])
            file.write(header_bytes)
            # Write trace data
            file.seek(Utils.get_data_position(i, trace_data_size))
            data_bytes = struct.pack(data_format, *traces_data[:, i])
            file.write(data_bytes)