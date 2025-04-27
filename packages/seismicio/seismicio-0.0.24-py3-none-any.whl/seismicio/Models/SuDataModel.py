from types import SimpleNamespace
import numpy as np
import numpy.typing as npt
from .UtilsModel import Utils
import pandas as pd


class Header(SimpleNamespace):
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class HeadersView:
    def __init__(self, start, stop, headers):
        self._start = start
        self._stop = stop
        self._headers = headers

    def __getitem__(self, header_keyword):
        return self._headers[header_keyword][self._start : self._stop]


class GatherView:
    def __init__(self, start: int, stop: int, data, headers):
        self._start = start
        self._stop = stop
        self._origin_data = data
        self._origin_headers = headers
        self._headers_view = HeadersView(start, stop, headers)
        self.num_traces: int = stop - start

    @property
    def data(self):
        return self._origin_data[:, self._start : self._stop]

    @property
    def headers(self):
        return self._headers_view


class iGatherIndexer:

    def __init__(self, gather_indices: pd.DataFrame, origin_data, origin_headers):
        self.gather_indices = gather_indices
        self.origin_data = origin_data
        self.origin_headers = origin_headers

    def __getitem__(self, key):
        if isinstance(key, int):
            start_index = self.gather_indices["start"].iat[key]
            stop_index = self.gather_indices["stop"].iat[key]
        elif isinstance(key, slice):
            if (not key.step is None) and (key.step != 1):
                raise ValueError("No support for step in slice!")
            if key.start is None:
                start_index = 0
            else:
                start_index = self.gather_indices["start"].iat[key.start]
            if key.stop is None:
                stop_index = self.origin_data.shape[1] - 1  # num_traces - 1
            else:
                stop_index = self.gather_indices["stop"].iat[key.stop - 1]
        else:
            raise TypeError("key must be either int or slice!")
        return GatherView(start_index, stop_index, self.origin_data, self.origin_headers)


class vGatherIndexer:

    def __init__(self, gather_indices: pd.DataFrame, origin_data, origin_headers):
        self.gather_indices = gather_indices
        self.origin_data = origin_data
        self.origin_headers = origin_headers

    def __getitem__(self, key):
        print(f"key type {type(key)}")
        if isinstance(key, int):
            start_index = self.gather_indices["start"].at[key]
            stop_index = self.gather_indices["stop"].at[key]
        elif isinstance(key, slice):
            if (not key.step is None) and (key.step != 1):
                raise ValueError("No support for step in slice!")
            if key.start is None:
                start_index = 0
            else:
                start_index = self.gather_indices["start"].at[key.start]
            if key.stop is None:
                stop_index = self.origin_data.shape[1] - 1  # num_traces - 1
            else:
                stop_index = self.gather_indices["stop"].at[key.stop]
        else:
            raise TypeError("key must be either int or slice!")
        return GatherView(start_index, stop_index, self.origin_data, self.origin_headers)


class SuFile:
    """Store and manipulate a seismic data file in SU format.

    Attributes:
      data (ndarray): Trace data from the entire file.
      headers (Header): Trace headers from the entire file.
      num_traces (int): Number of traces.
      num_gathers (int): Number of gathers. None if gather_keyword was not
        specified at creation.
    """

    def __init__(self, data: npt.NDArray[np.float64], headers: Header, gather_keyword=None):
        """Initialize the instance using already prepared data.

        Args:
          data: Trace data for this instance.
          headers: Trace headers for this instance.
          gather_keyword: Header keyword that comprises the gathers.
        """
        self.data = data
        self.headers = headers
        self.num_traces = data.shape[1]
        self.gather_keyword = gather_keyword

        self.num_gathers = None
        self.gather_indices_df = None
        self._vGatherIndexer = None
        self._iGatherIndexer = None

        # Ignore gather slicing capabilities if no gather keyword was given
        if gather_keyword is None:
            return

        # Set up gather slicing capabilites
        # ---------------------------------

        separation_indices = [0]
        separation_key = self.headers[gather_keyword]

        gather_values = [separation_key[0]]

        for trace_index in range(1, self.num_traces):
            if separation_key[trace_index] != separation_key[trace_index - 1]:
                gather_values.append(separation_key[trace_index])
                separation_indices.append(trace_index)
        separation_indices.append(self.num_traces)

        self.gather_indices_df = pd.DataFrame(
            {"start": separation_indices[:-1], "stop": separation_indices[1:]},
            index=gather_values,
        )

        self.num_gathers = len(separation_indices) - 1

        self._vGatherIndexer = vGatherIndexer(self.gather_indices_df, data, headers)
        self._iGatherIndexer = iGatherIndexer(self.gather_indices_df, data, headers)

    @staticmethod
    def new_empty_gathers(
        num_samples_per_trace: int,
        gather_keyword: str,
        gather_values: list,
        num_traces_per_gather: int,
    ):
        num_traces = num_traces_per_gather * len(gather_values)
        traces = np.zeros(shape=(num_samples_per_trace, num_traces), dtype=float)
        headers = Utils.new_empty_header(num_traces)
        for i, value in enumerate(gather_values):
            itrace_start = i * num_traces_per_gather
            itrace_end = itrace_start + num_traces_per_gather
            headers[gather_keyword][itrace_start:itrace_end] = value

        return SuFile(traces, Header(**headers), gather_keyword)

    @property
    def num_samples(self) -> int:
        """Number of samples per data trace."""
        return self.headers.ns[0]

    @property
    def gather(self) -> vGatherIndexer:
        """Access a single gather or a group of gathers by label.

        A (gather) label is gather keyword value that indentifies a specific
        gather in the seismic data file.

        When slicing by label, both the start and the stop are included, which
        is contrary to usual python slices, where start is included but stop
        is excluded.

        Allowed inputs are:
        - A single label, e.g. ``200``.
        - A slice object with labels, e.g. ``200:201``.

        In order to work correctly, this feature needs two conditions met:
        - The ``gather_keyword`` attribute was set to a valid keyword when
          creating the object.
        - The traces in the file are already sorted by the specified keyword.
        """
        return self._vGatherIndexer

    @property
    def igather(self) -> iGatherIndexer:
        """Access a single gather or an interval of gathers by zero-based
        integer position (index).

        It provides lookups based on the order that the gathers were found in
        the file. The first gather has index 0, the second has index 1, and so
        forth.

        When slicing by index, the behaviour is the same as in usual Python
        slices, that is, start is included but stop is excluded.

        In order to work correctly, this feature needs two conditions met:
        - The ``gather_keyword`` attribute was set to a valid keyword when
          creating the object.
        - The traces in the file are already sorted by the specified keyword.
        """
        return self._iGatherIndexer

    @property
    def gather_values(self):
        return self.gather_indices_df.index.to_numpy()

    def gather_value_to_index(self, gather_value: int):
        """Find out the integer position index of the gather with the given value"""
        gather_values: pd.Index = self.gather_indices_df.index
        gather_index = gather_values.get_loc(gather_value)
        return gather_index

    def gather_index_to_value(self, gather_index: int):
        """Find out the value of the gather with the given integer position index"""
        gather_values: pd.Index = self.gather_indices_df.index
        gather_value = gather_values[gather_index]
        return gather_value
