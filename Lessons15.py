class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        x = 0
        for i in range(len(stones)):
            for j in range(len(jewels)):
                x += 1
        return x
