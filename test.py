from bst import BST

t = BST(url="http://shive.bbakhtiari.ir/")
# t = BST(file="a.txt")
# t.put("salam")
# t.put("salam")
# t.put("salam")
# t.put("mahdi")
# t.put("salam")
# t.put("mamad")
# t.put("mahdi")
# t.put("aa")
# t.put("aaa")
# t.put("zzz")
# t.put("hi")
# t.put(u"salam")
# t.put("هههه")
# t.put(u"الف")
# t.put("aab")
# t.put("salav")
# t.put("mamas")
# t.put("mahdi2")

for i,j in t.sorted_by_count():
    print(i,j)
print(t.root.value)
t.delete("s1")
print(t.root.value)

t.plot()




# print()
#
# for i,j in t:
#     print(i,j)

# def p(node):
#     p=node.parent.value if node.parent else None
#     l=node.left.value if node.left else None
#     r=node.right.value if node.right else None
#
#     print(node.value, r, l , p)
#
# t.root.in_order(p)
