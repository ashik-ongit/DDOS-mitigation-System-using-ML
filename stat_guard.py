# ---------------------------------------------------------
# ShieldX Statistical Guard
# Hybrid layer used along with ML detector
# ---------------------------------------------------------

def stat_check(feature):
    """
    Feature format:
    [ rps,
      burst,
      unique_path_ratio,
      avg_gap,
      error_rate ]
    """

    rps, burst, uniq, gap, err = feature


    # -----------------------------------------------------
    # 1) Extreme Volume Rule
    # -----------------------------------------------------
    # Any single source crossing this is almost certainly flood
    if rps > 30:
        return True


    # -----------------------------------------------------
    # 2) Burst Attack Rule
    # -----------------------------------------------------
    # Many requests in one second to same endpoint
    if burst > 15 and uniq < 0.35:
        return True


    # -----------------------------------------------------
    # 3) Non‑Human Speed Rule
    # -----------------------------------------------------
    # Humans cannot generate requests with <50ms gap continuously
    if gap < 0.05 and rps > 10:
        return True


    # -----------------------------------------------------
    # 4) Error Explosion Rule
    # -----------------------------------------------------
    # Bots often trigger large 4xx/5xx ratios
    if err > 0.40:
        return True


    # -----------------------------------------------------
    # 5) Low Diversity Flood
    # -----------------------------------------------------
    # Hitting same path again and again
    if uniq < 0.20 and rps > 12:
        return True


    # -----------------------------------------------------
    # 6) Slow‑rate but consistent attack
    # -----------------------------------------------------
    # Medium RPS but very regular interval = tool traffic
    if 8 < rps < 15 and gap < 0.08:
        return True


    return False
