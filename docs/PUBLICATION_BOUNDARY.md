# Publication boundary

The control center has two capability classes.

## PUBLIC_SAFE
Generic operational infrastructure only:
- repository health and git metadata
- process/task status and reversible controls
- GitHub issue/repository status
- network reachability and latency
- generic bounded log tailing and health alerts
- module contracts and UI shell

## PRIVATE_EDGE
Never include these in a public export without explicit review:
- contest- or campaign-specific logic and room selection
- roster/candidate scoring or tactical allocation logic
- autonomous response policies or prompts
- private evidence ranking or recruitment heuristics
- local identity/mailbox mappings, local paths and task names
- signer client paths, custody implementation details or secrets
- private runtime state, unpublished evidence or local operational history

The public export is deny-by-default: only explicitly allowlisted files may leave the local repository.
