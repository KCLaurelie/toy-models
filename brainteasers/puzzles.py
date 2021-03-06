# https://www.educative.io/blog/crack-amazon-coding-interview-questions#overview
import random
import timeit
import collections
import math
from collections import Counter
from collections import defaultdict
from itertools import groupby



#region Largest Rectangle
# https://www.hackerrank.com/challenges/largest-rectangle/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=stacks-queues
# https://www.geeksforgeeks.org/largest-rectangle-under-histogram/
# Runtime: O(n)

def getMaxArea(arr):
    s = [-1]
    n = len(arr)
    area = 0
    i = 0
    left_smaller = [-1] * n
    right_smaller = [n] * n
    while i < n:
        while s and (s[-1] != -1) and (arr[s[-1]] > arr[i]):
            right_smaller[s[-1]] = i
            s.pop()
        if ((i > 0) and (arr[i] == arr[i - 1])):
            left_smaller[i] = left_smaller[i - 1]
        else:
            left_smaller[i] = s[-1]
        s.append(i)
        i += 1
    for j in range(0, n):
        area = max(area, arr[j] * (right_smaller[j] - left_smaller[j] - 1))
    return area


hist = [6, 2, 5, 4, 5, 1, 6]
print("maxArea = ", getMaxArea(hist))
#endregion

#region 9. Coin change problem (dynamic programming solution)
"""
You are given coins of different denominations and a total amount of money. 
Write a function to compute the number of combinations that make up that amount. 
You may assume that you have an infinite number of each kind of coin.

Input:
  - Amount: 5
  - Coins: [1, 2, 5]
Output: 4
Explanation: There are 4 ways to make up the amount:
  - 5 = 5
  - 5 = 2 + 2 + 1
  - 5 = 2 + 1 + 1 + 1
  - 5 = 1 + 1 + 1 + 1 + 1

https://www.geeksforgeeks.org/coin-change-dp-7/
  
Runtime Complexity: Quadratic, O(m*n), m=number of coins, m=amount
Memory Complexity: Linear, O(n)O(n)
"""

class Solution9(object):
    def change(self, amount, coins):
        solution = [0]*(amount+1)
        solution[0] = 1 # base case (given value is 0)
        for coin in coins: #pick all coins one by one
            for i in range(coin, amount+1):
                solution[i] += solution[i-coin]
        return solution

Solution9().change(amount=5,coins=[1,2,5])

class Solution9b(object):
    def make_change(self, goal, coins):
        wallets = [[coin] for coin in coins]
        new_wallets = []
        collected = []

        while wallets:
            for wallet in wallets:
                s = sum(wallet)
                for coin in coins:
                    if coin >= wallet[-1]:
                        if s + coin < goal:
                            new_wallets.append(wallet + [coin])
                        elif s + coin == goal:
                            collected.append(wallet + [coin])
            wallets = new_wallets
            new_wallets = []
        return collected
Solution9b().make_change(goal=5,coins=[1,2,5])

#endregion

#region 12. Print balanced brace combinations TODO
"""
Input: n=1
Output: {}
This the only sequence of balanced 
parenthesis formed using 1 pair of balanced parenthesis. 

Input : n=2
Output: 
{}{}
{{}}

Runtime Complexity: Exponential, 2^n2
Memory Complexity: Linear, O(n)
"""
class Solution12(object):
    def print_all_braces(self, n, left_count=0, right_count=0, output=[], result=[]):
        if left_count >= n and right_count >= n:
            result.append(output.copy());

        if left_count < n:
            output += '{'
            self.print_all_braces(n, left_count + 1, right_count, output, result)
            output.pop()

        if right_count < left_count:
            output += '}'
            self.print_all_braces(n, left_count, right_count + 1, output, result)
            output.pop()
        return result
Solution12().print_all_braces(2,0,0,[],[])
#endregion

#region 36. egg dropping puzzle for dynamic programming [**TO REVISE**]
"""
https://www.geeksforgeeks.org/egg-dropping-puzzle-dp-11/
"""
# METHOD1 brut force recursion
# Runtime complexity: O(2^k) (many subproblems solved repeatedly)
# Memory Complexity: O(1)
class Solution36(object):
    def egg_drops(self, n_eggs, n_floors):
        if n_floors <= 1 or n_eggs <= 1: return n_floors # base case
        min = 9223372036854775807
        for floor in range(1, n_floors+1):
            res = max(self.egg_drops(n_eggs-1, floor-1),
                      self.egg_drops(n_eggs, n_floors-floor))
            if res < min: min = res
        return min+1


