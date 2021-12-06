


n = 3

dp = [[]]

for i in range(1,n+1):
    dp.append([])
    for j in range(0,2*i+1):
        if i == 1:
            dp[i].append(1)
        else:
            sm = 0
            for c in range(3):
                if(j-c>=0 and j-c<=2*(i-1)):
                    sm+=dp[i-1][j-c]

            dp[i].append(sm)



print(dp)
res = 1

for i in range(6,0,-1):
    

# print(res)

