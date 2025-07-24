#Henry Faya
#5083025
#7/2/2025

import hashlib

#Read Transactions
def read_transactions_from_file(file_path):
    with open(file_path, 'r') as file:
        transactions = [line.strip().replace('\r', '') for line in file if line.strip()]
    return transactions

#Sha256
def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

#Merkle a1 + global storage
def build_merkle_tree(transactions):
    if not transactions:
        return None

    # Start with the transaction hashes as the current level
    current_level = transactions[:]

    # Store all intermediate hashes for verification purposes (global storage)
    global merkle_tree_hashes
    merkle_tree_hashes = {}

    # Build the tree level by level
    while len(current_level) > 1:
        next_level = []

        # Process pairs of hashes
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                # Pair exists - combine the two hashes
                left = current_level[i]
                right = current_level[i + 1]
                combined = sha256(left + right)
                next_level.append(combined)

                # Store the hash combination for verification
                merkle_tree_hashes[combined] = (left, right, i, i + 1)
            else:
                # Odd number of hashes - duplicate the last one
                left = current_level[i]
                combined = sha256(left + left)
                next_level.append(combined)

                # Store the hash combination for verification
                merkle_tree_hashes[combined] = (left, left, i, i)

        current_level = next_level

    return current_level[0]

#Verify Inconsistencies
def verify_merkle_tree(transactions, expected_interim_hash):
    global merkle_tree_hashes

    # Check if the expected interim hash exists in our tree
    if expected_interim_hash not in merkle_tree_hashes:
        print(f"Error: Interim hash '{expected_interim_hash}' does not exist in the tree.")
        return []

    # Find the hash and identify the transactions
    left_hash, right_hash, left_idx, right_idx = merkle_tree_hashes[expected_interim_hash]

    # Check if these are original transaction hashes (direct leaf nodes)
    if left_hash in transactions and right_hash in transactions:
        left_tx_idx = transactions.index(left_hash)
        right_tx_idx = transactions.index(right_hash)
        print(f'Interim hash found at combination of {transactions[left_tx_idx]} and {transactions[right_tx_idx]}')
        return [left_tx_idx, right_tx_idx]
    else:
        # This is a higher-level combination of intermediate hashes
        print(f'Interim hash found at combination of intermediate hashes')

        # Recursively find all leaf transactions under this hash
        def find_leaf_transactions(hash_value):
            if hash_value in transactions:
                return [transactions.index(hash_value)]
            elif hash_value in merkle_tree_hashes:
                left, right, _, _ = merkle_tree_hashes[hash_value]  # Fixed unpacking
                result = []
                result.extend(find_leaf_transactions(left))
                if right != left:  # Avoid duplicates for odd-numbered levels
                    result.extend(find_leaf_transactions(right))
                return result
            return []

        tampered_indices = []
        tampered_indices.extend(find_leaf_transactions(left_hash))
        if right_hash != left_hash:
            tampered_indices.extend(find_leaf_transactions(right_hash))

        return sorted(list(set(tampered_indices)))


def main():
    print("=== Phase 2: Verifying Integrity with Interim Hash ===")

    # Read transactions from the file
    transactions = read_transactions_from_file('a1.txt')
    print(f"Read {len(transactions)} transactions from file")

    # Build the Merkle tree first (required for verification)
    top_hash = build_merkle_tree(transactions)
    print(f"Built Merkle tree with top hash: {top_hash}")

    # Example interim hash for verification
    interim_hash = "36a17b6cb3611e408829353cbff4f0d9582231a23ef05ab08302bc9215005390"

    print(f"Verifying interim hash: {interim_hash}")
    tampered_indices = verify_merkle_tree(transactions, interim_hash)

    if tampered_indices:
        print(f"Potentially tampered transactions (indices): {tampered_indices}")
        print("Potentially tampered transactions:")
        for idx in tampered_indices:
            print(f"  Transaction {idx}: {transactions[idx]}")
    else:
        print("No tampering detected or interim hash not found.")


if __name__ == "__main__":
    main()