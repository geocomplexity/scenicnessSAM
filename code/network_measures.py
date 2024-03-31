import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Polygon
import matplotlib.image as mpimg
import os

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
	# print(nx.diameter(G))
	# print(nx.density(G))
	return G


def flip_nodes(graph):
	pos = nx.get_node_attributes(graph, 'pos')
	
	# Get the minimum y-coordinate to determine the offset
	min_y = min(y for _, y in pos.values())
	
	# Flip the y-coordinates
	flipped_pos = {node: (x, min_y - y) for node, (x, y) in pos.items()}

	return flipped_pos


def draw_rectangle_graph(graph, polygons):
	# flipped_pos = flip_nodes(graph)
	pos = nx.get_node_attributes(graph, 'pos')
	labels = nx.get_node_attributes(graph, 'coords')
	fig, ax = plt.subplots()

	nx.draw(graph, pos, with_labels=False, node_size=100, node_color="skyblue")
	# nx.draw_networkx_edges(graph, flipped_pos, ax=ax)
	# nx.draw(graph, flipped_pos, with_labels=False, node_size=100, node_color="skyblue")
	# nx.draw_networkx_nodes(graph, flipped_pos, node_size=100, node_color="skyblue")
	# nx.draw_networkx_nodes(graph, flipped_pos, with_labels=False, node_size=100, node_color="skyblue")



	for node, coord in labels.items():
		x, y, w, h = coord
		# plt.text(x + w / 2, y + h / 2, f"Node {node}\nCoords: {coord}", fontsize=8, ha='center')
		plt.text(x + w / 2, y + h / 2, f"Node {node}", fontsize=8, ha='center')

	for polygon in polygons:
		adjusted_polygon = [(x, y) for x, y in polygon]  # Adjust the polygon for plotting
		ax.add_patch(Polygon(adjusted_polygon, fill=False, edgecolor='green'))

	background_img = mpimg.imread('network/1887_old.jpg')
	# Create a figure and axis
	
	# Plot the background image
	# ax.imshow(background_img, extent=ax.get_xlim() + ax.get_ylim(), aspect='auto', zorder=-1, origin='lower')
	# ax.imshow(background_img, origin='lower', alpha=0.5)
	ax.imshow(background_img, alpha=0.5)

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
	# print(rectangles)
	G = generate_rectangle_graph(rectangles, centroid_coordinates)
	# print(rectangle_graph)
	# # print(nx.degree(rectangles))
	print(nx.diameter(G))
	print(nx.density(G))

	
def main():
	oFile = open("data_rmr/nw_index3.tsv", "w")
	print("program starts ...")
	files = os.listdir("network3")
	conn = 0
	for file in files:
		# print(file)
		idx = file.split("_")[0]
		# print(idx)
		data = []
		mFile = open("network3/" + file, "r")
		rectangles = []
		centroid_coordinates = []
		for ele in mFile:
			data = ele.rstrip().split('\t')
			coord = ast.literal_eval(data[0])
			pts = ast.literal_eval(data[1])
			rectangles.append(pts)
			centroid_coordinates.append(coord)
		G = generate_rectangle_graph(rectangles, centroid_coordinates)
		if (nx.is_connected(G)):
			conn = 1
		else:
			conn = 0
		density = nx.density(G)
		average_clustering  = nx.average_clustering(G)
		local_efficiency = nx.local_efficiency(G)
		global_efficiency = nx.global_efficiency(G)
		# print(nx.average_shortest_path_length(G))
		# scaled_shannon_index = scaled_shannon_diversity_index(data)
		# gini = gini_coefficient(data)
		# ht_index = htb(data)
		mString = idx + "\t" + str(density) + "\t" + str(average_clustering) + "\t" + str(local_efficiency) + "\t" + str(global_efficiency) + "\t" + str(conn) + "\n"
		oFile.write(mString)
	oFile.close()


if __name__ == '__main__':
	main()
