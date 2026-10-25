# Compatibility

What has been seen on real TVs. This table is built from **device reports**: if yours
isn't here, please [send one](../../../issues/new?template=device_report.yml).

Do not post serial numbers, MAC addresses or device IDs.

| Software version | Bridge page loads | Functions seen | Probe result | Notes |
|---|---|---|---|---|
| `V0011.09.09C.P0930` (ext. `C.P0930.X0005.W01.Y01.J01`) | Yes, through the vendor domain | 86 via IP address, 118 via the vendor domain | Not run yet | Observed with another community tool, not with sidecar. Reading `Appinfo.json` and a limited set of files worked; most system paths were not visible. |

## Reading the table

- **Functions seen**: how many `Hisense_*`, `TvInfo_*` and related functions the page
  found. A low number usually means the page was opened through an IP address instead of
  the vendor domain, or that the firmware hides functions from this origin.
- **Probe result**: whether `sidecar web` produced a report.

## Adding a row

Open a device report with the same columns. One row per software version.
