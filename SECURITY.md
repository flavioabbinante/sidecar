# Security policy

## Supported versions

Only the latest release and the `main` branch receive fixes.

## Reporting a vulnerability

**Please don't open a public issue.** Use GitHub's private reporting instead:
go to the **Security** tab of this repository and choose **Report a vulnerability**.

Include what you found, how to reproduce it, and what you think the impact is. You
should get a first answer within a few days. Please give us reasonable time to fix the
problem before you disclose it.

## What is in scope

- Code execution, file access or data exposure caused by sidecar's DNS or HTTPS servers
- Ways for a device on the network to make sidecar write outside its report folder
- Personal data that gets into a report despite redaction
- Weaknesses in the generated certificate or its permissions

## What is out of scope

- Weaknesses in a TV's firmware or in the vendor's services. Report those to the vendor.
- Anything that needs the attacker to already control your computer or your network
- The fact that the certificate is self-signed. That's by design.

## Running sidecar safely

- Run it only while you need it, on a trusted home network, and restore the TV's DNS
  afterwards.
- The servers have no authentication. Anyone on the same network can reach them while
  they run. Don't run sidecar on shared or public Wi-Fi.
- Reports and DNS logs describe your own devices and browsing. Keep `reports/`,
  `certs/` and `*.log` out of version control (the provided `.gitignore` does this).
