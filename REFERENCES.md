# References

One list for the replication and all its extensions. Under each reference:

- **Used in:** Base (the replication in the root folder), Swarm learning, Swarm topology,
  Open source or Stigmergy.
- **Why:** what we take from it.

## Base paper

- Santos, F. C., Pacheco, J. M. & Lenaerts, T. (2006). Evolutionary dynamics of social dilemmas
  in structured heterogeneous populations. *PNAS* 103(9), 3490–3494.
  https://doi.org/10.1073/pnas.0508201103
  - **Used in:** all.
  - **Why:** the model, the four networks, the update rule and the (T, S) heatmaps of Figs. 2–3.

## Foundations and framing

- Nowak, M. A. (2006). Five rules for the evolution of cooperation. *Science* 314(5805),
  1560–1563. https://doi.org/10.1126/science.1133755
  - **Used in:** all.
  - **Why:** network reciprocity is one of the five rules. It's the mechanism behind the base
    paper's topology effect, and the extensions test it under other learning rules.

- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). John Wiley & Sons.
  https://www.wiley.com/en-us/An+Introduction+to+MultiAgent+Systems%2C+2nd+Edition-p-9780470519462
  - **Used in:** all (framing).
  - **Why:** standard textbook definition of agents and multi-agent systems. Frames the
    population as a multi-agent system: autonomous agents, each acting on local information,
    whose interactions produce the collective outcome (here, the level of cooperation).

- Pedreschi, D., Pappalardo, L., Ferragina, E., et al. (2025). Human-AI coevolution.
  *Artificial Intelligence* 339, 104244. https://doi.org/10.1016/j.artint.2024.104244
  - **Used in:** extensions.
  - **Why:** PhD framing: humans and AI shaping each other in feedback loops. Motivates comparing
    different learning rules within one population.

- Hammond, L., Chan, A., Clifton, J., et al. (2025). *Multi-Agent Risks from Advanced AI.*
  Cooperative AI Foundation, Technical Report #1. arXiv:2502.14143.
  https://arxiv.org/abs/2502.14143
  - **Used in:** extensions.
  - **Why:** PhD framing: risks from interacting AI agents, including cooperation failures.
    Motivates asking whether AI-style learners keep the network reciprocity that human-style
    imitation relies on.

## Networks

- Erdős, P. & Rényi, A. (1959). On random graphs I. *Publicationes Mathematicae Debrecen* 6,
  290–297. https://doi.org/10.5486/PMD.1959.6.3-4.12
  - **Used in:** Base, Swarm topology.
  - **Why:** foundational random-graph model. `network.py`'s `single_scale` uses its Poisson
    degree distribution (configuration model on a Poisson degree sequence). That's the
    homogeneous baseline.

- Barabási, A.-L. & Albert, R. (1999). Emergence of scaling in random networks. *Science*
  286(5439), 509–512. https://doi.org/10.1126/science.286.5439.509
  - **Used in:** Base, all extensions.
  - **Why:** preferential attachment, used for `scale_free`.

- Santos, F. C. & Pacheco, J. M. (2005). Scale-free networks provide a unifying framework for
  the emergence of cooperation. *Physical Review Letters* 95, 098104.
  https://doi.org/10.1103/PhysRevLett.95.098104
  - **Used in:** Base, all extensions.
  - **Why:** the first paper to show scale-free networks promote cooperation. Santos et al.
    2006 builds on it. It also explains the "cooperator clusters anchored on hubs" mechanism
    that Swarm topology found again at c1=0.

- Yu, M., Wang, S., Zhang, G., Mao, J., Yin, C., Liu, Q., Wang, K., Wen, Q. & Wang, Y. (2025).
  NetSafe: Exploring the topological safety of multi-agent system. In *Findings of the
  Association for Computational Linguistics: ACL 2025*, 2905–2938.
  https://doi.org/10.18653/v1/2025.findings-acl.150
  - **Used in:** Swarm topology, extensions (framing).
  - **Why:** the same question as ours, "does network topology change the collective
    outcome?", asked for LLM agents instead of game players. The agents update each round by
    reading their neighbours' answers. That's like imitation: behaviour spreads along edges.
    The result points the other way from Santos: highly connected, hub-centred systems (star,
    complete) spread misinformation, bias and harmful content fastest, and larger systems are
    more vulnerable too ("Security Bottleneck"). Sparse ones (chain, cycle) are safest.
    Together with the base paper, this means hubs amplify whatever spreads, whether that's
    cooperation or an attack. Differences: small hand-built graphs, no game or payoffs, and
    no evolution.

