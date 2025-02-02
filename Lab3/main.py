import random
import networkx as nx
import matplotlib.pyplot as plt

def create_lunar_map(num_districts):
    """Creates a randomly generated map of Luna-City districts."""
    adj_list = {i: set() for i in range(num_districts)}

    for i in range(num_districts - 1):
        adj_list[i].add(i + 1)
        adj_list[i + 1].add(i)

    for _ in range(num_districts * 2):
        d1 = random.randint(0, num_districts - 1)
        d2 = random.randint(0, num_districts - 1)
        if d1 != d2:
            adj_list[d1].add(d2)
            adj_list[d2].add(d1)
    return adj_list


def color_map(adj_list):
    
    num_districts = len(adj_list)
    colors = {}
    available_colors = set(range(1, num_districts + 1))

    for district in range(num_districts):
        used_colors = set()
        for neighbor in adj_list[district]:
            if neighbor in colors:
                used_colors.add(colors[neighbor])

        for color in available_colors:
            if color not in used_colors:
                colors[district] = color
                break
        else:
            return None

    return colors


def display_map(adj_list, colors):
    if colors is None:
        print("Map is not colorable with this algorithm.")
        return

    print("District Colors:")
    for district, color in colors.items():
        print(f"District {district + 1}: Color {color}")

    
    graph = nx.Graph(adj_list)  

    # Node colors based on the coloring
    node_colors = [colors[node] for node in graph.nodes()]

    
    pos = nx.spring_layout(graph, seed=42)  

    nx.draw(graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.get_cmap('viridis'), node_size=600, font_size=10, font_color="white")  # Draw the graph
    plt.title("Lunar-City Map")
    plt.show()



# Example usage:
num_districts = 10
lunar_map = create_lunar_map(num_districts)
colored_map = color_map(lunar_map)
display_map(lunar_map, colored_map)