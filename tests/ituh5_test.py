"""Module for testing kb_imex.ituh5 package."""

# needed for debugging
import sys, os
import datetime
sys.path.append(os.path.abspath('./src/'))

import numpy as np
from itusm2117 import write_iq_dataset, read_iq_dataset


def test_basic():
    filename = "test_basic.h5"
    recordings = [1+1j, 2+2j, 3+3j, 4+4j]
    recordingsri= [[1, 2, 3, 4], [1,2,3,4]]
    recordingsri2 = [[1,1], [2,2], [3,3], [4,4]]
    metadata = {
        "sampling_frequency": 1,
        "my_field": 3
    }
    channel_suffixes = None
    group = None

    write_iq_dataset(filename, recordings, 125e6, metadata, mode = "w")
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0")
    assert len(channels) == 1 
    assert channels[0] == "Channel_0"
    assert meta["User my_field"] == 3
    assert meta["ITU-R data set class"] == "I/Q"
    assert meta["ITU-R Recommendation"] == "Rec. ITU-R SM.2117-0"
    assert meta["RF carrier frequency (Hz)"] == 0
    assert meta["Sampling frequency (Hz)"] == metadata["sampling_frequency"]
    assert meta["Data set unit"] == ""
    assert meta["Data set scaling factor"] == 1
    assert np.array_equal(arr[0], np.array(recordings, dtype="complex64"))

    
    write_iq_dataset(filename, recordings, 125e6, metadata, group = "Basic")
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0")
    assert len(channels) == 1
    assert channels[0] == "Channel_0"
    assert np.array_equal(arr[0], np.array(recordings, dtype="complex64"))
    _assert_metadata_basic(meta, metadata)
    
    write_iq_dataset(filename, recordingsri, 125e6, metadata, dataset_name = "MyDataset", group = "Basic")
    meta, arr, channels = read_iq_dataset(filename, "MyDataset", group="Basic")
    assert len(channels) == 1
    assert channels[0] == "Channel_0"    
    assert np.array_equal(arr[0], np.array(recordings, dtype="complex64"))
    _assert_metadata_basic(meta, metadata)
    
    write_iq_dataset(filename, recordingsri2, 125e6, metadata, group = "Basic")
    meta, arr, channels = read_iq_dataset(filename, "Dataset_1", group="Basic")
    assert len(channels) == 1
    assert np.array_equal(arr[0], np.array(recordings, dtype="complex64"))
    _assert_metadata_basic(meta, metadata)
    
    write_iq_dataset(filename, recordingsri2, 125e6, metadata, group = "Basic", channel_suffixes="Special")
    meta, arr, channels = read_iq_dataset(filename, "Dataset_2", group= "Basic")
    assert len(channels) == 1    
    assert np.array_equal(arr[0], np.array(recordings, dtype="complex64"))
    _assert_metadata_basic(meta, metadata)
    
    os.remove(filename)


