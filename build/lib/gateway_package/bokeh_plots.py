from bokeh.plotting import figure


def bokeh_line_graph(data_x, data_y, x_axis, y_axis, title, line_data):
    """
    Generates a bokeh line graph. Makes generating line graphs for the gateway software more simple

    :param data_x: The data for the X coordinate, can be a list of X coordinates for each line in the graph
    :param data_y: The data for the Y coordinate, can be a list of Y coordinates for each line in the graph
    :param x_axis: The label name for the X axis of the graph
    :param y_axis: The label name for the Y axis of the graph
    :param title: The title of the graph
    :param line_data: Config setup for each line in the line graph, is a list of dictionaries
            Example config: line_data[{color: 'navy', line_width: 2, legend_label: 'Sensor1'},
                                      {color: 'turquoise', line_width: 2, legend_label: 'Sensor3'}]
    :return: The bokeh generated line graph
    """

    tool_tips = [
        ("Index", "$index"),
        (f"{y_axis}, {x_axis}", "($y, $x)"),
        ("Type", f"{title}"),
    ]

    f_plot = figure(
        title=title,
        x_axis_label=x_axis,
        y_axis_label=y_axis,
        x_axis_type='datetime',
        sizing_mode="stretch_both",
        tools="pan, wheel_zoom, box_zoom, save, reset",
        tooltips=tool_tips
    )

    for index in range(len(data_x)):
        f_plot.line(data_x[index], data_y[index], color=line_data[index]['color'],
                    line_width=line_data[index]['line_width'], legend_label=line_data[index]['legend_label'])

    f_plot.legend.location = "top_left"
    f_plot.legend.title = "Sensors"
    f_plot.legend.title_text_font_style = "bold"
    f_plot.legend.title_text_font_size = "15pt"

    return f_plot
