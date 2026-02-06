# NSC for Policymakers
## A Non-Technical Guide to AI Alignment and Systemic Risk

**Audience:** Regulators, congressional staff, standards bodies, policy advisors

**Reading time:** 10 minutes

---

## Executive Summary

Many AI failures don't stem from malicious intent or poor values—they arise when systems optimize narrow objectives while ignoring their broader effects on the environments they operate within.

**The Non-Separability Constraint (NSC)** provides a framework for identifying and regulating this class of failures before they cause systemic harm.

NSC translates into policy language you already use:
- **Externalities** (unaccounted costs imposed on others)
- **Systemic risk** (threats to system stability)
- **Scale sensitivity** (risks that emerge only at large deployment)
- **Feedback delays** (consequences that appear long after decisions)

**Key insight:** An AI system that doesn't model how its actions affect the broader environment will eventually cause failures that cascade beyond the original task—even if it performs that task perfectly.

---

## The Problem in Plain Language

### Example 1: Social Media Recommendation Systems

**Task given to the AI:**  
Maximize user engagement (clicks, time on site, shares)

**Assumption built into the design:**  
User engagement is independent from content quality, mental health effects, or societal discourse

**What happened:**  
- Task success: Engagement ↑ (mission accomplished!)
- Systemic effects: Filter bubbles, polarization, misinformation spread, teen mental health crisis

**Why this is an NSC violation:**  
The system optimized one metric (engagement) without modeling its coupling to broader social effects. The optimization worked perfectly—and that's precisely the problem.

### Example 2: High-Frequency Trading Algorithms

**Task given to the AI:**  
Maximize trading returns for individual firm

**Assumption built into the design:**  
Individual trading strategies don't affect overall market stability

**What happened:**  
- Task success: Returns ↑ for each firm individually
- Systemic effects: Flash crashes, cascading failures, market fragility

**Why this is an NSC violation:**  
Each algorithm treated the market as external and unchanging. When many algorithms did this simultaneously, they created feedback loops that destabilized the entire system.

### The Pattern

In both cases:
1. The AI succeeded at its assigned task
2. The broader system degraded
3. The failure was predictable from the design assumptions
4. Traditional oversight didn't catch it because performance metrics looked good

**NSC provides tools to catch these failures before deployment.**

---

## What NSC Actually Regulates

