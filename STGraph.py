"""
Kei Imada
20180506
A distraction that I am developing currently
"""
import matplotlib.pyplot as plt
import networkx as nx

class STGraph(object):
    """
    The class for the Storyteller
    """
    def __init__(self, initial_id, initial_text):
        """
        Constructor
        @params TODO
        """
        G = nx.DiGraph()
        start_node = initial_id
        G.add_node(initial_id, text=initial_text)
        self.G = G
        self.curr = start_node
    def add_node(self, node_id, node_text):
        """
        TODO
        """
        # print "c1",self.G.nodes.data("text")
        if node_id in self.G:
            if self.G.nodes.data("text")[node_id] != node_text:
                print node_text
                print self.G.nodes.data("text")[node_id]
                raise Exception("STGraph::add_node node with same id but different text exists!")
        self.G.add_node(node_id, text=node_text)
    def get_current(self):
        """
        gets current text
        """
        return self.G.nodes.data("text")[self.curr]
    def add_choice(self, src, dest, choice):
        """
        adds a choice to the graph, if src or dest not in graph, throws error
        """
        if src not in self.G:
            raise Exception("STGraph::add_choice src is not in graph!")
        if dest not in self.G:
            raise Exception("STGraph::add_choice dest is not in graph!")
        self.G.add_edge(src, dest, choice=choice)
    def get_choices(self):
        """
        get current choices
        """
        return [self.G[self.curr][n_id]["choice"] for n_id in self.G.neighbors(self.curr)]
    def choose(self, selected_choice):
        """
        choose a choice, if choice does not exist, no change
        """
        choice_dict = dict([(self.G[self.curr][n_id]["choice"], n_id) for n_id in self.G.neighbors(self.curr)])
        for possible_choice in choice_dict:
            if possible_choice == selected_choice:
                self.curr = choice_dict[possible_choice]
    def visualize(self, show_story_text=True, show_choice_texts=True):
        """
        Visualize the Storyteller graph with matplotlib
        """
        pos = nx.kamada_kawai_layout(self.G)
        # node_labels = dict(self.G.nodes.data("text"))
        # node_labels = dict(zip(self.G.nodes, self.G.nodes))
        node_labels = dict(self.G.nodes.data("text")) if show_story_text else dict(zip(self.G.nodes, self.G.nodes))
        edge_labels = dict([(edge,self.G[edge[0]][edge[1]]["choice"]) for edge in self.G.edges()]) if show_choice_texts else dict([(edge,i) for (edge, i) in zip(self.G.edges(), range(len(self.G.edges())))])
        # edge_labels = dict([(edge,edge[1]) for edge in self.G.edges()])

        # print self.G.nodes

        # print node_labels
        # print node_labels

        plt.figure(1,figsize=(10,7))
        nx.draw(self.G, pos=pos, edge_labels=edge_labels, node_color="white", node_size=1000, font_weight='bold')
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=edge_labels, label_pos=0.4, arrows=False)
        nx.draw_networkx_labels(self.G, pos=pos, labels=node_labels)
        plt.show()
