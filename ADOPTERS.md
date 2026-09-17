# Adopters

Verified external use is tracked separately from stars, forks, or self-tests.

An adopter entry should include:
- repository or project
- platform
- Control Center commit or release
- mode used (`demo`, `public-safe local`, or embedded/integrated)
- reproducible evidence such as CI, command output, or a public integration commit

Machine-readable reports use `flop.adopter-report.v1`; see `schemas/flop-adopter-report-v1.schema.json` and `tools/validate_adopter_report.py`.

Classifications are explicit:
- `SELF_TEST`: maintainer/local/synthetic use; never counted as external adoption.
- `EXTERNAL_REPORTED`: an independent party supplied bounded evidence.
- `EXTERNAL_VERIFIED`: the supplied public evidence was independently reproduced or directly verified.

Self-use by this repository's maintainer is not counted as external adoption.

## Verified external adopters

None yet.

To submit evidence, open the **External adopter report** issue template. Reports must not include secrets, private keys, passphrases, private configuration, or custody material.
