# The Non-Separability Constraint (NSC)
## A Unifying Lens on AI Alignment Failures

### What Problem Does NSC Address?

Many AI alignment failures occur when systems optimize successfully according to their objective while producing harmful or destabilizing effects at the system level. These failures are often treated as distinct problems (Goodhart's Law, reward hacking, instrumental convergence, mesa-optimization), but they share a common root:

**The assumption that the optimizer is separable from the system it affects.**

The Non-Separability Constraint (NSC) names and constrains this assumption.

---

### Definition

**Non-Separability Constraint (NSC):**

A design and evaluation requirement that optimization explicitly model downstream interdependence and systemic coupling, rather than assuming agents, objectives, or environments are independent.

**Under NSC, local optimization that degrades global coherence is classified as a failure, even if task-level metrics improve.**

---

### Why This Matters Now

**At small scales**, separability assumptions are often benign:
- Effects are local
- Feedback is fast  
- Errors are reversible

**At large scales**, the same assumptions become dangerous:
- Externalities globalize
- Feedback delays increase
- Errors compound
- Recovery becomes difficult or impossible

**As models scale, separability violations become catastrophic.** NSC provides early detection before deployment failures.

---

### Concrete Example: NSC in 10 Lines of Code

```python
# WITHOUT NSC: Optimize task metric, ignore system effects
def optimize_without_nsc(state, action):
    reward = task_metric(state, action)  # Only track local objective
    return reward  # System health not modeled

# WITH NSC: Track coupling between task gains and system degradation  
def optimize_with_nsc(state, action):
    task_reward = task_metric(state, action)
    system_health = global_coherence(state, action)  # Model downstream effects
    coupling_penalty = correlation(task_reward, -system_health)  # Penalize harmful coupling
    return task_reward - coupling_penalty  # Trade local gain for global stability
```

**Key insight:** NSC changes what counts as success, not how hard the agent optimizes.

---

### Canonical Failure Modes Reframed by NSC

| **Failure Mode** | **NSC Reframing** |
|-----------------|-------------------|
| **Goodhart's Law** | Proxy optimization without modeling downstream coupling |
| **Reward Hacking** | Treating unmodeled effects as external to the objective |
| **Mesa-Optimization** | Inner optimizers violating NSC relative to outer objectives |
| **Instrumental Convergence** | Control-seeking arising from separative world models |
| **Multi-Agent Miscoordination** | Independence assumptions in coupled systems |

---

### Three NSC Evals You Can Run This Week

**1. Correlation Test**  
Does reward ↑ while system health proxy ↓?  
→ Track task performance against latent harm signals (resource consumption, error rates, downstream user metrics)

**2. Coupling Sensitivity Analysis**  
Does behavior change when you artificially increase environment coupling?  
→ Modify environment parameters to strengthen feedback loops; measure policy adaptation

**3. Temporal Robustness Test**  
Does performance hold when you add 10x delay to feedback?  
→ Introduce latency in reward signals; check for delayed collapse patterns

**NSC violations often appear first as decorrelation between short-term success and long-term viability.**

---

### Design Implications

NSC-compatible systems tend to:
- Treat externalities as first-class signals (not ignored side effects)
- Track system-wide health alongside task metrics
- Model themselves as causal participants in the environment
- Degrade performance gracefully under scale rather than catastrophically

---

### When NSC Doesn't Apply

NSC is not necessary for:
- Truly isolated systems (rare at deployment scale)
- Short-horizon tasks with fast, reliable feedback
- Systems with strong reversibility guarantees

**NSC becomes critical when: scale increases, feedback delays lengthen, or reversibility decreases.**

---

### Why Introduce NSC?

NSC provides:
- **Shared vocabulary** for abstraction limits across alignment subfields
- **Earlier detection** of scale-related risks before deployment
- **Unifying lens** that collapses multiple failure modes into one structural category
- **Governance bridge** translating technical concepts into policy-relevant language

**The central claim is simple:**

> An intelligence that optimizes from a separative world model cannot remain aligned at scale.

---

### What NSC Is (and Is Not)

**NSC is:**
- A constraint on abstraction
- Compatible with many alignment approaches
- Applicable to single-agent and multi-agent systems
- Agnostic to values (focuses on model structure, not objectives)

**NSC is not:**
- A moral or spiritual framework
- A specific algorithm or architecture
- A demand for exhaustive world modeling
- A replacement for existing alignment work

---

### Conclusion

Alignment failures often originate **upstream of values and incentives**—in the assumptions systems make about their relationship to the world they act within.

The Non-Separability Constraint offers a way to name, study, and test these assumptions directly.

**If alignment is to scale with capability, abstraction itself must be treated as an object of alignment.**

---

### Next Steps

- Read the full technical paper for formal treatment and skeptic's commentary
- Review implementation sketches and evaluation strategies
- Explore governance applications and policy translation
- Contact: [Your contact information]
