import numpy as np


def get_val(val) -> float | int:
    if val:
        return int(val) * 0.000001
    else:
        return 0


def conv_time_secs(time_series_data_list):
    ts_secs = [(int(time[11:13]) * 3600) + (int(time[14:16]) * 60) + (int(time[17:19])) + get_val(time[20:])
               for time in time_series_data_list]
    time_diff = np.diff(ts_secs)
    time_step = np.mean(time_diff)
    data_freq = 1 / time_step
    print("Data Frequency Rate: ", data_freq)
    # print("time_step: ", time_step)
    return data_freq, time_step, ts_secs


def preform_fft(time_series_list, acceleration_values_list):
    """
    Function to Perform FFT on the given data and return its Dominant Frequency
    Args:
        time_series_list (numpy array): Array Obtained after converting datetime data into seconds (time_step)
        acceleration_values_list (list): List containing all acceleration values of single axis corresponding to the time_series_list

    Returns:
        dominant_freq : Dominant Frequency values
        frequencies_positive : List containing all +ve Frequency values
        fft_values_positive : List containing all +ve fft values
    """
    pos_acceleration = [abs(i) for i in acceleration_values_list]
    acceleration = np.array(pos_acceleration)
    min_val = np.min(acceleration)
    max_val = np.max(acceleration)
    scaled_acceleration = (acceleration - min_val) / (max_val - min_val)
    fft_values = np.fft.fft(scaled_acceleration)
    freq = np.fft.fftfreq(len(scaled_acceleration), d=time_series_list)  # Compute frequency bins
    pve_freq = np.where(freq > 0)
    frequencies_positive = freq[pve_freq]
    fft_values_positive = fft_values[pve_freq]
    dominant_freq = frequencies_positive[np.argmax(np.abs(fft_values_positive))]
    # print("Dominant Frequency: ", dominant_freq)
    return scaled_acceleration, dominant_freq, frequencies_positive, np.abs(fft_values_positive)
