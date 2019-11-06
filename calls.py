from api_calls import ApiCall
from data_parser import Parser
from bokeh.plotting import figure, output_file, show
import os


def main():

    sensor_settings = {
        "Sensor 1": "70B3D5C1F001408D",
        "Sensor 2": "70B3D5C1F0014054",
        "Sensor 3": "70B3D5C1F0014056"
    }

    test = ApiCall()

    test.set_server_address(server_address="http://10.110.127.117:8081")
    test.set_login_info(user="mythings@behrtech.com", password="mythings")
    test.set_sensor_list(sensor_settings)

    get1 = test.get_sensor_data(return_count=-1, offset=0, senor_name="Sensor 1")
    get2 = test.get_sensor_data(return_count=-1, offset=0, senor_name="Sensor 3")

    parse_sensor1 = Parser()
    parse_sensor3 = Parser()

    parse_sensor1.set_data_message(get1.text)
    parse_sensor3.set_data_message(get2.text)

    data_sensor1_pressures = parse_sensor1.get_message_pressure()
    data_sensor1_datatimes = parse_sensor1.get_message_datetime_as_datetime()
    data_sensor3_pressures = parse_sensor3.get_message_pressure()
    data_sensor3_datatimes = parse_sensor3.get_message_datetime_as_datetime()

    data_x_times = [data_sensor1_datatimes, data_sensor3_datatimes]
    data_y_pressure = [data_sensor1_pressures, data_sensor3_pressures]

    graph_with_bokeh(data_x_times, data_y_pressure, "index.html", "Time", "Pressure", "Pressure Over Time")


def get_full_pathname():

    filename = os.path.abspath(os.path.join('sensors' + '.json'))

    return filename


def graph_with_bokeh(data_x, data_y, file_name, x_axis, y_axis, title):

    output_file(file_name)

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

    show(f)


if __name__ == "__main__":
    main()
