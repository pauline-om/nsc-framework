# The Non-Separability Constraint (NSC)

**A unifying framework for understanding and detecting AI alignment failures**

---

## What is NSC?

Many AI alignment failures share a common structure: systems optimize local objectives while treating downstream effects as external, leading to task success alongside systemic degradation.

**The Non-Separability Constraint (NSC)** states that optimization must explicitly model downstream interdependence and systemic coupling, particularly under scale, delayed feedback, or tight coupling to critical systems.

### The Core Claim

> An intelligence that optimizes from a separative world model cannot remain aligned at scale.

---

## Quick Examples

**YouTube Recommendation (2010s)**

- **Optimized for:** Watch time
- **Ignored coupling to:** Content quality, polarization, mental health
- **Result:** Task success (engagement up) alongside systemic harm (radicalization pathways)

**High-Frequency Trading (2010 Flash Crash)**

- **Optimized for:** Individual returns
- **Ignored coupling to:** Market stability
- **Result:** Task success (profits up) alongside systemic fragility ($1T erased in minutes)

**The Pattern:** Local optimization succeeds. System-wide outcomes degrade. NSC provides tools to catch this before deployment.

---

## What's in This Repository

### Core Documents

1. **[One-Pager](NSC_One_Pager_REFINED.md)** (3-5 min read)
   - Concept overview with code example
   - Quick-start evaluation protocols
   - Best for initial understanding

2. **[White Paper](NSC_White_Paper_REFINED.md)** (30-35 min read)
   - Full technical treatment, now grounded in structural causal models rather than undefined notation
   - Formal definitions and worked examples
   - Relationship to existing alignment work
   - For researchers and technical audiences

3. **[Causal Foundations](NSC_Causal_Foundations.md)** (10 min read, technical)
   - Defines coupling strength and separability as measurable causal quantities rather than asserted ones
   - Explains why "system health" is a modeling choice that has to be stated explicitly, not assumed
   - The basis for the formal section of the white paper

4. **[Practice & Deployment Guide](NSC_Practice_Deployment_REFINED.md)** (25 min read)
   - Working evaluation code, tested against a real simulated environment rather than left as pseudocode
   - Documents where the original evaluation protocols actually fail, with numbers
   - Implementation sketches and governance applications

5. **[Empirical Results](NSC_Empirical_Results.md)** (10 min read)
   - What happened when the three evaluation protocols were run against a real environment
   - Two of the three, as originally specified, missed an unambiguous violation
   - Full reproduction instructions

6. **[NSC for Policymakers](NSC_for_Policymakers.md)** (15 min read)
   - Non-technical governance guide
   - Risk-tiered regulatory framework
   - Real-world case studies

### Code

- **[nsc_toy_environment.py](nsc_toy_environment.py)** - a minimal, runnable simulation implementing the three evaluation protocols against an actual coupled environment, rather than describing them in prose. Run it with `python3 nsc_toy_environment.py`.

### Getting Started

**If you're new to alignment:** Start with the [One-Pager](NSC_One_Pager_REFINED.md)

**If you're a technical researcher:** Read the [White Paper](NSC_White_Paper_REFINED.md), then [Causal Foundations](NSC_Causal_Foundations.md)

**If you want to implement NSC:** Use the [Practice Guide](NSC_Practice_Deployment_REFINED.md) and run `nsc_toy_environment.py` yourself before trusting any of the protocols on a real system

**If you're in policy or governance:** Read [NSC for Policymakers](NSC_for_Policymakers.md)

---

## Key Contributions

### 1. Unifying Lens

NSC reframes multiple alignment failures as violations of a single constraint:

| **Failure Mode**            | **NSC Reframing**                                          |
| ---------------------------- | ----------------------------------------------------------- |
| Goodhart's Law               | Proxy optimization without modeling downstream coupling     |
| Reward Hacking               | Treating unmodeled effects as external                      |
| Mesa-Optimization            | Inner optimizer violating NSC relative to outer objective   |
| Instrumental Convergence     | Power-seeking from separative world models                  |
| Multi-Agent Miscoordination  | Independence assumptions in coupled systems                 |

### 2. A Causal Definition, Not Just a Description

Coupling strength and separability are defined as measurable quantities using structural causal models: coupling is a causal effect estimable by intervention, and separability is the gap between that effect and the policy's actual sensitivity to it. See [Causal Foundations](NSC_Causal_Foundations.md).

### 3. Evaluation Protocols, Tested, With Known Limitations Documented

Three evaluation protocols exist. One of them, the correlation test, produces a false negative on the clearest possible violation (a total, irreversible collapse of system health while the task metric stays flat), because a step-change in health doesn't correlate with a constant metric. This is documented with real numbers in [Empirical Results](NSC_Empirical_Results.md), rather than glossed over. The coupling-sensitivity protocol held up under the same test.

### 4. Governance Bridge

NSC translates technical concepts into policy-relevant language:

- **Separability assumption** to "Does the system account for unintended consequences?"
- **Coupling strength** to "How connected is this to critical infrastructure?"
- **System health** to "What indicators measure societal or environmental impact, and who chose them?"
- **NSC violation** to "Does optimization create systemic risk?"

