import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import filedialog

# TreeNode Class Definition
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

# Main Tree App with Tkinter
class TreeApp:
    def __init__(self, master):
        self.master = master
        master.title("Tree Data Structure Explorer")
        self.tree = None
        self.selected_node = None
        self.create_widgets()

    def create_widgets(self):
        # Menu for file operations
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load Tree from File", command=self.load_tree_from_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

        # Treeview for displaying the tree structure
        self.treeview = ttk.Treeview(self.master)
        self.treeview.pack(expand=True, fill='both')
        self.treeview.bind("<ButtonRelease-1>", self.select_node)

        # Node operations frame
        self.node_frame = ttk.Frame(self.master)
        self.node_frame.pack(pady=10)

        ttk.Label(self.node_frame, text="Node Data:").grid(row=0, column=0, sticky="w")
        self.node_data_entry = ttk.Entry(self.node_frame)
        self.node_data_entry.grid(row=0, column=1)

        ttk.Button(self.node_frame, text="Add Child", command=self.add_child).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(self.node_frame, text="Delete Node", command=self.delete_node).grid(row=2, column=0, columnspan=2, pady=5)

        # Button for visualization
        ttk.Button(self.node_frame, text="Visualize Tree", command=self.visualize_tree).grid(row=3, column=0, columnspan=2, pady=5)

    def load_tree_from_file(self):
        filename = filedialog.askopenfilename(title="Select Tree Data File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = eval(f.read()) # Read data from the file
                self.tree = self.build_tree(data) # Build tree
                self.populate_treeview(self.tree) # Display tree
            except Exception as e:
                print(f"Failed to load or parse tree data: {e}")

    def build_tree(self, data):
        if isinstance(data, dict):
            root = Node(list(data.keys())[0]) # Create root node
            for child_data in list(data.values())[0]: # Iterate through child data
                root.children.append(self.build_tree(child_data)) # Recursively build children
            return root
        else:
            return Node(data) # Create leaf node

    def populate_treeview(self, node, parent=""):
        if node:
            node_id = self.treeview.insert(parent, 'end', text=node.data)
            for child in node.children:
                self.populate_treeview(child, node_id)

    def select_node(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            self.selected_node = selected_item[0]
            self.node_data_entry.delete(0, tk.END)
            self.node_data_entry.insert(0, self.treeview.item(self.selected_node)['text'])

    def add_child(self):
        if self.selected_node:
            child_data = self.node_data_entry.get()
            if child_data:
                new_node = Node(child_data)
                parent_node_id = self.selected_node
                self.add_child_to_tree(parent_node_id, new_node)
                self.treeview.insert(parent_node_id, 'end', text=child_data)
            else:
                print("Please enter data for the new child node.")
        else:
            print("Please select a node to add a child to.")

    def add_child_to_tree(self, parent_node_id, new_node):
        def find_node(node, node_id):
            if self.treeview.item(node_id)['text'] == node.data:
                return node
            for child in node.children:
                found = find_node(child, node_id)
                if found:
                    return found
            return None

        parent_node = find_node(self.tree, parent_node_id)
        if parent_node:
            parent_node.children.append(new_node)

    def delete_node(self):
        if self.selected_node:
            parent_node = self.treeview.parent(self.selected_node)
            self.treeview.delete(self.selected_node)
            self.delete_node_from_tree(self.tree, self.treeview.item(self.selected_node)['text'])
            self.selected_node = None
            self.node_data_entry.delete(0, tk.END)
        else:
            print("Please select a node to delete.")

    def delete_node_from_tree(self, node, node_data):
        for child in node.children:
            if child.data == node_data:
                node.children.remove(child)
                return
            self.delete_node_from_tree(child, node_data)

    def visualize_tree(self):
        G = nx.DiGraph()
        self.build_graph(self.tree, G)

        # Draw the graph
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        plt.title("Tree Structure Visualization")
        plt.show()

    def build_graph(self, node, graph, parent=None):
        graph.add_node(node.data)
        if parent:
            graph.add_edge(parent, node.data)
        for child in node.children:
            self.build_graph(child, graph, node.data)

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()