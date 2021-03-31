import os
import sys
import re

# # 自作クラス
# import Generic_tree.Gtree_Node as gnode
# import Generic_tree.Gtree as gtree
# import Generic_tree.Gforest as gforest

from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, PostOrderIter
from anytree.search import findall, find_by_attr

"""
anytree 例文
# Node,treeの構築
f = Node("f")
b = Node("b", parent=f)
a = Node("a", parent=b)
# Nodeの削除
a.parent = None
# treeのレンダリング
print(RenderTree(f, style=AsciiStyle()).by_attr())
# ラムダ式によるNodeの検索
print(search.findall(f, filter_=lambda node: node.name in ("a")))
# 属性値(デフォルトはname)での検索
search.find_by_attr(f, 'a')
# Nodeインスタンスのrootからの経路取得
[str(node.name) for node in a.path]
"""


class FieldTree:
    # nodeList :{"name":node}とすれば検索機能は不要になる
    def __init__(self, nodeList: list or dict) -> None:
        # super().__init__()
        # nodeListに盤面上のNodeをすべていれる->nodeListをdict型に変更
        if isinstance(nodeList,dict):
            self.nodeList = nodeList
        elif isinstance(nodeList,list):
            self.nodeList=dict()
            for ele in nodeList:
                # print(ele)
                self.nodeList[ele.name]=ele
        else:
            raise TypeError("nodeList must be list or dict")

        self.fieldroot = Node("FieldRoot", parent=None)
        return

    def renderTree(self, node=None):

        if node is None:
            print("\n***************************************")
            print(f"Render Whole FieldTree\n")
            print(RenderTree(self.fieldroot, style=AsciiStyle()).by_attr())
        else:
            # 引数:Nodeインスタンスの場合
            if type(node) is Node:
                print("\n***************************************")
                print(f"Render Partial node:[{node.name}] Tree\n")
                print(RenderTree(node, style=AsciiStyle()).by_attr())

            # 引数:str(node.nameにあたる)の場合
            elif type(node) is str:
                print("\n***************************************")
                print(f"Render Partial node:[{node}] Tree\n")
                print(RenderTree(self.searchNode(node),
                                 style=AsciiStyle()).by_attr())

        print("\n***************************************")
        print()

        return

    def searchNodeInList(self, name: str) -> Node:
        # name:str　からノードを取得する
        # tree上にないNodeの取得にも使用するため
        # treeではなく、nodeListにて検索
        
        try :
            res=self.nodeList[name]
        except KeyError:
            print(f"KeyError : [{name}] doesn't exist")

        return res

    def searchNodeInTree(self, name: str) -> Node:
        # tree上にあるNodeの中から
        # 引数 name:str　に対応するノードを１つ取得する
        # 前提として、ノード名とノードインスタンスは１対１になるように注意すること(ノード名１つにつきノードは１個のみ！！)
        # tree上にない場合はNoneを返す
        # tree上への存在判定にも間接的に使える
        # 存在判定にはsearchNodeInListでNodeを取得してparentを使うことでも調べられる
        # 状況に応じて使おう(ノード総数、木の大きさ,...etc)

        res=findall(self.fieldroot, filter_=lambda node: node.name == name, maxcount=1)
        if res==():
            return None
        else:
            return res[0]



    def makeRoot(self, node: Node or str) -> None:
        if type(node) is Node:
            node.parent = self.fieldroot
            return
        elif type(node) is str:
            self.searchNodeInList(node).parent = self.fieldroot
            return

    def addChild(self, child: Node or str, parent: Node or str) -> None:
        try:
            if type(parent) != type(child):
                raise TypeError
        except TypeError:
            print(f"ParentNode's type doesn't match ChildNode's type")
            print(f"Parent type : {type(parent)}")
            print(f"Child type : {type(child)}\n")
            raise

        if type(child) is Node:
            child.parent = parent
            return
        elif type(child) is str:
            self.searchNodeInList(child).parent = self.searchNodeInList(parent)
            return

    def getPartialTreeNodes(self, node: Node or str):
        if type(node) is Node:
            # 指定したノード以下の部分木のノードを
            return [ele.name for ele in PreOrderIter(node)]
        elif type(node) is str:
            return [ele.name for ele in PreOrderIter(self.searchNodeInList(node))]

    def delPartialTree(self, node: Node or str) -> None:
        # 引数:node含むそれ以下の部分木のリンク削除
        if type(node) is Node:
            for ele in PostOrderIter(node):
                ele.parent = None
        elif type(node) is str:
            for ele in PostOrderIter(self.searchNodeInList(node)):
                ele.parent = None

    def changeParent(self, child: Node or str, parent: Node or str) -> None:
        try:
            if type(parent) != type(child):
                raise TypeError
        except TypeError:
            print(f"ParentNode's type doesn't match ChildNode's type")
            print(f"Parent type : {type(parent)}")
            print(f"Child type : {type(child)}\n")
            raise

        self.delPartialTree(child)
        self.addChild(child, parent)
        return

    def setOffset(self,node:Node or str , offset :int) ->None:
        # ノードのoffset attrを変更する
        if type(node) is str:
            node=self.searchNodeInTree(node)
            if node is None:
                print("doesn't exist")
                return
        
        node.offset=offset
    
    def getOffsetDict(self)->dict:
        # とりあえず存在するノードすべてのoffsetを(name:offset)の形で格納したdictを返す
        res=dict()
        for ele in self.nodeList.values():
            res[ele.name]=ele.offset
        
        return res
    

    def getParentDict(self)->dict:
        # とりあえず存在するノードすべての親を(name:parent)の形で格納したdictを返す
        # 親がいなければ(name:None)
        # アルゴリズム上のrootノードは(name:)
        res=dict()
        for ele in self.nodeList.values():
            if ele.parent is not None:
                res[ele.name]=ele.parent.name
            else:
                res[ele.name]=None
        
        return res
       
       


