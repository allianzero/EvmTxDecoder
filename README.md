# EvmTxDecoder

A pure, offline Python decoder for common ERC-20 transaction calldata: `transfer`, `approve`, and `transferFrom`.

## Installation

No third-party dependencies. Requires Python 3.9 or later.

## Usage

```bash
python evm_tx_decoder.py --data 0xa9059cbb000000000000000000000000abababababababababababababababababababab000000000000000000000000000000000000000000000000000000000000007b
```

Example output:

```json
{
  "function": "transfer",
  "to": "0xabababababababababababababababababababab",
  "amount": 123
}
```

Amounts are raw token units (before dividing by `10 ** decimals`).

## How it works

- The first 4 bytes are the function selector: `a9059cbb` for transfer, `095ea7b3` for approve, `23b872dd` for transferFrom.
- Each argument is one 32-byte word. Addresses are the last 20 bytes of their word; amounts are the full word as an integer.
- Unknown selectors and malformed calldata raise an error instead of guessing.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests are fully offline.

## Limitations

- Only the three ERC-20 functions above are supported.
- This tool decodes calldata you already have. It does not fetch transactions, sign anything, or need a private key.

## License

MIT. See `LICENSE`.
