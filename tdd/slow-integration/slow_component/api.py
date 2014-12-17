
import time

class SlowApi(object):
    def invoke_api(self):
        time.sleep(1000)
        return 3;
