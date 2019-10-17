from pprint import pprint as pp
from maxflow import maxflow_compact as maxflow_func
from dfs_recursive import dfs_compact as dfs_funcs

can_win = lambda var: (
    # read input (n_teams, current scores, games left)
    var.update({
        "n_teams": int(input()),
        "scores": list(map(int, input().split()))            
    })
    or
    var.update({
        "games": [list(map(int, input().split())) for _ in range(var["n_teams"])]
    })
    or
    # assume team 0 win all remaining match
    var.update({
        "max_score": var["scores"][0] + sum(var["games"][0])
    })
    or
    (
        # team 0 cannot win if any other team has more than max_score
        # return False if that's the case
        False if any(x > var["max_score"] for x in var["scores"][1:]) else

        # else: create a graph and run max flow to find out
        var.update({
            "edges": {"s":{}}
        })
        or
        # each team (except 0) has a team vertex that connects to sink ("t") with weight = max_scores - cur_score
        any(var["edges"].update({ team: {"t": var["max_score"]-var["scores"][team]} }) for team in range(1, var["n_teams"]))
        or
        # each pair of team (A, B) excluding 0 has game a vertex v with
        # weight s -> v is number of matches left between A and B (= games[A][B] or games[B][A])
        # weight v -> team A's vertex is infinity 
        # weight v -> team B's vertex is infinity 
        any(
            # create edge from source ("s") to game vertex (i, j)
            var["edges"]["s"].update({ (i, j): var["games"][i][j] })
            or
            # create edges from (i, j) to i and to j
            var["edges"].update({ 
                (i, j): { i: var["games"][i][j], j: var["games"][i][j] }
            })
            # for each pair of teams i, j
            for i in range(1, var["n_teams"]) for j in range(i+1, var["n_teams"])
        ) # evaluate to False
        or
        # run maxflow on the graph from s to t
        # the return value of maxflow_func is a tuple of the max flow and the
        # flow graph, so return_val[1] is the flow graph
        # If all out edges from s are saturated (weight 0) in the flow graph, 
        # it is possible for team 0 to win
        all(w == 0 for w in maxflow_func("s", "t", var["edges"], dfs_funcs, {})[1].get("s",{}).values())
    )
)

print(can_win({}))