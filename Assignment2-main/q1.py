"""
Efficient suffix tree construction using Ukkonens algorithm
"""
__author__ = "Linjun Cai"
__studentID__ = "33120102"

import sys 
from graphviz import Digraph



class Node:
    def __init__(self, edge="", index = None, children=None):
        self.edge = edge
        self.index = index if index is not None else (0,0) #start and end index 
        self.ch = children or []

class UkkonenSuffixTree:
    def __init__(self, string, position):
        #self.orginal_string = string with $ at the end
        self.orginal_string = string[0:-1]
        self.root_node = [Node()]
        #Let lastj be the last extension j that was performed using rule 2.
        self.lastj = 0
        #The remainder is the number of suffixes that must be added to the tree in the current phase.
        self.remainder = 0
        self.active_node = None
        self.active_edge = None
        self.active_length = 0
        # (startIndex, globalEnd) set it as N, 
        self.global_end = len(self.orginal_string)

        #do the first char to begin with 
        self.root_node[0].ch.append(1)
        self.root_node.append(Node(edge=self.orginal_string[0:self.global_end], index=(0, self.global_end-1)))

        #loop through the string
        for i in range(1, len(self.orginal_string)):
            #reset 
            self.remainder = 0
            self.active_node = 0
            self.active_edge = self.root_node[self.active_node].edge
            self.active_length = 0
            #Rapid leaf extension
            self.rapid_leaf_extension(i+1)

            #testing
            #self.visualize_tree(0).render('suffix_tree_visualization', view=True)

            print("self.lastj", self.lastj+1, i+1)
            for j in range(self.lastj+1, i+1):
                current_substring = self.orginal_string[j:i+1]
                print("=====after rapid", current_substring, j, i)
                #traverse the suffix tree
                #traverse start with the string of index lastj+1 to i, lastj + 2 to i  
                result = self.traverse(j, i)
                if result:
                    self.makeExtension(j, i)


        #testing 
        self.visualize_tree(0).render('suffix_tree_visualization', view=True)

    def rapid_leaf_extension(self, i):
        """
        Rapid leaf extension
        Continues until all characters in suffix_string have been processed before index lastj +1
        Parameters:
        i: int, the index of the suffix string
        """
        current_substring = self.orginal_string[:i]
        print("current_substring", current_substring, "self.lastj", self.lastj, i)
    
        #loop till lastj, only rule one will be used before lastj
        for j in range(self.lastj+1):
            print("======rapid leaf extension", self.orginal_string[j:i], self.lastj, i)
            #we dont need to do rapid leaf extension if we have endIndex to N 
            self.remainder += 1

    def traverse(self, extension, phase)->bool:
        """
        This function traverses the suffix tree, look for paths
        Parameters:
        extension: int, the start index of the suffix string
        phase: int, the end index of the suffix string
        """

        #check every leaf node
        #all children nodes from the active node
        nodes = self.root_node[self.active_node]
        print("=====traverse", self.lastj, len(nodes.ch))

        #return false if there is path, means no extension needed
        for node_index in range(self.lastj, len(nodes.ch)):
            print("node_index", node_index, len(nodes.ch))

            #get the active node's children
            children = nodes.ch[node_index]

            #get the edge of the children
            edge = self.root_node[children].edge[:phase]
            print("edge", edge, self.orginal_string[extension:phase+1], edge[:len(self.orginal_string[extension:phase+1])])
            #if there is a path
            #this is checked by the if the last character of the edge is the same as the last character of the suffix string
            self.active_node = node_index
            self.active_edge = edge
            self.active_length = len(edge)
            #if there is a rule 3, return false
            print("self.remainder:", self.remainder, phase)
            if edge[:len(self.orginal_string[extension:phase+1])] == self.orginal_string[extension:phase+1]:
                #checked by for the same length of the edge and the suffix string, if they are the same 
                print("found path, rule 3")
                return False
            #if there isnt a path, continue to check the next leaf node
            else:
                continue 
        print("no path found, rule 2")
        return True

    def makeExtension(self, j, i):
        #apply rule 2
        #update lastj to j
        print("add new node", self.orginal_string[j], self.lastj, i, j)
        self.root_node[0].ch.append(len(self.root_node))
        self.root_node.append(Node(edge=self.orginal_string[j:self.global_end], index=(j, self.global_end-1)))
        print("lastj updated", self.lastj, j)
        self.lastj = j

    def visualize_tree(self, node_index, graph=None, parent_name=None, edge_label=''):
        if graph is None:
            graph = Digraph(comment='Suffix Tree', format='png')

        node = self.root_node[node_index]
        node_label = f"{node_index} ({node.index[0]}, {node.index[1]})" if node.edge else "Root"

        # Use the edge label or node label as node name in the graph
        node_name = f"{node_label}"
        graph.node(node_name, label=node_label)

        if parent_name is not None:
            graph.edge(parent_name, node_name, label=edge_label)

        for child_index in node.ch:
            child_node = self.root_node[child_index]
            self.visualize_tree(child_index, graph, node_name, child_node.edge)

        return graph


def main():
    string_filename, position_filename = sys.argv[1:3]
    # Read the string and position from the specified files
    try:
        with open(string_filename, 'r') as file:
            string = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found '{string_filename}'")
        sys.exit(1)

    try:
        with open(position_filename, 'r') as file:
            position = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found '{position_filename}'")
        sys.exit(1)

    UkkonenSuffixTree(string, position)

    # Write the match positions to the output file, adjusting for 1-based indexing
    #with open('output_q1.txt', 'w') as file:
    #    for match in matches:
    #        file.write(f"{match + 1}\n")

if __name__ == "__main__":
    UkkonenSuffixTree("abba$", "12") 
