from energyMinimization import *
from skimage.measure import *


# build the node class
class node:
    movable = True

    def __init__(self, name, loc):
        self.name = name
        self.loc = loc


input_node_data_file = "Datasets/Applications/mosaic/Fast Flow/Image_6/final_nodes_image6_64_64.csv"
input_weight_data_file = "Datasets/Applications/mosaic/Fast Flow/Image_6/Girls_randomweight_64_64.txt"

output_filename = 'output_mosaic_fastflow_Girls_64_64'
square_grid = 64
output_image_size = [1024, 1024]

is_image_output = True
input_img_file = "Datasets/Applications/mosaic/Fast Flow/Image_6/girls.png"



grid_horiz = square_grid
grid_vert = square_grid

if __name__ == "__main__":
    print("Started - Reading data from")
    nodes = []

    sample_val = []
    input_file = open(input_node_data_file, "r")
    in_total_str = ''
    in_str = input_file.readlines()
    for i in range(len(in_str)):
        in_total_str += in_str[i].replace('\n', '').replace(' ', '')

    val_str = in_total_str.split(",")
    input_file.close()

    for i in range(grid_horiz + 1):
        x = []
        for j in range(grid_vert + 1):
            x.append(node(str(i) + "_" + str(j), Point(i, j)))
        nodes.append(x)

    counter = 0
    for j in range(grid_vert, -1, -1):
        for i in range(grid_horiz + 1):
            nodes[i][j].loc = Point(float(val_str[counter].split('__')[0]), float(val_str[counter].split('__')[1]))
            counter += 1

    poly_draw_for_maxflow("output/" + output_filename + "_polygon.png", output_image_size, nodes, grid_horiz, grid_vert)
    print("Ended with polygon drawing")

    values_actual = read_text_file(input_weight_data_file, grid_horiz, grid_vert)
    values = np.zeros((grid_horiz, grid_vert))

    for x in range(grid_horiz):
        for y in range(grid_vert):
            values[x][y] = values_actual[x, y]

    values = values / np.sum(values)

    # all values sum to totalarea
    values = values * grid_horiz * grid_vert

    out_file_name = "output/out_log_" + output_filename + ".txt"
    output_txt_file = open(out_file_name, "w")
    output_txt_file.write("Nothing, |UV-EV|/EV, UV/EV - 1, RMSE, MQE = (((|UV-EV|/EV) ** 2) ** 0.5)/N,"
                          " Updated MQE = (((|UV-EV|/(UV+EV)) ** 2) ** 0.5)/N, Average Aspect Ratio (height/width),"
                          "Average Aspect Ratio min(height/width)/max(height/width), Nothing\n")
    output_txt_file.close()
    all_error_calc(values, nodes, grid_horiz, grid_vert, 0, output_filename, 1)


    input_image = Image.open(input_img_file)
    input_image = input_image.convert("RGBA")
    output_image_size = input_image.size


    output_image_path = newImageDraw(input_image, nodes, output_filename,
                                     grid_horiz, grid_vert, True)

    print("Finished")