def test_multiple_complex():
    filename = "test_multiple_complex.h5"
    recordings = np.array([[1+1j, 2+2j, 3+3j, 4+4j], [1+1j, 2+2j, 3+3j, 4+4j]])
    recordings_ri = np.array([[[1,2,3,4], [1, 2, 3, 4] ], [[1,2,3,4],[1, 2, 3, 4]]])
    recordings_ri2 = np.array([[[1, 1],[2, 2],[3, 3],[4,4]],[[1, 1],[2, 2],[3, 3],[4,4]]] )
    metadata = {
        "sampling_frequency": 125e6,
        "CBRS bin": 3,
        "Recording model": "Radar V5",
        "UserX": "X",
        "carrier_frequency": 3.6e9,
        "unit": "V",
        "scaling": 3,
        "comment": "test_multiple_complex",
        "bandwidth": 100e6,
        "device": "AIRT",
        "timestamp": datetime.datetime.now(),
        "timestamp_fine": datetime.datetime.now(),
        "latitude": 20,
        "longitude": 50,
        "altitude": 10,
        "separation": 3.1,
        "Speed over ground magnitude (m/s)": 31.4,
        "speed_azimuth": 30.3,
        "orientation_azimuth": 189.1,
        "orientation_elevation": 13.1,
        "orientation_skew":  -91.1,
        "magnetic_declination": 3.1,
        "unsynced_flag": 0,
        "invalid_flag": 0,
        "pllunlocked_flag": 0,
        "agc_flag": 0,
        "detected_flag": 1,
        "spectral_inversion_flag": 1,
        "overrange_flag": 1,
        "lostsample_flag": 1,
        "attenuator": -10.1,
        "antenna_factor": 0,
        "reference": "Antenna output port",
        "receiver_impedance": 50
    }

    write_iq_dataset(filename, recordings, 125e6, metadata, mode="w")
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0")
    assert len(channels) == 2
    assert channels[0] == "Channel_0"
    assert channels[1] == "Channel_1"
    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))
    _assert_metadata_complex(meta, metadata)    

    write_iq_dataset(filename, recordings, 125e6, metadata, group=("My", "Dataset"))
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0", group=("My", "Dataset"))
    assert len(channels) == 2
    assert channels[0] == "Channel_0"
    assert channels[1] == "Channel_1"
    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))
    _assert_metadata_complex(meta, metadata)

    write_iq_dataset(filename, recordings, 125e6, metadata, group=("My", "Dataset", "Child"), channel_suffixes=("A", "B"))
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0", group=["My", "Dataset", "Child"])
    assert len(channels) == 2
    assert channels[0] == "Channel_A"
    assert channels[1] == "Channel_B"
    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))
    _assert_metadata_complex(meta, metadata)
    
    write_iq_dataset(filename, recordings_ri, 125e6, metadata, group=("My", "Dataset", "Child2"), channel_suffixes=("A", "B"))
    meta, arr, channels = read_iq_dataset(filename, "Dataset_0", group=["My", "Dataset", "Child2"])
    assert len(channels) == 2
    assert channels[0] == "Channel_A"
    assert channels[1] == "Channel_B"
    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))
    _assert_metadata_complex(meta, metadata)
    
    write_iq_dataset(filename, recordings_ri2, 125e6, metadata, group=("My", "Dataset", "Child2"), channel_suffixes=(0, "XXXX"))
    meta, arr, channels = read_iq_dataset(filename, "Dataset_1", group=["My", "Dataset", "Child2"])
    assert len(channels) == 2
    assert channels[0] == "Channel_0"
    assert channels[1] == "Channel_XXXX"
    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))
    _assert_metadata_complex(meta, metadata)
    
    os.remove(filename)


def test_readme_flexibe():
    filename = fn = "test.h5"
    sr = sampling_rate = 125e6
    name = dataset_name = "MyDataset"

    # supports several input formats
    complex_single_channel   = np.array([1+1j, 2+2j, 3+3j, 4+4j], dtype="complex64")
    timefirst_single_channel = np.array([[1, 2, 3, 4], [1, 2, 3, 4]], dtype="float32")
    iqpairs_single_channel   = np.array([[1,1], [2,2], [3,3], [4,4]], dtype="float32")
    complex_multichannel     = np.array([[1+1j, 2+2j, 3+3j, 4+4j],  # Channel_0
                                         [1+1j, 2+2j, 3+3j, 4+4j]], # Channel_1
                                         dtype="complex64")
    timefirst_multichannel   = np.array([[[1, 2, 3, 4], [1, 2, 3, 4 ]],  # Channel_0
                                         [[1, 2, 3, 4], [1, 2, 3, 4 ]]], # Channel_1
                                         dtype="float32")
    iqpairs_multichannel     = np.array([[[1, 1],[2, 2],[3, 3],[4, 4]],  # Channel_0
                                         [[1, 1],[2, 2],[3, 3],[4, 4]]], # Channel_1
                                         dtype="float32")

    # single channel, complex data - shape (n,)
    # n = number of samples per recording
    write_iq_dataset(fn, complex_single_channel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)
    assert np.array_equal(arr[0], complex_single_channel)
    
    # single channel, one array of Is, one array Qs, shape = (2, n)
    write_iq_dataset(fn, timefirst_single_channel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)
    # the return type of arr is always complex and multi channel 
    assert np.array_equal(arr[0], complex_single_channel)

    # single channel, I/Q pairs, shape = (n, 2)
    write_iq_dataset(fn, iqpairs_single_channel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)    
    assert np.array_equal(arr[0], complex_single_channel)

    # multi channel, complex data, shape (nchannels, n)
    write_iq_dataset(fn, complex_multichannel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)
    assert np.array_equal(arr, complex_multichannel)
    
    # multi channel, one array of Is, one array Qs, shape = (nchannels, 2, n)
    write_iq_dataset(fn, timefirst_multichannel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)    
    assert np.array_equal(arr, complex_multichannel)

    # single channel, I/Q pairs, shape = (nchannels, n, 2)
    write_iq_dataset(fn, iqpairs_multichannel, sr, dataset_name = name, mode = "w")
    meta, arr, channels = read_iq_dataset(fn, name)    
    assert np.array_equal(arr, complex_multichannel)

    os.remove(fn)


