"""Fewest unlimited positive-denomination coins for a nonnegative amount.
Return -1 if impossible. DP: O(amount * number of coins) time, O(amount) space.
Baseline recursively enumerates choices (exponential).
"""
def min_coins_for_amount(coins, amount):
    coins = list(coins)
    if type(amount) is not int or amount < 0:
        raise ValueError("Amount must be a nonnegative integer")
    if any(type(c) is not int or c <= 0 for c in coins):
        raise ValueError("Coins must be positive integers")
    coins = set(coins)
    dp = [0] + [amount + 1] * amount
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


if __name__ == "__main__":
    print(min_coins_for_amount([1, 2, 5], 11))  # 3
