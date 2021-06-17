from datetime import datetime


print(datetime.now().strftime('%Y%m%d_%H%M%S'))


print(type(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))