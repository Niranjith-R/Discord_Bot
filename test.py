from time import localtime

a= localtime()

time = str(a.tm_hour) + ':' + str(a.tm_min) + ":" + str(a.tm_sec)
date = str(a.tm_mday) + "/" + str(a.tm_mon) + "/" + str(a.tm_year)

print(date, time)