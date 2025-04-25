import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
import torch.optim as optim
import time
import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC
from abc import abstractmethod

"""
This module implements a compositional computational network using PyTorch and NetworkX.
It defines a Cell interface, a neural network-based cell (Cell_NN), and a graph-based container (CCN)
to manage interconnected cells that can forward and train in sequence.
"""
class Cell(ABC):
    """
    Abstract base class representing a computational cell.

    Attributes:
        model (nn.Module): PyTorch model representing the cell's computation.
        num_inputs (int): Number of inputs the cell expects.
        num_outputs (int): Number of outputs the cell produces.
        loss_func (nn.Module): PyTorch loss function.
        device (str): Device on which the model is run ('cpu' or 'cuda').
    """
    def __init__(self, model, *, inputs, outputs, loss_func, device):
        #super().__init__()
        self.model = model
        self.num_inputs = inputs
        self.num_outputs = outputs
        self.loss_func = loss_func
        self.device = device
        
    def change_model(self, new_model):
        """
        Replace the current model with a new one.

        Args:
            new_model (nn.Module): The new PyTorch model.
        """
        self.model = new_model

    def forward(self, x_input):
        """
        Pass input through the model.

        Args:
            x_input (list): List of float inputs.

        Returns:
            Model output.
        """
        x = [float(x_input[i]) for i in range(len(x_input))]
        output = self.model(x)
        return output
    
    @abstractmethod
    def train(self, X, y, alpha, batch_size):
        pass

    @abstractmethod
    def one_opt_train(self, X, y, batch_size, opt):
        pass

class Cell_NN(nn.Module, Cell):
    """
    A concrete implementation of the Cell class using a PyTorch Sequential model.

    Inherits from both PyTorch's nn.Module and the abstract Cell class.
    """
    def __init__(self, model, *, inputs, outputs, loss_func, device):
        nn.Module.__init__(self)
        Cell.__init__(self, model, inputs=inputs, outputs=outputs, loss_func=loss_func, device=device)

    def change_model(self, new_model):
        """
        Override to replace model in both nn.Module and Cell.
        """
        self.model = new_model

    def forward(self, x_input):
        """
        Converts input list to tensor and passes through the model.

        Args:
            x_input (list): List of numeric values.

        Returns:
            List of float outputs.
        """
        x = [float(x_input[i]) for i in range(len(x_input))]
        x = torch.tensor(x).to(self.device)
        output = self.model(x)
        output = [i.item() for i in output]
        return output
    
    def train(self, X, y, alpha, batch_size):
        """
        Train the model for one epoch using SGD optimizer.

        Args:
            X (list): Input feature matrix.
            y (list): Target labels.
            alpha (float): Learning rate.
            batch_size (int): Number of samples per batch.

        Returns:
            float: Total loss for the epoch.
        """
        loss = 0
        end = batch_size
        opt = optim.SGD(self.model.parameters(), lr=alpha)
        for start in range(0, len(X), batch_size):
            end = start + batch_size
            X_i = torch.tensor(X[start:end]).float().to(self.device)
            y_i = torch.tensor(y[start:end]).to(self.device)
            opt.zero_grad()
            loss_iter = self.loss_func(self.model(X_i), y_i.unsqueeze(1))
            loss_iter.backward()
            opt.step()
            loss += loss_iter
        return loss.item()
        
    def one_opt_train(self, X, y, batch_size, opt):
        """
        Train the model for one epoch using a given optimizer.

        Args:
            X (list): Input features.
            y (list): Target labels.
            batch_size (int): Number of samples per batch.
            opt (torch.optim.Optimizer): Optimizer instance.

        Returns:
            float: Total loss for the epoch.
        """
        loss = 0
        end = batch_size
        for start in range(0, len(X), batch_size):
            end = start + batch_size
            X_i = torch.tensor(X[start:end]).float().to(self.device)
            y_i = torch.tensor(y[start:end]).to(self.device)
            opt.zero_grad()
            loss_iter = self.loss_func(self.model(X_i), y_i)
            loss_iter.backward()
            opt.step()
            loss += loss_iter
        return loss.item()

