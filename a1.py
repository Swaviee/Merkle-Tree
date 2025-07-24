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

#Build Merkle
def build_merkle_tree(transactions):
    if not transactions:
        return None

    # Start with the transaction hashes as the current level
    current_level = transactions[:]

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
            else:
                # Odd number of hashes - duplicate the last one
                left = current_level[i]
                combined = sha256(left + left)
                next_level.append(combined)

        current_level = next_level

    return current_level[0]

#Check for Top Hash
def main():
    print("=== Phase 1: Building Merkle Tree ===")

    # Read transactions from the file
    transactions = read_transactions_from_file('a1.txt')
    print(f"Read {len(transactions)} transactions from file")

    # Build the Merkle tree and get the top hash
    top_hash = build_merkle_tree(transactions)

    print(f'Top hash of the Merkle tree: {top_hash}')

    # Assert the top hash matches the expected hash
    expected_top_hash = "2d800e7a04fa0e27ced3c37f9dc1086309304d2d6660bade4ecee773c06b1652"
    assert top_hash == expected_top_hash, "Computed top hash does not match the expected top hash."

    print("✓ Top hash verification passed!")


if __name__ == "__main__":
    main()