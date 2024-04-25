"""
Efficient suffix tree construction using Ukkonens algorithm
"""
__author__ = "Linjun Cai"
__studentID__ = "33120102"

import sys 
from graphviz import Digraph



class Node:
    def __init__(self, edge="", index = None, children=None, leaf_num=None):
        self.edge = edge
        self.index = index if index is not None else (0,0) #start and end index 
        self.ch = children or []
        self.leaf_num = leaf_num or "U"

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
        self.active_node_child = None
        #count how many leaf
        self.leaf_count = 1
        # (startIndex, globalEnd) set it as N, 
        self.global_end = len(self.orginal_string)

        #do the first char to begin with 
        self.root_node[0].ch.append(1)
        self.root_node.append(Node(edge=self.orginal_string[0:self.global_end], index=(0, self.global_end-1), leaf_num=self.leaf_count))
        print("+++++leaf count")
        self.leaf_count += 1

        #loop through the string
        for i in range(1, len(self.orginal_string)):
            #reset 
            self.remainder = 0
            self.active_node = 0
            self.active_edge = 0
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
                print("self.remainder:", self.remainder, i, result)
                if result == "2a" or result == "2b":
                    self.makeExtension(j, i, result)


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

    def traverse(self, extension, phase):
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

        length = (0,len(nodes.ch))

        #return false if there is path, means no extension needed
        for node_index in range(length[0], length[1]):
            print("node_index", node_index, len(nodes.ch), self.root_node[node_index].edge, nodes.ch, self.active_node)

            #get the active node's child
            child = nodes.ch[node_index]

            #get the edge of the child
            edge = self.root_node[child].edge[:phase]
            print("edge", edge, node_index, child)
            #if there is a path
            #this is checked by the if the last character of the edge is the same as the last character of the suffix string

            #this is because i set the root node as node 0, the first node is index 1 
            if length[0] == 0:      #if the active node is not the root node
                self.active_node = node_index
            else:                   #if the active node is the root node, because i want the children to start as index 0
                self.active_node = node_index -1
                print("-------------------------------------------------", self.active_node, node_index, child)

            self.active_edge = edge
            self.active_length = len(edge)
            #keep track of the child node
            self.active_node_child = child
            #if there is a rule 3, return false
            edge_index = 0      #used to compare edge and suffix string
            temp_remainder = self.remainder
            print(self.remainder, phase+1, edge, node_index)
            for k in range(self.remainder, phase+1):
                #if the edge and the suffix string are the same and its not the last character of the suffix string
                #then continue to check the next character, no rule apply here 
                print("edge compare1", edge[edge_index], self.orginal_string[k], k, phase)
                if edge[edge_index] == self.orginal_string[k] and k != phase:
                    temp_remainder += 1
                #if the edge and the suffix string are the same and its the last character of the suffix string
                elif edge[edge_index] == self.orginal_string[k] and k == phase:
                    print("found path, rule 3")
                    self.remainder = temp_remainder
                    return "3"
                edge_index += 1
            
            temp_remainder = self.remainder
            #aftering checking for rule 3, check for rule 2
            edge_index = 0      #used to compare edge and suffix string
            for k in range(self.remainder, phase+1):
                #if the edge and the suffix string are the same and its not the last character of the suffix string
                #then continue to check the next character, no rule apply here 
                print("edge compare2", edge[edge_index], self.orginal_string[k], k, phase, edge_index, len(edge))
                if edge[edge_index] == self.orginal_string[k] and k != phase:
                    temp_remainder += 1
                #if the edge and the suffix string are the same and its the last character of the suffix string
                elif edge[edge_index] != self.orginal_string[k] and edge_index != 0:
                    print("rule 2 alter")
                    self.remainder = temp_remainder
                    self.active_node_child = edge_index
                    return "2b"
                edge_index += 1

        return "2a"
        
        
    def makeExtension(self, j, i, result):
        #apply rule 2
        #update lastj to j
        print("add new node", self.orginal_string[j], self.lastj, i, j, result)
        #rule 2a
        print("remainder", self.remainder, j+1)
        if result == "2a":
            self.root_node[self.active_node].ch.append(len(self.root_node))
            self.root_node.append(Node(edge=self.orginal_string[j:self.global_end], index=(j, self.global_end-1), leaf_num=self.leaf_count))
            print("+++++leaf count")
            self.leaf_count += 1
            print("lastj updated", self.lastj, j)
            self.lastj = j
        #rule 2 alter 
        else:
            self.splitNode(j, i)            
    
    def splitNode(self, j, i):
        print("=============split node", j, i, "active node", self.active_node, self.active_node_child)
        #get the leaf node index
        edge = self.root_node[self.active_node].ch[self.active_node_child]
        #get the leaf node
        node = self.root_node[edge]
        print("edge", edge, )
        
        #start spliting
        new_edge = node.edge[:j-1]
        remain_edge = node.edge[j-1:]
        print("new_edge", new_edge, remain_edge)

        new_edge_index = (node.index[0], j-1)
        remain_edge_index = (j, node.index[1])
        print("new_edge_index", new_edge_index, remain_edge_index)

        #create new internal node
        new_internal_node = Node(edge=new_edge, index=new_edge_index)

        #update the leaf node
        node.edge = remain_edge
        node.index = remain_edge_index

        #new character edge 
        new_char_edge = self.orginal_string[j+1:i+1]
        print("new_char_edge", new_char_edge)

        #create new leaf node
        new_leaf_node = Node(edge=new_char_edge, index=(j+1, i), leaf_num=self.leaf_count)
        print("+++++leaf count")
        self.leaf_count += 1

        #add the new leaf node and orginal node to the new internal node
        new_internal_node.ch.append(edge)

        #update the active node's children
        self.root_node[self.active_node].ch[self.active_node_child] = len(self.root_node)
        self.root_node.append(new_internal_node)
        
        #add the new leaf node to the new internal node
        self.root_node.append(new_leaf_node)
        new_internal_node.ch.append(self.leaf_count)
        self.leaf_count += 1
        
        #update lastj
        self.remainder += 1
        self.lastj = j

    def visualize_tree(self, node_index, graph=None, parent_name=None, edge_label=''):
        if graph is None:
            graph = Digraph(comment='Suffix Tree', format='png')

        node = self.root_node[node_index]
        node_label = f"{node.leaf_num} ({node.index[0]}, {node.index[1]})" if node.edge else "Root"

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
