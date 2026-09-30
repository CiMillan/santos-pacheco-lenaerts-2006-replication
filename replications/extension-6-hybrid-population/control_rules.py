"""Control rules for the AI agents -- stubborn players that never learn and
never imitate. Used to ask: is the hub collapse caused by Q-learning, or
just by hubs that never imitate? (design choice, no source; see ARCHITECTURE.txt)"""

CONTROL_RULES = ["always_defect", "always_cooperate", "coin_flip"]


def fixed_action(rule, rng):
    """
    rule: "always_defect"    -- plays D every generation;
          "always_cooperate" -- plays C every generation;
          "coin_flip"        -- C or D with probability 1/2, ignoring payoffs.
    Returns "C" or "D". Only "coin_flip" draws from rng.
    """
    if rule == "always_defect":
        return "D"
    if rule == "always_cooperate":
        return "C"
    if rule == "coin_flip":
        return "C" if rng.random() < 0.5 else "D"
    raise ValueError(f"unknown rule: {rule}")
