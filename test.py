from datetime import datetime
from time import sleep


from datetime import datetime

date1 = datetime(2020, 5, 17, 17, 10)
date2 = datetime(2020, 5, 17, 18, 10)
diff = date1 - date2
print(diff.total_seconds())
