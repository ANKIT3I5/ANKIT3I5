# WHITE AI ALL CHECK: GitHub + ChatGPT workflow

## Purpose

The `.github/workflows/all-check.yml` workflow runs on pushes, pull requests to `main`, and manual dispatch. It is intended to be the central blocking check for the WHITE AI repository.

## Blocking checks

- Gitleaks secret scan
- Python source compilation
- Python dependency audit with `pip-audit`
- Python static security scan with Bandit
- Python tests, if test files exist; if none exist, the workflow reports that test coverage is not configured
- Android production dependency audit with `npm audit --omit=dev --audit-level=high`
- Expo Doctor diagnostics
- Required module directory completeness gate

No vulnerability is ignored or downgraded. A failing dependency audit must remain failed until the issue is resolved through a verified compatible fix.

## Module inventory and limitations

The workflow reports whether the Android app, backend API, DNS module, RF simulation module, VPN module, and documentation exist. It fails the completeness gate if any required module directory is missing.

A directory being present does not prove that a module works. Add module-specific automated tests as each module is implemented.

RF hardware tests cannot be honestly performed by a normal GitHub-hosted runner. They require compatible physical hardware, an authorized frequency/test setup, and separate hardware test procedures. The workflow does not claim that simulated tests prove real RF connectivity.

## Run it

1. Open the repository's **Actions** tab.
2. Select **WHITE AI ALL CHECK**.
3. Click **Run workflow** for a manual run, or push a commit / open a pull request.
4. Open each job for detailed logs.
5. Download the `white-ai-module-inventory` artifact when available.

## Use the report in the ChatGPT conversation

Paste the workflow run URL into the WHITE AI project chat. For a failure, include the relevant error excerpt after removing tokens, passwords, private URLs, and personal data. The ChatGPT conversation can explain the report and help draft a fix; it does not automatically become a live dashboard for every GitHub run.

## Current state

The RF hardware is not connected and the internet uplink is unavailable. DNS, RF simulation, and VPN should be treated as incomplete until their code, tests, and required connectivity/hardware are actually available.
