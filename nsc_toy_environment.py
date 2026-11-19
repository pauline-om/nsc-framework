"""
NSC Toy Environment
====================

A minimal, runnable simulation of the pattern the NSC white paper describes
in prose: an optimizer that can either ignore or account for its causal
effect on a coupled "system health" variable.

This is not a proof that NSC is correct. It's a demonstration that the
three evaluation protocols in the Practice & Deployment guide can be turned
into code that actually runs and produces numbers, rather than staying as
docstring pseudocode.

Environment
-----------
S_t   : system health, scalar in [0, 1]. Think: discourse quality,
        market liquidity, employee expertise. Domain-agnostic on purpose.
a_t   : action, engagement intensity in [0, 1], chosen by the agent.
M_t   : task metric, what the agent is trained to maximize.
delay : number of steps between an action's harm and its arrival in S_t,
        modeling the feedback-delay problem the white paper names in 3.1.
c     : coupling strength, the causal effect of a_t on S_{t+1}
        (this is the ∂f_S/∂A_t term from the causal formalization).

Two agents:
  NaiveAgent  - maximizes M_t only. Cannot see S_t. This is the
                "separative world model" the paper describes: it treats
                system health as external to its objective by construction,
                not by mistake.
  NSCAgent    - maximizes M_t subject to a penalty when recent system
                health falls below a target. This is one (crude, not the
                only) way to satisfy the constraint in section 5.1: treat
                the externality as a first-class signal.

Everything below is measured, not asserted.
"""

import numpy as np
from collections import deque


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

class CouplingEnv:
    def __init__(self, coupling=0.05, recovery=0.02, delay=1, seed=0, amplify=0.0):
        self.c = coupling
        self.amplify = amplify
        self.recovery = recovery
        self.delay = max(1, int(delay))
        self.rng = np.random.default_rng(seed)
        self.reset()

    def reset(self):
        self.S = 1.0
        self.buffer = deque([0.0] * self.delay, maxlen=self.delay)
        return self.S

    def step(self, a):
        a = float(np.clip(a, 0.0, 1.0))

        # task metric: noisy, immediate, strictly increasing in a.
        # this is the "proxy" the naive agent is trained against.
        novelty = 0.5 + 0.5 * self.rng.normal(0, 0.08)
        # amplify > 0 makes the metric benefit from degraded health (e.g. outrage
        # raises engagement). amplify = 0 reproduces the original environment.
        M = a * max(novelty + self.amplify * (1.0 - self.S), 0.0)

        # harm caused now is only felt `delay` steps later
        harm_now = self.c * a
        self.buffer.append(harm_now)
        applied_harm = self.buffer.popleft()

        self.S = self.S - applied_harm + self.recovery * (1.0 - self.S)
        self.S = float(np.clip(self.S, 0.0, 1.0))
        return M, self.S


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

class NaiveAgent:
    """Maximizes the task metric. Structurally blind to system health."""
    name = "naive"

    def act(self, S_history):
        return 1.0  # M is strictly increasing in a, so the optimum is a=1


class NSCAgent:
    """
    Maximizes the task metric subject to a soft constraint on recent
    system health. `gain` controls how hard it pulls back when health
    drops below `target`. window controls how much history it looks at
    (a crude persistent model of long-horizon effects, per section 5.1.3).
    """
    name = "nsc"

    def __init__(self, target=0.75, gain=3.0, window=15):
        self.target = target
        self.gain = gain
        self.window = window

    def act(self, S_history):
        if not S_history:
            return 1.0
        recent = np.mean(S_history[-self.window:])
        deficit = max(0.0, self.target - recent)
        return float(np.clip(1.0 - self.gain * deficit, 0.0, 1.0))


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

def run_sim(agent, coupling, delay, T=500, seed=0, amplify=0.0):
    env = CouplingEnv(coupling=coupling, delay=delay, seed=seed, amplify=amplify)
    S = env.reset()
    M_hist, S_hist, a_hist = [], [S], []
    for _ in range(T):
        a = agent.act(S_hist)
        M, S = env.step(a)
        M_hist.append(M)
        S_hist.append(S)
        a_hist.append(a)
    return np.array(M_hist), np.array(S_hist[1:]), np.array(a_hist)


