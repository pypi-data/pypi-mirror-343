class Graph:
    """
    Graph class represents an undirected graph using an adjacency list.
    Attributes:
        vertex_count (int): The number of vertices in the graph.
        edge_count (int): The number of edges in the graph.
        adjacency_list (dict): A dictionary where keys are vertex indices and values are lists of adjacent vertices.
    Methods:
        __init__(v):
            Initializes a graph with a specified number of vertices and no edges.
        add_edge(u, v):
            Adds an undirected edge between vertices `u` and `v`.
            Raises:
                ValueError: If either `u` or `v` is out of bounds.
        E:
            Returns the number of edges in the graph.
        V:
            Returns the number of vertices in the graph.
        adjacent(u):
            Returns a list of vertices adjacent to vertex `u`.
            If `u` has no adjacent vertices, returns an empty list.
        __str__():
            Returns a string representation of the graph, including the number of vertices and edges.
        from_input_string(input_string):
            Creates a Graph instance from an input string.
            The input string should contain the number of vertices on the first line,
            followed by lines of edges in the format "u v", where `u` and `v` are vertex indices.
    """
    def __init__(self, v: int):
        self.vertex_count = v
        self.edge_count = 0
        self.adjacency_list = {}

    def add_edge(self, u: int, v: int):
        """
        Adds an edge between two vertices in the graph.
        This method updates the adjacency list to include the edge between
        the vertices `u` and `v`. If the vertices do not exist in the adjacency
        list, they are added. The graph is treated as undirected, so the edge
        is added in both directions. The edge count is incremented accordingly.
        Args:
            u (int): The first vertex of the edge.
            v (int): The second vertex of the edge.
        Raises:
            ValueError: If either `u` or `v` is out of bounds of the graph's
                        vertex count.
        """
        if v >= self.vertex_count or u >= self.vertex_count:
            raise ValueError("Vertex out of bounds.")
        
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)  # For undirected graph

        self.edge_count += 1

    @property
    def E(self):
        """
        int: The number of edges in the graph.
        """
        return self.edge_count
    
    @property
    def V(self):
        return self.vertex_count

    def adjacent(self, u):
        """
        Retrieve the list of nodes adjacent to a given node.

        Args:
            u: The node for which to find adjacent nodes.

        Returns:
            A list of nodes that are adjacent to the given node `u`.
            If the node `u` is not present in the adjacency list, an empty list is returned.
        """
        return list(self.adjacency_list.get(u, []))
    
    def __str__(self):
        """
        Returns a string representation of the graph.
        The string contains the number of vertices and edges, followed by
        the adjacency list for each vertex.

        Returns:
            str: A string representation of the graph.
        """
        result = f"Graph with {self.vertex_count} vertices and {self.edge_count} edges:\n"
        for vertex, edges in self.adjacency_list.items():
            result += f"{vertex}: {edges}\n"
        return result.strip()
    
    def from_input_string(input_string: str) -> 'Graph':
        """
        Creates a Graph instance from an input string.

        Args:
            input_string (str): The input string containing the number of vertices
                                and the edges.

        Returns:
            Graph: A Graph instance created from the input string.
        """
        lines = input_string.strip().split('\n')
        v = int(lines[0])
        graph = Graph(v)
        for line in lines[1:]:
            u, v = map(int, line.split())
            graph.add_edge(u, v)
        return graph
    
