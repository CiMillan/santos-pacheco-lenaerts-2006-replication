"""The program menu and its outcome table -- open-source game theory.
Each agent holds a PROGRAM instead of C/D. When x meets y, x plays
ACTION[(x's program, y's program)]. Outcomes are worked out once, from
Barasz et al. (2014), arXiv:1401.5577 -- page numbers are that PDF's.
"Definition" = follows directly from the program's pseudocode.
"Unexploitable" = FairBot/PrudentBot never play C against an opponent that
plays D against them (p. 7 for FairBot, Theorem 3.2 p. 9 for PrudentBot)."""

PROGRAMS = ["CooperateBot", "DefectBot", "CliqueBot", "FairBot", "PrudentBot"]

# (my program, opponent's program) -> my action
ACTION = {
    # CooperateBot: always C (Algorithm 1, p. 6) -- definition.
    ("CooperateBot", "CooperateBot"): "C",
    ("CooperateBot", "DefectBot"): "C",
    ("CooperateBot", "CliqueBot"): "C",
    ("CooperateBot", "FairBot"): "C",
    ("CooperateBot", "PrudentBot"): "C",
    # DefectBot: always D (Algorithm 2, p. 6) -- definition.
    ("DefectBot", "CooperateBot"): "D",
    ("DefectBot", "DefectBot"): "D",
    ("DefectBot", "CliqueBot"): "D",
    ("DefectBot", "FairBot"): "D",
    ("DefectBot", "PrudentBot"): "D",
    # CliqueBot: C only against an exact copy of itself (Algorithm 3, p. 6)
    # -- definition. All CliqueBots in the simulation are exact copies.
    ("CliqueBot", "CooperateBot"): "D",
    ("CliqueBot", "DefectBot"): "D",
    ("CliqueBot", "CliqueBot"): "C",
    ("CliqueBot", "FairBot"): "D",
    ("CliqueBot", "PrudentBot"): "D",
    # FairBot: C iff it can prove the opponent plays C against it
    # (Algorithm 4, p. 7).
    ("FairBot", "CooperateBot"): "C",  # p. 8: "cooperating even with CooperateBot"
    ("FairBot", "DefectBot"): "D",     # unexploitable; also p. 9: PA+1 proves FB(DB)=D
    ("FairBot", "CliqueBot"): "D",     # unexploitable: CliqueBot plays D against FairBot
    ("FairBot", "FairBot"): "C",       # Theorem 3.1, p. 8 (Loeb)
    ("FairBot", "PrudentBot"): "C",    # Theorem 3.2, p. 9
    # PrudentBot: C iff it proves the opponent plays C against it AND
    # (one level up) proves the opponent plays D against DefectBot
    # (Algorithm 5, p. 9).
    ("PrudentBot", "CooperateBot"): "D",  # Theorem 3.2, p. 9
    ("PrudentBot", "DefectBot"): "D",     # p. 9: PA+1 proves PB(DB)=D
    ("PrudentBot", "CliqueBot"): "D",     # unexploitable: CliqueBot plays D against PrudentBot
    ("PrudentBot", "FairBot"): "C",       # Theorem 3.2, p. 9
    ("PrudentBot", "PrudentBot"): "C",    # Theorem 3.2, p. 9
}


def outcome(prog_x, prog_y):
    """Returns (x's action, y's action) when a prog_x agent meets a prog_y agent."""
    return ACTION[(prog_x, prog_y)], ACTION[(prog_y, prog_x)]
