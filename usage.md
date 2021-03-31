# 利用例

if __name__=="__main__":
    nodes = [
        Node("a", offset=0),
        Node("b", offset=0),
        Node("c", offset=0),
        Node("d", offset=0),
        Node("e", offset=0),
        Node("f", offset=0),
        Node("g", offset=0),
        Node("h", offset=0),
        Node("i", offset=0)
    ]


    tree = FieldTree(nodes)

    # for node in tree.nodeList.values():
    #     print(repr(node))


    # tree.makeRoot(tree.searchNodeInList("a"))
    # tree.makeRoot(tree.searchNodeInList("b"))
    # tree.makeRoot(tree.searchNodeInList("c"))

    tree.makeRoot("a")
    tree.makeRoot("b")
    tree.makeRoot("c")

    # tree.addChild(tree.searchNodeInList("a"), tree.searchNodeInList("d"))
    # tree.addChild(tree.searchNodeInList("d"), tree.searchNodeInList("g"))
    # tree.addChild(tree.searchNodeInList("g"), tree.searchNodeInList("i"))
    # tree.addChild(tree.searchNodeInList("d"), tree.searchNodeInList("h"))
    # tree.addChild(tree.searchNodeInList("b"), tree.searchNodeInList("e"))
    # tree.addChild(tree.searchNodeInList("c"), tree.searchNodeInList("f"))

    tree.addChild("d", "a")
    tree.addChild("g", "d")
    tree.addChild("i", "g")
    tree.addChild("h", "d")
    tree.addChild("e", "b")
    tree.addChild("f", "c")

    tree.setOffset("b",10)


    tree.renderTree()


    print(tree.searchNodeInTree("b"))

    print(tree.getOffsetDict())
    print(tree.getParentDict())



    # print(tree.getPartialTreeNodes("d"))
    # tree.renderTree(tree.searchNodeInList("d"))


    # tree.delPartialTree("d")
    # # tree.searchNodeInList("d").parent=None
    # tree.renderTree("h")


    tree.changeParent("d", "e")

    tree.renderTree()

    # print(tree.getOffsetDict())
    # print(tree.getParentDict())
