# References

One list for the replication and all its extensions. Each entry says where it is used:
**Base** (the replication in the root folder), **Swarm learning**, **Swarm topology**,
**Open source**.

## Base paper

- Santos, F. C., Pacheco, J. M. & Lenaerts, T. (2006). Evolutionary dynamics of social
  dilemmas in structured heterogeneous populations. *PNAS* 103(9), 3490–3494.
  https://doi.org/10.1073/pnas.0508201103
  — **All.** The model, the four networks, the update rule and the (T, S) heatmaps of Figs. 2–3.

## Foundations and framing

- Nowak, M. A. (2006). Five rules for the evolution of cooperation. *Science* 314(5805),
  1560–1563. https://doi.org/10.1126/science.1133755
  — **All.** Network reciprocity is one of the five rules. It's the mechanism behind the base
  paper's topology effect, and the one the extensions test under other learning rules.
- Pedreschi, D., Pappalardo, L., Ferragina, E., et al. (2025). Human-AI coevolution.
  *Artificial Intelligence* 339, 104244. https://doi.org/10.1016/j.artint.2024.104244
  — **Extensions.** PhD framing: humans and AI shaping each other in feedback loops.
  Motivates comparing different learning rules within one population.
- Hammond, L., Chan, A., Clifton, J., et al. (2025). *Multi-Agent Risks from Advanced AI.*
  Cooperative AI Foundation, Technical Report #1. arXiv:2502.14143.
  https://arxiv.org/abs/2502.14143
  — **Extensions.** PhD framing: risks from interacting AI agents, including cooperation
  failures. Motivates asking whether AI-style learners keep the network reciprocity that
  human-style imitation relies on.

## Networks

- Erdős, P. & Rényi, A. (1959). On random graphs I. *Publicationes Mathematicae Debrecen* 6,
  290–297.
  — **Base, Swarm topology.** Foundational random-graph model. Its Poisson degree
  distribution is what `network.py`'s `single_scale` uses (configuration model on a Poisson
  degree sequence). That's the homogeneous baseline.
- Barabási, A.-L. & Albert, R. (1999). Emergence of scaling in random networks. *Science*
  286(5439), 509–512. https://doi.org/10.1126/science.286.5439.509
  — **Base, all extensions.** Preferential attachment, used for `scale_free`.
- Santos, F. C. & Pacheco, J. M. (2005). Scale-free networks provide a unifying framework
  for the emergence of cooperation. *Physical Review Letters* 95, 098104.
  https://doi.org/10.1103/PhysRevLett.95.098104
  — **Base, all extensions.** The first paper to show scale-free networks promote
  cooperation. Santos et al. 2006 builds on it. It also explains the "cooperator clusters
  anchored on hubs" mechanism that Swarm topology found again at c1=0.

## Imitation update rule (`update_rule.py`)

Santos et al. 2006 (Methods, p. 3493) call their rule the "finite population analog of
replicator dynamics (18, 30)", which "typically models cultural evolution, in which
individuals tend to imitate the strategies of those performing better." Refs 18 and 30:

- Hauert, C. & Doebeli, M. (2004). Spatial structure often inhibits the evolution of
  cooperation in the snowdrift game. *Nature* 428, 643–646.
  https://doi.org/10.1038/nature02360
  — **Base, Swarm learning.** Same pairwise-comparison imitation rule on structured
  populations.
- Gintis, H. (2000). *Game Theory Evolving.* Princeton University Press.
  — **Base, Swarm learning.** Textbook source for imitation dynamics converging to the
  replicator dynamics.

## Particle swarm optimization (`swarm_update_rule.py`)

- Kennedy, J. & Eberhart, R. (1995). Particle swarm optimization. *Proceedings of ICNN'95,
  International Conference on Neural Networks*, vol. 4, 1942–1948.
  https://doi.org/10.1109/ICNN.1995.488968
  — **Swarm learning, Swarm topology.** Position + velocity per particle. Cognitive
  (personal best, c1) and social (neighbourhood best, c2) terms.
- Shi, Y. & Eberhart, R. (1998). A modified particle swarm optimizer. *IEEE International
  Conference on Evolutionary Computation*, 69–73. https://doi.org/10.1109/ICEC.1998.699146
  — **Swarm learning, Swarm topology.** The inertia weight w (we use 0.7).
- Eberhart, R. C. & Shi, Y. (2000). Comparing inertia weights and constriction factors in
  particle swarm optimization. *Proceedings of the 2000 Congress on Evolutionary
  Computation*, 84–88. https://doi.org/10.1109/CEC.2000.870279
  — **Swarm learning.** Common defaults w ≈ 0.729, c1 = c2 ≈ 1.494. Our w=0.7, c1=c2=1.5 are a
  rounded version, not tuned.
- Clerc, M. & Kennedy, J. (2002). The particle swarm — explosion, stability, and convergence
  in a multidimensional complex space. *IEEE Transactions on Evolutionary Computation* 6(1),
  58–73. https://doi.org/10.1109/4235.985692
  — **Swarm learning, Swarm topology.** Stability analysis behind those defaults. A particle
  keeps oscillating between its personal best and its neighbourhood best while they disagree.
  That fits the velocity-test finding that with any c1 > 0, agents never stop moving.

### Local-best PSO and swarm topology

