from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Initialise the Hash Table.
        """
        """complexity : O(1)"""
        self.array: ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        """complexity: O(depth) where depth is the number of nested hash tables where the key is found"""
        position = self.hash(key) # O(1)
        if self.array[position] is None: # O(1)
            raise KeyError("Key not found") # O(1)
        else:
            collision = self.array[position] # O(1)
            if collision[0] == key: # O(1)
                return collision[1] # O(1)
            elif isinstance(self.array[position], InfiniteHashTable):
                lower_table = self.array[position]
                return lower_table[key]
        
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        """
        complexity: O(depth) where depth is the number of nested hash 
        tables where the position to place the key is found
        """
        position = self.hash(key)
        
        if self.array[position] is None:
            self.array[position] = (key, value)

        elif isinstance(self.array[position], tuple):
            collision = self.array[position]
            self.array[position] = None
            # Create a new hash table and insert the previous collision
            new_table = InfiniteHashTable()
            new_table.level = self.level + 1
            new_table[collision[0]] = collision[1]
            # Insert the new value into the new hash table
            new_table[key] = value
            self.array[position] = new_table

        else:
            self.array[position][key] = value
        self.count += 1
        
    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        """
        complexity:  
        best: O(depth) where depth is the number of nested hash
        tables where the key is found
        worst: O(depth * n) where depth is the number of nested hash tables 
        and n is the inner hash table size that the key is found
        """
        position = self.hash(key)

        if self.array[position] is None:
            raise KeyError("Key not found")
        
        elif isinstance(self.array[position], tuple):
            if self.array[position][0] != key:
                raise KeyError("Key not found")
            self.array[position] = None
            self.count -= 1
            
        elif isinstance(self.array[position], InfiniteHashTable):
            lower_table = self.array[position]
            del lower_table[key]
            self.count -= 1

            if self.array[position].count == 1:
                for i in range(len(self.array)):
                    if self.array[position].array[i] is not None:
                        self.array[position] = self.array[position].array[i]
                        break

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        return str(self.array)

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        """
        complexity: O(depth) where depth is the number of nested hash
        tables where the key is found
        """
        position = self.hash(key)
        location = [position]
        current_table = self

        while isinstance(current_table.array[position], InfiniteHashTable):
            current_table = current_table.array[position]
            position = current_table.hash(key)
            location.append(position)

        if isinstance(current_table.array[position], tuple):
            if current_table.array[position][0] == key:
                return location
            else:
                raise KeyError("Key not found")
        raise KeyError("Key not found")
    

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        """complexity: best = O(nlogn) 
                       worst = O(n^depth) where n is the number of keys in the table"""
        current = current or 0
        keys = []
        for stuffs in self.array:
            if stuffs is None:
                continue
            elif isinstance(stuffs, InfiniteHashTable):
                current +=1
                keys.extend(stuffs.sort_keys(current)) #O(1)
            else:
                keys.append(stuffs[0])
        return self.quick_sort(keys)

    # def insertion_sort(self,lst):
    #     for i in range(1, len(lst)):
    #         current = lst[i]
    #         position = i
    #         while position > 0 and lst[position-1] > current:
    #             lst[position] = lst[position-1]
    #             position -= 1
    #         lst[position] = current
    #     return lst
    
    def quick_sort(self, lst):
        if len(lst) <= 1:
            return lst
        else:
            pivot = lst[0]
            less = []
            greater = []
            for item in lst[1:]:
                if item < pivot:
                    less.append(item)
                else:
                    greater.append(item)
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

    