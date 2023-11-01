import numpy as np


def conv_time_secs(ts_sec_list):  # Note: the list is in epoch timestamp (in second) Not Datetime
    # ts_secs = [(int(time[11:13]) * 3600) + (int(time[14:16]) * 60) + (int(time[17:19])) + (int(time[20:]) * 0.000001)
    #            for time in time_series_data_list]
    time_diff = np.diff(ts_sec_list)
    time_step = np.mean(time_diff)
    data_freq = 1 / time_step
    print("Data Frequency Rate: ", data_freq)
    return data_freq, time_step


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
    acceleration = np.array(acceleration_values_list)
    min_val = np.min(acceleration)
    max_val = np.max(acceleration)
    scaled_acceleration = (acceleration - min_val) / (max_val - min_val)

    fft_values = np.fft.fft(scaled_acceleration)
    freq = np.fft.fftfreq(len(scaled_acceleration), d=time_series_list)  # Compute frequency bins
    pve_freq = np.where(freq > 0)
    frequencies_positive = freq[pve_freq]
    fft_values_positive = fft_values[pve_freq]
    dominant_freq = frequencies_positive[np.argmax(np.abs(fft_values_positive))]
    print("Dominant Frequency: ", dominant_freq)
    return dominant_freq, frequencies_positive, np.abs(fft_values_positive)