class CCN():
    """
    Compositional Computational Network - manages a graph of connected Cell_NN units.

    Uses NetworkX to store relationships and dependencies between cells.
    """
    def __init__(self):
        self.cells = nx.DiGraph()
        self.abstracted_graph = nx.DiGraph()
        self.invisible_nodes = set()
        self.ratios = {}
    
    def add_cell(self, cell, label):
        """
        Add a new cell to the network.

        Args:
            cell (Cell_NN): The cell to add.
            label (str): Unique identifier for the cell.
        """
        self.ratios[label] = {(label,): 1}
        self.cells.add_node(label, structure=cell, group=["None"])
        self.abstracted_graph.add_node(label, structure=cell, group=["None"])

    def remove_cell(self, label):
        """
        Remove a cell and related edges from both base and abstracted graphs.

        Args:
            label (str): Identifier of the cell to remove.
        """
        if (label in self.abstracted_graph.nodes and not label in self.cells.nodes):
            self.abstracted_graph.remove_node(label)
            nodes = [l for l in list(self.cells.nodes)]
            for l in nodes:
                if label in self.cells.nodes[l]["group"]:
                    self.cells.remove_node(l)
            return
        self.cells.remove_node(label)
        self.abstracted_graph.remove_node(label)
    
    def link(self, labelA, labelB, weight):
        """
        Create a directional link between two cells.

        Args:
            labelA (str): Source cell label.
            labelB (str): Destination cell label.
            weight (int): Weight or number of values passed along the edge.
        """
        self.cells.add_edge(labelA, labelB, weight=weight)
        self.abstracted_graph.add_edge(labelA, labelB, weight=weight)

    def unlink(self, labelA, labelB):
        """
        Remove an edge from the graph.

        Args:
            labelA (str): Source label.
            labelB (str): Destination label.
        """
        if (labelA in self.abstracted_graph.nodes and not labelA in self.cells.nodes) and (labelB in self.abstracted_graph.nodes and not labelB in self.cells.nodes):
            self.abstracted_graph.remove_edge(labelA, labelB)
            for label in self.cells.nodes:
                if labelA in self.cells.nodes[label]["group"]:
                    children = [l for l in list(self.cells.successors(label))]
                    for child in children:
                        if labelB in self.cells.nodes[child]["group"]:
                            self.cells.remove_edge(label, child)
            return
        if (labelA in self.abstracted_graph.nodes and not labelA in self.cells.nodes):
            self.abstracted_graph.remove_edge(labelA, labelB)
            for label in self.cells.nodes:
                if labelA in self.cells.nodes[label]["group"]:
                    if self.cells.has_edge(label, labelB):
                        self.cells.remove_edge(label, labelB)
            return
        if (labelB in self.abstracted_graph.nodes and not labelB in self.cells.nodes):
            self.abstracted_graph.remove_edge(labelA, labelB)
            for label in self.cells.nodes:
                if labelB in self.cells.nodes[label]["group"]:
                    if self.cells.has_edge(labelA, label):
                        self.cells.remove_edge(labelA, label)
            return
        self.cells.remove_edge(labelA, labelB)
        if labelA in self.abstracted_graph.nodes and labelB in self.abstracted_graph.nodes:
            self.abstracted_graph.remove_edge(labelA, labelB)
    
    def get_sequence(self):
        """
        Returns a topological sort of the cell graph for forward computation.

        Returns:
            list: Ordered list of cell labels.
        """
        labels = [l for l in list(self.cells.nodes)]
        visited = {i: False for i in labels}
        result = []
        def visit(label):
            if visited[label]:
                return
            visited[label] = True
            for connection in list(self.cells.neighbors(label)):
                visit(connection)
            result.append(label)
        for label in labels:
            visit(label)
        return result[::-1]
    
    def load_graph(self, adjacency_matrix, *, labels=None, default_structure, overwrite=[], activation=nn.ReLU(), loss_func=nn.MSELoss(), device='cpu'):
        """
        Build the network graph from an adjacency matrix.

        Args:
            adjacency_matrix (list of lists): Defines the connections.
            labels (list, optional): Custom labels for nodes.
            default_structure (list): Default layer sizes for all nodes.
            overwrite (list): Tuples (label, structure) to override default.
            activation (nn.Module): Activation function.
            loss_func (nn.Module): Loss function.
            device (str): Device for models.
        """
        if labels == None:
            labels = [str(i) for i in range(len(adjacency_matrix))]
        structures = [default_structure for i in range(len(labels))]
        for o in overwrite:
            structures[labels.index(str(o[0]))] = o[1]
        for i in range(len(labels)):
            modules = []
            for j in range(1, len(structures[i])):
                modules.append(nn.Linear(structures[i][j-1], structures[i][j]))
                if j == len(structures[i])-1:
                    break
                modules.append(activation)
            cell = Cell_NN(nn.Sequential(*modules), inputs=structures[i][0], outputs=structures[i][len(structures[i])-1], loss_func=loss_func, device=device).to(device)
            self.add_cell(cell, labels[i])
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix[i])):
                if adjacency_matrix[i][j] > 0:
                    self.link(labels[i], labels[j], adjacency_matrix[i][j])
        self.abstracted_graph = self.cells.copy()

    def change_structure(self, label, structure, activation=nn.ReLU()):
        """
        Update the architecture of a specific node.

        Args:
            label (str): Target node label.
            structure (list): List of layer sizes.
            activation (nn.Module): Activation function.
        """
        modules = []
        for i in range(1, len(structure)):
            modules.append(nn.Linear(structure[i-1], structure[i]))
            modules.append(activation)
        self.cells.nodes[label].change_model(nn.Sequential(*modules))
        self.abstracted_graph.nodes[label].change_model(nn.Sequential(*modules))

    def clear_connections(self):
        """
        Remove all edges from the cell graphs.
        """
        edges = list(self.cells.edges())
        self.cells.remove_edges_from(edges)
        self.abstracted_graph.remove_edges_from(edges)

    def change_graph(self, adjacency_matrix):
        """
        Change the entire connection structure of the graph.

        Args:
            adjacency_matrix (list of lists): New connection matrix.
        """
        self.clear_connections()
        labels = list(self.cells.nodes)
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix[i])):
                if adjacency_matrix[i][j] > 0:
                    self.link(labels[i], labels[j], adjacency_matrix[i][j])

    def forward(self, X_input):
        """
        Forward propagate inputs through the network.

        Args:
            X_input (dict): Dict of inputs per node.

        Returns:
            tuple: (updated X_input, final outputs per node)
        """
        X = X_input.copy()
        
        sequence = self.get_sequence()
        final_output = {}
        index_rev = {i: 0 for i in sequence}
        for label in sequence:
            if len(X[label]) < self.cells.nodes[label]['structure'].num_inputs:
                diff = self.cells.nodes[label]['structure'].num_inputs - len(X[label])
                X[label].extend([0 for i in range(diff)])
        for label in sequence:
            output = self.cells.nodes[label]['structure'].forward(X[label])
            final_output[label] = output
            for connection in list(self.cells.neighbors(label)):
                for index in range(self.cells.get_edge_data(label, connection)['weight'])[::-1]:
                    X[connection][len(X[connection])-index_rev[connection]-1] = output[index]
                    index_rev[connection] += 1
        return X, final_output
    
    def train(self, X, y, epochs, alpha, batch_size):
        """
        Train the entire network over multiple epochs.

        Args:
            X (dict): Input data per node.
            y (dict): Labels per node.
            epochs (int): Number of training epochs.
            alpha (float): Learning rate.
            batch_size (int): Mini-batch size.

        Returns:
            dict: Training loss history per node.
        """
        labels = list(self.cells.nodes)
        groups = {}
        losses = {l: [0 for e in range(epochs)] for l in labels}
        for l in groups.keys():
            losses[l] = [0 for e in range(epochs)]
        X_list = [{l: X[l][i] for l in labels} for i in range(len(X[labels[0]]))]
        y_list = [1 for i in range(len(X[labels[0]]))]
        for e in range(epochs):
            for iter in range(len(X[labels[0]])):
                y_list[iter] = {l: y[l][iter] for l in labels}
                X_list[iter] = self.forward(X_list[iter])[0]
            for label in labels:
                label_list_X = [d[label] for d in X_list]
                label_list_y = [d[label] for d in y_list]
                for r in list(self.ratios[label].keys()):
                    curr_alpha = alpha * self.ratios[label][r]
                    losses[label][e] = self.custom_train(label, r, X_list, y_list, curr_alpha, batch_size)
            print(f"Epoch {e+1}/{epochs} - Losses: {[losses[l][e] for l in labels]}")
        return losses
    
    def custom_train(self, label, key, X, y, alpha, batch_size, device='cpu'):
        """
        Train a single cell or group of cells using a custom key.

        Args:
            label (str): Label of the node.
            key (tuple): Keys to use for training.
            X (list): Input dicts per sample.
            y (list): Target dicts per sample.
            alpha (float): Learning rate.
            batch_size (int): Batch size.
            device (str): Training device.

        Returns:
            float: Accumulated loss.
        """
        opt = optim.SGD(self.cells.nodes[label]['structure'].model.parameters(), lr=alpha)
        total_loss = 0
        for start in range(0, len(X), batch_size):
            opt.zero_grad()
            end = min(start + batch_size, len(X))
            loss_iter = 0
            for k in key:
                X_label = torch.tensor([d[k] for d in X], dtype=torch.float32, device=device)
                y_label = torch.tensor([d[k] for d in y], device=device)
                preds = self.cells.nodes[k]['structure'].model(X_label[start:end])
                preds = preds.clamp(min=-1e6, max=1e6)
                loss_k = self.cells.nodes[k]['structure'].loss_func(preds, y_label[start:end])
                loss_iter += loss_k
            if len(key) > 0:
                loss_iter /= len(key)
            total_loss += loss_iter.detach().item()
            loss_iter.backward()
            torch.nn.utils.clip_grad_norm_(self.cells.nodes[label]['structure'].model.parameters(), max_norm=1.0)
            opt.step()
        return total_loss

    def define_loss(self, label, ratios):
        """
        Define the loss ratios used for training a cell.

        Args:
            label (str): Cell label.
            ratios (dict): Mapping from cell group to weight ratio.
        """
        self.ratios[label] = ratios

    def merge(self, nodes_to_collapse, new_label):
        """
        Collapse multiple nodes into a higher-level node in the abstracted graph.

        Args:
            nodes_to_collapse (list): Labels of nodes to merge.
            new_label (str): Label for the new abstracted node.
        """
        for node in nodes_to_collapse:
            if "None" in self.cells.nodes[node]['group']:
                self.cells.nodes[node]['group'].remove("None")
            self.cells.nodes[node]['group'].append(new_label)
            if "None" in self.cells.nodes[node]['group']:
                self.abstracted_graph.nodes[node]['group'].remove("None")
            self.abstracted_graph.nodes[node]['group'].append(new_label)
        H = self.abstracted_graph.subgraph(nodes_to_collapse)
        children = {}
        parents = {}
        for label in nodes_to_collapse:
            for connection in self.abstracted_graph.successors(label):
                children[connection] = children.get(connection, 0) + self.abstracted_graph.get_edge_data(label, connection, 0)['weight']
            for connection in self.abstracted_graph.predecessors(label):
                parents[connection] = parents.get(connection, 0) + self.abstracted_graph.get_edge_data(connection, label, 0)['weight']
        self.abstracted_graph.add_node(new_label, structure=H, group=new_label)
        for child, weight in children.items():
            self.abstracted_graph.add_edge(new_label, child, weight=weight)
        for parent, weight in parents.items():
            self.abstracted_graph.add_edge(parent, new_label, weight=weight)
        for label in nodes_to_collapse:
            self.invisible_nodes.add(label)

    def plot_losses(self, losses):
        """
        Plot training loss over epochs for each node.

        Args:
            losses (dict): Mapping of labels to loss lists.
        """
        labels = [l for l in list(losses.keys())]
        fig, ax = plt.subplots()
        ax.set_xlabel("epochs")
        ax.set_ylabel("loss")
        for l in labels:
            line, = ax.plot(range(len(list(losses[l]))), list(losses[l]))
            line.set_label(l)
            ax.legend()
        plt.show()

    def get_accuracy(self, X, y):
        """
        Calculate accuracy per node based on max-class prediction.

        Args:
            X (dict): Input samples.
            y (dict): Target labels.

        Returns:
            dict: Accuracy per label.
        """
        labels = [l for l in list(self.cells.nodes)]

        outs = np.array([self.forward({l: X[l][i] for l in labels})[1] for i in range(len(X[labels[0]]))])
        preds = {l: [] for l in labels}
        for out in outs:
            for label in list(preds.keys()):
                preds[label].append(np.argmax(out[label]))
        acc = {l: np.where([preds[l][i] == y[l][i] for i in range(len(preds[l]))], 1, 0) for l in list(preds.keys())}
        acc = {l: np.sum(acc[l])/len(acc[l]) for l in list(preds.keys())}
        return acc

    def display(self):
        """
        Visualize the abstracted graph with visible nodes and weights.
        """
        visible_nodes = set(self.abstracted_graph.nodes())-self.invisible_nodes
        visible_edges = [edge for edge in self.abstracted_graph.edges if edge[0] not in self.invisible_nodes and edge[1] not in self.invisible_nodes]
        labels = {node: str(node) for node in visible_nodes}
        pos = nx.shell_layout(self.abstracted_graph.subgraph(visible_nodes))
        nx.draw_networkx(self.abstracted_graph, pos, with_labels=False, nodelist=visible_nodes, edgelist=visible_edges, edge_color="black")
        nx.draw_networkx_labels(self.abstracted_graph, pos, labels=labels)
        edge_labels = {(u, v): self.abstracted_graph[u][v]['weight'] for u, v in visible_edges}
        nx.draw_networkx_edge_labels(self.abstracted_graph, pos, edge_labels=edge_labels)

    def display_base(self):
        """
        Visualize the base cell graph with edge weights.
        """
        pos = nx.shell_layout(self.cells)
        nx.draw_networkx(self.cells, pos)
        edge_labels = nx.get_edge_attributes(self.cells, 'weight')
        nx.draw_networkx_edge_labels(self.cells, pos, edge_labels=edge_labels)