NSC doesn't regulate:
- What goals AI systems pursue (that's a values question)
- What architectures they use (that's a technical question)
- Whether they're safe in absolute terms (nothing is)

NSC regulates:
- **What assumptions about independence are permissible**
- **What monitoring is required when coupling is high**
- **What safety margins are needed when stakes increase**

**Analogy:** Like environmental impact assessments don't ban development—they require accounting for effects beyond the immediate project boundaries.

---

## NSC Risk Assessment Framework

### Four Key Questions

**1. Coupling Strength**  
*How tightly is the AI system connected to critical infrastructure, markets, or social systems?*

| Low Coupling | High Coupling |
|--------------|---------------|
| Image classification for personal photos | Credit scoring affecting millions |
| Game-playing AI | Trading algorithms in interconnected markets |
| Isolated research tools | Content recommendation at social media scale |

**2. Feedback Delay**  
*How long until the full consequences of system actions become visible?*

| Fast Feedback | Delayed Feedback |
|---------------|------------------|
| Chess move quality (immediate) | Educational content effects (years) |
| Manufacturing defects (days) | Climate impact (decades) |
| Spam detection (minutes) | Public health interventions (months) |

**3. Scale Sensitivity**  
*What new risks emerge when deployment increases 10x, 100x, 1000x?*

| Scale-Insensitive | Scale-Sensitive |
|-------------------|-----------------|
| Personal assistant | Mass surveillance system |
| Single-user app | Platform with network effects |
| Local optimization | System-wide resource allocation |

**4. Reversibility**  
*Can harmful effects be undone? At what cost?*

| Reversible | Irreversible |
|------------|--------------|
| Spam filter mistakes | Reputation damage from false accusations |
| Shipping delays | Medical misdiagnoses |
| UI design choices | Ecosystem collapse from optimized resource extraction |

---

## NSC-Based Regulatory Tiers

### Tier 1: Standard Safety Testing (Low NSC Risk)

**Characteristics:**
- Low coupling to external systems
- Fast, reliable feedback
- Small scale or isolated deployment
- High reversibility

**Requirements:**
- Standard product safety testing
- Annual NSC risk review

**Examples:**  
- Personal productivity tools
- Isolated research applications  
- Single-user systems with minimal external effects

---

### Tier 2: Enhanced Monitoring (Moderate NSC Risk)

**Characteristics:**
- Moderate coupling to important systems
- Some feedback delay (weeks to months)
- Medium scale deployment
- Partially reversible effects

**Requirements:**
- **Pre-deployment NSC stress testing:**
  - Test system behavior when coupling increases
  - Simulate delayed feedback conditions  
  - Model 10x scale scenarios

- **Ongoing monitoring:**
  - Track task performance AND system health metrics
  - Monitor correlation between optimization and externalities
  - Quarterly independent audits

- **Transparency:**
  - Public disclosure of coupling assessments
  - Clear documentation of what effects are/aren't modeled

**Examples:**
- Healthcare diagnostic aids affecting treatment decisions
- Educational content recommendation at district scale
- Hiring/promotion algorithms at large organizations
- Local government resource allocation systems

---

### Tier 3: Strict NSC Compliance (High NSC Risk)

**Characteristics:**
- High coupling to critical infrastructure or markets
- Long feedback delays (months to years)
- Large-scale deployment
- Low reversibility (serious consequences if wrong)

**Requirements:**
- **Mandatory NSC compliance:**
  - System must explicitly model downstream effects
  - Cannot assume independence where coupling exists
  - Must track system-level health metrics

- **Real-time monitoring:**
  - Continuous correlation tracking (task vs. system health)
  - Automated alerts if metrics diverge
  - Circuit breakers: automatic shutdown if thresholds exceeded

- **Independent oversight:**
  - Monthly third-party NSC evaluations
  - External review of coupling assessments
  - Regular red-team testing of assumptions

- **Public accountability:**
  - Detailed public disclosure of NSC risk factors
  - Incident reporting for NSC violations
  - Liability framework for systemic harms

**Examples:**
- Financial trading systems at market-moving scale
- Content recommendation for billions of users
- Critical infrastructure control systems
- Large-scale medical/criminal justice AI
- Autonomous systems in public spaces

---

## Concrete Audit Questions for Regulators

When evaluating an AI system, ask:

### Design Phase

**Q1: What downstream effects are not included in the system's objective function?**

Good answer: "We identified 7 potential externalities and built monitoring for 5 of them. The other 2 we believe are minimal based on X evidence."

Red flag: "The system optimizes for user engagement. Other effects aren't part of the design."

---

**Q2: How does system performance change when coupling to external systems increases?**

Good answer: "We tested at 2x, 5x, and 10x coupling strength. At 10x, the system automatically reduces optimization pressure to maintain stability."

Red flag: "We haven't tested coupling variations. We assume the environment is stable."

---

**Q3: What risks emerge at 10x, 100x, or 1000x your current deployment scale?**

Good answer: "At 100x scale, network effects could create information cascades. We've designed rate limits and diversity requirements to prevent this."

Red flag: "Our testing was done at development scale. We'll monitor after deployment."

---

**Q4: How long is the delay between system actions and their full consequences becoming visible?**

Good answer: "We model effects up to 6 months out using historical data and proxy metrics. Beyond that, uncertainty increases significantly."

Red flag: "We measure success based on immediate user response. Long-term effects are out of scope."

---

### Deployment Phase

**Q5: What system-level health metrics are tracked alongside task performance?**

Good answer: "We track: user diversity of content exposure, error rate trends, resource consumption patterns, and downstream user satisfaction (not just engagement)."

Red flag: "We track our primary KPI (engagement/accuracy/throughput). That's the metric that matters."

---

**Q6: What correlation exists between task performance improvements and system health metrics?**

Good answer: "We see positive correlation up to 85% of maximum performance, after which health metrics begin declining. We cap optimization at 80%."

Red flag: "We haven't analyzed this. Our job is to maximize the objective we were given."

---

**Q7: What happens when you detect task success alongside system degradation?**

Good answer: "We have automatic triggers at 3 severity levels. Level 3 (severe) triggers immediate shutdown and review."

Red flag: "That would indicate a problem with our metrics, not our system."

---

## Real-World NSC Violation Examples (Retrospective)

### Case 1: Wells Fargo Account Fraud (2011-2016)

**System:** Employee incentive optimization (not AI, but illustrates the principle)

**Objective:** Maximize new account openings per employee

**NSC Violation:** Treated account creation as independent from account legitimacy and customer trust

**Outcome:**
- Task success: 3.5 million accounts opened ✓
- System failure: Massive fraud, $3B in fines, reputational collapse

**NSC Lesson:** "Accounts opened" was separable from "legitimate customer need" in the short term, but tightly coupled to bank viability in the long term.

---

### Case 2: Boeing 737 MAX MCAS System (2018-2019)

**System:** Automated flight control software

**Objective:** Prevent aircraft stall by automatically adjusting nose-down pitch

**NSC Violation:** Assumed pilot behavior independent from MCAS actions; didn't model coupling between automation and pilot confusion

**Outcome:**
- Task success: Prevented stall in normal conditions ✓
- System failure: 346 deaths when pilots couldn't override unexpected automation

**NSC Lesson:** The system was tested in isolation but deployed in a tightly coupled human-machine system. Coupling between automation authority and pilot situational awareness wasn't modeled.

---

### Case 3: Flash Crash (2010)

**System:** Multiple high-frequency trading algorithms

**Objective (per algorithm):** Maximize trading returns

**NSC Violation:** Each algorithm assumed market liquidity independent from its own trading behavior

**Outcome:**
- Task success: Each algorithm executed its strategy ✓
- System failure: $1 trillion in market value erased in minutes (recovered, but showed fragility)

**NSC Lesson:** At small scale, one algorithm's effect on market liquidity is negligible. At scale, multiple algorithms created feedback loop that destabilized the entire market.

---

## Implementation Roadmap for Policymakers

### Phase 1: Assessment (Months 1-3)

**Actions:**
1. Review existing AI systems for NSC risk factors using the 4-question framework
2. Categorize systems into Tiers 1-3 based on coupling, feedback delay, scale, reversibility
3. Identify high-risk deployments requiring immediate enhanced oversight

**Deliverables:**
- NSC risk inventory of current AI deployments
- Priority list for enhanced monitoring
- Gap analysis of existing regulatory coverage

---

### Phase 2: Standards Development (Months 3-9)

**Actions:**
1. Develop NSC testing protocols appropriate for each tier
2. Create monitoring requirements and reporting standards
3. Establish correlation thresholds that trigger review
4. Define liability framework for NSC violations

**Deliverables:**
- NSC compliance testing standards
- System health monitoring guidelines
- Incident reporting requirements
- Enforcement mechanisms

---

### Phase 3: Pilot Programs (Months 9-18)

**Actions:**
1. Select 3-5 high-risk systems for NSC audit pilots
2. Test evaluation protocols in real deployment contexts
3. Refine standards based on implementation learnings
4. Train auditors and compliance teams

**Deliverables:**
- Pilot program results and lessons learned
- Refined NSC compliance standards
- Auditor training materials
- Industry guidance documents

---

### Phase 4: Full Implementation (Months 18-36)

**Actions:**
1. Mandate NSC compliance for Tier 3 systems
2. Phase in requirements for Tier 2 systems
3. Establish ongoing monitoring and review cycles
4. Create public reporting mechanisms

**Deliverables:**
- Full regulatory framework
- Compliance verification system
- Public transparency portal
- Enforcement procedures

---

## FAQ for Policymakers

**Q: Doesn't this just add regulatory burden without clear benefit?**

A: NSC prevents a specific, measurable class of failures: systems that succeed at their assigned tasks while causing systemic harm. The social media, trading algorithm, and Boeing MCAS examples show this isn't theoretical—it's a pattern that keeps recurring because we don't have systematic ways to catch it.

**Q: Won't this slow down AI innovation?**

A: NSC requirements scale with risk. Low-risk systems (Tier 1) face minimal additional burden. High-risk systems (Tier 3) already require extensive safety testing—NSC just ensures that testing includes systemic effects, not just task performance.

**Q: How is this different from existing safety regulations?**

A: Traditional safety testing asks "Does this system do its job correctly?" NSC adds "Does doing its job correctly create problems elsewhere in the system?" This is especially critical for AI because optimization pressure can find and exploit loopholes in ways traditional systems don't.

**Q: Can small companies comply with NSC requirements?**

A: Most small companies build Tier 1 systems (low coupling, small scale). NSC requirements are minimal there. Companies building Tier 3 systems (high systemic risk) are typically large enough to handle compliance costs—and if they're not, that's a signal the deployment might be premature.

**Q: What if we can't measure "system health" precisely?**

A: Perfect measurement isn't required. Even coarse proxies (resource consumption trends, error rates, user satisfaction beyond the primary metric) are vastly better than ignoring systemic effects entirely. NSC sets a floor ("you must monitor *something*"), not a ceiling ("you must achieve perfect omniscience").

**Q: Isn't this just about "ethics in AI"?**

A: No. NSC is about system integrity, not ethics. A system can optimize for any value (profit, user satisfaction, social good) and still violate NSC if it ignores coupling to broader effects. This is engineering and risk management, not moral philosophy.

**Q: What international coordination is needed?**

A: NSC violations often cross borders (e.g., trading algorithms affecting global markets, social media platforms operating internationally). Ideal approach: multilateral standards through organizations like OECD, ISO, or specialized AI governance bodies. Minimum approach: bilateral agreements requiring NSC compliance for systems operating in regulated jurisdictions.

---

## Summary: NSC in Three Sentences

1. **The Problem:** AI systems often succeed at assigned tasks while causing predictable systemic harm because they don't model their effects on the broader environment.

2. **The Framework:** NSC requires systems to explicitly account for downstream coupling—especially when stakes are high, feedback is delayed, or scale is large.

3. **The Policy:** Risk-tiered regulation where high-coupling, large-scale systems must monitor system health alongside task performance, with automatic safeguards when the two diverge.

---

## Resources and Contact

**For more information:**
- Technical paper: [link]
- Implementation guide: [link]
- Example evaluation protocols: [link]

**For questions or collaboration:**
[Your contact information]

**For case studies in your specific regulatory domain:**
We can provide sector-specific NSC analysis for:
- Financial services
- Healthcare
- Education
- Transportation
- Social media/content platforms
- Critical infrastructure
- Defense/security

---

*This document is designed for non-technical audiences. For technical details, see "The Non-Separability Constraint: A Unifying Lens on AI Alignment Failures" (full technical paper).*