# METHOD2 recursion + memoization
# Runtime complexity: O(n*k^2)
# Memory Complexity: O(n*k)
class Solution36b(object):
    def egg_drops_rec(self, n_eggs, n_floors, memo):
        if memo[n_eggs][n_floors] != -1: return memo[n_eggs][n_floors]
        if n_floors <= 1 or n_eggs <= 1: return n_floors

        # recursion
        min = 9223372036854775807
        for floor in range(1, n_floors+1):
            res = max(self.egg_drops_rec(n_eggs-1, floor-1, memo),
                      self.egg_drops_rec(n_eggs, n_floors-floor, memo))
            if res < min: min = res
        memo[n_eggs][n_floors] = min + 1
        return min+1

    def egg_drops(self, n_eggs, n_floors):
        memo = [[-1 for x in range(n_floors + 1)] for x in range(n_eggs + 1)]
        return self.egg_drops_rec(n_eggs, n_floors, memo)


# METHOD3 dynamic programming
# Runtime complexity: O(n*k^2)
# Memory Complexity: O(n*k)
class Solution36c(object):
    def egg_drops(self, n_eggs, n_floors, min = 32767):
        memo = [[0 for x in range(n_floors + 1)] for x in range(n_eggs + 1)]

        for egg in range(1, n_eggs+1): # for 1 floor, 1 trial is needed, for 0 floors, 0 trial needed
            memo[egg][1] = 1
            memo[egg][0] = 0
        for floor in range(1, n_floors+1): # for 1 egg, we need n_floors trials
            memo[1][floor] = floor
        # recursion

        for egg in range(2, n_eggs+1):
            for floor in range(2, n_floors+1):
                memo[egg][floor] = min
                for floor_int in range(1, floor):
                    res = 1 + max(memo[egg-1][floor_int-1], memo[egg][floor-floor_int])
                    if res < memo[egg][floor]: memo[egg][floor] = res

        return memo[egg][floor]


Solution36().egg_drops(n_eggs=2, n_floors=10)
Solution36b().egg_drops(n_eggs=2, n_floors=10)

#endregion

#region 39. knapsack problem [**TO REVISE**]
"""
https://www.educative.io/blog/0-1-knapsack-problem-dynamic-solution
https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
to trace elements: https://codereview.stackexchange.com/questions/125374/solution-to-the-0-1-knapsack-in-python
"""


# METHOD1: using recursion (slow)
# Runtime complexity: O(2^n), due to the number of calls with overlapping subcalls
# Memory Complexity: Constant, O(1)
class Solution39(object):
    def knapsack_rec(self, profits, weights, capacity, curr_item):
        # stop condition
        if curr_item >= len(profits) or capacity <= 0:
            return 0
        weight_curr_item = weights[curr_item]
        if weight_curr_item > capacity: # if weight of nth item bigger than the capacity then we exclude it
            return self.knapsack_rec(profits, weights, capacity, curr_item+1)
        else: # take the best solution between including curr_item or not
            profit_with_curr_item = profits[curr_item] \
                                    + self.knapsack_rec(profits, weights, capacity - weight_curr_item, curr_item + 1)

            profit_wo_curr_item = self.knapsack_rec(profits, weights, capacity, curr_item + 1)
            return max(profit_wo_curr_item, profit_with_curr_item)

    def solve_knapsack(self, profits, weights, capacity):
        return self.knapsack_rec(profits, weights, capacity, curr_item=0)


# METHOD2: using dynamic programming
# Runtime complexity: O(n*capacity)
# Memory Complexity: Constant, O(n*capacity)
class Solution39b(object):
    def solve_knapsack(self, profits, weights, capacity):
        nb_items = len(profits)
        states = [[0 for i in range(capacity + 1)] for j in range(nb_items + 1)]
        # build states table in bottle up manner
        for item in range(nb_items+1):
            for curr_C in range(capacity+1):
                if item <= 0 or curr_C <= 0: states[item][curr_C] = 0
                elif weights[item-1] <= curr_C:
                    profit_with_new_item = profits[item - 1] + states[item - 1][curr_C - weights[item - 1]]
                    if profit_with_new_item > states[item-1][curr_C]:
                        print('item picked', item -1, profits[item-1], weights[item-1])
                        states[item][curr_C] = profit_with_new_item
                    else: states[item][curr_C] = states[item-1][curr_C]
                else: states[item][curr_C] = states[item-1][curr_C]
        print('final state:', states)
        return states[nb_items][curr_C]


