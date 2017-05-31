import datetime


def time_conversion(**kwargs):
    time = kwargs.get('time')

    try:
        given_time = datetime.datetime.strptime(time, "%H:%M %d-%m")
    except ValueError:
        try:
            given_time = datetime.datetime.strptime(time, "%I:%M%p %d-%m")
        except ValueError:
            return "Error"

    current_time = datetime.datetime.utcnow().strftime("%H:%M %d-%m")
    current_time_str = datetime.datetime.strptime(current_time, "%H:%M %d-%m")
    diff_time = current_time_str - given_time
    if '-1 day' in str(diff_time):
        diff_time = given_time - current_time_str
        flag = 0
    else:
        flag = 1
    diff_time_str = str(diff_time)[-8:][:-6]
    if flag == 0:
        time_difference = int(diff_time_str)
        if time_difference > 12:
            return "Error"
    elif flag == 1:
        time_difference = - int(diff_time_str)
        if time_difference < -12:
            return "Error"
    else:
        return "Error"

    return time_difference
