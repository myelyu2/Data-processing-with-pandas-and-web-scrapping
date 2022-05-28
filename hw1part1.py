import pandas as pd
import numpy as np

# Question 1.1

def extract_hour(time):
    """
    Extracts hour information from military time.
    
    Args: 
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with hour information.  
          Should only take on integer values in 0-23
    """
    cleared = time.where(np.isnan(time) == False, "NaN")
    res = []
    for i in range(len(cleared)):
        if cleared[i] == "NaN":
            res.append(np.nan)
        else:
            if len(str(cleared[i])) == 6:
                temp = int(str(cleared[i])[0:2])
                res.append(temp if temp <= 23 and temp >= 0 else np.nan)
            elif len(str(cleared[i])) == 5:
                temp = int(str(cleared[i])[:1])
                res.append(temp if temp <= 23 and temp >= 0 else np.nan)
            elif str(cleared[i]) == "0.0":
                temp = int(str(cleared[i])[0])
                res.append(temp)
            else:
                res.append(np.nan)

    return pd.Series(res, dtype='float64')
    
def extract_mins(time):
    """
    Extracts minute information from military time
    
    Args: 
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with hour information.  
          Should only take on integer values in 0-59
    """
    cleared = time.where(np.isnan(time) == False, "NaN")
    res = []
    for i in range(len(cleared)):
        if cleared[i] == "NaN":
            res.append(np.nan)
        else:
            if len(str(cleared[i])) == 6:
                temp = int(str(cleared[i])[2:4])
                res.append(temp if temp < 60 and temp >= 0 else np.nan)
            elif len(str(cleared[i])) == 5:
                temp = int(str(cleared[i])[1:3])
                res.append(temp if temp < 60 and temp >= 0 else np.nan)
            elif str(cleared[i]) == "0.0":
                temp = int(str(cleared[i])[2])
                res.append(temp)
            else:
                res.append(np.nan)
    

    return pd.Series(res, dtype='float64')    

# Question 1.2

def convert_to_minofday(time):
    """
    Converts military time to minute of day
    
    Args:
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with minute of day
    
    Example: 1:03pm is converted to 783.0
    >>> convert_to_minofday(1303.0)
    783.0
    """
    res = []
    hours = extract_hour(time)
    minutes = extract_mins(time)
    
    for i in range(len(time)):
        res.append(hours[i]*60 + minutes[i])
    
    return pd.Series(res, dtype='float64')
    
    
def calc_time_diff(x, y):
    """
    Calculates delay times y - x
    
    Args:
        x (float64): array of scheduled time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
        y (float64): array of same dimensions giving actual time
    
    Returns:
        array (float64): array of input dimension with delay time
    """
    res = []
    scheduled = convert_to_minofday(x)
    actual = convert_to_minofday(y)
    
    for i in range(len(x)):
        res.append(actual[i] - scheduled[i])

    return pd.Series(res, dtype='float64')
    