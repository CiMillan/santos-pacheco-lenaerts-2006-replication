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
Each file has a test in [`tests/`](tests/) with the command, expected output and interpretation.
Requires Python 3.9+, `networkx`, `numpy` and `matplotlib`.

## Extensions

Row 0 is the base replication. Each row of the results table links to its folder.

**Scripts.** Root scripts are never edited. *Changed* = a variant of a root script
(root → variant). *Created* = no root counterpart. Each folder keeps its tests in `tests/`.

| # | Scripts changed | Scripts created |
|---|---|---|
| 0 | — | [`main.py`](main.py), [`network.py`](network.py), [`payoff.py`](payoff.py), [`update_rule.py`](update_rule.py), [`sweep.py`](sweep.py), [`plot.py`](plot.py), [`reduced_scale_figures.py`](reduced_scale_figures.py) |
| 1 | [`update_rule.py`](update_rule.py) → [`swarm_update_rule.py`](replication-extension-swarm-learning/swarm_update_rule.py); [`main.py`](main.py) → [`main_swarm.py`](replication-extension-swarm-learning/main_swarm.py) | [`compare_imitation_vs_swarm.py`](replication-extension-swarm-learning/compare_imitation_vs_swarm.py), [`plot_comparison.py`](replication-extension-swarm-learning/plot_comparison.py) |
| 2 | [`sweep.py`](sweep.py) → [`sweep_swarm.py`](replication-extension-swarm-topology/sweep_swarm.py); [`plot.py`](plot.py) → [`plot_topology.py`](replication-extension-swarm-topology/plot_topology.py) | [`topology_experiment.py`](replication-extension-swarm-topology/topology_experiment.py), [`c1_zero_experiment.py`](replication-extension-swarm-topology/c1_zero_experiment.py), [`c1_sweep.py`](replication-extension-swarm-topology/c1_sweep.py), [`velocity_test.py`](replication-extension-swarm-topology/velocity_test.py), [`plot_c1_curve.py`](replication-extension-swarm-topology/plot_c1_curve.py) |
| 3 | [`main.py`](main.py) → [`main_os.py`](replication-extension-open-source/main_os.py); [`payoff.py`](payoff.py) → [`payoff_os.py`](replication-extension-open-source/payoff_os.py); [`sweep.py`](sweep.py) → [`sweep_os.py`](replication-extension-open-source/sweep_os.py) | [`programs.py`](replication-extension-open-source/programs.py), [`open_source_experiment.py`](replication-extension-open-source/open_source_experiment.py), [`cost_experiment.py`](replication-extension-open-source/cost_experiment.py) |
| 4 | [`update_rule.py`](update_rule.py) → [`stigmergy_update_rule.py`](replication-extension-stigmergy/stigmergy_update_rule.py); [`main.py`](main.py) → [`main_stigmergy.py`](replication-extension-stigmergy/main_stigmergy.py); [`sweep.py`](sweep.py) → [`sweep_stigmergy.py`](replication-extension-stigmergy/sweep_stigmergy.py) | [`lam_experiment.py`](replication-extension-stigmergy/lam_experiment.py), [`plot_lam_curve.py`](replication-extension-stigmergy/plot_lam_curve.py) |

**Results.** The paper's finding: the more heterogeneous the network, the more cooperation
(complete < single-scale < random scale-free < Barabási–Albert). "Base" below is our
reduced-scale run of the paper's model (row 0), so every comparison uses the same scale and seeds.

| # | Idea | Main results vs. the paper |
|---|---|---|
| 0 | **Base replication**: Santos et al. (2006), imitation on four networks over the (T, S) grid | **Paper's finding reproduced.** Same ordering: 0.49 < 0.57 < 0.62 < 0.65. Values are not exact because of the reduced scale |
| 1 | [**Swarm learning**](replication-extension-swarm-learning/): particle-swarm (PSO) learning instead of the paper's imitation; PD on the BA network | **Less cooperation than the paper's rule.** Base 0.90 → swarm 0.33. PSO's personal best keeps 89% of agents pulled toward old defection payoffs |
| 2 | [**Swarm topology**](replication-extension-swarm-topology/): swarm learning on all four networks; vary memory weight c₁ | **Paper's ordering disappears** with default swarm (c₁=1.5): every network ≈0.58. **It comes back, stronger, without memory** (c₁=0): 0.45 < 0.76 < 0.87 < 0.88 vs. base 0.49 < 0.57 < 0.62 < 0.65 |
| 3 | [**Open-source game theory**](replication-extension-open-source/): agents hold programs that read each other's code; then add a code-reading cost | **Paper's ordering disappears**: every network ≈0.97–1.00 (base 0.49–0.65), even in the PD where base gets 0. **It comes back when code-reading is costly**: at cost 1.0, 0.50 < 0.58 < 0.61 < 0.64, the same as base |
| 4 | [**Stigmergic imitation**](replication-extension-stigmergy/): agents read a fading payoff trace left at each node instead of the neighbour's current payoff (idea from SwarmWorld) | **Paper's ordering holds** with a payoff trace, even with long memory (BA 0.65 → 0.67). **It weakens only when the trace remembers the strategy** behind the best payoff: BA 0.65 → 0.61, complete unchanged, so the gap shrinks 0.16 → 0.12 |

