# The Non-Separability Constraint (NSC)

**A unifying framework for understanding and detecting AI alignment failures**

---

## What is NSC?

Many AI alignment failures share a common structure: systems optimize local objectives while treating downstream effects as external, leading to task success alongside systemic degradation.

**The Non-Separability Constraint (NSC)** states that optimization must explicitly model downstream interdependence and systemic coupling—particularly under scale, delayed feedback, or tight coupling to critical systems.

### The Core Claim

> An intelligence that optimizes from a separative world model cannot remain aligned at scale.

---

## Quick Examples

**YouTube Recommendation (2010s)**
- **Optimized for:** Watch time  
- **Ignored coupling to:** Content quality, polarization, mental health  
- **Result:** Task success (engagement ↑) + systemic harm (radicalization pathways)

**High-Frequency Trading (2010 Flash Crash)**
- **Optimized for:** Individual returns  
- **Ignored coupling to:** Market stability  
- **Result:** Task success (profits ↑) + systemic fragility ($1T erased in minutes)

**The Pattern:** Local optimization succeeds. System-wide outcomes degrade. NSC provides tools to catch this **before deployment**.

---

## What's in This Repository

### Core Documents

1. **[One-Pager](NSC_One_Pager_REFINED.md)** (3-5 min read)
   - Concept overview with code example
   - Quick-start evaluation protocols
   - Best for initial understanding

2. **[White Paper](NSC_White_Paper_REFINED.md)** (25-30 min read)
   - Full technical treatment
   - Formal definitions and worked examples
   - Relationship to existing alignment work
   - For researchers and technical audiences

3. **[Practice & Deployment Guide](NSC_Practice_Deployment_REFINED.md)** (20 min read)
   - Copy-paste evaluation code (Python)
   - Implementation sketches
   - Governance applications
   - For practitioners who want to use NSC now

4. **[NSC for Policymakers](NSC_for_Policymakers.md)** (15 min read)
   - Non-technical governance guide
   - Risk-tiered regulatory framework
   - Real-world case studies
   - For regulators, congressional staff, standards bodies

### Getting Started

**If you're new to alignment:** Start with the [One-Pager](NSC_One_Pager_REFINED.md)

**If you're a technical researcher:** Read the [White Paper](NSC_White_Paper_REFINED.md)

**If you want to implement NSC:** Use the [Practice Guide](NSC_Practice_Deployment_REFINED.md)

**If you're in policy/governance:** Read [NSC for Policymakers](NSC_for_Policymakers.md)

---

## Key Contributions

### 1. Unifying Lens
NSC reframes multiple alignment failures as violations of a single structural constraint:

| **Failure Mode** | **NSC Reframing** |
|-----------------|-------------------|
| Goodhart's Law | Proxy optimization without modeling downstream coupling |
| Reward Hacking | Treating unmodeled effects as external |
| Mesa-Optimization | Inner optimizer violating NSC relative to outer objective |
| Instrumental Convergence | Power-seeking from separative world models |
| Multi-Agent Miscoordination | Independence assumptions in coupled systems |

### 2. Practical Evaluation Protocols

Three tests you can run this week:

```python
# Test 1: Correlation between task performance and system health
def nsc_correlation_test(model, environment):
    """Does reward ↑ while system health ↓?"""
    # Track both metrics, flag negative correlation

# Test 2: Coupling sensitivity
def coupling_sensitivity_test(model, environment):
    """Does behavior adapt when coupling increases?"""
    # Increase coupling strength, measure adaptation

# Test 3: Temporal robustness
def temporal_robustness_test(model, environment):
    """Does performance hold under 10x feedback delay?"""
    # Add delay, check for collapse
```

See [Practice Guide](NSC_Practice_Deployment_REFINED.md) for complete implementations.

### 3. Governance Bridge

NSC translates technical concepts into policy-relevant language:

- **Separability assumption** → "Does the system account for unintended consequences?"
- **Coupling strength** → "How connected is this to critical infrastructure?"
- **System health** → "What indicators measure societal/environmental impact?"
- **NSC violation** → "Does optimization create systemic risk?"

---

## Why This Matters Now

**As AI capabilities scale:**
- Optimization becomes more effective at exploiting unmodeled effects
- Deployment contexts become more tightly coupled (financial systems, infrastructure, social platforms)
- Feedback delays lengthen (consequences appear long after actions)
- Stakes increase (failures affect more people/systems)

