import argparse
import collections
import sys
from pathlib import Path

from . import __version__, dnsd, web

DEFAULT_DOMAIN = "vidaahub.com"


def run_dns(a):
    blocklist = dnsd.Blocklist.from_files(a.blocklist)
    logfile = open(a.log, "a", encoding="utf-8") if a.log else None

    def log(line):
        print(line, flush=True)
        if logfile:
            logfile.write(line + "\n")
            logfile.flush()

    print(f"dns {a.ip}:{a.port}  {a.domain} -> {a.ip}  {len(blocklist.names)} blocked names", flush=True)
    dnsd.serve(a.ip, a.port, a.domain, a.ip, a.upstream, blocklist, log)


def run_summarize(a):
    counts = collections.Counter()
    for line in a.log.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 5:
            counts[(parts[2], parts[4])] += 1
    for (name, action), n in counts.most_common(a.top):
        print(f"{n:5}  {action:7} {name}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="sidecar", description="Inspect and quiet a VIDAA TV from your LAN.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dns", help="DNS front: points the bridge domain here, blocks listed names")
    d.add_argument("--ip", required=True, help="LAN IP of this machine")
    d.add_argument("--port", type=int, default=53)
    d.add_argument("--domain", default=DEFAULT_DOMAIN)
    d.add_argument("--upstream", default="1.1.1.1")
    d.add_argument("--blocklist", action="append", default=[], type=Path, help="file of names, repeatable")
    d.add_argument("--log", type=Path, help="append every decision to this file")
    d.set_defaults(run=run_dns)

    w = sub.add_parser("web", help="HTTPS server with the read-only probe page")
    w.add_argument("--bind", default="0.0.0.0")
    w.add_argument("--port", type=int, default=443)
    w.add_argument("--domain", default=DEFAULT_DOMAIN)
    w.add_argument("--out", type=Path, default=Path("reports"))
    w.add_argument("--certs", type=Path, default=Path("certs"))
    w.set_defaults(run=lambda a: web.serve(a.bind, a.port, a.domain, a.out, a.certs))

    s = sub.add_parser("summarize", help="count the names in a dns log")
    s.add_argument("log", type=Path)
    s.add_argument("--top", type=int, default=30)
    s.set_defaults(run=run_summarize)

    args = p.parse_args(argv)
    try:
        args.run(args)
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError) as e:
        print(f"sidecar: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
