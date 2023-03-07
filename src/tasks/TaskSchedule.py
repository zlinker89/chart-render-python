import schedule
import time
import logging
import os
import shutil
import threading
# the __name__ resolve to "uicheckapp.services"
logger = logging.getLogger(__name__)
# This will load the uicheckapp logger
class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        schedule.every().day.at("21:00:00").do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        logger.info("start job garbage")
        folder = os.getcwd() + '/public/images'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


