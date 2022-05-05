"""Private helper methods of the kb_imex.ituh5 package."""

from enum import Enum

import numpy as np

from itusm2117._schema import ORDER

def navigate_groups(parent, groups):
    if len(groups) == 1:
        group = groups[0]
        if group in parent:
            return parent[group]
        else:
            raise IndexError("Group name not found")
    else:
        group = groups.pop()
        if group in parent:
            parent = parent[group]
        else:
            raise IndexError("Group name not found")
        return create_or_navigate_groups(parent, groups)

def create_or_navigate_groups(parent, groups):
    if len(groups) == 1:
        group = groups[0]
        if group in parent:
            return parent[group]
        else:
            return parent.create_group(group)
    else:
        group = groups.pop()
        if group in parent:
            parent = parent[group]
        else:
            parent = parent.create_group(group)
        return create_or_navigate_groups(parent, groups)

def index_generator(size):
    for i in range(0, size):
        yield i

def get_next_dataset_index(group):
    keys = group.keys()
    suffixes = ["_".join(key.split("_")[1:]) for key in keys if key.startswith("Dataset_")]
    numbers = [int(s) for s in suffixes if s.isdigit()]
    numbers.sort()
    if len(numbers) == 0:
        next_int = 0
    else:
        next_int = numbers[len(numbers)-1] + 1
    return next_int

def list_generator(suffixes):
    for suffix in suffixes:
        yield suffix        

def reorder_metadata(metadata):
        result = {}        
        for key in ORDER:
            if key in metadata:
                result[key] = metadata[key]
        for k, v in metadata.items():
            if k not in result:
                if k.startswith("User"):
                    result[k] = v
                else:
                    result["User " + k] = v
        return result

class RecordingFormat(Enum):
    SINGLE_COMPLEX = (None,)
    SINGLE_IQ_FIRST = (2, None)
    SINGLE_TIME_FIRST = (None, 2)
    MULTIPLE_COMPLEX = (None, None)
    MULTIPLE_IQ_FIRST = (None, 2, None)
    MULTIPLE_TIME_FIRST = (None, None, 2)
    INVALID = 6

    def get_size(self, recordings):
        if self ==  RecordingFormat.SINGLE_COMPLEX:
            return recordings.shape[0]
        elif self == RecordingFormat.SINGLE_IQ_FIRST:
            return recordings.shape[1]
        elif self == RecordingFormat.SINGLE_TIME_FIRST:
            return recordings.shape[0]
        elif self ==  RecordingFormat.MULTIPLE_COMPLEX:
            return recordings.shape[1]
        elif self == RecordingFormat.MULTIPLE_IQ_FIRST:
            return recordings.shape[2]
        elif self == RecordingFormat.MULTIPLE_TIME_FIRST:
            return recordings.shape[1]

    def get_parsing_function(self):
        def complex_parse(recording):
            # if recording.dtype != np.complex64:
            #     recording = np.complex64(recording)
            real = np.real(recording)
            imag = np.imag(recording)
            arr = np.float32([real, imag])
            newarr = np.swapaxes(arr,0,1)
            return list(map(tuple, newarr))
            # newarr = newarr.view(dtype = np.dtype([("Real", newarr.dtype), ("Imag", newarr.dtype)]))
            # newarr = newarr.reshape(arr.shape[:-1])
            # return arr   

        def iqfirst_parse(recording):
            newarr = np.swapaxes(np.float32(recording),0,1)
            return list(map(tuple, newarr))
            # if recording.dtype != np.float32:
            #     recording = np.float32(recording)
            # real = recording[0]
            # imag = recording[1]
            # return real, imag
        def timefirst_parse(recording):
            newarr = np.float32(recording)
            return list(map(tuple, newarr))
            # if recording.dtype != np.float32:
            #     recording = np.float32(recording)
            # real = recording[:,0]
            # imag = recording[:,1]
            # return real, imag

        if (self == RecordingFormat.SINGLE_COMPLEX 
            or self == RecordingFormat.MULTIPLE_COMPLEX):
            return complex_parse
        elif (self == RecordingFormat.SINGLE_IQ_FIRST
            or self == RecordingFormat.MULTIPLE_IQ_FIRST):
            return iqfirst_parse
        else:
            return timefirst_parse

MULTIPLE_RECORDINGS = set((RecordingFormat.MULTIPLE_COMPLEX, RecordingFormat.MULTIPLE_IQ_FIRST, RecordingFormat.MULTIPLE_TIME_FIRST))

SINGLE_RECORDING = set((RecordingFormat.SINGLE_COMPLEX, RecordingFormat.SINGLE_IQ_FIRST, RecordingFormat.SINGLE_TIME_FIRST))

def determine_format(recordings):

    if len(recordings.shape) == 1:
        return RecordingFormat.SINGLE_COMPLEX
    
    elif len(recordings.shape) == 2:
        if recordings.shape[0] == 2 and recordings.shape[1] !=2 and not np.iscomplexobj(recordings):
            return RecordingFormat.SINGLE_IQ_FIRST
        elif recordings.shape[1] == 2 and recordings.shape[0] !=2:
            return RecordingFormat.SINGLE_TIME_FIRST
        else:
            return RecordingFormat.MULTIPLE_COMPLEX
    
    elif len(recordings.shape) == 3:
        if recordings.shape[1] == 2 and recordings.shape[2] !=2:
            return RecordingFormat.MULTIPLE_IQ_FIRST
        elif recordings.shape[2] == 2 and recordings.shape[1] !=2:
            return RecordingFormat.MULTIPLE_TIME_FIRST
        else:
            return RecordingFormat.INVALID

    else:
        return RecordingFormat.INVALID