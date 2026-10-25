"""A tiny DNS front for one device on your LAN.

It answers one name with your machine's IP, sinks names on a blocklist and
forwards everything else to a real resolver. Every decision is logged.
"""

import socket
import struct
import time

A = 1
BLOCK_IP = "0.0.0.0"


class Blocklist:
    """Exact names plus all their subdomains. Accepts plain or hosts-file lines."""

    def __init__(self, names=()):
        self.names = {n.strip().lower().rstrip(".") for n in names if n.strip()}

    @classmethod
    def from_files(cls, paths):
        names = []
        for path in paths:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    tokens = line.split("#")[0].split()
                    if tokens:
                        names.append(tokens[-1])  # last token also handles "0.0.0.0 host"
        return cls(names)

    def matches(self, name):
        parts = name.split(".")
        return any(".".join(parts[i:]) in self.names for i in range(len(parts)))


def parse_question(pkt):
    """Return (name, qtype, end_offset) of the first question."""
    i, labels = 12, []
    try:
        while pkt[i]:
            n = pkt[i]
            if n & 0xC0:
                raise ValueError("compressed name in question")
            labels.append(pkt[i + 1 : i + 1 + n].decode("ascii"))
            i += n + 1
        (qtype,) = struct.unpack(">H", pkt[i + 1 : i + 3])
    except (IndexError, struct.error, UnicodeDecodeError) as e:
        raise ValueError("malformed question") from e
    if i + 5 > len(pkt):
        raise ValueError("truncated question")
    return ".".join(labels).lower(), qtype, i + 5


def build_reply(pkt, qend, qtype, ip):
    """Answer an A query with `ip`; any other type gets an empty NOERROR."""
    answer = qtype == A
    head = pkt[:2] + struct.pack(">HHHHH", 0x8180, 1, int(answer), 0, 0)
    rr = b"\xc0\x0c" + struct.pack(">HHIH", A, 1, 60, 4) + socket.inet_aton(ip) if answer else b""
    return head + pkt[12:qend] + rr


def decide(name, local_name, blocklist):
    if name == local_name:
        return "local"
    return "block" if blocklist.matches(name) else "forward"


def forward(pkt, upstream, timeout=3.0):
    # shortcut: UDP only, so answers that need TCP fallback are not relayed; upgrade if a client needs it
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as up:
        up.settimeout(timeout)
        up.sendto(pkt, (upstream, 53))
        try:
            return up.recv(4096)
        except socket.timeout:
            return None


def serve(bind_ip, port, local_name, local_ip, upstream, blocklist, log):
    # shortcut: one query at a time; fine for a single TV, use threads for a whole network
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((bind_ip, port))
    while True:
        pkt, client = sock.recvfrom(4096)
        try:
            name, qtype, qend = parse_question(pkt)
        except ValueError:
            continue
        action = decide(name, local_name, blocklist)
        if action == "forward":
            reply = forward(pkt, upstream)
        else:
            reply = build_reply(pkt, qend, qtype, local_ip if action == "local" else BLOCK_IP)
        log(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {client[0]} {name} {qtype} {action}")
        if reply:
            sock.sendto(reply, client)