- Kennedy, J. (1999). Small worlds and mega-minds: effects of neighborhood topology on
  particle swarm performance. *Proceedings of the 1999 Congress on Evolutionary
  Computation.* https://doi.org/10.1109/CEC.1999.785509
- Kennedy, J. & Mendes, R. (2002). Population structure and particle swarm performance.
  *Proceedings of the 2002 Congress on Evolutionary Computation.*
  https://doi.org/10.1109/CEC.2002.1004493

  — **Swarm learning, Swarm topology.** "Local best" PSO: each particle follows the best of
  its graph neighbours. They vary the neighbourhood graph and measure optimization
  performance. We vary it and measure cooperation. On a complete graph, local best becomes
  global best.

### PSO in changing landscapes (background, not used in the code)

- Carlisle, A. & Dozier, G. (2000). Adapting particle swarm optimization to dynamic
  environments. *Proceedings of the International Conference on Artificial Intelligence
  (ICAI 2000).*
- Hu, X. & Eberhart, R. C. (2002). Adaptive particle swarm optimization: detection and
  response to dynamic systems. *Proceedings of the 2002 Congress on Evolutionary
  Computation.* https://doi.org/10.1109/CEC.2002.1004492

  — **Swarm learning.** Stale personal bests when the landscape changes: reset or re-evaluate
  the memory. That's the same problem found in Swarm learning's `CONCLUSIONS.txt` (stale
  defection windfalls). A starting point for a "decaying personal best" follow-up.

## Open-source game theory (`programs.py`)

- Critch, A., Dennis, M. & Russell, S. (2022). Cooperative and uncooperative institution
  designs: Surprises and problems in open-source game theory. arXiv:2208.07006.
  https://arxiv.org/abs/2208.07006
  — **Open source (main paper).** What we use:
  - CUPOD(k) ("Cooperate Unless Proof Of Defection") and DUPOC(k) ("Defect Unless Proof Of
    Cooperation"), Section 2.
  - Prop. 3.1: CUPOD never exploits. Prop. 3.2: DUPOC is never exploited.
  - Thm. 3.4: CUPOD(k) vs CUPOD(k) → (D,D) for large k. Thm. 3.7: DUPOC(k) vs DUPOC(k) → (C,C)
    for large k. Both via the parametric bounded Löb theorem (PBLT).
  - Section 3.5: DUPOCs reward legible cooperation.
  - Open Problem 2: when does a population containing DUPOCs evolve so that everyone rewards
    legible cooperation?
  - Open Problem 3: DUPOC(k) vs CUPOD(k), conjectured (D,C), unsolved.
  - Open Problem 9: does a bounded PrudentBot exist? If so, study population dynamics among
    CooperateBots, DefectBots, DUPOCs and PrudentBots, with proof-search cost in the payoffs.
- Sistla, S. & Kleiman-Weiner, M. (2026). Evaluating LLMs in open-source games. *Advances in
  Neural Information Processing Systems* 38, 104032–104063. arXiv:2512.00371.
  https://arxiv.org/abs/2512.00371
  — **Open source.** LLMs write the programs themselves in open-source games (Iterated
  Prisoner's Dilemma and the Coin Game). The resulting program strategies are studied one-on-one
  and under replicator dynamics in a well-mixed population. Closest recent work to this
  extension. Differences: their programs are LLM-written, not provability-logic bots; their
  population has no network; and they don't put a cost on reading code. Our extension adds
  both network structure and a proof cost.
- Math for AI Safety — Open-source game theory.
  https://mathforaisafety.org/research/open-source-game-theory
  — **Open source.** Plain-language intro: FairBot, Löb's theorem, DUPOC/CUPOD, bounded
  FairBot(k).
- Barasz, M., Christiano, P., Fallenstein, B., Herreshoff, M., LaVictoire, P. & Yudkowsky, E.
  (2014). Robust cooperation in the Prisoner's Dilemma: Program equilibrium via provability
  logic. arXiv:1401.5577. https://arxiv.org/abs/1401.5577
  — **Open source.** FairBot, PrudentBot, CliqueBot, CooperateBot, DefectBot and their
  pairwise outcomes (the outcome table).
- LaVictoire, P., Fallenstein, B., Yudkowsky, E., Barasz, M., Christiano, P. & Herreshoff, M.
  (2014). Program equilibrium in the prisoner's dilemma via Löb's theorem. *AAAI Workshop on
  Multiagent Interaction without Prior Coordination.* (Critch et al. ref [47].)
  — **Open source.** Outcome table.
- Tennenholtz, M. (2004). Program equilibrium. *Games and Economic Behavior* 49(2), 363–373.
  — **Open source.** Defines program equilibrium.
- Critch, A. (2019). A parametric, resource-bounded generalization of Löb's theorem, and a
  robust cooperation criterion for open-source game theory. *Journal of Symbolic Logic*
  84(4), 1368–1381.
  — **Open source.** The bounded Löb theorem (PBLT) behind Thms. 3.4 and 3.7.
- Kalai, A. T., Kalai, E., Lehrer, E. & Samet, D. (2010). A commitment folk theorem. *Games
  and Economic Behavior* 69(1), 127–137.
  — **Open source.** Background.
- [github.com/klao/provability](https://github.com/klao/provability)
  — **Open source.** Haskell tool that computes outcomes of unbounded modal
  (provability-logic) agents. Could double-check the outcome table.