# METHOD3: using recursion + memoization technique to remove redundant states
# # uses 2D arrays to store particular states (nb_irems, weights) to avoid computing redundant states
# Runtime complexity: O(n*capacity)
# Memory Complexity: Constant, O(n*capacity)
class Solution39c(object):
    def knapsack_rec(self, profits, weights, capacity, curr_item, states):
        if curr_item <= 0 or capacity <= 0:
            return 0
        if states[curr_item][capacity] != -1:
            pass
        if weights[curr_item-1] <= capacity:
            states[curr_item][capacity] = max(
                profits[curr_item-1] + self.knapsack_rec(profits, weights, capacity-weights[curr_item-1], curr_item-1, states),
                self.knapsack_rec(profits, weights, capacity, curr_item - 1, states))
        else:
            states[curr_item][capacity] = self.knapsack_rec(profits, weights, capacity, curr_item - 1, states)

        print(states)
        return states[curr_item][capacity]

    def solve_knapsack(self, profits, weights, capacity):
        nb_items = len(profits)
        # We initialize the matrix with -1 at first.
        states_init = [[-1 for i in range(capacity + 1)] for j in range(nb_items + 1)]
        return self.knapsack_rec(profits, weights, capacity, curr_item=nb_items, states=states_init)


profits, weights, capacity = [[60, 100, 20], [1, 2, 3], 5]
Solution39().solve_knapsack(profits, weights, capacity)
Solution39b().solve_knapsack(profits, weights, capacity)
Solution39c().solve_knapsack(profits, weights, capacity)



#endregion

#region 42. Print nth number in the Fibonacci series
"""
https://www.geeksforgeeks.org/python-program-for-n-th-fibonacci-number/
F(n) = F(n-1) + F(n-2)
F(0) = 0
F(1) = 1
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
"""

# METHOD1: recursion
# Runtime complexity: O(2^n)
# Memory complexity: O(1)
class Solution42(object):
    def fibonacci(self, n):
        if n< 0:
            pass
        elif n <= 2:
            return n-1
        else:
            return self.fibonacci(n-1) + self.fibonacci(n-2)

# METHOD2: recursion with memoization
# Runtime complexity:
# Memory complexity: O(n)
class Solution42b(object):
    def fibonacci(self, n, FibSequence=[0,1]):
        if n< 0:
            pass
        elif n <= len(FibSequence):
            return FibSequence[n-1]
        else:
            newFibNb = self.fibonacci(n-1, FibSequence) + self.fibonacci(n-2, FibSequence)
            FibSequence.append(newFibNb)
            return newFibNb

#METHOD3: dynamic programming
# Runtime complexity: O(n)
# Memory complexity: O(1)
class Solution42c(object):
    def fibonacci(self, n):
        fib0 = 0
        fib1 = 1
        if n < 0:
            pass
        elif n <= 2:
            return n-1
        else:
            for i in range(2, n):
                fibnew = fib0 + fib1
                fib0 = fib1
                fib1 = fibnew
            return fibnew

Solution42().fibonacci(9)
Solution42b().fibonacci(9)
Solution42c().fibonacci(9)

#endregion

#region FizzBuzz
def fizz_buzz(num):
    string = ''
    if num % 3 == 0: string +='Fizz'
    if num % 5 == 0: string +='Buzz'
    return string if string else num


if __name__ == "__main__":
    for n in range(1, 5):
        print(fizz_buzz(n))

def fizzBuzz(n):
    # Write your code here
    for i in range(1, n+1):
        print("Fizz"*(i%3==0) + "Buzz"*(i%5==0) or i)

if __name__ == '__main__':
    n = int(input().strip())

    fizzBuzz(n)
#endregion

#region bribes in queue - NY Chaos
def minimumBribes(q):
    orig_queue=list(range(1,len(q)+1))
    diff = [o_i - i for o_i, i in zip(orig_queue, q)]
    #print(diff)
    if max(diff) <=-2:
        print('Too chaotic')
    else:
        print(-(sum(x for x in diff if x < 0)))

# optimized
def minimumBribesb(q):
    # Write your code here
    bribes = 0
    for i in range(len(q)-1,-1,-1):
        if q[i] - (i + 1) > 2:
            print('Too chaotic')
            return
        for j in range(max(0, q[i] - 2),i):
            if q[j] > q[i]:
                bribes += 1
    print(bribes)

q = [1,2,3,5,4,6,7,8]
q = [4,1,2,3,5,6,7,8]
q = [2, 1, 5, 3, 4]

#endregion

#region Ransom pb (find if string could have been written using another string)
note = 'hello i am zelda'.split()
magazine = 'hello my name is zelda and i am cool and awesome'.split()

def checkMagazine0(magazine, note):
    for word in note:
        if word not in magazine:
            print('No')
            return
        else:
            magazine.remove(word)
    print('Yes')

