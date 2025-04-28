import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Create Graph Data
def create_graph():
    G = nx.Graph()  # You can use nx.DiGraph() for a directed graph
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
    return G

# Step 2: Visualize Graph using NetworkX and Matplotlib
def visualize_graph(G):
    try:
        # Ensure the graph has nodes and edges
        print(f"Nodes: {G.nodes()}")
        print(f"Edges: {G.edges()}")

        # Create the plot using NetworkX and Matplotlib
        pos = nx.spring_layout(G)  # Compute positions using spring layout (force-directed)
        plt.figure(figsize=(8, 8))

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=16, font_weight='bold', edge_color='gray')

        # Display the graph interactively
        plt.title("Interactive Graph Visualization")
        plt.show()

    except Exception as e:
        print(f"An error occurred while visualizing the graph: {e}")

# Step 3: Add a Node to the Graph
def add_node(G):
    new_node = simpledialog.askstring("Input", "Enter the new node value:", parent=root)
    if new_node:
        G.add_node(new_node)
        print(f"Added node {new_node}")
        visualize_graph(G)

# Step 4: Add an Edge to the Graph
def add_edge(G):
    node1 = simpledialog.askstring("Input", "Enter the first node:", parent=root)
    node2 = simpledialog.askstring("Input", "Enter the second node:", parent=root)
    if node1 and node2:
        G.add_edge(node1, node2)
        print(f"Added edge between {node1} and {node2}")
        visualize_graph(G)

# Step 5: GUI for User Interaction
def create_gui():
    global root
    root = tk.Tk()
    root.title("Interactive Graph Visualization")

    # Create Graph Data
    G = create_graph()

    # Button to visualize the graph
    visualize_button = tk.Button(root, text="Visualize Graph", command=lambda: visualize_graph(G))
    visualize_button.pack()

    # Button to add a node to the graph
    add_node_button = tk.Button(root, text="Add Node", command=lambda: add_node(G))
    add_node_button.pack()

    # Button to add an edge to the graph
    add_edge_button = tk.Button(root, text="Add Edge", command=lambda: add_edge(G))
    add_edge_button.pack()

    # Start the GUI loop
    root.mainloop()

# Step 6: Main Program
if __name__ == "__main__":
    create_gui()