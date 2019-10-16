# Perform DFS on a weighted, directed graph
# starting at vertex s, ending at vertex t.
# Only consider edges with positive weight.
# Return a list of vertices denoting the path from s to t
# in reverse order (e.g. [t, c, b, a, s])
# Return empty list if no path is found
#
# Note: Since this algorithm is recursive, it only works reliably
# if there is no path longer than Python max recursion depth.
#
# Usage:
#   dfs(s, t, edges, set(), dfs)
#
# where:
#   s: source node
#   t: destination node
#   edges: map vertex to dictionary, such that edges[v][u] = w 
#          where v, u are vertices and w is the weight of edge (v, u)
#   visited: set of visited vertices, should start off as an empty set.
#   dfs_func: this function, inserted as argument to enable recursion
#
dfs = lambda s, t, edges, visited, dfs_func: (
    
    # reached the destination, return path which is just [destination]
    [t] if s == t else
    
    # already visited this vertex, not a valid path, return empty list
    [] if s in visited else  

    # s has not been visited, return recursive call on neighbors of s
    visited.add(s) or  # add s to visited set. this method return None, so we can chain 
                       # to other values using or operation (None or x results in x) 
        
        # If find a path, return path + [s], otherwise return None
        (lambda path: path + [s] if path else [])(  # if recursive call find a path, add s to that path. If no path, return no path.
            # this create a valid path or None
            next(filter(None,
                (dfs_func(v, t, edges, visited, dfs_func) for v,w in edges.get(s, {}).items() if w > 0) # any recursive call that find a path 
            ), [])
        )
)

# compact version
dfs_compact = lambda s,t,E,A,f:[t]if s==t else[]if s in A else A.add(s)or(lambda p:p and p.append(s)or p)(next(filter(None,(f(v,t,E,A,f)for v,w in E.get(s,{}).items()if w>0)),[]))


# test
if __name__ == '__main__':
    edges = {
        0: {1: 1, 2: 1},
        1: {2: 1},
        2: {0: 1, 3: 1},
        3: {3: 1, 1: -1}
    }
    print(dfs(2, 1, edges, set(), dfs))
    print(dfs(2, 0, edges, set(), dfs))
    print(dfs(2, 3, edges, set(), dfs))