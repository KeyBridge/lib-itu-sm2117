"""
Public methods for writing I/Q recordings according to ITU-R SM.2117-0.
"""

import h5py
import numpy as np

from itusm2117._internal import *
from itusm2117._schema import validator


def write_iq_dataset(filename, recordings, sampling_frequency=None, metadata = {}, \
    group = None, dataset_name = None, channel_suffixes = None, mode = "a", **kw):
    """ Method for storing I/Q recordings according to ITU-R SM.2117-0.

    This method is flexibe to support different use cases althouth it currently
    lacks the following ITU-R SM.2117-0 features:
        - BitField datasets
        - Multisector recordings
        - Integer I/Q recordings (H5T_STD_I32LE & H5T_STD_I16LE)

    Example usage:
    >>> from kb_imex.ituh5 import write_iq_dataset
    >>> iq = [1+1j, 2+2j, 3+3j, 4+4j]
    >>> sampling_frequency = 125e5
    >>> write_iq_dataset("my_iq_data.h5", iq, sampling_frequency)
    
    Args:
        filename (str): The filename of the .h5 file where the recordings 
            should be stored. If the file doens't exists it will be created,
            if it does, the recordings will be appended.
        recordings (np.array): The I/Q data itself as a Numpy array. It can be
            a single channel or multiple channels/recordings. If n is the 
            number of time samples, the channel (or channels) can be a complex
            array of shape (n,) or it can have I/Q as a dimension, either being 
            the first dimension (second dimension for multichannel), i.e., one 
            array of shape (2, n) with I samples first Q samples second, or
            being the second dimension (third dimension for multichannel), i.e.
            , each timestep is an I/Q pair of shape (n, 2). Refer to the Enum 
            class RecordingFormat to a completed description of the supported 
            shapes. If a unsupported shape is provided, a ValueError exception
            will be raised.
        sampling_frequency (float): Defaults to None. This is the only 
            obrigatory user provided metadata of the ITU recommedation. 
            Alternatively it can be provided via the metadata dictionary (using 
            sampling_frequency as key or "Sampling frequency (Hz)"). If the 
            sampling frequency is not provided via this paramater or via the 
            dictionary, a ValueError exception will be raised.
        metadata (dict, optional): Defaults to empty dict. A dictionary with
            the metadata associated with the recordings/channels. The keys of
            the dictionary can either be the standard strings used in the
            ITU recommendation or underscored shorthands, or a combination. If
            shorthands are used, they can also be passed as standard method
            parameters. Bellow is a complete table of all metadata, with 
            standard ITU strings and shorthands. For a complete description of
            each metadata/attribute and it's accepted values, refer to the ITU 
            SM.2117-0 recommendation. Note that all metadata values are 
            validated according to the ITU rules (e.g., types, accepted 
            values). Fields not specified in the Recommendation are preffixed 
            with 'User ' unless they already starts with 'User'.
            | KB IMEX Column            | ITU Column                          |
            | _________________________ |____________________________________ |
            | (readonly)                | ITU_R data set class                |
            | (readonly)                | ITU_R Recommendation                |
            | carrier_frequency         | RF carrier frequency (Hz)           |
            | sampling_frequency        | Sampling frequency (Hz)             |
            | (readonly)                | Data set type interpretation        |
            | unit                      | Data set unit                       |
            | scaling                   | Data set scaling factor             |
            | comment                   | Comment                             |
            | device                    | Device                              |
            | bandwidth                 | Filter bandwidth (Hz)               |
            | timestamp                 | Timestamp coarse (s)                |
            | timestamp_fine            | Timestamp fine (ns)                 |
            | latitude                  | Geolocation latitude (degree)       |
            | longitude                 | Geolocation longitude (degree)      |
            | altitude                  | Geolocation altitude (m)            |
            | separation                | Geolocation separation (m)          |
            | speed                     | Speed over ground magnitude (m/s)   |
            | speed_azimuth             | Speed over ground azimuth (degree)  |
            | orientation_azimuth       | Orientation azimuth (degree)        |
            | orientation_elevation     | Orientation elevation (degree)      |
            | orientation_skew          | Orientation skew (degree)           |
            | magnetic_declination      | Magnetic declination (degree)       |
            | unsynced_flag             | Unsynced timestamp flag             |
            | invalid_flag              | Invalid flag                        |
            | pllunlocked_flag          | PLL unlocked                        |
            | agc_flag                  | AGC flag                            |
            | detected_flag             | Detected signal flag                |
            | spectral_inversion_flag   | Spectral inversion flag             |
            | overrange_flag            | Over range flag                     |
            | lostsample_flag           | Lost sample flag                    |
            | attenuator                | Attenuator (dB)                     |
            | antenna_factor            | Antenna factor (1/m)                |
            | reference                 | Reference point                     |
            | receiver_impedance        | Receiver input impedance (Ohm)      |
        group (str, list or tuple): Where to place the dataset. Defaults to 
            None. If not provided, the dataset will be placed at the root of 
            the .h5 file. If it's a string, the dataset will be placed under
            the group with specified name, and if a list or tuple of strings is
            provide, the sequence will be used as subgroups. If the any group
            doesn't exists it is created.
        dataset_name (str): The name of the dataset. Defaults to None. If not 
            provided, an auto generated name will be given with the preffix 
            Dataset_X, with X being an integer auto incremented. If a 
            duplicated name is given an error is raised.
        channel_suffixes (str, list or tuple): Name suffixes to be used for 
            each channel/recording. If not provided, a zero-based integer
            index is used.
        mode (str): Writing mode. "a" (default) for appending a new dataset and 
            "w" for creating a new file. Both modes creates a new file if it 
            doesn't exits.
        **kw: Additional metadata.

    Return:
        None
    """
    
    # Initialization
    metadata.update(kw)
    if sampling_frequency is not None:
        metadata["sampling_frequency"] = sampling_frequency    
    if isinstance(recordings, list):
        recordings = np.array(recordings)
    if not filename.endswith(".h5"):
        filename = filename + ".h5"

    # Format validation
    format = determine_format(recordings)
    if format is RecordingFormat.INVALID:
        raise ValueError(f"Invalid recording shape {recordings.shape}")
    if format in MULTIPLE_RECORDINGS and channel_suffixes is not None:
        if len(channel_suffixes) != recordings.shape[0]:
            raise ValueError(f"Number of provided recordings {recordings.shape[0]} differ from \
                number of provided channel suffixes {len(channel_suffixes)}.")

    # Cast data to appropriate type
    if format in [RecordingFormat.MULTIPLE_COMPLEX, RecordingFormat.SINGLE_COMPLEX]:
        if recordings.dtype != np.complex64:
            recordings = recordings.astype(np.complex64)
    else:
        if recordings.dtype != np.float32:
            recordings = recordings.astype(np.float32)


    # Prepare channel suffix generator
    if channel_suffixes is None:
        suffix_generator = index_generator(recordings.shape[0])
        suffix = 0
    else:
        if isinstance(channel_suffixes, str):
            channel_suffixes = [channel_suffixes]              
        suffix_generator = list_generator(channel_suffixes)
        suffix = channel_suffixes[0]

    # Normalize & order metadata
    normalized_metadata = validator.validated(metadata)
    if normalized_metadata is None:
        raise ValueError("\n".join([str(f"{k}: {v}") for k, v in validator.errors.items()]))    
    normalized_metadata = reorder_metadata(normalized_metadata) 

    # Create or navigate group
    h5 = h5py.File(filename, mode)
    if group is None:
        group = h5
    else:
        if isinstance(group, str):
            group = create_or_navigate_groups(h5, [group])
        else:
            group = list(group)
            group.reverse()
            group = create_or_navigate_groups(h5, group) 

    # Define dataset name
    if dataset_name is None:
        dataset_name = f"Dataset_{get_next_dataset_index(group)}"
    else:
        if dataset_name in group:
            raise ValueError("Dataset name {dataset_name} already exists in group.")

    # Store iq data
    if format in MULTIPLE_RECORDINGS:    
        suffixes = list(suffix_generator)
        dataset = _store_recordings(group, dataset_name, recordings, format, suffixes)
    else:    
        dataset = _store_recording(group, dataset_name, recordings, format, suffix)

    # Store metadata & exit
    for k,v in normalized_metadata.items():
        dataset.attrs.create(k, v)
    h5.close()

    return normalized_metadata


