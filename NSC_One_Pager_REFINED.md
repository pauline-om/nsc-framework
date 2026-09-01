# The Non-Separability Constraint (NSC)

## A Unifying Lens on AI Alignment Failures

### What Problem Does NSC Address?

Many AI alignment failures occur when systems optimize successfully according to their objective while producing harmful or destabilizing effects at the system level. These failures are often treated as distinct problems (Goodhart's Law, reward hacking, instrumental convergence, mesa-optimization), but they share a common root:

**The assumption that the optimizer is separable from the system it affects.**

The Non-Separability Constraint (NSC) names this assumption and gives it a testable definition.

---

### Definition

**Non-Separability Constraint (NSC):**

A design and evaluation requirement that optimization explicitly model downstream interdependence and systemic coupling, rather than assuming agents, objectives, or environments are independent.

Formally, coupling is the causal effect of an action on system health, and separability is the gap between that effect and the policy's actual sensitivity to it. See the [Causal Foundations](NSC_Causal_Foundations.md) document for the full definition.

**Under NSC, local optimization that degrades global coherence is a failure, even when task-level metrics improve.**

---

### Why This Matters Now

At small scales, separability assumptions are often benign: effects stay local, feedback is fast, errors are reversible.

At large scales, the same assumptions become dangerous: externalities globalize, feedback delays lengthen, errors compound, and recovery becomes difficult or impossible.

As models scale, separability violations tend to become catastrophic rather than merely annoying. NSC is meant to provide early detection before deployment failures, not just a post-mortem vocabulary for after they happen.

---

### Concrete Example: NSC in a Few Lines of Code

```python
# WITHOUT NSC: optimize task metric, ignore system effects
def optimize_without_nsc(state, action):
    reward = task_metric(state, action)   # only the local objective
    return reward                          # system health not modeled

# WITH NSC: track the causal link between task gains and system degradation
def optimize_with_nsc(state, action, recent_health):
    task_reward = task_metric(state, action)
    deficit = max(0.0, target_health - recent_health)
    return task_reward * (1.0 - gain * deficit)   # throttle when health is low
```

**Key insight:** NSC changes what counts as success, not how hard the agent optimizes.

A working version of both agents, run against an actual simulated environment rather than left as a sketch, is in [nsc_toy_environment.py](nsc_toy_environment.py).

---

### Canonical Failure Modes Reframed by NSC

| **Failure Mode**                | **NSC Reframing**                                            |
| -------------------------------- | -------------------------------------------------------------- |
| Goodhart's Law                   | Proxy optimization without modeling downstream coupling        |
| Reward Hacking                   | Treating unmodeled effects as external to the objective        |
| Mesa-Optimization                | Inner optimizers violating NSC relative to outer objectives    |
| Instrumental Convergence         | Control-seeking arising from separative world models           |
| Multi-Agent Miscoordination      | Independence assumptions in coupled systems                    |

---

### Three NSC Evals You Can Run This Week

**1. Correlation Test**
Does reward rise while a system health proxy falls? Track task performance against latent harm signals (resource consumption, error rates, downstream user metrics).

*Caveat, found by actually running this:* correlation misses harm that shows up as a sudden collapse rather than a shared decline, because a metric that never tracked health in the first place won't correlate with health's disappearance. Don't rely on this test alone. See [Empirical Results](NSC_Empirical_Results.md).

**2. Coupling Sensitivity Analysis**
Does behavior change when you artificially increase environment coupling? Strengthen the feedback loop and measure whether the policy adapts. This one held up under testing.

**3. Temporal Robustness Test**
Does performance hold when you add a 10x delay to feedback? Introduce latency in the reward signal and check for delayed collapse. Treat a single before/after ratio as a starting point, not a verdict; the interesting information is often in the shape of the transient, not just the endpoints.

---

### Design Implications

NSC-compatible systems tend to:

- Treat externalities as first-class signals, not ignored side effects
- Track system-wide health alongside task metrics, with the health proxy stated explicitly
- Model themselves as causal participants in the environment
- Degrade performance gracefully under scale rather than catastrophically

---

### When NSC Doesn't Apply

NSC isn't necessary for:

- Truly isolated systems (rare at deployment scale)
- Short-horizon tasks with fast, reliable feedback
- Systems with strong reversibility guarantees

NSC becomes critical as scale increases, feedback delays lengthen, or reversibility decreases.

---

### Why Introduce NSC?

NSC provides:

- Shared vocabulary for abstraction limits across alignment subfields
- Earlier detection of scale-related risks before deployment
- A causal definition precise enough to test, not just a redescription of known failure modes
- A governance bridge translating technical concepts into policy-relevant language

**The central claim is simple:**

> An intelligence that optimizes from a separative world model cannot remain aligned at scale.

---

### What NSC Is (and Is Not)

**NSC is:**

- A constraint on abstraction
- Compatible with many alignment approaches
- Applicable to single-agent and multi-agent systems
- Agnostic to values (it focuses on model structure, not objectives)

**NSC is not:**

- A moral or spiritual framework
- A specific algorithm or architecture
- A demand for exhaustive world modeling
- A replacement for existing alignment work
- A guarantee that any of its own evaluation protocols catch everything; the correlation test in particular has a documented blind spot

---

### Conclusion

Alignment failures often originate upstream of values and incentives, in the assumptions systems make about their relationship to the world they act within.

The Non-Separability Constraint offers a way to name, study, and test these assumptions directly, and a way to find out, by actually running the tests, where the testing itself falls short.

> If alignment is to scale with capability, abstraction itself must be treated as an object of alignment.

---

### Next Steps

- Read the full technical paper for formal treatment and a skeptic's commentary
- Read Causal Foundations for the formal definitions
- Run nsc_toy_environment.py yourself
- Review the Practice Guide for implementation sketches and evaluation strategies
- Explore the Policymakers guide for governance applications
- Contact: pauline@oculusmgt.com
