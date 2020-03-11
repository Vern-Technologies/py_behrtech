from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool


def line_graph(data_x, data_y, x_axis, y_axis, title, line_data):
    """
    Generates a bokeh line graph. Makes generating line graphs for the gateway software more simple

    :param data_x: The data for the X coordinate, can be a list of X coordinates for each line in the graph
    :param data_y: The data for the Y coordinate, can be a list of Y coordinates for each line in the graph
    :param x_axis: The label name for the X axis of the graph
    :param y_axis: The label name for the Y axis of the graph
    :param title: The title of the graph
    :param line_data: Config setup for each line in the line graph, is a list of dictionaries
            Example config: line_data[{color: 'navy', legend_label: 'Sensor1'},
                                      {color: 'turquoise', legend_label: 'Sensor3'}]
    :return: The bokeh generated line graph
    """

    f_plot = figure(
        title=title,
        x_axis_label=x_axis,
        y_axis_label=y_axis,
        x_axis_type='datetime',
        sizing_mode="stretch_both",
        tools="pan, wheel_zoom, box_zoom, save, reset"
    )

    for index in range(len(data_x)):

        source = ColumnDataSource(data={
            'Date': data_x[index],
            'Data': data_y[index],
        })

        f_plot.line('Date', 'Data', color=line_data[index]['color'],
                    line_width=2, legend_label=line_data[index]['legend_label'], source=source)

    f_plot.legend.location = "top_left"
    f_plot.legend.title = "Sensors"
    f_plot.legend.title_text_font_style = "bold"
    f_plot.legend.title_text_font_size = "15pt"
    f_plot.add_tools(HoverTool(
        tooltips=[
            ("Index", "$index"),
            (y_axis, "$y"),
            ('Date', '@Date{%Y-%m-%d %H:%M:%S}')
        ],

        formatters={
            'Date': 'datetime',  # Use 'datetime' formatter for 'date' field
        },

        # Display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    return f_plot
