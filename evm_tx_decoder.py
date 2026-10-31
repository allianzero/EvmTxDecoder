"""Pure, offline decoder for common ERC-20 calldata.

Decodes transfer, approve, and transferFrom calls from raw transaction
input data. No RPC, no network, and no private key are involved: the
input is just the hex calldata of a transaction you already have.
"""
import argparse
import json
import sys

SELECTORS = {
    "a9059cbb": "transfer",
    "095ea7b3": "approve",
    "23b872dd": "transferFrom",
}


def _clean_hex(data):
    if not isinstance(data, str):
        raise ValueError("calldata must be a hex string")
    text = data[2:] if data.startswith("0x") else data
    if len(text) % 2 != 0 or any(c not in "0123456789abcdefABCDEF" for c in text):
        raise ValueError("calldata must be even-length hex")
    return text.lower()


def _address_word(word):
    return "0x" + word[-40:]


def _uint_word(word):
    return int(word, 16)


def decode_calldata(data):
    """Decode ERC-20 calldata into a dict. Raises ValueError if unknown."""
    text = _clean_hex(data)
    if len(text) < 8:
        raise ValueError("calldata too short for a function selector")
    selector, body = text[:8], text[8:]
    name = SELECTORS.get(selector)
    if name is None:
        raise ValueError(f"Unknown function selector: 0x{selector}")
    words = [body[i:i + 64] for i in range(0, len(body), 64)]
    if name in ("transfer", "approve"):
        if len(words) != 2:
            raise ValueError(f"{name} expects 2 arguments, got {len(words)}")
        key = "to" if name == "transfer" else "spender"
        return {"function": name, key: _address_word(words[0]), "amount": _uint_word(words[1])}
    # transferFrom
    if len(words) != 3:
        raise ValueError(f"transferFrom expects 3 arguments, got {len(words)}")
    return {"function": name, "from": _address_word(words[0]),
            "to": _address_word(words[1]), "amount": _uint_word(words[2])}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Decode ERC-20 calldata offline")
    parser.add_argument("--data", required=True, help="Hex calldata, e.g. 0xa9059cbb...")
    args = parser.parse_args(argv)
    try:
        result = decode_calldata(args.data)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