class Digraph:
    """
    A class representing a directed graph (Digraph).
    This class provides a representation of a directed graph using an adjacency list.
    It supports operations such as adding edges, retrieving adjacent vertices, and
    reversing the graph. The graph is initialized with a fixed number of vertices,
    and edges can be added between these vertices.
    Attributes:
        vertex_count (int): The number of vertices in the graph.
        edge_count (int): The number of edges in the graph.
        adjacency_list (dict): A dictionary where keys are vertices and values are
            lists of vertices that are adjacent to the key vertex.
    Methods:
        add_edge(u, v):
            Adds a directed edge from vertex `u` to vertex `v`.
        E:
            Returns the number of edges in the graph.
        V:
            Returns the number of vertices in the graph.
        adjacent(u):
            Retrieves the list of vertices adjacent to vertex `u`.
        reverse():
            Returns a new Digraph that is the reverse of the current graph.
    """
    
    def __init__(self, v: int):
        self.vertex_count = v
        self.edge_count = 0
        self.adjacency_list = {}

    def add_edge(self, u: int, v: int):
        """
        Adds an edge between two vertices in the graph.
        This method updates the adjacency list to include the edge between
        the vertices `u` and `v`. If the vertices do not exist in the adjacency
        list, they are added. The graph is treated as undirected, so the edge
        is added in both directions. The edge count is incremented accordingly.
        Args:
            u (int): The first vertex of the edge.
            v (int): The second vertex of the edge.
        Raises:
            ValueError: If either `u` or `v` is out of bounds of the graph's
                        vertex count.
        """
        if v >= self.vertex_count or u >= self.vertex_count:
            raise ValueError("Vertex out of bounds.")
        
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append(v)

        self.edge_count += 1

    @property
    def E(self):
        """
        int: The number of edges in the graph.
        """
        return self.edge_count
    
    @property
    def V(self):
        return self.vertex_count

    def adjacent(self, u):
        """
        Retrieve the list of nodes adjacent to a given node.

        Args:
            u: The node for which to find adjacent nodes.

        Returns:
            A list of nodes that are adjacent to the given node `u`.
            If the node `u` is not present in the adjacency list, an empty list is returned.
        """
        return list(self.adjacency_list.get(u, []))
    
    def reverse(self):
        """
        Returns a new Digraph that is the reverse of the current graph.
        """
        reverse_graph = Digraph(self.vertex_count)
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                reverse_graph.add_edge(v, u)
        return reverse_graph
    
class Search:

    def __init__(self, graph: Graph, start: int):
        self.graph = graph
        self.visited = [False] * self.graph.V
        self.start = start
        self._search()

    def _search(self) -> None:
        """
        Perform a search starting from the given vertex.
        """
        self.visited[self.start] = True
        for neighbor in self.graph.adjacent(self.start):
            if not self.visited[neighbor]:
                self.start = neighbor
                self.search()
    
    def connected(self, v: int) -> bool:
        """
        Check if the given vertex is connected to the starting vertex.

        Args:
            v (int): The vertex to check for connectivity.

        Returns:
            bool: True if the vertex is connected, False otherwise.
        """
        return self.visited[v]

class DFS:
    """
    Class to perform Depth First Search (DFS) on a graph.
    Attributes:
        graph (Graph): The graph on which DFS is performed.
        visited (set): A set to keep track of visited vertices.
    Methods:
        __init__(graph):
            Initializes the DFS with the given graph.
        dfs(start):
            Performs DFS starting from the given vertex `start`.
            Returns a list of vertices in the order they were visited.
    """
    def __init__(self, graph: Graph):
        self.graph = graph
        self.visited = set()

    def dfs(self, start: int) -> list:
        """
        Perform DFS starting from the given vertex.

        Args:
            start (int): The starting vertex for DFS.

        Returns:
            list: A list of vertices in the order they were visited.
        """
        stack = [start]
        result = []

        while stack:
            vertex = stack.pop()
            if vertex not in self.visited:
                self.visited.add(vertex)
                result.append(vertex)
                stack.extend(reversed(self.graph.adjacent(vertex)))

        return result
    
