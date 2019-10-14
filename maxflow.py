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
#             See dfs_recursive.py for description and implementation.
#   var_dict: buffer to store local variable. Simply use an empty dict
#             as the actual parameter.
#
maxflow = lambda s, t, edges, dfs_func, var_dict: ( 
    # var_dict is used to assign local variable, 
    # since dict.update({"var": value}) is an expression rather than a statement
    # which is allowed inside lambda

    # create augmented graph with back edges
    var_dict.update({
        "edges": 
            (lambda edges, new_edges: 
                all(
                    (
                        new_edges.setdefault(u, {}).update({v: w}), 
                        new_edges.setdefault(v, {}).setdefault(u, 0)
                    )
                    for u, neigbors in edges.items() for v, w in neigbors.items()
                )  # evaluate to True, since each item in iterator is a non-empty tuple (truthy)
                and new_edges
            ) (edges, {}),
        "maxflow": 0,
    }) 
    or # prev expresion is False

    # repeatedly: find a path from source to sink, then put as much flow through that path as possible.
    # (increase corresponding back edges by the flow, decrease corresponding forward edges by the flow)
    # repeat until no more paths are found
    any(  # loop until a truthy value is encountered (aka while loop)
        var_dict.update({"path": dfs_func(s, t, var_dict["edges"], set(), dfs_func)[::-1]}) or # get a DFS path from s to t
        not var_dict["path"]  # return True to stop loop if no path is found
        or var_dict.update({
            "flow": min(var_dict["edges"][v1][v2] for v1, v2 in zip(var_dict["path"], var_dict["path"][1:]))
        }) # flow is min of all edges in path
        or var_dict.update({"maxflow": var_dict["maxflow"] + var_dict["flow"]})  # maxflow += flow
        or any(
            var_dict["edges"][v1].update({v2: var_dict["edges"][v1][v2] - var_dict["flow"]})  # decrease forward edge in path by flow
            or var_dict["edges"][v2].update({v1: var_dict["edges"][v2][v1] + var_dict["flow"]})  # increase back edge in path by flow
            for v1, v2 in zip(var_dict["path"], var_dict["path"][1:])  # for all edges in path
        )  # evaluate to False since each item in iterator is False (None or None)
        # return False to continue loop if a path is found
        for _ in iter(int, 1)  # loop forever
    )
    and # prev expresion is True, since any() eventually find a Truthy value in iterator (the stop loop signal)
    (var_dict["maxflow"], var_dict["edges"]) # return max flow and max flow graph
)

#===================================
# Compact version
#
# var_dict (D) keys:
# edge D[0]
# maxflow D[1]
# path D[2]
# flow D[3]
maxflow_compact = lambda s,t,E,f,D:(D.update({0:(lambda E,G:all((G.setdefault(u,{}).update({v:w}),G.setdefault(v,{}).setdefault(u,0))for u,e in E.items() for v,w in e.items())and G)(E,{}),1:0})or any(D.update({2:f(s,t,D[0],set(),f)[::-1]}) or not D[2]or D.update({3:min(D[0][v][u] for v,u in zip(D[2],D[2][1:]))})or D.update({1:D[1]+D[3]})or any(D[0][v].update({u:D[0][v][u]-D[3]})or D[0][u].update({v:D[0][u][v]+D[3]})for v,u in zip(D[2],D[2][1:]))for _ in iter(int,1))and(D[1],D[0]))


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