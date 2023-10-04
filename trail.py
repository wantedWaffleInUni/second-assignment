from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from data_structures.linked_stack import LinkedStack
from mountain_manager import MountainManager
from infinite_hash_table import InfiniteHashTable

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality, SmartWalker

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.following.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        return TrailSeries(
            mountain=mountain,
            following=Trail(self)
            )
    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        return TrailSplit(
            top=Trail(store=None),
            bottom=Trail(store=None),
            following=Trail(store=self)
        )
        
    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        return TrailSeries(
            mountain=self.mountain, 
            following=Trail(store=TrailSeries(
                    mountain=mountain,
                    following=self.following
                ))
            )        

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        return TrailSeries(
            mountain=self.mountain, 
            following=Trail(store=TrailSplit(
                top=Trail(store=None), 
                bottom=Trail(store=None), 
                following=self.following
                ))
            )
        
TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        return Trail(store=TrailSeries(
            mountain=mountain,
            following=self
        ))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        return Trail(store=TrailSplit(
            top=Trail(store=None), 
            bottom=Trail(store=None), 
            following=self
        ))
        
    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        path = LinkedStack()
        path.push(self.store)
        while path.is_empty() is False:
            pointer = path.pop()
            if isinstance(pointer, TrailSplit):
                if pointer.following.store is not None:
                    path.push(pointer.following.store)
                decision = personality.select_branch(pointer.top, pointer.bottom)
                if decision.name  == 'TOP':
                    path.push(pointer.top.store)
                elif decision.name =='BOTTOM':
                    path.push(pointer.bottom.store)
                else:
                    break
            elif isinstance(pointer, TrailSeries):
                personality.add_mountain(pointer.mountain)
                if pointer.following.store is not None:
                    path.push(pointer.following.store)        
                
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        path = LinkedStack()
        mountains = []
        path.push(self.store)
        while path.is_empty() is False:
            pointer = path.pop()
            if isinstance(pointer, TrailSplit):
                path.push(pointer.following.store)
                path.push(pointer.top.store)
                path.push(pointer.bottom.store)
            elif isinstance(pointer, TrailSeries):
                mountains.append(pointer.mountain)
                if pointer.following.store is not None:
                    path.push(pointer.following.store)
            else:
                continue
        return mountains
            
    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        """
        Find all possible paths to the target mountain.
        """
        paths = []
        paths.append(self.difficulty_maximum_aux(self.store, max_difficulty))
        return [self.difficulty_maximum_aux(self.store, max_difficulty)]
    
    def difficulty_maximum_aux(self, current_point, max_difficulty):
        
        return self.finding_a_way(self.store, [], LinkedStack(), max_difficulty)
        
    def finding_a_way(self, node, current_mountains, current_path: LinkedStack, max_difficulty: int) -> list[Mountain]:
        current_path.push(node)
        while current_path.is_empty() is False:
            node = current_path.pop()
            if isinstance(node, TrailSeries):
                if node.mountain.difficulty_level <= max_difficulty:
                    current_path.push(node.mountain)
                    current_mountains.append(node.mountain)
                else:
                    return []
                if node.mountain.name == 'final':
                    current_mountains.append(node.mountain)
                if node.following.store is not None:
                    current_path.push(node.following.store)
                    current_mountains.append(self.finding_a_way(node.following.store, current_mountains, current_path, max_difficulty))
            elif isinstance(node, TrailSplit):
                if node.following.store is not None:
                    current_path.push(node.following.store)
                if node.top.store is not None:
                    current_path.push(node.top.store)
                    current_mountains.append(self.finding_a_way(node.top.store, current_mountains, current_path, max_difficulty))
                if node.bottom.store is not None:
                    current_path.push(node.bottom.store)
                    current_mountains.append(self.finding_a_way(node.bottom.store, current_mountains, current_path, max_difficulty))
            else:
                return current_path
                 

        # current_path.push(node)
        # mountains = []
        # while current_path.is_empty() is False:
        #     pointer = current_path.pop()
        #     if isinstance(pointer, TrailSplit):
        #         if pointer.following.store is not None:
        #             current_path.push(pointer.following.store)
        #         if pointer.top.store is not None:
        #             current_path.push(pointer.top.store)
        #             current_mountains.append(self.finding_a_way(pointer.top.store, current_mountains, current_path, max_difficulty))
        #         if pointer.bottom.store is not None:
        #             current_path.push(pointer.bottom.store)
        #             current_mountains.append(self.finding_a_way(pointer.bottom.store, current_mountains, current_path, max_difficulty))
        #     elif isinstance(pointer, TrailSeries):
        #         if pointer.mountain.difficulty_level <= max_difficulty:
        #             mountains.append(pointer.mountain)
        #         elif pointer.mountain.difficulty_level > max_difficulty:
        #             return
        #         else:
        #             continue
        #         if pointer.following.store is not None:
        #             current_path.push(pointer.following.store)
        # print(current_mountains)
        # return mountains


        # def dfs_traverse(node):
        #     if node is not None:
        #         if isinstance(node, TrailSeries):
        #             if node.mountain.difficulty_level <= max_difficulty:
        #                 current_path.append(node.mountain)
        #             else:
        #                 paths.append(current_path.copy())

        #             if node.mountain.name == 'final':

        #                 paths.append(current_path.copy())

        #             dfs_traverse(node.following.store)

        #             # current_path.pop()
                    
        #         elif isinstance(node, TrailSplit):
        #             dfs_traverse(node.top.store)
        #             dfs_traverse(node.bottom.store)
        #             dfs_traverse(node.following.store)
        #     else:
        #         return
            
    
        # def mountain_hash(self, diff_level: int, table: InfiniteHashTable) -> int:
        #     """
        #     Hash function for the mountain infinite hash table.
        #     """
        #     return diff_level % table.TABLE_SIZE
    
        # def path_finder(self) -> list[Mountain]:
        #     path = InfiniteHashTable()
        #     path.hash = lambda k: self.mountain_hash(k, path)
        #     path[0] = [self.store.mountain]
        #     for i in range(1, max_difficulty+1):
        #         path[i] = []
            
        # pass

        # def find_path(self, personality: WalkerPersonality) -> None:
        #     path = LinkedStack()
        #     path.push(self.store)
        #     while path.is_empty() is False:
        #         pointer = path.pop()
        #         if isinstance(pointer, TrailSplit):
        #             if pointer.following.store is not None:
        #                 path.push(pointer.following.store)
        #             decision = personality.select_branch(pointer.top, pointer.bottom)
        #             if decision.name  == 'TOP':
        #                 path.push(pointer.top.store)
        #             elif decision.name =='BOTTOM':
        #                 path.push(pointer.bottom.store)
        #             else:
        #                 break
        #         elif isinstance(pointer, TrailSeries):
        #             personality.add_mountain(pointer.mountain)
        #             if pointer.following.store is not None:
        #                 path.push(pointer.following.store)  
        
         
        # manager = MountainManager()
        # manager.mountains = self.collect_all_mountains()
        # for i in manager.mountains:
        #     print(i)
        # print(manager.group_by_difficulty())
        
        # valid_paths = []
        # stack = [(self.mountain, [], 0)]

        # while stack:
        #     current_mountain, current_path, current_difficulty = stack.pop()

        #     if current_difficulty > max_difficulty:
        #         continue

        #     current_path.append(current_mountain)
        #     current_difficulty += current_mountain.difficulty_level

        #     if current_mountain == self.mountain:
        #         if current_difficulty <= max_difficulty:
        #             valid_paths.append(current_path.copy())
        #     else:
        #         for neighbor in current_mountain.neighbors:
        #             stack.append((neighbor, current_path.copy(), current_difficulty))

        # return valid_paths
        

        # def dfs(current, current_path, current_difficulty):
        #     if current_difficulty > max_difficulty:
        #         return
        #     if isinstance(current, TrailSplit):
        #         current_path.push(current.following.store)
        #         current_path.push(current.top.store)
        #         current_path.push(current.bottom.store)
        #     elif isinstance(current, TrailSeries):

        #         if current.following.store is not None:
        #             current_path.push(current.following.store)


        #     current_path.push(current_mountain)
        #     current_difficulty += current_mountain.difficulty_level

        #     if current_mountain == self.store.mountain:
        #         if current_difficulty <= max_difficulty:
        #             valid_paths.append(current_path.copy())
        #     else:
        #         for neighbor in current_mountain:
        #             dfs(neighbor, current_path, current_difficulty)

        #     current_path.pop()  # Backtrack
        #     valid_paths = []
        #     dfs(self.store, [], 0)
        #     return valid_paths  

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()



