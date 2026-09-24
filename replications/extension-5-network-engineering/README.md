# Extension 5 — Network-engineering bots (work in progress)

> **Status: WIP.** Built so far: `bots.py` and `main_bots.py`, each tested (`tests/`).
> Not yet built: `sweep_bots.py`, `bots_experiment.py`, the plot, and results.

**Question.** Shirado & Christakis (2020) added always-cooperating bots to human networks, each
offering its human one rewiring option per round. Bots that cut ties to defectors raised
cooperation; bots that introduce people to cooperators made it collapse. Do the same bots change
what the paper's imitating agents do, and does that ordering (disengaged > random > engaged)
come out of the model?

**Model.** Agents play and imitate exactly as in the base replication. One extra bot node per
agent, always C, never imitates. After imitation, each bot makes one rewiring offer, which its
agent accepts. Conditions: none, always C (no rewiring), random, engaged, disengaged.
Game: $T=2$, $S=-1$ (the paper's donation game, $b/c = 2$).

**Details.** Full design and decisions: [ARCHITECTURE.txt](ARCHITECTURE.txt).
Sources: [REFERENCES.md](../../REFERENCES.md).