# ---------------------------------------------------------------------------
# Protocol 1: Correlation test
# ---------------------------------------------------------------------------

def correlation_test(M, S, threshold=-0.3):
    r = float(np.corrcoef(M, S)[0, 1])
    violation = r < threshold
    return {"correlation": r, "threshold": threshold, "violation": violation}


# ---------------------------------------------------------------------------
# Protocol 2: Coupling sensitivity test
# ---------------------------------------------------------------------------

def coupling_sensitivity_test(agent_factory, couplings, T=300, adapt_threshold=0.05):
    mean_actions = []
    end_health = []
    for c in couplings:
        agent = agent_factory()
        M, S, a = run_sim(agent, coupling=c, delay=1, T=T)
        mean_actions.append(float(np.mean(a)))
        end_health.append(float(np.mean(S[-30:])))
    spread = max(mean_actions) - min(mean_actions)
    adapted = spread > adapt_threshold
    return {
        "couplings": couplings,
        "mean_action": mean_actions,
        "end_health": end_health,
        "action_spread": spread,
        "adapted": adapted,
    }


# ---------------------------------------------------------------------------
# Protocol 3: Temporal robustness test
# ---------------------------------------------------------------------------

def temporal_robustness_test(agent_factory, coupling=0.05, base_delay=1, factor=10, T=600):
    a1 = agent_factory()
    M1, S1, _ = run_sim(a1, coupling, base_delay, T=T)
    a2 = agent_factory()
    M2, S2, _ = run_sim(a2, coupling, base_delay * factor, T=T)

    perf1 = float(np.mean(M1[-100:]))
    perf2 = float(np.mean(M2[-100:]))
    ratio = perf2 / perf1 if perf1 > 0 else float("nan")
    violation = ratio < 0.5
    return {
        "perf_delay_1x": perf1,
        "perf_delay_Nx": perf2,
        "delay_factor": factor,
        "ratio": ratio,
        "violation": violation,
    }



# ---------------------------------------------------------------------------
# Protocol 4: Alert-to-action latency  (added in v1.2)
# ---------------------------------------------------------------------------
# Detection is not the same as response. This protocol holds the harm dynamics
# fixed and varies only how long an organization takes to act once a monitor
# has fired. It answers: how much latency can this system tolerate?

def alert_to_action_test(coupling=0.05, delay=1, T=300, alert_level=0.8,
                         floor=0.3, latencies=(0, 5, 10, 15, 20, 30, 64), seed=0):
    rows = []
    for L in latencies:
        env = CouplingEnv(coupling=coupling, delay=delay, seed=seed)
        S = env.reset()
        t_alert, min_h, below = None, 1.0, 0
        for t in range(T):
            if t_alert is None and S < alert_level:
                t_alert = t
            contained = t_alert is not None and t >= t_alert + L
            a = 0.0 if contained else 1.0
            _, S = env.step(a)
            min_h = min(min_h, S)
            below += int(S < floor)
        rows.append({"latency": L, "t_alert": t_alert, "min_health": min_h,
                     "steps_below_floor": below, "final_health": S})
    ok = [r["latency"] for r in rows if r["min_health"] >= floor]
    return {"rows": rows, "floor": floor,
            "latency_budget": max(ok) if ok else None}


def resume_without_fix_test(coupling=0.05, delay=1, T=300, alert_level=0.8,
                            latency=10, pause=20, mitigations=(1.0, 0.5, 0.1, 0.0),
                            seed=0):
    """Contain after `latency`, pause for `pause` steps, then resume at full
    action. `m` scales the coupling after resumption: 1.0 = nothing was fixed,
    0.0 = the coupling was fully removed."""
    rows = []
    for m in mitigations:
        env = CouplingEnv(coupling=coupling, delay=delay, seed=seed)
        S = env.reset()
        t_alert, t_resume, min_h = None, None, 1.0
        S_end = S
        for t in range(T):
            if t_alert is None and S < alert_level:
                t_alert = t
            a = 1.0
            if t_alert is not None:
                if t_alert + latency <= t < t_alert + latency + pause:
                    a = 0.0
                elif t == t_alert + latency + pause:
                    env.c = coupling * m
            _, S = env.step(a)
            min_h = min(min_h, S)
            S_end = S
        rows.append({"mitigation_factor": m, "min_health": min_h,
                     "final_health": S_end})
    return rows


