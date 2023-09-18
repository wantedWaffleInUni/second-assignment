from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from data_structures.linked_stack import LinkedStack

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

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
        return TrailSeries(
            mountain=self.following.store.mountain,
            following=Trail(store=None)
        )

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

        return self.following
    
        # TrailSeries(
        #     mountain=self.following.store.mountain,
        #     following=self.following.store.following
        # )

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
        from personality import PersonalityDecision

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
        raise NotImplementedError()

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        raise NotImplementedError()

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
