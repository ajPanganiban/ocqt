import matlab.engine
import numpy as np

def remove_symmetry(data):
    '''Tranforms ocqt coefficients to spectrogram-ready data.
    :param data: transform coefficients from ocqt
    :type data: numpy array
    :returns: array with removed symmetry over the x axis
    '''
    num_rows = data.shape[0]
    half = data[:int(np.floor(num_rows/2))]
    mid = data[int(np.floor(num_rows/2))]
    imag = np.imag(half)
    return {'half': half, 'mid': mid, 'imag':imag}