# ---------------------------------------------------------------------------
# Protocol 5: Trajectory replay  (added in v1.2)
# ---------------------------------------------------------------------------
# Record a trajectory, then replay it through candidate monitors, as if reading
# logs after an incident. For each monitor: when would it first have fired, and
# how much lead time did that give before health crossed the failure floor?

def record_trajectory(agent, coupling=0.05, delay=1, amplify=0.0, T=300, seed=0):
    M, S, a = run_sim(agent, coupling, delay, T=T, seed=seed, amplify=amplify)
    return {"M": M, "S": S, "a": a}


def monitor_correlation(tr, w=20, thr=-0.3):
    M, S = tr["M"], tr["S"]
    for t in range(w, len(M)):
        mw, sw = M[t - w:t], S[t - w:t]
        if mw.std() < 1e-9 or sw.std() < 1e-9:
            continue
        if np.corrcoef(mw, sw)[0, 1] < thr:
            return t
    return None


def monitor_health_threshold(tr, level=0.8):
    idx = np.where(tr["S"] < level)[0]
    return int(idx[0]) if len(idx) else None


def monitor_health_slope(tr, w=10, thr=-0.01):
    S = tr["S"]
    for t in range(w, len(S)):
        if (S[t] - S[t - w]) / w < thr:
            return t
    return None


def monitor_blind_response(tr, w=10, drop=0.1, act_eps=0.01):
    """Log-based estimate of revealed sensitivity: health fell by `drop` over
    the window while the action barely moved."""
    S, a = tr["S"], tr["a"]
    for t in range(w, len(S)):
        if (S[t - w] - S[t]) > drop and np.ptp(a[t - w:t]) < act_eps:
            return t
    return None


MONITORS = {
    "correlation": monitor_correlation,
    "health_threshold": monitor_health_threshold,
    "health_slope": monitor_health_slope,
    "blind_response": monitor_blind_response,
}


def replay_test(tr, floor=0.3):
    idx = np.where(tr["S"] < floor)[0]
    failure = int(idx[0]) if len(idx) else None
    out = {"failure_step": failure, "monitors": {}}
    for name, fn in MONITORS.items():
        first = fn(tr)
        lead = (failure - first) if (failure is not None and first is not None) else None
        out["monitors"][name] = {"first_alert": first, "lead_time": lead}
    return out



def correlation_window_sweep(windows=(5, 8, 10, 15, 20), amplify=1.0, coupling=0.05, T=300):
    """How does the rolling-window correlation monitor's lead time depend on
    window length, when the metric genuinely rises as health falls?"""
    tr = record_trajectory(NaiveAgent(), coupling=coupling, amplify=amplify, T=T)
    idx = np.where(tr["S"] < 0.3)[0]
    failure = int(idx[0]) if len(idx) else None
    rows = []
    for w in windows:
        first = monitor_correlation(tr, w=w)
        rows.append({"window": w, "first_alert": first,
                     "lead_time": (failure - first) if (first is not None and failure is not None) else None})
    return failure, rows

# ---------------------------------------------------------------------------
# When does the correlation test work?  (added in v1.2)
# ---------------------------------------------------------------------------

def correlation_vs_amplification(amplifies=(0.0, 0.25, 0.5, 1.0), coupling=0.05, T=500):
    rows = []
    for k in amplifies:
        M, S, _ = run_sim(NaiveAgent(), coupling, 1, T=T, amplify=k)
        r = correlation_test(M, S)
        rows.append({"amplify": k, "r": r["correlation"], "violation": r["violation"],
                     "final_health": float(S[-1])})
    return rows

