import plotly.graph_objects as go
import numpy as np
from src.utils.constanst import RANGES
import uuid
class GaugeChartController:
    def get_data_from_range(self, rsi: float):
        """
            Get label and color by rsi
        """
        for range in RANGES:
            if range['min'] <= rsi <= range['max']:
                return {"label": range['label'], "color": range['color']}

    def generate_gauge(self, rsi: float):
        """
            Generate gauge chart ploty PIE
        """
        path_file = "public/images/%s.png" % str(uuid.uuid4())
        datos = self.get_data_from_range(rsi)
        plot_bgcolor = "#fff"
        quadrant_colors = [plot_bgcolor, "#f25829", "#eff229", "#85e043", "#eff229", "#f25829"] 
        quadrant_text = ["", "<b>Altamente Corrosiva</b>", "<b>Ligeramente Corrosiva</b>", "<b>Equilibrio</b>", "<b>Ligeramente Incrustante</b>", "<b>Altamente Incrustante</b>"]
        # n_quadrants = len(quadrant_colors) - 1
        current_value = rsi
        min_value = 0
        max_value = 10
        hand_length = np.sqrt(2) / 3.5
        hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))
        # quadrants = [0.5, 0.25, 0.07,0.7,0.011]
        # print([0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist())
        quadrants = [0.5, 0.125, 0.025,0.050,0.050,0.255]
        # print(self.get_range(quadrants))
        fig = go.Figure(
            data=[
                go.Pie(
                    values=quadrants,                    
                    # values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                    rotation=90,
                    hole=0.7,
                    marker_colors=quadrant_colors,
                    text=quadrant_text,
                    textinfo="text",
                    hoverinfo="skip",
                    textfont={"color": "#000", "size": 12},
                    sort=False
                ),
            ],
            layout=go.Layout(
                showlegend=False,
                margin=dict(b=0,t=10,l=10,r=10),
                width=750,
                height=750,
                paper_bgcolor=plot_bgcolor,
                annotations=[
                    go.layout.Annotation(
                        font={"color": datos['color'], 'size': 20},
                        text=f"<b>%s:</b><br>{current_value}" % datos['label'],
                        x=0.5, xanchor="center", xref="paper",
                        y=0.5, yanchor="bottom", yref="paper",
                        showarrow=False,
                    )
                ],
                shapes=[
                    go.layout.Shape(
                        type="circle",
                        x0=0.48, x1=0.52,
                        y0=0.58, y1=0.62,
                        fillcolor="#333",
                        line_color="#333",
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.6, y1=0.5 + hand_length * np.sin(hand_angle),
                        line=dict(color="#333", width=4)
                    )
                ]
            )
        )
        fig.write_image(path_file)
        return path_file