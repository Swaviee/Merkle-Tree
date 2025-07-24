# Merkle-Tree

Phase 1: Building the Merkle Tree
Objective:
Build a Merkle tree from a list of transactions and compute the top hash.

Instructions:
Read the list of transactions from the file a1.txt.
Implement a function to compute the SHA-256 hash of concatenated transaction hashes. Please note that, a SHA256 implementation is already available in Python and you can use it as hashlib.sha256(data.encode('utf-8')).hexdigest().
As we are working with transaction hashes (instead of transaction content), we can build the Merkle tree with SHA256(txhash_1+txhash_2) rather than SHA256(SHA256(tx1content)+SHA256(tx2content)).
Implement a function to build the Merkle tree and compute the top hash, preserving the order of transactions as they appear in the file.
Print the top hash of the Merkle tree, which I computed as "2d800e7a04fa0e27ced3c37f9dc1086309304d2d6660bade4ecee773c06b1652".


Phase 2: Verifying Integrity with Interim Hash
Objective:
Given an interim hash, determine if transactions may have been tampered with by identifying inconsistencies in the Merkle tree. [UNGRADED: If you are good at coding, consider listing each transaction that may have been tampered with.]

Instructions:
You will be given an interim hash (e.g., "36a17b6cb3611e408829353cbff4f0d9582231a23ef05ab08302bc9215005390").
Implement a function to find inconsistencies in the Merkle tree and identify the transactions that may have been tampered with.
Print the potentially tampered transactions.