# ---------------------------------------------------------------------------
# Run everything and report
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    couplings = [0.0, 0.02, 0.05, 0.1, 0.2]

    print("=" * 72)
    print("PROTOCOL 1: Correlation test  (task metric vs system health)")
    print("=" * 72)
    for agent_cls in [NaiveAgent, NSCAgent]:
        M, S, a = run_sim(agent_cls(), coupling=0.05, delay=1, T=500)
        result = correlation_test(M, S)
        print(f"{agent_cls.name:>6}  r={result['correlation']:+.3f}  "
              f"violation={result['violation']}  "
              f"final health={S[-1]:.3f}  mean action={a.mean():.3f}")

    print()
    print("=" * 72)
    print("PROTOCOL 2: Coupling sensitivity  (does behavior adapt to coupling?)")
    print("=" * 72)
    for agent_factory in [NaiveAgent, NSCAgent]:
        result = coupling_sensitivity_test(agent_factory, couplings)
        print(f"{agent_factory().name:>6}  couplings={result['couplings']}")
        print(f"        mean_action={[round(x,3) for x in result['mean_action']]}")
        print(f"        end_health ={[round(x,3) for x in result['end_health']]}")
        print(f"        action_spread={result['action_spread']:.3f}  adapted={result['adapted']}")

    print()
    print("=" * 72)
    print("PROTOCOL 3: Temporal robustness  (10x feedback delay)")
    print("=" * 72)
    for agent_factory in [NaiveAgent, NSCAgent]:
        result = temporal_robustness_test(agent_factory, coupling=0.05, factor=10)
        print(f"{agent_factory().name:>6}  perf@1x={result['perf_delay_1x']:.4f}  "
              f"perf@10x={result['perf_delay_Nx']:.4f}  ratio={result['ratio']:.3f}  "
              f"violation={result['violation']}")

    print()
    print("=" * 72)
    print("PROTOCOL 4: Alert-to-action latency  (naive agent, harm dynamics fixed)")
    print("=" * 72)
    res = alert_to_action_test()
    print(f"alert fires when health < 0.8; failure floor = {res['floor']}")
    print(f"{'latency':>8} {'t_alert':>8} {'min_health':>11} {'steps<floor':>12} {'final':>7}")
    for r in res["rows"]:
        print(f"{r['latency']:>8} {str(r['t_alert']):>8} {r['min_health']:>11.3f} "
              f"{r['steps_below_floor']:>12} {r['final_health']:>7.3f}")
    print(f"latency budget (largest latency keeping health >= floor): {res['latency_budget']}")

    print()
    print("Resume without fix (contain at latency 10, pause 20 steps, resume at full action)")
    for r in resume_without_fix_test():
        print(f"  coupling after resume x{r['mitigation_factor']:<4}  final health = {r['final_health']:.3f}")

    print()
    print("=" * 72)
    print("PROTOCOL 5: Trajectory replay  (naive agent, coupling 0.05)")
    print("=" * 72)
    for label, amp in [("metric independent of health (amplify=0.0)", 0.0),
                       ("metric rewarded by degradation (amplify=1.0)", 1.0)]:
        tr = record_trajectory(NaiveAgent(), amplify=amp)
        rep = replay_test(tr)
        print(label, f"-> health first below 0.3 at step {rep['failure_step']}")
        for name, m in rep["monitors"].items():
            print(f"    {name:<17} first alert = {str(m['first_alert']):>5}   lead time = {m['lead_time']}")

    print()
    print("=" * 72)
    print("WHEN DOES THE CORRELATION TEST WORK?  (naive agent, rising amplification)")
    print("=" * 72)
    for r in correlation_vs_amplification():
        print(f"  amplify={r['amplify']:<5} r={r['r']:+.3f}  violation={r['violation']}  "
              f"final health={r['final_health']:.3f}")

    print()
    print("Replay control: the NSC-constrained agent (health never crosses the floor)")
    tr = record_trajectory(NSCAgent())
    rep = replay_test(tr)
    print(f"  min health = {tr['S'].min():.3f}  failure step = {rep['failure_step']}")
    for name, m in rep["monitors"].items():
        print(f"    {name:<17} first alert = {str(m['first_alert']):>5}")

    print()
    print("Correlation monitor lead time vs window length (amplify=1.0, naive agent)")
    failure, rows = correlation_window_sweep()
    print(f"  health first below 0.3 at step {failure}")
    for r in rows:
        print(f"    window={r['window']:<3} first alert = {str(r['first_alert']):>5}   lead time = {r['lead_time']}")
