from src.controllers.GaugeChartController import GaugeChartController
from typing import Union
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
# task for delete all images
from src.tasks.TaskSchedule import BackgroundTasks
# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.
logger.info("Server start")


app = FastAPI()
task = BackgroundTasks()
task.start()


@app.get("/gauge/{rsi}")
def gauge_chart(rsi: float):
    """
        Generate chart with ryznar stability index
    """
    gauge = GaugeChartController()
    img = gauge.generate_gauge(rsi)
    return FileResponse(img, media_type="image/png")
