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
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array:ArrayR[tuple[K1, V]] = ArrayR(self.TABLE_SIZES[self.size_index])
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
                    table = self.array[outer_position][1]
                    table.hash = lambda k: self.hash2(k, table)
                else:
                    raise KeyError(key1)
            elif self.array[outer_position][0] == key1:
                break
            else:
                outer_position = (outer_position + 1) % self.table_size
        
        inner_table = self.array[outer_position][1]
        inner_table.hash = lambda k: self.hash2(k, inner_table)
        inner_position = inner_table._linear_probe(key2, is_insert)

        return outer_position, inner_position

        # for _ in range(inner_table.table_size):
        #     if inner_table.array[inner_position] is None:
        #         if is_insert:
        #             break
        #         else:
        #             raise KeyError(key1)
        #     elif self.array[outer_position][0] == key1:
        #         break
        #     else:
        #         inner_position = (inner_position + 1) % inner_table.table_size

        # if inner_table.array[inner_position] != key2:
        #     raise FullError("Table is full!")
    
        
    

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        class KeyIterator:
            def __iter__(self):
                return self
            def __next__(self):
                if key is None:
                    for sub_table in self.array:
                        if sub_table is not None:
                            for key, value in sub_table:
                                yield key
                elif key in self:
                    for key, value in self.array[self.hash1(key)]:
                        yield key
                else:
                    raise StopIteration
        return KeyIterator()

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        output = []
        if key is not None:
            for sub_table in self.array:
                if sub_table is not None:
                    for key, value in sub_table:
                        output.append(key)
        else:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    output.append(self.array[i][0])
        return output
    
    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        class ValueIterator:
            def __iter__(self):
                return self
            def __next__(self):
                if key is None:
                    for sub_table in self.array:
                        if sub_table is not None:
                            for key, value in sub_table:
                                yield value
                elif key in self:
                    for key, value in self.array[self.hash1(key)]:
                        yield value
                else:
                    raise StopIteration
        return ValueIterator()
    
    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        output = []
        if key is not None:
            position = self.hash1(key)
            sub_table = self.array[position]
            if sub_table is not None:
                for k2, v in sub_table:
                    output.append(v)
        else:
            for i in range(self.table_size):
                sub_table = self.array[i]
                if sub_table is not None:
                    for k2, v in sub_table:
                        output.append(v)
        return output
    
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
        top = self.array[position[0]][1]
        bottom = top.array[position[1]]
        return bottom[1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        position = self._linear_probe(key[0], key[1], True)
        top = position[0]
        bottom = position[1]

        if self.array[top] is None:
            self.array[top] =(key[0], LinearProbeTable(self.internal_sizes))
            self.array[top][1].hash = lambda k: self.hash2(k, self.array[top][1])

        if self.array[top][1].array[bottom] is None:
            self.count += 1

        self.array[top][1].array[bottom] = (key[1], data)

        if len(self) > (self.table_size / 2) + 1:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key[0], key[1], False)
        top = position[0]
        bottom = position[1]

        self.array[top][1].array[bottom] = None

        self.count -= 1
        
        bottom = (bottom + 1) % self.internal_sizes[self.size_index]

        while self.array[top][1].array[bottom] is not None:

            keykey, value = self.array[top][1].array[bottom]
            self.array[top][1].array[bottom] = None

            newpos = self._linear_probe(keykey, value, True)
            self.array[newpos[0]][1].array[newpos[1]] = (keykey, value)

            bottom = (bottom + 1) % self.internal_sizes[self.size_index]
            
    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            return 
        
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        for sub_table in old_array:
            if sub_table is not None:
                self[sub_table[0]] = sub_table[1]



    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.TABLE_SIZES[self.size_index]

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