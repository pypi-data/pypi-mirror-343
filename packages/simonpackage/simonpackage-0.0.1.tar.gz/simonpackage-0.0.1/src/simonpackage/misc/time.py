import time


def timeString2Seconds(time_string):
    """
     * Convert time string to seconds
     :param time_string: time string in format 'HH:MM:SS' or 'MM:SS'
     :return: time in seconds
     """
    time_list = time_string.split(':')
    if len(time_list) == 2:
        m, s = map(int, time_list)
        return m * 60 + s
    elif len(time_list) == 3:
        h, m, s = map(int, time_list)
        return h * 3600 + m * 60 + s
    else:
        return 0

def getJSTimeStamp(time_str=None):
    """
     *Get current time in milliseconds, 13 digits, usually used in JavaScript
    :param time_str: time string in format 'YYYY-MM-DD HH:MM:SS' , if none, the time is now
    :return: int time stamp
    """
    if time_str is None:
        return int(time.time() * 1000)
    else:
        tm_struct = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')     # tm_struct
        return int(time.mktime(tm_struct) * 1000)


def parseJSTimeStamp(time_stamp):
    """
     * Parse time stamp in milliseconds to string
     :param time_stamp: time stamp in milliseconds, int or str
     :return: time string in format 'YYYY-MM-DD HH:MM:SS'
     """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_stamp) / 1000))


if __name__ == '__main__':
    print(getJSTimeStamp())



   








