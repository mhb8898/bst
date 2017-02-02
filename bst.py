"""
bst library:


"""

import urllib.request, re
from collections import OrderedDict
from bs4 import BeautifulSoup
import networkx as nx
import itertools as IT
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


class Node:
    def __init__(self, val, left=None, right=None, parent=None, count=1):
        self.right = right
        self.left = left
        self.value = val
        self.count = count
        self.parent = parent

    def __len__(self):
        return self.count

    def __iter__(self):
        if self:
            if self.left:
                for elem in self.left:
                    yield elem
            yield (self.value, self.count)
            if self.right:
                for elem in self.right:
                    yield elem

    def replace(self, val, lc, rc):
        self.value = val
        self.left = lc
        self.right = rc
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def find_successor(self):
        s = None
        if self.right:
            s = self.right.find_min()
        else:
            if self.parent:
                if self.left:
                    s = self.parent
                else:
                    self.parent.right = None
                    s = self.parent.find_successor()
                    self.parent.right = self
        return s

    def find_min(self):
        current = self
        while current.left:
            current = current.left
        return current

    def splice_out(self):
        if not (self.right or self.left):
            if self.parent and self.parent.left == self:
                self.parent.left = None
            else:
                self.parent.right = None
        elif self.right or self.left:
            if self.left:
                if self.parent and self.parent.left == self:
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left
                self.left.parent = self.parent
            else:
                if self.parent and self.parent.left == self:
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
                self.right.parent = self.parent

    def edge_list(self, counter=IT.count().__next__):
        for node in (self.left, self.right):
            if node:
                yield (self.value, node.value)
        for node in (self.left, self.right):
            if node:
                for n in node.edge_list(counter):
                    yield n

    def in_order(self, f):
        if self.left:
            self.left.in_order(f)
        f(self)
        if self.right:
            self.right.in_order(f)


class BST:
    def __init__(self, url=None, file=None):
        self.root = None
        self.size = 0
        self.cd = dict()

        if url:
            text = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(text, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            word_list = re.sub("[^\w]", " ", visible_text).split()
            for i in word_list:
                self.put(i)

        if file:
            with open(file,"r") as f:
                data = f.read()
                word_list = re.sub("[^\w]", " ", data).split()
                for i in word_list:
                    self.put(i)

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self, val):
        t = self.get(val)
        if t:
            if self.cd[t.count] == 1:
                self.cd.pop(t.count)
            else:
                self.cd[t.count] -= 1
            t.count += 1
            self.cd[t.count] = self.cd.get(t.count, 0) + 1

        else:
            if self.root:
                self._put(val, self.root)
            else:
                self.root = Node(val)
                self.cd[self.root.count] = self.cd.get(self.root.count, 0) + 1

            self.size += 1

    def _put(self, val, cr):
        if val < cr.value:
            if cr.left:
                self._put(val, cr.left)
            else:
                cr.left = Node(val, parent=cr)
                self.cd[cr.left.count] = self.cd.get(cr.left.count, 0) + 1
        else:
            if cr.right:
                self._put(val, cr.right)
            else:
                cr.right = Node(val, parent=cr)
                self.cd[cr.right.count] = self.cd.get(cr.right.count, 0) + 1

    def get(self, val):
        if self.root:
            res = self._get(val, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None

    def _get(self, val, cr):
        if not cr:
            return None
        elif cr.value == val:
            return cr
        elif val < cr.value:
            return self._get(val, cr.left)
        else:
            return self._get(val, cr.right)

    def __contains__(self, val):
        if self._get(val, self.root):
            return True
        else:
            return False

    def delete(self, val):
        if self.size > 1:
            rm_node = self._get(val, self.root)
            if rm_node:
                self.remove(rm_node)
                self.size -= 1
                self.cd[rm_node.count] = self.cd.get(rm_node.count, 0) - 1

            else:
                raise KeyError("Error, Word not in tree")
        elif self.size == 1 and self.root.value == val:
            self.root = None
            self.size -= 1
        else:
            raise KeyError("Error, Word not in tree")

    def remove(self, cr):
        if not cr.right and not cr.left:  # barg
            if cr == cr.parent.left:
                cr.parent.left = None
            else:
                cr.parent.right = None
        elif cr.right and cr.left:  # interior
            s = cr.find_successor()
            s.splice_out()
            cr.value = s.value

        else:  # this node has one child
            if cr.left:
                if cr.parent and cr.parent.left == cr:
                    cr.left.parent = cr.parent
                    cr.parent.left = cr.left
                elif cr.parent and cr.parent.right == cr:
                    cr.left.parent = cr.parent
                    cr.parent.right = cr.left
                else:
                    cr.replace(cr.left.value,
                               cr.left.left,
                               cr.left.right)
            else:
                if cr.parent and cr.parent.left == cr:
                    cr.right.parent = cr.parent
                    cr.parent.left = cr.right
                elif cr.parent and cr.parent.right == cr:
                    cr.right.parent = cr.parent
                    cr.parent.right = cr.right
                else:
                    cr.replace(cr.right.value,
                               cr.right.left,
                               cr.right.right)

    def sorted_by_count(self):
        l = [None] * self.size
        cd = OrderedDict(self.cd)
        d = OrderedDict()
        s = -1
        print(cd,self.size)
        for i in cd:
            d[i] = cd[i] + s
            s += cd[i]
        print(d)
        for i, j in self:
            l[d[j]] = (i, j)
            d[j] -= 1

        return l[::-1]

    def plot(self):
        # print(list(self.root.edge_list()))
        labels = {}
        for i, j in self.root.edge_list():
            labels[i] = i
            labels[j] = j
        G = nx.Graph(self.root.edge_list())
        pos = graphviz_layout(G, prog='dot')

        nx.draw(G, pos)

        nx.draw_networkx_labels(G, pos, labels)

        plt.show()

# class BST_count(BST):
#     def __init__(self, url=None, file=None,tree=None):
#         if tree:
#             pass
#         else:
#             super(BST).__init__(url,file)
