import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Polygon
import matplotlib.image as mpimg


def convert_to_vertices(previous_format_rectangles):
    vertices_rectangles = []
    for x, y, w, h in previous_format_rectangles:
        # Calculate the coordinates of the four corners of the rectangle.
        top_left = (x, y)
        top_right = (x + w, y)
        bottom_right = (x + w, y + h)
        bottom_left = (x, y + h)
        vertices = [top_left, top_right, bottom_right, bottom_left]
        vertices_rectangles.append(vertices)
    return vertices_rectangles


# def rectangles_intersect(rect1, rect2):
#   x1, y1, w1, h1 = rect1
#   x2, y2, w2, h2 = rect2
#   return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

# # def generate_rectangle_graph(rectangles, centroid_coordinates):
# #     G = nx.Graph()

# #     for i, rect1 in enumerate(rectangles):
# #         G.add_node(i, pos=(rect1[0] + rect1[2] / 2, rect1[1] + rect1[3] / 2))

# #         for j, rect2 in enumerate(rectangles[i+1:], start=i+1):
# #             if rectangles_intersect(rect1, rect2):
# #                 G.add_edge(i, j)

# #     return G

# def generate_rectangle_graph(rectangles, centroid_coordinates):
#   G = nx.Graph()

#   for i, (x, y, w, h) in enumerate(rectangles):
#       G.add_node(i, pos=(x, y), coords=(x, y, w, h))

#       for j, (x2, y2, w2, h2) in enumerate(rectangles[i+1:], start=i+1):
#           if rectangles_intersect((x, y, w, h), (x2, y2, w2, h2)):
#               G.add_edge(i, j)

#   return G



# # def draw_rectangle_graph(graph):
# #     pos = nx.get_node_attributes(graph, 'pos')
# #     nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue", font_size=8)
# #     plt.show()


# def draw_rectangle_graph(graph, polygons):
#     pos = nx.get_node_attributes(graph, 'pos')
#     labels = nx.get_node_attributes(graph, 'coords')

#     nx.draw(graph, pos, with_labels=False, node_size=700, node_color="skyblue")

#     for node, coord in labels.items():
#         x, y, w, h = coord
#         plt.text(x + w / 2, y + h / 2, f"Node {node}\nCoords: {coord}", fontsize=8, ha='center')

#     for polygon in polygons:
#         plt.gca().add_patch(Polygon(polygon, fill=False, edgecolor='red'))

#     plt.show()

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def rectangles_intersect(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def generate_rectangle_graph(rectangles, centroid_coordinates):
    G = nx.Graph()

    for i, (x, y, w, h) in enumerate(rectangles):
        G.add_node(i, pos=(x, y), coords=(x, y, w, h))

        for j, (x2, y2, w2, h2) in enumerate(rectangles[i+1:], start=i+1):
            if rectangles_intersect((x, y, w, h), (x2, y2, w2, h2)):
                G.add_edge(i, j)
    # print(nx.degree(G))
    # print(nx.average_degree_connectivity(G))
    print(nx.diameter(G))
    print(nx.density(G))
    return G

def draw_rectangle_graph(graph, polygons):
    pos = nx.get_node_attributes(graph, 'pos')
    labels = nx.get_node_attributes(graph, 'coords')
    fig, ax = plt.subplots()

    nx.draw(graph, pos, with_labels=False, node_size=100, node_color="skyblue")

    for node, coord in labels.items():
        x, y, w, h = coord
        # plt.text(x + w / 2, y + h / 2, f"Node {node}\nCoords: {coord}", fontsize=8, ha='center')
        plt.text(x + w / 2, y + h / 2, f"Node {node}", fontsize=8, ha='center')

    for polygon in polygons:
        adjusted_polygon = [(x, y) for x, y in polygon]  # Adjust the polygon for plotting
        plt.gca().add_patch(Polygon(adjusted_polygon, fill=False, edgecolor='green'))

    background_img = mpimg.imread('network/1887.jpg')
    # Create a figure and axis
    
    # Plot the background image
    ax.imshow(background_img, alpha=0.1)

    # Load the overlay image
    # overlay_img = mpimg.imread('path/to/overlay_image.png')

    # # Overlay the second image on top of the first
    # ax.imshow(overlay_img, alpha=0.5)  # Adjust alpha to control transparency

    # Show the plot
    plt.show()








def plot():
    print("starts...")
    mFile = open("network/1887_graph.csv", "r")
    rectangles = []
    centroid_coordinates = []

    for ele in mFile:
        data = ele.rstrip().split('\t')
        coord = ast.literal_eval(data[0])
        # print(coord)
        pts = ast.literal_eval(data[1])
        rectangles.append(pts)
        centroid_coordinates.append(coord)
    print(rectangles)
    rectangle_graph = generate_rectangle_graph(rectangles, centroid_coordinates)
    print(rectangle_graph)
    # print(nx.degree(rectangles))
    polygons = convert_to_vertices(rectangles)


    draw_rectangle_graph(rectangle_graph, polygons)

    


def main():
    plot()


if __name__ == '__main__':
    main()
