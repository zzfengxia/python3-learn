import datetime
import pytz


def parse_date_str(timestamp_ms):
    tz = pytz.timezone('Asia/Shanghai')
    dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000, tz)
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')

    print(formatted_time)


if __name__ == '__main__':
    parse_date_str(1746672606000)
