# archerqueen/main.py
def main():
    print("🏹 Archer Queen is ready! 🏹")
#EXPERIMENT 5

    import pandas as pd
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from textblob import TextBlob
    import seaborn as sns
    import nltk

    # Download necessary NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Step 1: Text Preprocessing (Tokenization, Stopword Removal, Lemmatization)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def preprocess_text(text):
        # Tokenize
        tokens = word_tokenize(text.lower())
        # Remove stopwords and non-alphabetic words
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
        return ' '.join(tokens)

    d['Processed Document'] = d['product'].apply(preprocess_text)

    # Step 2: Word Frequency Analysis using CountVectorizer
    vectorizer = CountVectorizer(max_features=10)
    X = vectorizer.fit_transform(d['Processed Document'])
    word_freq = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    word_freq = word_freq.sum(axis=0).sort_values(ascending=False)

    # Step 3: Sentiment Analysis using TextBlob
    def get_sentiment(text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    d['Sentiment'] = d['product'].apply(get_sentiment)

    # Step 4: Topic Modeling using LDA (Latent Dirichlet Allocation)
    lda = LatentDirichletAllocation(n_components=2, random_state=42)
    lda.fit(X)


    # 1. Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(d['Processed Document']))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Processed Documents')
    plt.tight_layout()
    plt.show()

    # 2. Bar Chart for Word Frequencies
    plt.figure(figsize=(8, 6))
    word_freq.head(10).plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Top 10 Word Frequencies')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()


    # 3. Sentiment Analysis Pie Chart
    sentiment_counts = d['Sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')).value_counts()
    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Sentiment Analysis')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()



    # 4. Topic Modeling Bar Chart (Topic Distribution)
    topic_distribution = lda.transform(X)
    topic_keywords = [', '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-6:-1]]) for topic in lda.components_]
    topic_df = pd.DataFrame(topic_distribution, columns=['Topic 1', 'Topic 2'])

    plt.figure(figsize=(8, 6))
    sns.barplot(x=topic_df.columns, y=topic_df.mean().values, palette='viridis')
    plt.title('Topic Modeling - Topic Distribution')
    plt.ylabel('Average Proportion')
    plt.tight_layout()
    plt.show()



    """


    #EXPERIMENT 6
    """

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

        
    """

    #EXPERIMENT 7
    """

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

    """


    #EXPERIMENT 8
    """

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.datasets import make_blobs
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score

    # Generate a synthetic dataset
    X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)
    X = StandardScaler().fit_transform(X)

    # Visualize the original dataset
    plt.scatter(X[:, 0], X[:, 1], s=50, c='gray', label='Data Points')
    plt.title('Original Dataset')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans_labels = kmeans.fit_predict(X)

    # Visualize K-Means clustering
    plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis', s=50)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', label='Centroids')
    plt.title('K-Means Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()

    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(X)

    # Visualize DBSCAN clustering
    plt.scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='plasma', s=50)
    plt.title('DBSCAN Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

    # Silhouette Scores
    kmeans_silhouette = silhouette_score(X, kmeans_labels)
    dbscan_silhouette = silhouette_score(X, dbscan_labels if len(set(dbscan_labels)) > 1 else np.zeros_like(dbscan_labels))

    print(f"Silhouette Score for K-Means: {kmeans_silhouette:.2f}")
    print(f"Silhouette Score for DBSCAN: {dbscan_silhouette:.2f} (if applicable)")

if __name__ == "__main__":
    main()   




    