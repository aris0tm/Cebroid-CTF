One encryption wasn't enough. So they encrypted it twice.
The first key is somewhere. The second key is somewhere else.
And neither file is named "key".

Files: final.enc, archive.dat, config.old, readme.txt

final.enc layout: [2-byte big-endian length][RSA-OAEP-encrypted AES key_A][IV_A || AES-256-CBC ciphertext of the flag under key_A]
archive.dat: IV_B || AES-256-CBC ciphertext of the RSA private key (PEM), encrypted under key_B
config.old: contains key_B (as backup_cipher_key, hex) hidden among ordinary config lines

Decryption order:
  1. Get key_B from config.old
  2. Decrypt archive.dat with key_B -> RSA private key (PEM)
  3. Parse final.enc: extract encrypted key_A length + blob, and ciphertext_A
  4. RSA-decrypt encrypted key_A with the recovered private key -> key_A
  5. AES-decrypt ciphertext_A with key_A -> flag
