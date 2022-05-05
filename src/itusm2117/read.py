"""
Public methods for reading I/Q recordings according to ITU-R SM.2117-0.
"""

import h5py
import numpy as np

from itusm2117._internal import *

def read_iq_dataset(filename, dataset_name, group = None):
    """ Method for reading I/Q recordings according to ITU-R SM.2117-0.   

    Example usage:
    >>> from kb_imex.ituh5 import write_iq_dataset, read_iq_dataset
    >>> import numpy as np
    >>> iq = [1+1j, 2+2j, 3+3j, 4+4j]
    >>> sampling_frequency = 125e5
    >>> write_iq_dataset("my_iq_data.h5", iq, sampling_frequency)
    >>> metadata, recordings, channels = read_iq_dataset("my_id_data.h5", "Dataset_0")
    >>> assert np.array_equal(recordings[0], np.array(iq))
    True
    >>> assert channels[0] == "Channel_0"
    True
    >>> assert metadata["Sampling frequency (Hz)"] == 125e6
    True

    Args:
        filename (str): Filename of the .h5 file to be read.
        dataset_name (str): Name of the dataset to be read.
        group (str, list or tuple): H5 group where the dataset resides. If a 
            list or tuple is provided, each element is considered a subgroup
            withing a tree structure. Defaults to None (root).        
    
    """

    h5 = h5py.File(filename, "r")
    try:
        if group is None:
            group = h5
        elif isinstance(group, str):
            group = h5[group]
        else:
            group = list(group)
            group.reverse()
            group = navigate_groups(h5, group)

        dataset = group[dataset_name]
        channels = dataset.dtype.names

        results = []
        for channel in channels:
            re =  dataset[channel]["Real"]
            im =  dataset[channel]["Imag"]
            results.append(re + (im * 1j))
        results = np.stack(results)

        metadata = {}
        for k, v in dataset.attrs.items():
            metadata[k] = v

        return metadata, results, channels
    
    finally:
        h5.close()

    




    
    
    