from .constants import ClarityType


# Define a class for BufferCV
class BufferCV:
    def __init__(self, clarity_type: ClarityType, buffer: bytes):
        self.type = clarity_type
        self.buffer = buffer

    @property
    def value(self):
        return self.buffer

    @property
    def buffer_length(self):
        return len(self.buffer)


# Define a function to create a BufferCV clarity type from a bytes buffer
def buffer_cv(buffer: bytes) -> BufferCV:
    if len(buffer) > 1_000_000:
        raise ValueError('Cannot construct clarity buffer that is greater than 1MB')
    return BufferCV(ClarityType.Buffer, buffer)


# Define a function to create a BufferCV clarity type from a string
def buffer_cv_from_string(input_string: str) -> BufferCV:
    buffer = input_string.encode('utf-8')
    return buffer_cv(buffer)
