from heapq import heappop, heapify


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbour_weights = dict()
        self.distance_to_A = None
        self.merged_nodes = [self]

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        if not self.distance_to_A:
            return False
        if not other.distance_to_A:
            return True
        return self.distance_to_A > other.distance_to_A

    def __repr__(self):
        return f'[Node {self.name}]'


class StoerWagnerMinCutNetwork:
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.original_nodes = list(nodes)

    def minimum_cut(self):
        minimum_cut_weight = None
        partition = None
        while len(self.nodes) > 1:
            s, t = self.minimum_cut_phase(self.nodes[0])

            cut_weight = sum(t.neighbour_weights.values())

            if not minimum_cut_weight or cut_weight < minimum_cut_weight:
                minimum_cut_weight = cut_weight
                partition = t.merged_nodes

            self.merge_nodes(s, t)

        return partition, [node for node in self.original_nodes if node not in partition]

    def minimum_cut_phase(self, start_node: Node):
        tightly_coupled_nodes = [start_node]
        nodes = list(filter(lambda n: n != start_node, self.nodes))

        for node in nodes:
            node.distance_to_A = node.neighbour_weights.get(start_node, None)
        heapify(nodes)

        while len(tightly_coupled_nodes) != len(self.nodes):
            next_neighbour = heappop(nodes)
            for neighbour in next_neighbour.neighbour_weights:
                if neighbour.distance_to_A:
                    neighbour.distance_to_A += next_neighbour.neighbour_weights[neighbour]
                else:
                    neighbour.distance_to_A = next_neighbour.neighbour_weights[neighbour]
            heapify(nodes)
            tightly_coupled_nodes.append(next_neighbour)

        return tightly_coupled_nodes[-2], tightly_coupled_nodes[-1]

    def merge_nodes(self, s: Node, t: Node):
        self.nodes.remove(s)
        self.nodes.remove(t)
        new_node = Node(f'({s.name}-{t.name})')
        new_node.merged_nodes = s.merged_nodes + t.merged_nodes
        self.nodes.append(new_node)

        for neighbour in s.neighbour_weights.keys():
            if neighbour is not t:
                new_node.neighbour_weights[neighbour] = new_node.neighbour_weights.get(neighbour, 0) + s.neighbour_weights[neighbour]

        for neighbour in t.neighbour_weights.keys():
            if neighbour is not s:
                new_node.neighbour_weights[neighbour] = new_node.neighbour_weights.get(neighbour, 0) + t.neighbour_weights[neighbour]

        for neighbour in new_node.neighbour_weights:
            neighbour.neighbour_weights.pop(s, None)
            neighbour.neighbour_weights.pop(t, None)
            neighbour.neighbour_weights[new_node] = new_node.neighbour_weights[neighbour]


with open('input/day_25.txt') as file:
    nodes = {}
    for line in file:
        source, targets = line.split(': ')
        target_labels = targets.strip().split(' ')

        source_node = Node(source)

        if source not in nodes:
            nodes[source] = source_node
        else:
            source_node = nodes[source]

        for label in target_labels:
            target_node = Node(label)
            if label not in nodes:
                nodes[label] = target_node
            else:
                target_node = nodes[label]

            source_node.neighbour_weights[target_node] = 1
            target_node.neighbour_weights[source_node] = 1

nodes = list(nodes.values())

network = StoerWagnerMinCutNetwork(nodes)
partition_1, partition_2 = network.minimum_cut()

print(len(partition_1) * len(partition_2))
