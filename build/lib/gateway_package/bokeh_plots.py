from bokeh.plotting import figure


def bokeh_line_graph(data_x, data_y, x_axis, y_axis, title):

    f = figure(
        width=1300,
        title=title,
        x_axis_label=x_axis,
        y_axis_label=y_axis,
        x_axis_type='datetime'
    )

    f.line(data_x[0], data_y[0], color='navy', line_width=2, legend_label='Sensor1')
    f.line(data_x[1], data_y[1], color='turquoise', line_width=2, legend_label='Sensor3')

    f.legend.location = "top_left"
    f.legend.title = "Sensors"
    f.legend.title_text_font_style = "bold"
    f.legend.title_text_font_size = "15pt"

    return f
