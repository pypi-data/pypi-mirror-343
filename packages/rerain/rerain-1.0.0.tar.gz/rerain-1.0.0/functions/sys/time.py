import time

def format_time(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    seconds = seconds % 60
    minutes = minutes % 60
    hours = hours % 24
    return f"Day {days} - {hours:02}:{minutes:02}:{seconds:02}"

def wait(ms):
    start_time = time.time()
    end_time = start_time + ms / 1000
    while time.time() < end_time:
        pass
    return format_time(time.time() - start_time)

def wait_seconds(seconds):
    start_time = time.time()
    end_time = start_time + seconds
    while time.time() < end_time:
        pass
    return format_time(time.time() - start_time)

def wait_minutes(minutes):
    start_time = time.time()
    end_time = start_time + minutes * 60
    while time.time() < end_time:
        pass
    return format_time(time.time() - start_time)

def wait_hours(hours):
    start_time = time.time()
    end_time = start_time + hours * 3600
    while time.time() < end_time:
        pass
    return format_time(time.time() - start_time)

def ct(*args):
    current_time = time.localtime()
    result = []
    if 'time' in args:
        result.append(time.strftime("%H:%M:%S", current_time))
    if 'date' in args:
        result.append(time.strftime("%Y-%m-%d", current_time))
    if 'year' in args:
        result.append(time.strftime("%Y", current_time))
    if not result:
        result.append(time.strftime("%Y-%m-%d %H:%M:%S", current_time))
    return ", ".join(result)

def time_elapsed(start_time):
    return format_time(time.time() - start_time)
