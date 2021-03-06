# How To's

## Storing I/Q data into H5 groups <a name="groups"></a>

By default, the IQ data will be placed in the root of the H5 file. You can change this behavior using the ``group`` argument of ``write_iq_dataset``. This argument can be a simple string or a list of strings that will be threaded as the hierarchy of groups.

```python
from itusm2117 import write_iq_dataset, read_iq_dataset
import numpy as np

iq = [1+1j, 2+2j, 3+3j, 4+4j]
iq2 = np.array(iq) * 2
sampling_frequency = 125e5

# filename must end with '.h5' else it is appended internally
write_iq_dataset("my_iq_data.h5", iq, sampling_frequency, group="GroupAtRoot")
metadata, recordings, channels = read_iq_dataset("my_id_data.h5", "Dataset_0", group="GroupAtRoot")
assert np.array_equal(recordings[0], np.array(iq))

write_iq_dataset("my_iq_data.h5", iq2, sampling_frequency, group=("GroupAtRoot", "Subgroup", "Subsubgroup"))
metadata, recordings, channels = read_iq_dataset("my_id_data.h5", "Dataset_0", group=("GroupAtRoot", "Subgroup", "Subsubgroup"))
assert np.array_equal(recordings[0], iq2)
```


> Note on dtypes: All data is stored and read as float32 or complex64. <br /> 
> If the input uses a higher or lower number of bytes, it will be converted internally accordingly. <br />
> For example, all float types will be converted to float32 (if needed) and all complex types will be converted to complex64 (if needed).

___

## Naming I/Q datasets

For each call of the ``write_iq_dataset``an H5 dataset is created. If the name for the dataset is not specified through the ``dataset_name`` argument one will be generated with the prefix **'Dataset_'** plus the next available integer in that H5 group (e.g., 'Dataset_0').

```python
from itusm2117 import write_iq_dataset, read_iq_dataset
import numpy as np

iq_with_name = [1+1j, 2+2j, 3+3j, 4+4j]
iq_without_name = np.array(iq_with_name) * 2
sampling_frequency = 125e5
fn = "test_dataset_name.h5"

write_iq_dataset(fn, iq_with_name, sampling_frequency, group="GroupAtRoot", dataset_name="MyDataset")
metadata, recordings, channels = read_iq_dataset(fn, "MyDataset", group="GroupAtRoot")
assert np.array_equal(recordings[0], np.array(iq_with_name))

write_iq_dataset(fn, iq_without_name, sampling_frequency, group="GroupAtRoot")
metadata, recordings, channels = read_iq_dataset(fn, "Dataset_0", group="GroupAtRoot")
assert np.array_equal(recordings[0], iq_without_name)
```
___

## Naming channels <a name="channels"></a>

Unspecified channels will be named 'Channel_0', 'Channel_1', and so on.
You can alter this behavior by specifying ``channel_suffixes``. 
Note that starting the channel name with "Channel_" is mandatory per ITU-R SM.2117-0.

```python
from itusm2117 import write_iq_dataset, read_iq_dataset
import numpy as np

iq = np.array([
[1+1j, 2+2j, 3+3j, 4+4j], 
[1+1j, 2+2j, 3+3j, 4+4j]])
sampling_frequency = 125e5

write_iq_dataset("my_iq_data.h5", iq, sampling_frequency, channel_suffixes = ("A", "B"))
metadata, recordings, channels = read_iq_dataset("my_iq_data.h5", "Dataset_0")

assert channels[0] == "Channel_A"
assert channels[1] == "Channel_B"
```
___

## Supported data types and shapes

This library supports 6 different input shapes. The one used is inferred at runtime.

```python
from itusm2117 import write_iq_dataset, read_iq_dataset
import numpy as np
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

# n = number of samples per recording
# single channel, complex data, shape = (n,)
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

# multi channel, complex data, shape = (nchannels, n)
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
```
___

## Adding metadata <a name="metadata"></a>

There are several predefined attributes (key-value pairs) supported by the ITU-R SM.2117-0, listed below. They can be passed to the ``write_iq_dataset`` method via the ``metadata`` dictionary or as a directly named method argument. In the latter case, it is necessary to use the shorthand notation below. When using the dictionary, it is possible to use either the shorthand and/or the full name. Attributes not listed below are considered user defined attributes and are prefixed with 'User ' as specified in the  ITU-R SM.2117-0.

> Note: The metadata is validated according to the ITU-R SM.2117-0 and ValueError exceptions will be raised if any value provided is not in accordance. Please refer to the official [document](https://www.itu.int/rec/R-REC-SM.2117-0-201809-I) for acceptable data types and values.


| Shorthand                 | Full name                           |
| :---:                     |:---:                                |
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

When reading files using ``read_iq_dataset`` the returned metadata is always in the full name notation.

```python
from itusm2117 import write_iq_dataset, read_iq_dataset
import numpy as np
filename = "test2.h5"
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
```
