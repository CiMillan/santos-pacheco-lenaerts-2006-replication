# Timing: current code vs. a vectorized prototype

How long the replication takes at reduced scale, and how long it would take at the paper's
scale (N = 10,000, 11,000 generations, 100 realizations per point, 5×5 (T, S) grid), for the
current code and for a quick vectorized prototype. One core of an Apple M5, 2026-09-24.

| Network | Current code, reduced scale (measured) | Current code, paper's scale (estimated) | Vectorized, paper's scale (estimated) |
|---|---|---|---|
| Complete | 6 min | ≈ 12 years | ≈ 40 min |
| Single-scale | 55 s | ≈ 4 days | ≈ 3 h |
| Random scale-free | 66 s | ≈ 4.5 days | ≈ 2 h |
| Barabási–Albert | 54 s | ≈ 4.5 days | ≈ 1.5 h |
| **All four** | **9 min** | **≈ 12 years** | **≈ 7 h** |

**Why the current code is slow.** It is written for reading, not speed: plain Python loops over
agents and neighbours, one function per file (see the root README). One generation at
N = 10,000 takes about 13 ms on the sparse networks. On the complete graph every agent has
9,999 neighbours, so the cost grows with N² and one generation takes about 14 s.

**The vectorized prototype** ([`vectorized_prototype.py`](vectorized_prototype.py)) runs the same
model with NumPy arrays: one sparse matrix product gives every agent's cooperating neighbours
at once, and the update rule is applied to all agents together. On the sparse networks one
generation takes 0.2–0.4 ms. On the complete graph it skips neighbours entirely: everyone plays
everyone, so payoffs depend only on how many cooperators there are, and one generation takes
0.09 ms. Running realizations on several cores in parallel would cut the times further.

**Checked.** Over 30 realizations at four (T, S) points, the prototype's cooperation levels match
the current code's within one standard error (e.g. 0.73 vs. 0.72 on Barabási–Albert at
$T=1.5$, $S=0$). See [`tests/test_02_check_prototype.txt`](tests/test_02_check_prototype.txt).

**Caveats.** Estimates, not full runs. The paper's own grid is finer than 5×5, so its real cost is
higher. The prototype is for timing only and is not used for any result in this repo.

Files: [`time_runs.py`](time_runs.py) (makes the table; raw output in
[`time_runs_output.txt`](time_runs_output.txt)), [`check_prototype.py`](check_prototype.py),
[`tests/`](tests/).
