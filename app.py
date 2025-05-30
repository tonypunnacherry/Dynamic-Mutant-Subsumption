import csv
import io
from flask import Flask, render_template, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


app = Flask(__name__)

def parse_kill_map(file_stream):
    kill_map = {}
    reader = csv.DictReader(io.StringIO(file_stream.read().decode('utf-8')))
    for row in reader:
        test = row['TestNo']
        mutant = row['MutantNo']
        result = row['[FAIL | TIME | EXC]']
        if result == "FAIL":
            kill_map.setdefault(mutant, set()).add(test)
    return kill_map

def build_dmsg(kill_map):
    grouped = {}
    for mutant, killed in kill_map.items():
        key = frozenset(killed)  # kill set as hashable key
        grouped.setdefault(key, []).append(mutant)

    # Step 2: Create nodes as merged labels
    killsets = list(grouped.keys())
    G = nx.DiGraph()

    # Each unique kill set becomes a node
    node_labels = {}  # maps killset key → merged mutant name
    for i, ks in enumerate(killsets):
        mutants = grouped[ks]
        label = ", ".join(sorted(mutants, key=int))
        node_labels[ks] = label
        G.add_node(label)

    # Step 3: Add edges based on subsumption (set containment)
    for i, ks1 in enumerate(killsets):
        for j, ks2 in enumerate(killsets):
            if i != j and ks1 < ks2:
                G.add_edge(node_labels[ks1], node_labels[ks2])
    
    return G

def compute_dominators(graph):
    """Return mutants with no incoming edges (dominators)."""
    dominator_nodes = [node for node in graph.nodes if graph.in_degree(node) == 0]

    # Split merged labels into individual mutants and flatten the list
    dominators = []
    for label in dominator_nodes:
        parts = [mut.strip() for mut in label.split(",")]
        dominators.extend(parts)

    return sorted(dominators, key=int)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csv_file']
        if not file:
            return redirect(request.url)

        kill_map = parse_kill_map(file)
        G = build_dmsg(kill_map)
        dominators = compute_dominators(G)
        # Assign levels (depths) using topological sort
        levels = defaultdict(list)
        depth = {}

        for node in nx.topological_sort(G):
            preds = list(G.predecessors(node))
            if preds:
                level = max(depth[p] for p in preds) + 1
            else:
                level = 0
            depth[node] = level
            levels[level].append(node)

        # Assign positions: same level -> same Y, spread across X
        pos = {}
        max_width = max(len(nodes) for nodes in levels.values())
        for level, nodes in levels.items():
            n = len(nodes)
            for i, node in enumerate(nodes):
                x = i - (n - 1) / 2  # center-align
                y = -level  # deeper levels go lower
                pos[node] = (x, y)

        # Draw graph
        plt.figure(figsize=(max(6, max_width * 1.5), len(levels) * 1.2))
        nx.draw(G, pos, with_labels=True, arrows=True,
                node_color='skyblue', edge_color='gray', node_size=1000,
                font_size=10, font_weight='bold', arrowstyle='->')

        plt.tight_layout()
        plt.savefig('static/dmsg.png')
        plt.close()

        return render_template('index.html', dominators=dominators)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)