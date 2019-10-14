from pprint import pprint as pp
from dfs_recursive import dfs_compact as dfs


# Ford-Fulkerson algorithm for maxflow
# Return the max flow and the max flow graph of
# a directed weighted graph.
# Only work with graphs whose edges are positive.
# 
# Usage:
#   maxflow(s, t, edges, dfs_func, {})
#
# where:
#   s: source vertex
#   t: sink vertex
#   edges: map vertex to dictionary, such that edges[v][u] = w 
#          where v, u are vertices and w is the weight of edge (v, u)
#   dfs_func: a dfs function that return a reversed path from s to t. 
#             See dfs_recursive.py for implementation
#   var_dict: buffer to store local variable. Simply use an empty dict
#             as the actual parameter.
#
maxflow = lambda s, t, edges, dfs_func, var_dict: (
    var_dict.update({
        "edges": 
            (lambda edges, new_edges: 
                next(filter(None, 
                    (
                        (
                            new_edges.setdefault(u, {}).update({v: w}), 
                            new_edges.setdefault(v, {}).setdefault(u, 0)
                        ) and None
                        for u, neigbors in edges.items() for v, w in neigbors.items()
                    )
                ), None)
                or new_edges
            ) (edges, {}),
        "maxflow": 0,
    }) or
    # loop until a truthy value is encountered (aka while loop)
    next(filter(None,  
        (
            var_dict.update({"path": dfs_func(s, t, var_dict["edges"], set(), dfs_func)[::-1]}) or # get a DFS path from s to t
            not var_dict["path"]  # return True (stop loop) if no path is found
            or var_dict.update({
                "flow": min(var_dict["edges"][v1][v2] for v1, v2 in zip(var_dict["path"], var_dict["path"][1:]))
            })
            or var_dict.update({"maxflow": var_dict["maxflow"] + var_dict["flow"]})
            or next(filter(None, 
                (
                    var_dict["edges"][v1].update({v2: var_dict["edges"][v1][v2] - var_dict["flow"]}) 
                    or var_dict["edges"][v2].update({v1: var_dict["edges"][v2][v1] + var_dict["flow"]})
                    for v1, v2 in zip(var_dict["path"], var_dict["path"][1:])
                )
            ), False) # return False (continue loop) if a path is found
            for _ in iter(int, 1)  # loop forever
        ))
    )
    and
    (var_dict["maxflow"], var_dict["edges"])
)

#===================================
# Compact version
#
# var_dict (D) keys:
# edge 0
# maxflow 1
# path 2
# flow 3
maxflow_compact = lambda s,t,E,f,D:(D.update({0:(lambda E,G:next(filter(None,((G.setdefault(u,{}).update({v:w}),G.setdefault(v,{}).setdefault(u,0))and 0 for u,e in E.items() for v,w in e.items())), 0)or G)(E,{}),1:0})or next(filter(None,(D.update({2:f(s,t,D[0],set(),f)[::-1]}) or not D[2]or D.update({3:min(D[0][v][u] for v,u in zip(D[2],D[2][1:]))})or D.update({1:D[1]+D[3]})or next(filter(None,(D[0][v].update({u:D[0][v][u]-D[3]})or D[0][u].update({v:D[0][u][v]+D[3]})for v,u in zip(D[2],D[2][1:]))),0)for _ in iter(int,1))))and(D[1],D[0]))


#===================================
# test
edges = {
    0: {1: 11, 2: 12},
    1: {3: 12},
    2: {1: 1, 4: 11},
    3: {5: 19},
    4: {3: 7, 5: 4}
}
s = 0
t = 5
# should get 23
maxflow, flow_edges = maxflow_compact(s, t, edges, dfs, {})

print("========================")
pp(edges)
print(maxflow)
pp(flow_edges)