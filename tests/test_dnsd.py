import json
import socket
import struct
import tempfile
import unittest
from pathlib import Path

from sidecar import dnsd, web


def query(name, qtype=1):
    labels = b"".join(bytes([len(p)]) + p.encode() for p in name.split("."))
    return b"\x12\x34" + struct.pack(">HHHHH", 0x0100, 1, 0, 0, 0) + labels + b"\x00" + struct.pack(">HH", qtype, 1)


class DnsTests(unittest.TestCase):
    def test_parse_question(self):
        pkt = query("Home.Example.com", 28)
        self.assertEqual(dnsd.parse_question(pkt), ("home.example.com", 28, len(pkt)))

    def test_parse_rejects_garbage(self):
        with self.assertRaises(ValueError):
            dnsd.parse_question(b"\x00" * 5)

    def test_blocklist_matches_subdomains_only_below(self):
        bl = dnsd.Blocklist(["ads.example.com"])
        self.assertTrue(bl.matches("ads.example.com"))
        self.assertTrue(bl.matches("x.ads.example.com"))
        self.assertFalse(bl.matches("example.com"))
        self.assertFalse(bl.matches("badads.example.com"))

    def test_blocklist_file_formats(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "l.txt"
            f.write_text("# comment\ntrack.example\n0.0.0.0 hosts.example  # inline\n\n")
            self.assertEqual(dnsd.Blocklist.from_files([f]).names, {"track.example", "hosts.example"})

    def test_decide(self):
        bl = dnsd.Blocklist(["ads.example"])
        self.assertEqual(dnsd.decide("bridge.example", "bridge.example", bl), "local")
        self.assertEqual(dnsd.decide("ads.example", "bridge.example", bl), "block")
        self.assertEqual(dnsd.decide("ok.example", "bridge.example", bl), "forward")

    def test_reply_a_and_aaaa(self):
        pkt = query("bridge.example")
        _, _, qend = dnsd.parse_question(pkt)
        reply = dnsd.build_reply(pkt, qend, 1, "192.168.1.5")
        self.assertEqual(reply[:2], pkt[:2])
        self.assertEqual(struct.unpack(">H", reply[6:8])[0], 1)  # one answer
        self.assertEqual(reply[-4:], socket.inet_aton("192.168.1.5"))
        empty = dnsd.build_reply(pkt, qend, 28, "192.168.1.5")
        self.assertEqual(struct.unpack(">H", empty[6:8])[0], 0)


class WebTests(unittest.TestCase):
    def test_redact_nested(self):
        getters = {"Hisense_GetSerialType": 1, "Hisense_GetUuid": "abc", "Hisense_GetBrand": "x"}
        data = {"getters": getters, "list": [{"mac": "1"}]}
        out = web.redact(data)
        self.assertEqual(out["getters"]["Hisense_GetUuid"], "<redacted>")
        self.assertEqual(out["getters"]["Hisense_GetBrand"], "x")
        self.assertEqual(out["list"][0]["mac"], "<redacted>")
        json.dumps(out)


if __name__ == "__main__":
    unittest.main()
