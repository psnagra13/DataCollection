from datetime import datetime

my_date_string = "2001/9/1 00:00:03"
d = datetime.strptime(my_date_string, "%Y/%m/%d %H:%M:%S")
print d.strftime("%d%m%Y %H%M%S")
print d.strftime("%d%m%Y")