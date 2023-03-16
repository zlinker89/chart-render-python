import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from src.utils.constanst import RANGES
import uuid
from skimage import io
import os


class GaugeChartController:
    color_text = 'rgb(30, 55, 99)'

    def get_data_from_range(self, rsi: float):
        """
            Get label and color by rsi
        """
        for range in RANGES:
            if range['min'] <= rsi <= range['max']:
                return {"label": range['label'], "color": range['color'], "dark_color": range['dark_color']}

    def get_ranges(self):
        range_list = []
        for range in RANGES:
            range_list.append({
                "range": [range['min'], range['max']],
                "color": range['color']
            })
        return range_list

    def generate_gauge_pie(self, rsi: float):
        """
            Generate gauge chart ploty PIE
        """
        path_file = "public/images/%s.png" % str(uuid.uuid4())
        datos = self.get_data_from_range(rsi)
        plot_bgcolor = "#fff"
        quadrant_colors = [plot_bgcolor, "#f25829",
                           "#eff229", "#85e043", "#eff229", "#f25829"]
        quadrant_text = ["", "<b>Altamente Corrosiva</b>", "<b>Ligeramente Corrosiva</b>",
                         "<b>Equilibrio</b>", "<b>Ligeramente Incrustante</b>", "<b>Altamente Incrustante</b>"]
        current_value = rsi
        min_value = 0
        max_value = 10
        hand_length = np.sqrt(2) / 3.5
        hand_angle = np.pi * \
            (1 - (max(min_value, min(max_value, current_value)) -
             min_value) / (max_value - min_value))
        quadrants = [0.5, 0.125, 0.025, 0.050, 0.050, 0.255]
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
                margin=dict(b=0, t=10, l=10, r=10),
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
                        fillcolor=self.color_text,
                        line_color=self.color_text,
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.6, y1=0.5 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    )
                ]
            )
        )
        fig.write_image(path_file)
        return path_file

    def generate_gauge_step(self, rsi: float):
        """
            Generate gauge chart ploty Gauge
        """
        path_file = os.getcwd() + "/public/images/%s.png" % str(uuid.uuid4())
        datos = self.get_data_from_range(rsi)
        min_value, max_value = 4, 8.5
        if not (min_value <= rsi <= max_value):
            img = io.imread(os.getcwd() + '/public/error.jpg')
            fig = px.imshow(img)
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                text="<a href='http://www.freepik.com'>Designed by stories / Freepik</a>",
                xref="paper",
                yref="paper",
                showarrow=False,
                font_size=20)
            fig.write_image(path_file)
            return path_file
        hand_length = np.sqrt(2) / 3
        hand_angle = np.pi * \
            (1 - (max(min_value, min(max_value, rsi)) -
             min_value) / (max_value - min_value))
        fig = go.Figure(
            data=[go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=rsi,
                mode="gauge",
                gauge={'axis': {
                    'range': [min_value, max_value],
                    'ticktext': list(map(lambda x: x['label'], RANGES)),
                    'showticklabels': True
                },
                    'bar': {'color': datos['dark_color']},
                    'steps': self.get_ranges()
                })
            ],
            layout=go.Layout(
                showlegend=False,
                margin=dict(b=0, t=10, l=80, r=80),
                width=900,
                height=750,
                paper_bgcolor='#FFF',
                annotations=[
                    go.layout.Annotation(
                        # bgcolor='rgba(0,0,0,0.8)',
                        font={"color": datos['color'], 'size': 30},
                        text=f"<b>%s:</b><br>{rsi}" % datos['label'],
                        x=0.5, xanchor="center", xref="paper",
                        y=0.10, yanchor="bottom", yref="paper",
                        showarrow=False,
                    )
                ],
                shapes=[
                    go.layout.Shape(
                        type="circle",
                        x0=0.46, x1=0.54,
                        y0=0.21, y1=0.29,
                        fillcolor=self.color_text,
                        line_color=self.color_text,
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 + 0.02, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 + 0.01, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 + 0.015, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 + 0.005, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 - 0.02, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 - 0.015, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 - 0.010, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5 - 0.005, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.25, y1=0.25 + hand_length * np.sin(hand_angle),
                        line=dict(color=self.color_text, width=4)
                    ),
                    go.layout.Shape(
                        type="circle",
                        x0=0.48, x1=0.52,
                        y0=0.23, y1=0.27,
                        fillcolor="#FFF",
                        line_color="#FFF",
                    )
                ]
            ))
        fig.update_layout(font={'color': self.color_text, 'family': "Arial"})
        fig.add_annotation(
            x=-0.085, y=0.46, text='Altamente <br>Incrustante', showarrow=False)
        fig.add_annotation(
            x=0.1, y=0.75, text='Ligeramente <br>Incrustante', showarrow=False)
        fig.add_annotation(x=0.60, y=0.80, text='Equilibrio', showarrow=False)
        fig.add_annotation(
            x=0.95, y=0.70, text='Ligeramente <br>Corrosiva', showarrow=False)
        fig.add_annotation(
            x=1.1, y=0.43, text='Altamente <br>Corrosiva', showarrow=False)
        fig.write_image(path_file)
        return path_file
