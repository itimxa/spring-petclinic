import urllib
import json
import time


url = 'http://127.0.0.1:8080/manage/health'

for i in range(6):
    time.sleep(10)
    try:
        request = urllib.urlopen(url)
        data = json.loads(request.read())
        break

    except IOError:
        continue
    
if data['status'] == 'UP':
    print "Service is up"
