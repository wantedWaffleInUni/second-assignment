from __future__ import annotations

from mountain import Mountain
 
class MountainOrganiser:

    def __init__(self) -> None:
        #initialisation
        self.mountains = []
        
    def cur_position(self, mountain: Mountain) -> int:
        """complexity : best = O(1), when middle index contains item.
                        worst = O(log(N)), where N is the length of l.
        """
        #Finds the rank of the provided mountain given all mountains included so far.
        try:
            return self.mountains.index(mountain) # O(1)
        except ValueError:
            raise KeyError("Mountain not found") # O(1)

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """complexity : best =  O((log n) n * Comp) = O(n log n * Comp)
                        worst = O((n+n) * n * Comp) = O(n^2 * Comp) where Comp is the complexity of the comparison operator
                        n = len(lst)"""
        # Adds a list of mountains to the organiser
        self.mountains.extend(mountains) # O(1)
        self.mountain_quick_sort(self.mountains) # O(n)

    def mountain_quick_sort(self, lst):
        """complexity : best = O((log n) n * Comp) = O(n log n * Comp)
                        worst = O((n+n) * n * Comp) = O(n^2 * Comp) where Comp is the complexity of the comparison operator
                        n = len(lst)"""
        start = 0
        end =  len(lst) - 1
        self.sort_auxiliary(lst, start, end) # O(n)

    def sort_auxiliary(self, lst, start, end):
        """complexity : best = O((log n) * n * Comp) = O(n log n * Comp)
                        worst = O((n+n) * n * Comp) = O(n^2 * Comp) where Comp is the complexity of the comparison operator
                        n = len(lst)"""
        if start < end:
            boundary = self.partition(lst, start, end) # O(n)
            self.sort_auxiliary(lst, start, boundary-1) # O(n)
            self.sort_auxiliary(lst, boundary+1, end) # O(n)
        
    def partition(self, lst, start, end):
        """complexity: O(n*Comp), n = len(lst), Comp is the complexity of the comparison operator"""
        mid = (start + end) // 2 # O(1)
        pivot = lst[mid] # O(1)
        lst[start], lst[mid] = lst[mid], lst[start]
        boundary = start  
        for i in range(start+1, end+1): # O(n), n = len(lst)
            if lst[i].difficulty_level < pivot.difficulty_level: # O(Comp) where Comp is the complexity of the comparison operator
                boundary += 1 # O(1)
                lst[i], lst[boundary] = lst[boundary], lst[i] # O(1)
            elif lst[i].difficulty_level == pivot.difficulty_level: # O(Comp)
                if lst[i].name < pivot.name: # O(Comp)
                    boundary += 1 # O(1)
                    lst[i], lst[boundary] = lst[boundary], lst[i] # O(1)
        lst[start], lst[boundary] = lst[boundary], lst[start] # O(1)
        return boundary # O(1)
    
    # def quicksort_modified(self, lst):
    #     random.seed()
    #     start = 0
    #     end = len(lst)-1
    #     self.aux(lst, start, end)

    # def aux(self, lst, start, end):
    #     if start < end:
    #         pivot = self.select(lst,start,end)
    #         boundary = self.partition2(lst,start,end,pivot)
    #         self.aux(lst[:boundary],start,boundary-1)
    #         self.aux(lst[boundary:],boundary+1,end)

    # def select(self, lst, start, end):
    #     index = start - end + 1

    #     # counting the frequency of each element
    #     appear = [0] * index
    #     for i in range(index):
    #         appear[i] = lst[start + i:end + 1].count(lst[start + i])

    #     # finding the element that appears at least n/2 times
    #     pivot = None
    #     for i in range(index):
    #         if appear[i] >= (index + 1) // 2:
    #             pivot = start + i
    #             break

    #     if pivot is None:
    #         pivot = end
    #     return pivot
    
    # def partition2(self, lst, start, end, pivot= None):
    #     if pivot is None:
    #         pivot = random.randrange(start, end+1)
    #     else:
    #         assert start <= pivot <= end
    #     lst[start], lst[pivot] = lst[pivot], lst[start]

    #     pivot = start
        
    #     for i in range(start+1, end+1):
    #         if lst[i].difficulty_level < lst[start].difficulty_level:
    #             pivot += 1
    #             lst[i], lst[pivot] = lst[pivot], lst[i]
    #         elif lst[i].difficulty_level == lst[start].difficulty_level:
    #             if lst[i] > lst[pivot]:
    #                 lst[i], lst[pivot] = lst[pivot], lst[i]
    #     lst[start], lst[pivot] = lst[pivot], lst[start]
    #     return pivot
    
    # def quick_sort(self, lst):
    #     if len(lst) <= 1:
    #         return lst
    #     else:
    #         pivot = lst[len(lst)//2]
    #         less = []
    #         greater = []
    #         for item in lst[1:]:
    #             if item.difficulty_level < pivot.difficulty_level:
    #                 less.append(item)
    #             else:
    #                 greater.append(item)
    #         return self.quick_sort(less) + [pivot] + self.quick_sort(greater)
        
    

    # def insertion_sort(self,lst):
    #     for i in range(1, len(lst)):
    #         current = lst[i]
    #         position = i
    #         while position > 0 and lst[position-1].difficulty_level > current.difficulty_level:
    #             lst[position] = lst[position-1]
    #             position -= 1
    #         lst[position] = current
    #     return lst

        
    # def merge_sort(self, lst):
    #     if len(lst) <= 1:
    #         return lst
    #     else:
    #         mid = len(lst)//2
    #         left = self.merge_sort(lst[:mid])
    #         right = self.merge_sort(lst[mid:])
    #         return self.merge(left, right)
        
    # def merge(self, left, right):
    #     result = []
    #     i = j = 0
    #     while i < len(left) and j < len(right):
    #         if left[i].difficulty_level < right[j].difficulty_level:
    #             result.append(left[i])
    #             i += 1
    #         elif left[i].difficulty_level == right[j].difficulty_level:
    #             if left[i].name < right[j].name:
    #                 result.append(left[i])
    #                 i += 1
    #         else:
    #             result.append(right[j])
    #             j += 1
    #     result += left[i:]
    #     result += right[j:]
    #     return result
    


    