def test_readme_groups():
    iq = [1+1j, 2+2j, 3+3j, 4+4j]
    iq2 = np.array(iq) * 2
    sampling_frequency = 125e5
    fn = "test_groups.h5"
    write_iq_dataset(fn, iq, sampling_frequency, group="GroupAtRoot")
    metadata, recordings, channels = read_iq_dataset(fn, "Dataset_0", group="GroupAtRoot")
    assert np.array_equal(recordings[0], np.array(iq))
    write_iq_dataset(fn, iq2, sampling_frequency, group=("GroupAtRoot", "Subgroup", "Subsubgroup"))
    metadata, recordings, channels = read_iq_dataset(fn, "Dataset_0", group=("GroupAtRoot", "Subgroup", "Subsubgroup"))
    assert np.array_equal(recordings[0], iq2)
    os.remove(fn)


def test_readme_dataset_name():
    iq_with_name = [1+1j, 2+2j, 3+3j, 4+4j]
    iq_without_name = np.array(iq_with_name, dtype="complex64") * 2.3
   
    sampling_frequency = 125e5
    fn = "test_dataset_name.h5"

    write_iq_dataset(fn, iq_with_name, sampling_frequency, group="GroupAtRoot", dataset_name="MyDataset")
    metadata, recordings, channels = read_iq_dataset(fn, "MyDataset", group="GroupAtRoot")    
    assert np.array_equal(recordings[0], np.array(iq_with_name))

    write_iq_dataset(fn, iq_without_name, sampling_frequency, group="GroupAtRoot")
    metadata, recordings, channels = read_iq_dataset(fn, "Dataset_0", group="GroupAtRoot")
    assert np.array_equal(recordings[0], iq_without_name)
    
    os.remove(fn)


def test_readme_channel_name():
    iq = np.array([[1+1j, 2+2j, 3+3j, 4+4j], [1+1j, 2+2j, 3+3j, 4+4j]])
    sampling_frequency = 125e5
    fn = "test_channel_name.h5"
    write_iq_dataset(fn, iq, sampling_frequency, channel_suffixes = ("A", "B"))
    metadata, recordings, channels = read_iq_dataset(fn, "Dataset_0")
    assert channels[0] == "Channel_A"
    assert channels[1] == "Channel_B"
    os.remove(fn)


def test_readme_metadata():
    fn = filename = "test_metadata.h5"
    recordings = np.array([[1+1j, 2+2j, 3+3j, 4+4j], [1+1j, 2+2j, 3+3j, 4+4j]])

    # the metadata dictionary can use both shorthand and full name notations
    # note that the sampling_frequency can be specified there too.
    dict_metadata = {
        "sampling_frequency": 125e6, # shorthand key 
        "carrier_frequency": 3.6e9, # shorthand key
        "Speed over ground magnitude (m/s)": 701.4  # full name key
    }
    bandwidth = 100e6
    attenuator = -30

    # mode = "w" ensures the file is rewritten if it exists
    write_iq_dataset(filename, recordings, mode="w",
        attenuator = attenuator, # arg metadata (shorthand key)
        bandwidth = bandwidth, # arg metadata (shorthand key)
        metadata = dict_metadata )

    read_metadata, arr, channels = read_iq_dataset(filename, "Dataset_0")

    assert len(channels) == 2
    assert channels[0] == "Channel_0"
    assert channels[1] == "Channel_1"

    assert np.array_equal(arr, np.array(recordings, dtype="complex64"))

    assert read_metadata["Speed over ground magnitude (m/s)"] == dict_metadata["Speed over ground magnitude (m/s)"]
    assert read_metadata["Sampling frequency (Hz)"] == dict_metadata["sampling_frequency"]
    assert read_metadata["RF carrier frequency (Hz)"] == dict_metadata["carrier_frequency"]
    assert read_metadata["Filter bandwidth (Hz)"] == bandwidth
    assert read_metadata["Attenuator (dB)"] == attenuator
    os.remove(fn)


