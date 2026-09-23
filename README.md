# Santos, Pacheco & Lenaerts (2006) — replication

Replication of F. C. Santos, J. M. Pacheco & T. Lenaerts, *Evolutionary dynamics of social
dilemmas in structured heterogeneous populations*, PNAS 103(9):3490–3494, 2006.

**Question.** Does population structure change whether cooperation survives a social dilemma?

**Model.** Agents sit on the nodes of a graph and play a one-shot two-player game
(R=1, P=0, T∈[0,2], S∈[−1,1]) with every neighbour. Each generation, every agent *x* picks a
random neighbour *y* and, if P_y > P_x, adopts *y*'s strategy with probability
(P_y − P_x) / (k_> D_>). Four networks: complete, single-scale, random scale-free and
Barabási–Albert scale-free (average degree 4).

**Result.** The shape of the paper's Figs. 2–3 is reproduced: heterogeneous networks sustain
cooperation over a larger region of (T, S). Mean cooperation over the grid rises from 0.49
(complete) to 0.57 (single-scale), 0.62 (random scale-free) and 0.65 (Barabási–Albert).

| Complete vs. single-scale (cf. Fig. 2) | Random vs. BA scale-free (cf. Fig. 3) |
|---|---|
| ![](fig2_reduced_scale.png) | ![](fig3_reduced_scale.png) |

**Deviation from the paper.** Reduced scale, because the pure-Python code would need days
per figure at full scale (timings in `ARCHITECTURE.txt`):

| | Paper | Here |
|---|---|---|
| Population N | 10,000 | 500 (200 for complete) |
| Generations (transient + averaged) | 10,000 + 1,000 | 300 + 60 |
| Realizations per (T, S) point | 100 | 10 |

The shape is reproduced but the exact values are not, and finite-size noise is larger.

## Code

`main.py` (core loop) · `network.py` (the four graphs) · `payoff.py` · `update_rule.py`
· `sweep.py` ((T, S) grid) · `plot.py` · `reduced_scale_figures.py` (makes the figures above).
Each file has a `test_*.txt` with the command, expected output and interpretation.
Requires Python 3.9+, `networkx`, `numpy` and `matplotlib`.

## Extensions

- **Swarm learning** ([`replication-extension-swarm-learning/`](replication-extension-swarm-learning/)):
  the imitation rule is replaced by a particle-swarm (PSO) learning rule on one fixed network.
- **Swarm topology** ([`replication-extension-swarm-topology/`](replication-extension-swarm-topology/)):
  the swarm learning rule on all four networks. Does the topology effect survive?
- **Open-source game theory** ([`replication-extension-open-source/`](replication-extension-open-source/)):
  agents hold programs that read each other's code (FairBot, PrudentBot, ...). Does the network
  still matter, and what if reading code has a cost?

## References

Full list, with notes on where each one is used: [`REFERENCES.md`](REFERENCES.md).

**Base paper.** Santos, Pacheco & Lenaerts (2006), *PNAS* 103(9), 3490–3494.

**Foundations and framing.** Nowak (2006), *Five rules for the evolution of cooperation*,
Science · Pedreschi et al. (2025), *Human-AI coevolution*, Artificial Intelligence ·
Hammond et al. (2025), *Multi-Agent Risks from Advanced AI*, arXiv:2502.14143.

**Networks.** Erdős & Rényi (1959), *On random graphs I* · Barabási & Albert (1999),
*Emergence of scaling in random networks*, Science · Santos & Pacheco (2005), *Scale-free
networks provide a unifying framework for the emergence of cooperation*, PRL.

**Imitation rule.** Hauert & Doebeli (2004), Nature · Gintis (2000), *Game Theory Evolving*
(refs 18 and 30 of the base paper).

**Particle swarm (swarm extensions).** Kennedy & Eberhart (1995) · Shi & Eberhart (1998) ·
Eberhart & Shi (2000) · Clerc & Kennedy (2002) · Kennedy (1999) · Kennedy & Mendes (2002) ·
Carlisle & Dozier (2000) · Hu & Eberhart (2002).

**Open-source game theory.** Critch, Dennis & Russell (2022), arXiv:2208.07006 (main paper) ·
Sistla & Kleiman-Weiner (2026), *Evaluating LLMs in open-source games*, NeurIPS ·
Barasz et al. (2014) · LaVictoire et al. (2014) · Tennenholtz (2004) · Critch (2019) ·
Kalai et al. (2010).
