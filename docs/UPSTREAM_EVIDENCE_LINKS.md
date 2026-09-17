# Upstream evidence links

This map records public upstream discussions that produced concrete downstream fixtures or regressions. It is collaboration evidence, not an adoption count and not normative authority.

## Yellow Paper #26 — quote comparability

Upstream: https://github.com/flop-labs/yellowpaper/issues/26

Downstream sequence:
- Session Router regression: `retardio73-boop/flop-session-router@382f5bfa251c9e28cd5b943586412bbf7939896f` rejects unlike quote units rather than ranking them.
- Cross-System Conformance Lab fixture: `retardio73-boop/flop-conformance-lab@d98edd9169cb5fd10a929a0658204ad0ac1957e7` covers the specified `open_channel -> receipt` boundary and keeps the unresolved quote mapping fail-closed.

The upstream discussion subsequently confirmed that the current opening offer is not yet a complete reproducible cross-provider comparison quote. The downstream fixture therefore remains a boundary test, not a locally invented canonical schema.

## Yellow Paper #44 — wrong_path_orientation

Upstream: https://github.com/flop-labs/yellowpaper/issues/44

Downstream reproduction:
- Cross-System Conformance Lab commit: `retardio73-boop/flop-conformance-lab@f0666b165379fdeed0c5e27f2f1d13353f36fc48`.
- Fixture: `conformance/fixtures/flop-wire-v1-yellowpaper-44.json`.
- Reproduction: `conformance/reproductions/yellowpaper-44.py`.

A separate implementation by `miyawakiclaude/lineageauth` later reported the same conclusion from Appendix F text and the published corpus. That is independent corroboration of the discrepancy, not adoption of this stack.

## Boundary

Upstream comments, peer reproductions, and community projects are evidence inputs only. They do not automatically become official protocol truth, conformance authority, or external-adoption records.
