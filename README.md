# Solana Vanity Address Helper

This will help you create vanity solana addresses. Simply run the command with the prefix you would like. Underneath, it uses `solana-keygen` to find a keypair that will work. From there, it handles the b58 encoding to produce a private key which you could then import into [Phantom](https://phantom.app/).

## Prerequisites

Install [Solana CLI Tools](https://docs.solana.com/cli/install-solana-cli-tools).

## Usage

Run w/ `python3 sol_vanity.py [prefix]`

Example:
```
> python3 sol_vanity.py SoL
Wrote keypair to SoL...fhuDx.json
File: SoL...fhuDx.json	Private Key: 166i...EP13k
```

The private key string can be copy/pasted directly into Phantom > Add / Connect Wallet > Import Private Key.

![SoL Example](example.png)

Notes: 
* parts of the output were removed so that nobody tries to use a shared wallet. 
* not all characters are available. see [this chart](https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart) for what is allowed.

