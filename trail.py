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
        """best case = O(n) worst case = O(n)  where n is the number of branch""" # need to check this
        path = LinkedStack()
        path.push(self.store) # O(1)
        while path.is_empty() is False: # O(n)
            pointer = path.pop() # O(1)
            if isinstance(pointer, TrailSplit): # O(1)
                if pointer.following.store is not None: # O(1)
                    path.push(pointer.following.store) # O(1)
                decision = personality.select_branch(pointer.top, pointer.bottom) # O(1)
                if decision.name  == 'TOP': # O(1)
                    path.push(pointer.top.store) # O(1)
                elif decision.name =='BOTTOM': # O(1)
                    path.push(pointer.bottom.store) # O(1)
                else:
                    break
            elif isinstance(pointer, TrailSeries): # O(1)
                personality.add_mountain(pointer.mountain) # O(1)
                if pointer.following.store is not None: # O(1)
                    path.push(pointer.following.store) # O(1)
                
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

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[
        list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        """
        Find all possible paths to the target mountain.
        """
        current_node = self.store
        collection = []
        path = LinkedStack()
        self.finding_a_way(current_node, collection, [], path, max_difficulty)
        output = []
        for i in collection:
            add = False
            for j in i:
                if j.name == 'final':
                    add = True
            if add:
                output.append(i)
        return output

    def finding_a_way(self, current_node: Trail, total_mountains: list, current_mountains: list,
                      current_path: LinkedStack, max_difficulty: int) -> None:
        current_path.push(current_node)
        while current_path.is_empty() is False:
            current_node = current_path.pop()

            if isinstance(current_node, TrailSplit):
                current_path.push(current_node.following.store)

                top_path = LinkedStack()
                bottom_path = LinkedStack()
                for i in range(len(current_path)):
                    item = current_path.pop()
                    top_path.push(item)
                    bottom_path.push(item)

                passing_on = current_mountains.copy()
                passing_on2 = current_mountains.copy()

                self.finding_a_way(current_node.top.store, total_mountains, passing_on, top_path, max_difficulty)
                self.finding_a_way(current_node.bottom.store, total_mountains, passing_on2, bottom_path, max_difficulty)

            elif isinstance(current_node, TrailSeries):
                if current_node.mountain.difficulty_level > max_difficulty:
                    return
                else:
                    current_mountains.append(current_node.mountain)
                current_path.push(current_node.following.store)
            else:
                continue
        total_mountains.append(current_mountains) if current_mountains else None

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()