def _assert_metadata_complex(read_metadata, write_metadata):
    assert read_metadata["User CBRS bin"] == write_metadata["CBRS bin"]
    assert read_metadata["User Recording model"] == write_metadata["Recording model"]
    assert read_metadata["UserX"] == write_metadata["UserX"]
    assert read_metadata["ITU-R data set class"] == "I/Q"
    assert read_metadata["ITU-R Recommendation"] == "Rec. ITU-R SM.2117-0"
    assert read_metadata["RF carrier frequency (Hz)"] == write_metadata["carrier_frequency"]
    assert read_metadata["Sampling frequency (Hz)"] == write_metadata["sampling_frequency"]
    assert read_metadata["Data set unit"] == write_metadata["unit"]
    assert read_metadata["Data set scaling factor"] == write_metadata["scaling"]
    assert read_metadata["Comment"] == write_metadata["comment"]
    assert read_metadata["Device"] == write_metadata["device"]
    assert read_metadata["Filter bandwidth (Hz)"] == write_metadata["bandwidth"]
    assert read_metadata["Timestamp coarse (s)"] == int(write_metadata["timestamp"].timestamp())
    assert read_metadata["Timestamp fine (ns)"] == write_metadata["timestamp_fine"].timestamp()
    assert read_metadata["Geolocation latitude (degree)"]==write_metadata["latitude"]
    assert read_metadata["Geolocation longitude (degree)"]==write_metadata["longitude"]
    assert read_metadata["Geolocation altitude (m)"]==write_metadata["altitude"]
    assert read_metadata["Geolocation separation (m)"]==write_metadata["separation"]
    assert read_metadata["Speed over ground magnitude (m/s)"]==write_metadata["Speed over ground magnitude (m/s)"]
    assert read_metadata["Speed over ground azimuth (degree)"]==write_metadata["speed_azimuth"]
    assert read_metadata["Orientation azimuth (degree)"]==write_metadata["orientation_azimuth"]
    assert read_metadata["Orientation elevation (degree)"]==write_metadata["orientation_elevation"]
    assert read_metadata["Orientation skew (degree)"]==write_metadata["orientation_skew"]
    assert read_metadata["Magnetic declination (degree)"]==write_metadata["magnetic_declination"]
    assert read_metadata["Unsynced timestamp flag"]==write_metadata["unsynced_flag"]
    assert read_metadata["Invalid flag"]==write_metadata["invalid_flag"]
    assert read_metadata["PLL unlocked"]==write_metadata["pllunlocked_flag"]
    assert read_metadata["AGC flag"]==write_metadata["agc_flag"]
    assert read_metadata["Detected signal flag"]==write_metadata["detected_flag"]
    assert read_metadata["Spectral inversion flag"]==write_metadata["spectral_inversion_flag"]
    assert read_metadata["Over range flag"]==write_metadata["overrange_flag"]
    assert read_metadata["Lost sample flag"]==write_metadata["lostsample_flag"]
    assert read_metadata["Attenuator (dB)"]==write_metadata["attenuator"]
    assert read_metadata["Antenna factor (1/m)"]==write_metadata["antenna_factor"]
    assert read_metadata["Reference point"]==write_metadata["reference"]
    assert read_metadata["Receiver input impedance (Ohm)"]==write_metadata["receiver_impedance"]


def _assert_metadata_basic(read_metadata, write_metadata):
    assert read_metadata["User my_field"] == write_metadata["my_field"]
    assert read_metadata["ITU-R data set class"] == "I/Q"
    assert read_metadata["ITU-R Recommendation"] == "Rec. ITU-R SM.2117-0"
    assert read_metadata["RF carrier frequency (Hz)"] == 0
    assert read_metadata["Sampling frequency (Hz)"] == write_metadata["sampling_frequency"]
    assert read_metadata["Data set unit"] == ""
    assert read_metadata["Data set scaling factor"] == 1



if __name__ == "__main__":
    test_basic()
    test_multiple_complex()
    test_readme_flexibe()
    test_readme_channel_name()
    test_readme_dataset_name()
    test_readme_groups
    test_readme_metadata()