class BreadthFirstPaths:
    """
    Class to perform Breadth First Search (BFS) on a graph.
    Attributes:
        graph (Graph): The graph on which BFS is performed.
        start (int): The starting vertex for BFS.
        visited (set): A set to keep track of visited vertices.
        edge_to (dict): A dictionary to keep track of the path from the start vertex.
    Methods:
        __init__(graph, start):
            Initializes BFS with the given graph and starting vertex.
        bfs():
            Performs BFS starting from the given vertex `start`.
            Returns a list of vertices in the order they were visited.
        has_path_to(v):
            Checks if there is a path from the start vertex to vertex `v`.
        path_to(v):
            Retrieves the path from the start vertex to vertex `v`.
    """
    def __init__(self, graph: Graph, start: int):
        self.graph = graph
        self.start = start
        self.visited = set()
        self.edge_to = {}
        self.bfs()

    def bfs(self) -> None:
        """
        Perform BFS starting from the given vertex.
        """
        queue = [self.start]
        self.visited.add(self.start)
        
        while queue:
            vertex = queue.pop(0)
            for neighbor in self.graph.adjacent(vertex):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.edge_to[neighbor] = vertex
                    queue.append(neighbor)
    
    def has_path_to(self, v: int) -> bool:
        """
        Check if there is a path from the start vertex to vertex `v`.

        Args:
            v (int): The vertex to check for a path.

        Returns:
            bool: True if there is a path, False otherwise.
        """
        return v in self.visited
    
    def path_to(self, v: int) -> list:
        """
        Retrieve the path from the start vertex to vertex `v`.

        Args:
            v (int): The vertex to retrieve the path to.

        Returns:
            list: A list of vertices representing the path from the start vertex to `v`.
        """
        if not self.has_path_to(v):
            return None
        path = []
        while v != self.start:
            path.append(v)
            v = self.edge_to[v]
        path.append(self.start)
        return list(reversed(path))

class SymbolGraph:
    """
    A SymbolGraph represents a graph where vertices are identified by string keys
    rather than integer indices. It provides a mapping between string keys and 
    integer indices, and allows for graph operations using these indices.
    Attributes:
        index (dict): A dictionary mapping string keys to their corresponding integer indices.
        keys (list): A list of string keys, where the index of each key corresponds to its integer index.
    Methods:
        __init__(stream, delimiter):
            Initializes the SymbolGraph with data from a stream and a specified delimiter.
        contains(key):
            Checks if a given key exists in the symbol graph.
        index_of(key):
            Returns the integer index of a given key. Raises a ValueError if the key is not found.
        keys_list():
            Returns a copy of the list of keys.
        graph():
            Returns the underlying graph object.
        name_of(v):
            Returns the string key corresponding to a given vertex index. Raises a ValueError if the index is invalid.
        __str__():
            Returns a string representation of the SymbolGraph, including the number of keys and edges.
    """
    def __init__(self, stream: str, delimiter: str):
        """
        Initializes the object with a graph structure based on the input stream.
    
        Args:
            stream (iterable): An iterable of strings, where each string represents 
                a line of input. Each line should contain tokens separated by the 
                specified delimiter. The first token in each line represents a 
                vertex, and the subsequent tokens represent vertices connected to it.
            delimiter (str): The character used to split each line into tokens.
    
        Attributes:
            index (dict): A mapping from token strings to their corresponding 
                unique integer indices.
            keys (list): A list of tokens, where the index of each token corresponds 
                to its value in the `index` dictionary.
            graph (Graph): A graph object that stores the edges between vertices 
                based on the input stream.
        """
        self.index = {}
        self.keys = []
    
        # First pass: Build the index and keys
        for line in stream:
            tokens = line.strip().split(delimiter)
            for token in tokens:
                if token not in self.index:
                    self.index[token] = len(self.keys)
                    self.keys.append(token)
    
        # Initialize the graph with the correct number of vertices
        self._graph = Graph(len(self.keys))
    
        # Second pass: Add edges to the graph
        for line in stream:
            tokens = line.strip().split(delimiter)
            v = self.index[tokens[0]]
            for token in tokens[1:]:
                w = self.index[token]
                self._graph.add_edge(v, w)

    def contains(self, key: str) -> bool:
        return key in self.index
    
    def index_of(self, key: str) -> int:
        if key not in self.index:
            raise ValueError(f"{key} not found in symbol graph")
        return self.index[key]

    def keys_list(self) -> list:
        return self.keys.copy()

    def graph(self) -> Graph:
        return self._graph

    def name_of(self, v: int) -> str:
        if v < 0 or v >= len(self.keys):
            raise ValueError(f"Vertex {v} is not valid")
        return self.keys[v]

    def __str__(self):
        return f"SymbolGraph with {len(self.keys)} keys and {self.graph.E} edges."
