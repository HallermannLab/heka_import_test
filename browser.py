import os, sys
import pyqtgraph as pg
import numpy as np
import heka_reader
from pyqtgraph.Qt import QtWidgets, QtCore


app = pg.mkQApp()

# Configure Qt GUI:

# Main window + splitters to let user resize panes
win = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout()
win.setLayout(layout)
hsplit = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
layout.addWidget(hsplit, 0, 0)
vsplit = QtWidgets.QSplitter(QtCore.Qt.Vertical)
hsplit.addWidget(vsplit)
w1 = QtWidgets.QWidget()
w1l = QtWidgets.QGridLayout()
w1.setLayout(w1l)
vsplit.addWidget(w1)

# Button for loading .dat file
load_btn = QtWidgets.QPushButton("Load...")
w1l.addWidget(load_btn, 0, 0)

# Tree for displaying .pul structure
tree = QtWidgets.QTreeWidget()
tree.setHeaderLabels(['Node', 'Label'])
tree.setColumnWidth(0, 200)
w1l.addWidget(tree, 1, 0)

# Tree for displaying metadata for selected node
data_tree = pg.DataTreeWidget()
vsplit.addWidget(data_tree)

# Plot for displaying trace data
plot = pg.PlotWidget()
hsplit.addWidget(plot)

# Resize and show window
hsplit.setStretchFactor(0, 400)
hsplit.setStretchFactor(1, 600)
win.resize(1200, 800)
win.show()


def load_clicked():
    # Display a file dialog to select a .dat file
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName()
    if file_name == '':
        return
    load(file_name)

load_btn.clicked.connect(load_clicked)


def load(file_name):
    """Load a new .dat file into the browser."""
    global bundle, tree_items
    bundle = heka_reader.Bundle(file_name)

    # Clear and update tree
    tree.clear()
    update_tree(tree.invisibleRootItem(), [])
    replot()


def update_tree(root_item, index):
    """Recursively build tree structure."""
    global bundle
    root = bundle.pul
    node = root
    for i in index:
        node = node[i]
    node_type = node.__class__.__name__
    if node_type.endswith('Record'):
        node_type = node_type[:-6]
    try:
        node_type += str(getattr(node, node_type + 'Count'))
    except AttributeError:
        pass
    try:
        node_label = node.Label
    except AttributeError:
        node_label = ''
    item = QtWidgets.QTreeWidgetItem([node_type, node_label])
    root_item.addChild(item)
    item.node = node
    item.index = index
    if len(index) < 2:
        item.setExpanded(True)
    for i in range(len(node.children)):
        update_tree(item, index + [i])


def replot():
    """Update plot and data tree when user selects a trace."""
    plot.clear()
    data_tree.clear()

    selected = tree.selectedItems()
    if len(selected) < 1:
        return

    sel = selected[0]
    fields = sel.node.get_fields()
    data_tree.setData(fields)

    for sel in selected:
        index = sel.index
        if len(index) < 4:
            return
        trace = sel.node
        plot.setLabel('bottom', trace.XUnit)
        plot.setLabel('left', trace.Label, units=trace.YUnit)
        data = bundle.data[index]
        time = np.linspace(trace.XStart, trace.XStart + trace.XInterval * (len(data) - 1), len(data))
        plot.plot(time, data)


tree.itemSelectionChanged.connect(replot)

# Optional: Load demo data if present
demo = 'DemoV9Bundle.dat'
if os.path.isfile(demo):
    load(demo)

if __name__ == '__main__':
    if sys.flags.interactive == 0:
        app.exec_()
