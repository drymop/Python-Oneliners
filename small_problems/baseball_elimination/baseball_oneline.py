# ===================
# compact version, replacing all the imported function with lambda
# this oneline-version will work if copied and pasted to an isolated file
# var
# 0: n_teams
# 1: scores
# 2: games
# 3: max_scores
# 4: edges
print((lambda f,g,D:D.update({0: int(input()),1: list(map(int, input().split()))})or D.update({2:[list(map(int, input().split())) for _ in range(D[0])]})or D.update({3:D[1][0]+sum(D[2][0])})or(False if any(x>D[3]for x in D[1][1:])else D.update({4:{-1:{}}})or any(D[4].update({t:{-2:D[3]-D[1][t]}}) for t in range(1,D[0]))or any(D[4][-1].update({(i, j):D[2][i][j]})or D[4].update({(i,j):{i:D[2][i][j],j:D[2][i][j]}})for i in range(1,D[0])for j in range(i+1,D[0]))or all(w==0 for w in g(-1,-2,D[4],f,{})[1].get(-1,{}).values())))(lambda s,t,E,A,f:[t]if s==t else[]if s in A else A.add(s)or(lambda p:p and p.append(s)or p)(next(filter(None,(f(v,t,E,A,f)for v,w in E.get(s,{}).items()if w>0)),[])),lambda s,t,E,f,D:(D.update({0:(lambda E,G:all((G.setdefault(u,{}).update({v:w}),G.setdefault(v,{}).setdefault(u,0))for u,e in E.items() for v,w in e.items())and G)(E,{}),1:0})or any(D.update({2:f(s,t,D[0],set(),f)[::-1]}) or not D[2]or D.update({3:min(D[0][v][u] for v,u in zip(D[2],D[2][1:]))})or D.update({1:D[1]+D[3]})or any(D[0][v].update({u:D[0][v][u]-D[3]})or D[0][u].update({v:D[0][u][v]+D[3]})for v,u in zip(D[2],D[2][1:]))for _ in iter(int,1))and(D[1],D[0])),{})and"yes"or"no")