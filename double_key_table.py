from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Initialise the Hash Table.
        """
        if sizes is not None:
            self.table_sizes = sizes
        else:
            self.table_sizes = self.TABLE_SIZES
        self.size_index = 0
        self.array:ArrayR[tuple[K1, V]] = ArrayR(self.table_sizes[self.size_index])
        self.count = 0
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES
        

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
 
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value
    
    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        outer_position = self.hash1(key1)

        for _ in range(self.table_size):
            if self.array[outer_position] is None:
                if is_insert:
                    self.array[outer_position] = (key1, LinearProbeTable(self.internal_sizes))
                    internal_table = self.array[outer_position][1]
                    internal_table.hash = lambda k: self.hash2(k, internal_table)
                    self.count +=1
                else:
                    raise KeyError(key1)
            elif self.array[outer_position][0] == key1:
                break
            else:
                outer_position = (outer_position + 1) % self.table_size
        
        inner_table = self.array[outer_position][1]
        inner_position = inner_table._linear_probe(key2, is_insert)

        return outer_position, inner_position 
    
    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if not key:
            for row in self.array:
                if row is not None:
                    yield row[0]
        else:
            for row in self.array:
                if row is not None:
                    key1, value = row 
                    if key1 == key:
                        for column in value.array:
                            if column is not None:
                                yield column[0]

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        return [i for i in self.iter_keys(key)]
    
    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        for row in self.array:
            if row is not None:
                key1, value1 = row
                if key:
                    if key1 == key:
                        if value1 is not None:
                            for column in value1.array:
                                if column is not None:
                                    yield column[1]
                else:
                    if value1 is not None:
                        for column in value1.array:
                            if column is not None:
                                yield column[1]
        # if key:
        #     for row in self.array:
        #         if row is not None:
        #             key1, value1 = row
        #             if key1 == key:
        #                 if value1 is not None:
        #                     for column in value1.array:
        #                         if column is not None:
        #                             yield column[1]
        # else:
        #     for row in self.array:
        #         if row is not None:
        #             key1, value1 = row
        #             if value1 is not None:
        #                 for column in value1.array:
        #                     if column is not None:
        #                         yield column[1]
                                
    
    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        return [i for i in self.iter_values(key)]
       
    
    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        position = self._linear_probe(key[0], key[1], False)
        return self.array[position[0]][1].array[position[1]][1]
        # bottom = top.array[position[1]]
        # return bottom[1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        position = self._linear_probe(key[0], key[1], True)
        self.array[position[0]][1][key[1]] = data
        if len(self) >= (self.table_size / 2): #load factor > 0.5
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key[0], key[1], False)
        top = position[0]
        bottom = position[1]

        #deleting bottom key
        del self.array[top][1][key[1]]
        # check if bottom table is empty
        bottom_table = self.array[top][1]

        empty = True
        for i in range(bottom_table.table_size):
            if bottom_table.array[i] is not None:
                empty = False

        if empty:
            self.count -= 1
            self.array[top] = None
            # top = (top + 1) % self.table_size
            # while self.array[top] is not None:
            #     keykey, value = self.array[top]
            #     self.array[top] = None
            #     key2, value2 = value
            #     self[keykey,key2] = value
            #     # newpos = self._linear_probe(keykey[0], keykey[1], True)
            #     # self.array[newpos] = (keykey, value)
            #     top = (top + 1) % self.table_size
                
    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.table_sizes):
            self.size_index -= 1
            return None
        
        self.array = ArrayR(self.table_sizes[self.size_index])
        self.count = 0

        #reinsert all values
        for row in old_array:
            if row is not None:
                key, value = row
                if value is not None:
                    for column in value.array:
                        if column is not None:
                            key2, value2 = column
                            #  SET ITEM
                            self[(key,key2)] = value2

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.table_sizes[self.size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        output = ""
        for sub_table in self.array:
            if sub_table is not None:
                for key, value in sub_table:
                    output += f"{key}: {value}\n"
        return output