# faster
def checkMagazine(magazine, note):
    if Counter(note) - Counter(magazine) == {}:
        print('Yes')
    else:
        print('No')

checkMagazine(magazine, note)
#endregion

#region Parse queries

def freqQuery(queries):
    res = []
    cnt = dict()
    freq = defaultdict(int)

    for x in queries:
        ops, value = x
        initial = cnt.get(value, 0)

        if ops == 3:
                res.append(1 if freq.get(value) else 0)
        elif ops == 1: # insert the element
              freq[initial] -= 1
              cnt[value] = initial + 1
              freq[cnt.get(value,0)] += 1
        else: # remove 1 occurence of the element if exists
                freq[initial] -= 1
                if initial: cnt[value] -= 1
                freq[cnt.get(value,0)] += 1
        print('cnt', cnt, 'freq', freq)
    return res
queries=[[1,1],[2,2],[3,2],[1,1],[1,1],[2,1],[3,2]]
#endregion

#region Fraud detection

# SUPER SLOW
def med(expenditure, d):
    lastd = sorted(expenditure[:d])
    return lastd[d//2] if d % 2 == 1 else ((lastd[d//2] + lastd[d//2-1])/2)

def activityNotifications(expenditure, d):
    # Write your code here
    notif = 0
    for i in range(d, len(expenditure)-1):
        if expenditure[i] >= 2*med(expenditure, i):
            notif += 1
    return notif
res = activityNotifications(expenditure=[2, 3, 4, 2, 3 ,6 ,8 ,4, 5], d=5)
res = activityNotifications(expenditure=[10,20,30,40,50], d=3)

# FASTER
# https://www.martinkysel.com/hackerrank-fraudulent-activity-notifications-solution/
# https://shareablecode.com/snippets/python-solution-for-hackerrank-problem-fraudulent-activity-notifications-FuHR-WX84
from bisect import bisect_left, insort_left
def activityNotifications(expenditure, d):
    # Write your code here
    notif = 0
    lastd = sorted(expenditure[:d]) # sort expenditures for first d-days window
    for day, exp in enumerate(expenditure):
        if day < d: continue
        # compute the median
        median = lastd[d//2] if d % 2 == 1 else ((lastd[d//2] + lastd[d//2-1])/2)
        if exp >= median*2:
            notif +=1
        # remove previous element and add new element in median window
        del lastd[bisect_left(lastd, expenditure[day - d])]
        insort_left(lastd, exp)

    return notif

#endregion

#region Lily's homework
# https://www.martinkysel.com/hackerrank-lilys-homework-solution/
# Problem reformulation:
# The sum is minimal if the array is sorted
# So we need to count the number of swaps to sort the array (both ascending and descending)

def cntSwaps(arr):
    pos = sorted(list(enumerate(arr)), key=lambda e: e[1]) # sort the array and key indices
    swaps = 0
    for idx in range(len(arr)):
        while True: #loop until everything is at the right place
            if pos[idx][0] == idx: # already at the right position, exit the loop
                break
            else:
                swaps += 1
                swapped_idx = pos[idx][0]
                pos[idx], pos[swapped_idx] = pos[swapped_idx], pos[idx]
    return swaps

def lilysHomework(arr):
    # Write your code here
    # Run the count of swaps on both ascending and descending arrays
    return min(cntSwaps(arr), cntSwaps(arr[::-1]))

arr = [2, 5, 3, 1]
#endregion

#region Luck balance
"""
Lena passes a series of test of [Luck_i, Importance_i]
Initially, her luck balance is 0.
For each test she fails, ker luck increases by L[i] to her balance
She can fail at max k important tests
If Lena fails k important contests, what is the max amount of luck she can have
"""
contests = [[5, 1], [2, 1], [1, 1], [8, 1], [10, 0], [5, 0]]
nb_lost_ones = k = 3
contests = [[13, 1],[10, 1],[9, 1],[8, 1],[13 ,1],[12, 1],[18, 1],[13, 1]]
nb_lost_ones = k = 5
def luckBalance(nb_lost_ones, contests):
    zeros = sum([el[0] for el in contests if el[1]==0])
    ones = [el for el in contests if el[1]==1]
    ones.sort(reverse=True)
    ones_won = sum([el[0] for el in ones[nb_lost_ones:][:]])
    ones_lost = sum([el[0] for el in ones[:nb_lost_ones][:]])
    return zeros+ones_lost-ones_won

#endregion

#region Greedy florist
"""
Group of k people want to buy all flowers in shop
After the flower bought, the price of each following flower increases by i 
(price of nth bough flower = n*price)
"""
costs = [1, 3, 5, 7, 9, 10, 10]
k=3
# expected answer: 10+10+9 + 2*7 + 2*5 + 2*3 + 3*1 = 62
def getMinimumCost(k, costs):
    total_cost=0
    incr=1
    costs.sort(reverse=True)
    total_cost += sum(costs[0:k])
    for idx, c in enumerate(costs[k:]):
        if idx % k == 0: incr += 1
        print(idx, incr,c)
        total_cost += incr*c
    return total_cost
#endregion

#region Icecream parlor
"""
Each time Sunny and Johnny take a trip to the Ice Cream Parlor, 
they pool their money to buy ice cream. 
On any given day, the parlor offers a line of flavors, each flavor has a cost c.
Help Sunny and Johnny choose 2 distinct flavors such that they spend their entire pool of money during each visit.
Note: there is always a unique solution
Output: int int: the indices of the two flavors they will purchase as two space-separated integers on a line
"""
cost, money = [2,1,3,5,6], 5  # exp output [1, 3] (2+3)
cost, money = [1, 4, 5, 3, 2], 4 # exp output [1,4]
cost, money = [2, 2, 4, 3], 4 # exp output [1,2]

sorted_costs = dict(sorted(enumerate(cost), key=lambda e: e[1])) # need to swap keys, values
costs_dic = {k: v for v, k in enumerate(cost)} # not good because removes duplicates

def whatFlavors(cost, money):
    saved_values = {}
    for counter, value in enumerate(cost):
        print(saved_values)
        if money-value in saved_values:
            print(saved_values[money-value] + 1, counter + 1)
        elif value not in saved_values:
            saved_values[value] = counter

#endregion

#region Candies
"""
a teacher gives candies to her students.
if student has bigger score than their neighbor, they must receive more candies
when two children have equal score, they can have different number of candies.
minimum amount of candies?
"""
arr = [4,2,6,1,7,8,9,2,1]
# candies distributed: [1,2,1,2,1,2,3,4,2,1] total=18
def candies(arr):
    n=len(arr)
    candies = [1]*n
    for i in range(n-1):
        if arr[i+1]>arr[i]:
            candies[i+1] = candies[i]+1
        print("first pass", candies)
    for i in range(n-1,0,-1):
        if arr[i-1]>arr[i] and candies[i-1]<=candies[i]:
            candies[i-1] = candies[i]+1
        print("second pass", candies)
    return sum(candies)





#endregion

#region Poisonous plants
"""
There are a number of plants in a garden.
Each of the plants has been treated with some amount of pesticide.
After each day, if any plant has more pesticide than the plant on its left, it dies.

You are given the initial values of the pesticide in each of the plants. 
Determine the number of days after which no plant dies, 
i.e. the time after which there is no plant with more pesticide content than the plant to its left.
"""
p=[3,6,2,7,5]
#after day 1: [3,2,1], after day 2: [3,2]
class Plant:
    def __init__(self, pesticide, days):
        self.pesticide = pesticide
        self.days = days


def poisonousPlants(p):
    stack = []
    maxDaysAlive = 0

    for pesticide in p:
        daysAlive = 0
        while stack and pesticide <= stack[-1].pesticide:
            daysAlive = max(daysAlive, stack.pop().days)

        if not stack:
            daysAlive = 0
        else:
            daysAlive += 1
        maxDaysAlive = max(maxDaysAlive, daysAlive)
        stack.append(Plant(pesticide, daysAlive))

    return (maxDaysAlive)

#endregion

#region Minimum time required
"""
https://www.hackerrank.com/challenges/minimum-time-required/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=search

You have a number of machines that each have a fixed number of days to produce an item. 
All the machines operate simultaneously
Determine the minimum number of days to produce an order.

For example, you have to produce 10 items. You have 3 machines that take [2,3,2] days to make an item

Day Production  Count
2   2               2
3   1               3
4   2               5
6   3               8
8   2              10
It takes 8 days to produce 10 items using these machines.
"""
machines =[2,3,2]
goal = 10
def minTime(machines, goal):
    machines.sort()

    low_rate = machines[0] # fastest machines
    lower_bound = (goal // (len(machines) / low_rate))
    high_rate = machines[-1] # slowest machines
    upper_bound = (goal // (len(machines) / high_rate)) + 1

    while lower_bound < upper_bound:
        num_days = (lower_bound + upper_bound) // 2
        # get number of items
        total = 0
        for machine in machines:
            total += (num_days // machine)
        if total >= goal:
            upper_bound = num_days
        else:
            lower_bound = num_days + 1

    return int(lower_bound)


#endregion
