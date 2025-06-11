# app/infrastructure/stark/generate_keys.py
import starkbank

# Generate a new pair of private and public keys
private_key, public_key = starkbank.key.create()

# Print the generated keys
print("Private Key:", private_key)
print("Public Key:", public_key)