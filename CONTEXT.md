# Glossary

The words this repo uses, and what they mean in the model. Terms only, no implementation.

**Player** — a node of the network. Every generation it plays one Prisoner's Dilemma game with each neighbour and picks one action, cooperate (C) or defect (D), for all of them.

**Human** — a player that learns by **imitation**: it compares its payoff with one neighbour's and may copy that neighbour's action. In the model, "human" means *imitator*, nothing more.

**AI agent** — a player that **never imitates**. What drives it is its **rule**. In the model, "AI agent" means *a player that does not copy others*, nothing more.
- *Learning AI agent*: its rule is Q-learning. It learns from its own rewards only.
- *Stubborn AI agent*: its rule is fixed (always C, always D, or coin flip). It never learns. It's used only as a control.
- _Avoid_: "bot" (Extension 5 uses bots for players that rewire ties, not players that play).

**Hub** — a player with many more neighbours than average. When recording results, "the hubs" means the top 5% by degree.

**Placement** — which players are AI agents: **at random**, or **on the hubs** (highest degree first).

**Retaken** — a hub that defects and then switches back to cooperating by copying a cooperating neighbour. Only a human hub can be retaken.

**Cooperation level** — the fraction of players playing C, averaged over the last 60 generations and over all realizations.
