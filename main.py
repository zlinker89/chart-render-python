from src.controllers.GaugeChartController import GaugeChartController
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/gauge/{rsi}")
def gauge_chart(rsi: float):
    """
        Generate chart with ryznar stability index
    """
    gauge = GaugeChartController()
    img = gauge.generateGauge(rsi)
    return FileResponse(img, media_type="image/png")
