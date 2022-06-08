# ITU-R SM.2117-0 Python Library

## Table of contents

  - [Introduction](#introduction)
  - [Quick Start](#quick-start)  
    - [Installation](#installation)
    - [Dependencies](#installation)
    - [Writing Data](#installation)
    - [Reading Data](#installation)
  - [Limitations](#limitations)
  - [How To](#how-tos)
    - [Store I/Q data into H5 groups <a name="groups"></a>](docs/howtos.md#storing-iq-data-into-h5-groups)
    - [Name I/Q datasets](docs/howtos.md#naming-iq-datasets)
    - [Name channels <a name="channels"></a>](docs/howtos.md#naming-channels)
    - [Supported data types and shapes](docs/howtos.md#supported-data-types-and-shapes)
    - [Add metadata <a name="metadata"></a>](docs/howtos.md#adding-metadata)
  - [License](#license)
  - [Contact](#contact)
  
___


# Introduction

This is an HDF5 read-write Python library for the data format in [Recommendation 
ITU-R SM.2117-0](https://www.itu.int/rec/R-REC-SM.2117-0-201809-I). ITU-R SM.2117-0 is a data format definition for exchanging stored I/Q data with the intention of spectrum monitoring. Key Bridge Wireless supports the ITU in creating a library for the data format as a contribution to IEEE 1900.8 Working Group. 
___

### The Format

The HDF5 is a generic and flexible file format for storing data and metadata. The ITU-R SM.211-0 describes a way to store IQ data using the HDF5 format. Below is an overview of the format.

![itu hdf5](docs/ituhdf5.png)

Check the content of a given HDF5 file using a desktop application called [Argos](https://github.com/titusjan/argos). Below is an example of a file opened with Argos that follows the specs in the ITU-R SM.211-0.

![argos](docs/argos.png)
___

## Quick Start


### Installation

To get started, make sure to install Python version 2.8.2 on your machine. Use the following scrips: 
```bash
pip install itusm2117
```

### Dependencies

Direct dependiencies are the following. 
- **numpy** is used for array manipulation.
- **h5py** is for reading and writing HDF5 files.
- **cerberus** is for metadata validation and normalization.

### Writing Data

```python
import numpy as np
from itusm2117 import write_iq_dataset

# The data: a list or np.array with complex values.
# Other data types and shapes are possible, check the docs.
iq = [1+1j, 2+2j, 3+3j, 4+4j]

# The only mandatory metadata of the Recomendation that
# doens't have a default or fixed value is the Sampling Frequency
# in Hertz.
sampling_frequency = 125e6

# Method for writing the data. First argument is the filename.
# By default, it will store the iq data on a dataset named
# "Dataset_0" and channel named "Channel_0".
write_iq_dataset("my_iq_data.h5", iq, sampling_frequency)
```

### Reading Data
```python
from itusm2117 import read_iq_dataset

# Method for read the data. First argument is the filename and 
# the second is the dataset name.
metadata, recordings, channels = read_iq_dataset("my_iq_data.h5", "Dataset_0")
# metadata: A dict with the key-value pairs of metadata from "Dataset_0".
# recordings: np.array of complex64 with the IQ data. First dimension is the channel.
# channels: List with the channels names (can be only one).
```

## Limitations

Currently, this library does not support the following specs on the **ITU-R SM.2117-0**:
- **Multisector datasets** are used for IQ recordings with metadata changing over time
- **Bitfield datasets** are used for marking each sample of a recording with specific flags.
- **Integet datasets.** All datasets are stored as float32.
___

## How To's

Check the following information for the different datasets and channel. 
- [Store I/Q data into H5 groups <a name="groups"></a>](docs/howtos.md#storing-iq-data-into-h5-groups)
- [Name I/Q datasets](docs/howtos.md#naming-iq-datasets)
- [Name channels <a name="channels"></a>](docs/howtos.md#naming-channels)
- [Supported data types and shapes](docs/howtos.md#supported-data-types-and-shapes)
- [Add metadata <a name="metadata"></a>](docs/howtos.md#adding-metadata)

___

## License
[MIT](./LICENSE)
___

## Contact
Contact us through our GitHub account for comments, questions, or pull requests.