## References

Notes on where each reference is used: [`REFERENCES.md`](REFERENCES.md).

### Base paper

- Santos, F. C., Pacheco, J. M. & Lenaerts, T. (2006). Evolutionary dynamics of social dilemmas
  in structured heterogeneous populations. *PNAS* 103(9), 3490–3494.

### Foundations and framing

- Nowak, M. A. (2006). Five rules for the evolution of cooperation. *Science* 314(5805), 1560–1563.
- Pedreschi, D., Pappalardo, L., Ferragina, E., et al. (2025). Human-AI coevolution.
  *Artificial Intelligence* 339, 104244.
- Hammond, L., Chan, A., Clifton, J., et al. (2025). *Multi-Agent Risks from Advanced AI.*
  Cooperative AI Foundation, Technical Report #1. arXiv:2502.14143.

### Networks

- Erdős, P. & Rényi, A. (1959). On random graphs I. *Publicationes Mathematicae Debrecen* 6, 290–297.
- Barabási, A.-L. & Albert, R. (1999). Emergence of scaling in random networks. *Science* 286(5439),
  509–512.
- Santos, F. C. & Pacheco, J. M. (2005). Scale-free networks provide a unifying framework for the
  emergence of cooperation. *Physical Review Letters* 95, 098104.
- Yu, M., Wang, S., Zhang, G., et al. (2025). NetSafe: Exploring the topological safety of
  multi-agent system. *Findings of ACL 2025*, 2905–2938.
- Liu, Y., Zhang, G., Wang, K., Li, S., Pan, S. & An, B. (2026). Graph-augmented large language model
  agents: Current progress and future prospects. *IEEE Intelligent Systems* 41(2), 45–55.

### Imitation update rule

- Hauert, C. & Doebeli, M. (2004). Spatial structure often inhibits the evolution of cooperation
  in the snowdrift game. *Nature* 428, 643–646.
- Gintis, H. (2000). *Game Theory Evolving.* Princeton University Press.

### Particle swarm optimization (swarm extensions)

- Pal, S., Wang, F. Y. & Buehler, M. J. (2026). SwarmWorld: Stigmergic technological evolution
  in societies of language-model agents. arXiv:2608.26081. *(Motivated the swarm extensions and the stigmergy extension.)*
- Kennedy, J. & Eberhart, R. (1995). Particle swarm optimization. *Proceedings of ICNN'95*,
  1942–1948.
- Shi, Y. & Eberhart, R. (1998). A modified particle swarm optimizer. *IEEE International
  Conference on Evolutionary Computation*, 69–73.
- Eberhart, R. C. & Shi, Y. (2000). Comparing inertia weights and constriction factors in particle
  swarm optimization. *Proceedings of the 2000 Congress on Evolutionary Computation*, 84–88.
- Clerc, M. & Kennedy, J. (2002). The particle swarm — explosion, stability, and convergence in a
  multidimensional complex space. *IEEE Transactions on Evolutionary Computation* 6(1), 58–73.
- Kennedy, J. (1999). Small worlds and mega-minds: effects of neighborhood topology on particle
  swarm performance. *Proceedings of the 1999 Congress on Evolutionary Computation.*
- Kennedy, J. & Mendes, R. (2002). Population structure and particle swarm performance.
  *Proceedings of the 2002 Congress on Evolutionary Computation.*
- Carlisle, A. & Dozier, G. (2000). Adapting particle swarm optimization to dynamic environments.
  *Proceedings of ICAI 2000.*
- Hu, X. & Eberhart, R. C. (2002). Adaptive particle swarm optimization: detection and response to
  dynamic systems. *Proceedings of the 2002 Congress on Evolutionary Computation.*

### Open-source game theory

- Critch, A., Dennis, M. & Russell, S. (2022). Cooperative and uncooperative institution designs:
  Surprises and problems in open-source game theory. arXiv:2208.07006. *(Main paper for this
  extension.)*
- Sistla, S. & Kleiman-Weiner, M. (2026). Evaluating LLMs in Open-Source Games. *Advances in Neural
  Information Processing Systems* 38, 104032–104063.
- Barasz, M., Christiano, P., Fallenstein, B., Herreshoff, M., LaVictoire, P. & Yudkowsky, E.
  (2014). Robust cooperation in the Prisoner's Dilemma: Program equilibrium via provability logic.
  arXiv:1401.5577.
- LaVictoire, P., Fallenstein, B., Yudkowsky, E., Barasz, M., Christiano, P. & Herreshoff, M.
  (2014). Program equilibrium in the prisoner's dilemma via Löb's theorem. *AAAI Workshop on
  Multiagent Interaction without Prior Coordination.*
- Tennenholtz, M. (2004). Program equilibrium. *Games and Economic Behavior* 49(2), 363–373.
- Critch, A. (2019). A parametric, resource-bounded generalization of Löb's theorem, and a robust
  cooperation criterion for open-source game theory. *Journal of Symbolic Logic* 84(4), 1368–1381.
- Kalai, A. T., Kalai, E., Lehrer, E. & Samet, D. (2010). A commitment folk theorem. *Games and
  Economic Behavior* 69(1), 127–137.
