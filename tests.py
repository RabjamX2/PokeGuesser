def levenshteinDistance(A, B):
    N, M = len(A), len(B)
    # Create an array of size NxM
    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]

    # Base Case: When N = 0
    for j in range(M + 1):
        dp[0][j] = j
    # Base Case: When M = 0
    for i in range(N + 1):
        dp[i][0] = i
    # Transitions
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # Insertion
                    dp[i][j - 1],  # Deletion
                    dp[i - 1][j - 1],  # Replacement
                )

    return dp[N][M]


test = [1, 32, 657, 234, 857, 234]
new_top = test[3:]
test[3:] = []
test = new_top + test
print(test)
