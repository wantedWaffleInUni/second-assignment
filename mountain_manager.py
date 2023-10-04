from __future__ import annotations
from mountain import Mountain
from infinite_hash_table import InfiniteHashTable

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        if mountain in self.mountains:
            self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        if old in self.mountains:
            self.remove_mountain(old)
            self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        matching_mountains = [mountain for mountain in self.mountains if mountain.difficulty_level == diff]
        return matching_mountains
    
    def mountain_hash(self, diff_level: int, table: InfiniteHashTable) -> int:
        """
        Hash function for the mountain infinite hash table.
        """
        return diff_level % table.TABLE_SIZE
    
    def group_by_difficulty(self) -> list[list[Mountain]]:
        grouped_mountains = InfiniteHashTable()
        grouped_mountains.hash = lambda k: self.mountain_hash(k, grouped_mountains)

        for mountain in self.mountains:
            if mountain.difficulty_level in grouped_mountains:
                grouped_mountains[mountain.difficulty_level].append(mountain)
            else:
                grouped_mountains[mountain.difficulty_level] = [mountain]
        sorted_groups = grouped_mountains.sort_keys()
        return [grouped_mountains[group] for group in sorted_groups]

        
