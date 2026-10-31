import unittest

from evm_tx_decoder import decode_calldata


def word_address(addr):
    return "000000000000000000000000" + addr[2:].lower()


def word_uint(n):
    return f"{n:064x}"


class TestDecoder(unittest.TestCase):
    def test_transfer(self):
        to = "0x" + "ab" * 20
        data = "0xa9059cbb" + word_address(to) + word_uint(123)
        result = decode_calldata(data)
        self.assertEqual(result, {"function": "transfer", "to": to, "amount": 123})

    def test_approve(self):
        spender = "0x" + "11" * 20
        data = "0x095ea7b3" + word_address(spender) + word_uint(1000)
        result = decode_calldata(data)
        self.assertEqual(result["function"], "approve")
        self.assertEqual(result["spender"], spender)
        self.assertEqual(result["amount"], 1000)

    def test_transfer_from(self):
        frm, to = "0x" + "22" * 20, "0x" + "33" * 20
        data = "0x23b872dd" + word_address(frm) + word_address(to) + word_uint(7)
        result = decode_calldata(data)
        self.assertEqual(result, {"function": "transferFrom", "from": frm, "to": to, "amount": 7})

    def test_unknown_selector(self):
        with self.assertRaises(ValueError):
            decode_calldata("0xdeadbeef" + "00" * 64)


if __name__ == "__main__":
    unittest.main()
