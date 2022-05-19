"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
import time
import random
import sys

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_dataata = probe.data
                probe.data = new_item
                return old_dataata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            left = height1(top.left) if top.left is not None else -1
            right = height1(top.right) if top.right is not None else -1
            return max(left, right) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        print(len(list(self.inorder()))+1)
        print(2*math.log2(len(list(self.inorder()))+1))
        return self.height() < (2*math.log2(len(list(self.inorder())) + 1)) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        for i in range(len(lst)):
            element = lst[i]
            if element == low:
                low_pos = i
            if element == high:
                high_pos = i

        return lst[low_pos:][:high_pos-low_pos+1]


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        lst = list(self.inorder())

        def put_elements(lst):
            if len(lst) == 0:
                return None
            i = len(lst) // 2
            node = BSTNode(lst[i])
            if len(lst) > 1:
                node.left = put_elements(lst[:i])
                node.right = put_elements(lst[i + 1:])
            return node
        self._root = put_elements(lst)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self.inorder()
        for i in lst:
            if i > item:
                return i

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = list(self.inorder())[::-1]
        for i in lst:
            if i < item:
                return i

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def read_file(path_to_file):
            with open(path_to_file, 'r') as file:
                lines = file.readlines()
            res = []
            for line in lines:
                res.append(line.strip())
            return res

        def find_in_list(elements_to_find, lst):
            for element in elements_to_find:
                for word in lst:
                    if word == element:
                        break

        def find_in_tree(elements_to_find, tree):
            for element in elements_to_find:
                tree.find(element)
        print("Testing the efficiency of binary search tree for the search tasks...")
        print()
        # using list
        words = read_file(path)[:10000]
        rand_words = words.copy()
        random.shuffle(rand_words)
        rand_words_cropped = rand_words
        start_time = time.time()
        find_in_list(rand_words_cropped, words)
        list_time = time.time() - start_time
        print("Finding 1000 elements using built-in list:")
        print("--- %s seconds ---" % list_time)
        print()

        # using binary tree with words in alphabetic order
        words_bst = LinkedBST()
        for word in words:
            words_bst.add(word)

        start_time = time.time()
        find_in_tree(rand_words_cropped, words_bst)
        alphabetic_tree_time = time.time() - start_time
        print("Finding 1000 elements using binary tree with words in alphabetic order:")
        print("--- %s seconds ---" % alphabetic_tree_time)
        print()

        # using binary tree with words in random order
        words_bst = LinkedBST()
        random.shuffle(rand_words)
        for word in rand_words:
            words_bst.add(word)

        start_time = time.time()
        find_in_tree(rand_words_cropped, words_bst)
        random_tree_time = time.time() - start_time
        print("Finding 1000 elements using binary tree with words in random order:")
        print("--- %s seconds ---" % random_tree_time)
        print()

        # using rebalanced binary tree
        words_bst.rebalance()

        start_time = time.time()
        find_in_tree(rand_words_cropped, words_bst)
        rebalanced_tree_time = time.time() - start_time
        print("Finding 1000 elements using rebalanced binary tree :")
        print("--- %s seconds ---" % rebalanced_tree_time)
        print()
        return list_time, alphabetic_tree_time, random_tree_time, rebalanced_tree_time


if __name__ == "__main__":
    bst = LinkedBST()
    sys.setrecursionlimit(10000)

    def find_average(iterations):
        """Helping function for finding average time"""
        res = [0 for _ in range(4)]
        for _ in range(iterations):
            cur_res = bst.demo_bst("words.txt")
            for i in range(4):
                res[i] += cur_res[i]
        print("Average time for each method")
        for i in range(4):
            print(res[i]/iterations)

    find_average(1)