---

## Why This Matters Now

As AI capabilities scale:

- Optimization becomes more effective at exploiting unmodeled effects
- Deployment contexts become more tightly coupled (financial systems, infrastructure, social platforms)
- Feedback delays lengthen (consequences appear long after actions)
- Stakes increase (failures affect more people and systems)

NSC predicts that systems passing small-scale alignment tests can fail catastrophically at deployment scale, because separability assumptions that were benign during training stop being benign once coupling and scale increase.

---

## How NSC Relates to Existing Work

NSC doesn't replace existing alignment approaches. It constrains what kinds of abstractions are permissible when designing them.

**Compatible with:**

- RLHF and other value alignment methods
- Interpretability research
- Embedded agency work
- Multi-agent coordination approaches
- AI safety evals and red-teaming

**NSC adds:** a structural constraint on optimization that applies regardless of specific values or architectures, plus a causal definition precise enough to test.

---

## Use Cases

### For Researchers
- A shared frame for alignment failures across subfields
- Evaluation protocols for detecting NSC violations, with documented failure modes of the protocols themselves
- Open questions about tractable coupling representations

### For Industry Safety Teams
- Pre-deployment stress tests
- Monitoring protocols for production systems
- Risk assessment for scale-dependent failures

### For Policymakers
- Risk-tiered regulatory framework
- Concrete audit questions for AI systems
- Standards for system health monitoring

### For Educators
- A unifying concept for teaching alignment
- Examples connecting theory to real-world failures
- A worked simulation students can run and modify themselves

---

## Current Status

**Version:** 1.1 (August 2026)
**Status:** Framework complete. One protocol's failure mode identified and documented through simulation. Formal section rebuilt on causal grounds. Still pre-publication, still seeking feedback.

### What's Ready

- Core framework and causal definitions
- A runnable simulation implementing all three evaluation protocols
- Documented, numeric evidence of where one protocol fails
- Governance applications and policy translation
- Worked examples and case studies

### What's Next

- Testing the protocols against a second, structurally different toy environment to see whether the correlation-test failure generalizes
- A proper implementation toolkit beyond the single-file simulation
- Empirical validation on a real (not simulated) system
- Academic publication
- Collaboration with labs and policy organizations

---

## Get Involved

### Feedback Welcome

- Found gaps or confusions in the framework?
- Have examples of NSC violations we missed?
- Suggestions for improving evaluation protocols, especially the correlation test?
- Ideas for governance applications?

**Open an issue** or **email** pauline@oculusmgt.com

### Collaboration Opportunities

Looking for collaborators interested in:

- Formalizing NSC further (more general causal treatments, non-scalar health measures)
- Building tools (an evaluation library beyond the single toy environment here)
- Testing NSC on deployed systems
- Publishing refined versions in academic or industry venues
- Policy work (standards development, regulatory frameworks)

### Research Questions

- What are minimal sufficient representations of coupling for NSC compliance?
- Can we prove bounds on when separability assumptions are safe versus dangerous?
- What are reliable early warning signals of NSC violations, given that correlation alone isn't one?
- Which domains exhibit the strongest coupling (highest NSC risk)?
- How much performance is actually traded for NSC compliance in practice?

---

## Citation

If you use NSC in your work, please cite:

```
Chew, P. (2026). The Non-Separability Constraint: A Unifying Lens on AI Alignment Failures.
https://github.com/pauline-om/nsc-framework
```

---

## FAQ

**Q: Is NSC a new moral framework?**
A: No. NSC constrains abstraction structure, not values. It's agnostic to what is optimized, only to whether optimization assumes independence where coupling exists.

**Q: Won't this reduce AI performance?**
A: Possibly on narrow benchmarks that don't measure systemic effects. NSC predicts benchmark-optimized systems will collapse under real-world coupling. The trade is peak local performance for global robustness.

**Q: Isn't modeling downstream effects intractable?**
A: NSC doesn't require a perfect world model. Even coarse proxies for system health (resource use, error rates, user satisfaction) outperform ignoring coupling entirely, though picking a bad proxy has its own failure mode, covered in Causal Foundations.

**Q: How is this different from existing safety work?**
A: NSC gives a unifying lens across multiple failure modes and a causal definition precise enough to test. It's complementary to existing approaches, not a replacement.

**Q: Can small teams or companies comply?**
A: NSC requirements scale with risk. Low-coupling, small-scale systems face minimal burden. High-risk systems requiring full NSC compliance are typically large enough to handle it.

**Q: Have the evaluation protocols actually been tested?**
A: Yes, against a small simulated environment, and the results are mixed on purpose. The coupling-sensitivity test worked as intended. The correlation test missed a total system collapse. See [Empirical Results](NSC_Empirical_Results.md) for the numbers.

---

## License

This work is released under the MIT License to encourage widespread use, iteration, and collaboration.

---

## Contact

**Author:** Pauline Chew
**Email:** pauline@oculusmgt.com
**LinkedIn:** https://www.linkedin.com/in/om-pauline/

For collaboration, feedback, or questions about implementing NSC in your context, please reach out.

---

*Last updated: August 2026*
