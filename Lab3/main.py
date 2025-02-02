import networkx as nx
import matplotlib.pyplot as plt

def generate_random_map(num_districts, connection_probability=0.3):
    """Generates a random map (graph) with districts as nodes and random connections as edges."""
    G = nx.erdos_renyi_graph(num_districts, connection_probability)
    while not nx.is_connected(G):  # Ensure the graph is connected
        G = nx.erdos_renyi_graph(num_districts, connection_probability)
    return G

def color_map(G):
    """Solves the map coloring problem using a greedy coloring approach."""
    color_assignment = {}
    for node in sorted(G.nodes(), key=lambda x: len(list(G.neighbors(x))), reverse=True):
        neighbor_colors = {color_assignment.get(neigh) for neigh in G.neighbors(node)}
        for color in range(len(G.nodes())):
            if color not in neighbor_colors:
                color_assignment[node] = color
                break
    return color_assignment

def visualize_map(G, color_assignment):
    """Displays the map with assigned colors."""
    pos = nx.spring_layout(G)  # Layout for visualization
    colors = [color_assignment[node] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, cmap=plt.cm.tab10, edge_color='gray', node_size=700)
    plt.show()

# Main Execution
districts = 10  # Number of districts
random_map = generate_random_map(districts)
solution = color_map(random_map)
visualize_map(random_map, solution)