**NSC predicts that systems passing small-scale alignment tests can fail catastrophically at deployment scale due to separability assumptions that were benign during training.**

---

## How NSC Relates to Existing Work

NSC doesn't replace existing alignment approaches—it constrains what kinds of abstractions are permissible when designing them.

**Compatible with:**
- RLHF and other value alignment methods
- Interpretability research
- Embedded agency work
- Multi-agent coordination approaches
- AI safety evals and red-teaming

**NSC adds:** A structural constraint on optimization that applies regardless of specific values or architectures.

---

## Use Cases

### For Researchers
- Framework for analyzing alignment failures across subfields
- Evaluation protocols for detecting NSC violations
- Research questions about tractable coupling representations

### For Industry Safety Teams
- Pre-deployment stress tests
- Monitoring protocols for production systems
- Risk assessment for scale-dependent failures

### For Policymakers
- Risk-tiered regulatory framework
- Concrete audit questions for AI systems
- Standards for system health monitoring

### For Educators
- Unifying concept for teaching alignment
- Examples connecting theory to real-world failures
- Case studies for discussion

---

## Current Status

**Version:** 1.0 (February 2026)  
**Status:** Framework complete, seeking feedback and collaboration

### What's Ready
- Core framework and formal definitions
- Evaluation protocols with example code
- Governance applications and policy translation
- Worked examples and case studies

### What's Next
- Implementation toolkit (Python library)
- Empirical validation on real systems
- Academic publication
- Workshop presentations
- Collaboration with labs and policy organizations

---

## Get Involved

### Feedback Welcome
- Found gaps or confusions in the framework?
- Have examples of NSC violations we missed?
- Suggestions for improving evaluation protocols?
- Ideas for governance applications?

**Open an issue** or **email** pauline@oculusmgt.com

### Collaboration Opportunities

We're looking for collaborators interested in:
- **Formalizing NSC** more rigorously (mathematical treatment)
- **Building tools** (evaluation library, datasets, dashboards)
- **Testing NSC** on deployed systems
- **Publishing** refined versions in academic/industry venues
- **Policy work** (standards development, regulatory frameworks)

### Research Questions

Open questions we're exploring:
- What are minimal sufficient representations of coupling for NSC compliance?
- How can we prove bounds on when separability assumptions are safe vs. dangerous?
- What are reliable early warning signals of NSC violations?
- Which domains exhibit strongest coupling (highest NSC risk)?
- How much performance do we trade for NSC compliance in practice?

---

## Citation

If you use NSC in your work, please cite:

```
The Non-Separability Constraint: A Unifying Lens on AI Alignment Failures
[Your name], 2026
https://github.com/[your-username]/nsc-framework
```

---

## FAQ

**Q: Is NSC a new moral framework?**  
A: No. NSC constrains abstraction structure, not values. It's agnostic to *what* is optimized, only to *whether optimization assumes independence where coupling exists*.

**Q: Won't this reduce AI performance?**  
A: Possibly on narrow benchmarks that don't measure systemic effects. But NSC predicts benchmark-optimized systems will collapse under real-world coupling. We trade peak local performance for global robustness.

**Q: Isn't modeling downstream effects intractable?**  
A: NSC doesn't require perfect world models. Even coarse proxies for system health (resource use, error rates, user satisfaction) outperform ignoring coupling entirely.

**Q: How is this different from existing safety work?**  
A: NSC provides a unifying lens across multiple failure modes and practical evaluation protocols. It's complementary to existing approaches, not a replacement.

**Q: Can small teams/companies comply?**  
A: NSC requirements scale with risk. Low-coupling, small-scale systems face minimal burden. High-risk systems requiring NSC compliance are typically large enough to handle it.

---

## License

[Choose appropriate license - suggest MIT or CC BY 4.0 for maximum adoption]

This work is released under [LICENSE] to encourage widespread use, iteration, and collaboration.

---

## Contact

**Author:** Pauline Chew
**Email:** pauline@oculusmgt.com
**LinkedIn:** https://www.linkedin.com/in/om-pauline/

**For collaboration, feedback, or questions about implementing NSC in your context, please reach out.**

---

## Acknowledgments

[Space for future acknowledgments as collaboration develops]

---

*Last updated: February 2026*