- Liu, Y., Zhang, G., Wang, K., Li, S., Pan, S. & An, B. (2026). Graph-augmented large language model
  agents: Current progress and future prospects. *IEEE Intelligent Systems* 41(2), 45–55.
  https://doi.org/10.1109/MIS.2025.3642667
  - **Used in:** extensions (framing).
  - **Why:** a position paper surveying LLM multi-agent systems as graphs, where agents are
    nodes and communication links are edges. Its multi-agent section makes the same point as
    this repo from the AI-engineering side: topology is a design choice that changes what the
    system does. Three findings are relevant. Denser graphs don't reliably perform better
    (MacNet tests chain, star, tree, random and complete graphs). Sparse communication can
    beat dense (AgentPrune, sparse multi-agent debate). And topology shapes how harmful
    information spreads (NetSafe, G-Safeguard). It places NetSafe in the wider literature.
    Differences: a survey with no model or experiment of its own, no game or payoffs, and no
    evolution.

## Imitation update rule (`update_rule.py`)

Santos et al. 2006 (Methods, p. 3493) call their rule the "finite population analog of
replicator dynamics (18, 30)", which "typically models cultural evolution, in which individuals
tend to imitate the strategies of those performing better." Refs 18 and 30:

- Hauert, C. & Doebeli, M. (2004). Spatial structure often inhibits the evolution of
  cooperation in the snowdrift game. *Nature* 428, 643–646.
  https://doi.org/10.1038/nature02360
  - **Used in:** Base, Swarm learning.
  - **Why:** same pairwise-comparison imitation rule on structured populations.

- Gintis, H. (2000). *Game Theory Evolving.* Princeton University Press.
  https://archive.org/details/gametheoryevolvi0000gint
  - **Used in:** Base, Swarm learning.
  - **Why:** textbook source for imitation dynamics converging to the replicator dynamics.

## Particle swarm optimization (`swarm_update_rule.py`)

### Motivation

- Pal, S., Wang, F. Y. & Buehler, M. J. (2026). SwarmWorld: Stigmergic technological evolution
  in societies of language-model agents. arXiv:2608.26081. https://arxiv.org/abs/2608.26081
  - **Used in:** Swarm learning, Swarm topology, Stigmergy.
  - **Why:** the paper that prompted using PSO here. Its introduction places PSO in the
    swarm-intelligence lineage ("shares individual and population experience"). Related framing
    only: its LLM agents build technology in a shared world, with no social dilemma and no PSO
    update, so it is not a source for the PSO model or the results. It is the source of the
    Stigmergy extension's idea: about 95% of first reuse among its agents began by observing
    artifacts left in the world, not by direct contact.

### Core PSO

- Kennedy, J. & Eberhart, R. (1995). Particle swarm optimization. *Proceedings of ICNN'95,
  International Conference on Neural Networks*, vol. 4, 1942–1948.
  https://doi.org/10.1109/ICNN.1995.488968
  - **Used in:** Swarm learning, Swarm topology.
  - **Why:** position + velocity per particle. The cognitive term (pull toward the personal
    best, c1) and the social term (pull toward the neighbourhood best, c2).

- Shi, Y. & Eberhart, R. (1998). A modified particle swarm optimizer. *IEEE International
  Conference on Evolutionary Computation*, 69–73. https://doi.org/10.1109/ICEC.1998.699146
  - **Used in:** Swarm learning, Swarm topology.
  - **Why:** the inertia weight w (we use 0.7).

- Clerc, M. & Kennedy, J. (2002). The particle swarm — explosion, stability, and convergence
  in a multidimensional complex space. *IEEE Transactions on Evolutionary Computation* 6(1),
  58–73. https://doi.org/10.1109/4235.985692
  - **Used in:** Swarm learning, Swarm topology.
  - **Why:** the stability analysis behind the standard PSO settings (w, c1, c2). A particle keeps oscillating between
    its personal best and its neighbourhood best while they disagree. That fits the
    velocity-test finding: with any c1 > 0, agents never stop moving.

### Local-best PSO and swarm topology