def _store_recordings(group, dataset_name, recordings, format, suffixes):
    basic_channel_dtype = [('Real', 'float32'), ('Imag', 'float32')]
    names = [f"Channel_{s}" for s in suffixes]
    types = np.dtype([(name, basic_channel_dtype) for name in names])
    n = format.get_size(recordings)
    dataset = group.create_dataset(dataset_name, (n,), dtype=types)
    parse = format.get_parsing_function()
    for i in range(0, len(names)):
        lst = parse(recordings[i])
        dataset[names[i]] = lst
    return dataset       

def _store_recording(group, dataset_name, recording, format, suffix):
    basic_channel_dtype = np.dtype([('Real', 'float32'), ('Imag', 'float32')])
    name = f"Channel_{suffix}"
    typee = [(name, basic_channel_dtype)]
    n = format.get_size(recording)
    dataset = group.create_dataset(dataset_name, (n,), dtype=typee)
    parse = format.get_parsing_function()
    lst = parse(recording)
    dataset[name] = lst
    # dataset[name]["Real"] = r
    # dataset[name]["Imag"] = i
    return dataset
    

# def _store_recording(group, recording, channel_suffix):
#         channel_key = f"Channel_{channel_suffix}"
#         if len(recording.shape) > 2:
#             raise ValueError(f"IQ recording with unsupported shape of {recording.shape}.")
#         if len(recording.shape) == 2:
#             if recording.shape[0] == 2 and recording.shape[1] !=2:
#                 real = recording[0]
#                 imag = recording[1]
#                 n = recording.shape[1]
#             elif recording.shape[1] == 2 and recording.shape[0] !=2:
#                 real = recording[:,0]
#                 imag = recording[:,1]
#                 n = recording.shape[0]
#             else:
#                 raise ValueError(f"IQ recording with unsupported shape of {recording.shape}.")        
#         elif len(recording.shape) == 1:
#             real = np.real(recording)
#             imag = np.imag(recording)
#             n = recording.shape[0]
#         channel_dataset = group.create_dataset(channel_key, (n,), dtype=np.dtype([('Real', 'float32'), ('Imag', 'float32')]))
#         channel_dataset["Real"] = real
#         channel_dataset["Imag"] = imag