- Kennedy, J. (1999). Small worlds and mega-minds: effects of neighborhood topology on
  particle swarm performance. *Proceedings of the 1999 Congress on Evolutionary Computation.*
  https://doi.org/10.1109/CEC.1999.785509
  - **Used in:** Swarm learning, Swarm topology.
  - **Why:** "local best" PSO, where each particle follows the best of its graph neighbours.
    Closest prior work on whether topology matters for a swarm: it varies the neighbourhood
    graph and measures optimization performance. We measure cooperation instead.

- Kennedy, J. & Mendes, R. (2002). Population structure and particle swarm performance.
  *Proceedings of the 2002 Congress on Evolutionary Computation.*
  https://doi.org/10.1109/CEC.2002.1004493
  - **Used in:** Swarm learning, Swarm topology.
  - **Why:** same question as Kennedy (1999) on more graph types. It also explains the
    complete-graph caveat: on a complete graph, local best becomes global best.

## Open-source game theory (`programs.py`)

- Critch, A., Dennis, M. & Russell, S. (2022). Cooperative and uncooperative institution
  designs: Surprises and problems in open-source game theory. arXiv:2208.07006.
  https://arxiv.org/abs/2208.07006
  - **Used in:** Open source (main paper).
  - **Why:**
    - CUPOD(k) ("Cooperate Unless Proof Of Defection") and DUPOC(k) ("Defect Unless Proof
      Of Cooperation"), Section 2.
    - Prop. 3.1: CUPOD never exploits. Prop. 3.2: DUPOC is never exploited.
    - Thm. 3.4: CUPOD(k) vs CUPOD(k) → (D,D) for large k. Thm. 3.7: DUPOC(k) vs DUPOC(k) →
      (C,C) for large k. Both via the parametric bounded Löb theorem (PBLT).
    - Section 3.5: DUPOCs reward legible cooperation.
    - Open Problem 2: when does a population containing DUPOCs evolve so that everyone
      rewards legible cooperation?
    - Open Problem 3: DUPOC(k) vs CUPOD(k), conjectured (D,C), unsolved.
    - Open Problem 9: does a bounded PrudentBot exist? If so, study population dynamics
      among CooperateBots, DefectBots, DUPOCs and PrudentBots, with proof-search cost in the
      payoffs.

- Sistla, S. & Kleiman-Weiner, M. (2026). Evaluating LLMs in Open-Source Games. *Advances in
  Neural Information Processing Systems* 38, 104032–104063. arXiv:2512.00371.
  https://arxiv.org/abs/2512.00371
  - **Used in:** Open source.
  - **Why:** the closest recent work to this extension. LLMs write the programs themselves in
    open-source games (Iterated Prisoner's Dilemma and the Coin Game). The strategies are
    studied one-on-one and under replicator dynamics in a well-mixed population. Differences:
    their programs are LLM-written, not provability-logic bots; their population has no
    network; and they don't put a cost on reading code. Our extension adds both network
    structure and a proof cost.

- Barasz, M., Christiano, P., Fallenstein, B., Herreshoff, M., LaVictoire, P. & Yudkowsky, E.
  (2014). Robust cooperation in the Prisoner's Dilemma: Program equilibrium via provability
  logic. arXiv:1401.5577. https://arxiv.org/abs/1401.5577
  - **Used in:** Open source.
  - **Why:** FairBot, PrudentBot, CliqueBot, CooperateBot, DefectBot and their pairwise
    outcomes (the outcome table).

- Tennenholtz, M. (2004). Program equilibrium. *Games and Economic Behavior* 49(2), 363–373.
  - **Used in:** Open source.
  - **Why:** defines program equilibrium.

- Critch, A. (2019). A parametric, resource-bounded generalization of Löb's theorem, and a
  robust cooperation criterion for open-source game theory. *Journal of Symbolic Logic*
  84(4), 1368–1381.
  - **Used in:** Open source.
  - **Why:** the bounded Löb theorem (PBLT) behind Thms. 3.4 and 3.7.

- Kalai, A. T., Kalai, E., Lehrer, E. & Samet, D. (2010). A commitment folk theorem. *Games
  and Economic Behavior* 69(1), 127–137.
  - **Used in:** Open source.
  - **Why:** background.

### Other resources

- Math for AI Safety — Open-source game theory.
  https://mathforaisafety.org/research/open-source-game-theory
  - **Why:** plain-language intro: FairBot, Löb's theorem, DUPOC/CUPOD, bounded FairBot(k).

- [github.com/klao/provability](https://github.com/klao/provability)
  - **Why:** Haskell tool that computes outcomes of unbounded modal (provability-logic)
    agents. Could double-check the outcome table.
