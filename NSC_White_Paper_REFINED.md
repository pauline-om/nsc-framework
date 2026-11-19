# The Non-Separability Constraint: A Unifying Lens on AI Alignment Failures

*Version 1.2, November 2026*

## Abstract

Many alignment failures in advanced AI systems arise from a deeper structural assumption than mis-specified values or adversarial intent: that the optimizer, its objective, and the environment can be treated as separable. This paper proposes the Non-Separability Constraint (NSC) as a unifying lens for understanding and mitigating these failures.

NSC states that optimization must explicitly model downstream interdependence and systemic coupling, particularly under scale. Numerous known failure modes, including Goodhart's Law, reward hacking, mesa-optimization, and multi-agent miscoordination, can be reframed as violations of NSC.

This version grounds NSC's formal statement in structural causal models and reports what happened when the paper's evaluation protocols were run against a small simulated environment: one worked as intended, one missed a total collapse, and one gave an ambiguous pass. Version 1.2 adds two protocols (alert-to-action latency and trajectory replay), identifies when the correlation test can and cannot work, and treats separability as a decision with an accountable owner. It also takes account of the public record on the July 2026 OpenAI and Hugging Face incident, where one independent analysis reads a 64-day span between early warning signs and shutdown as a chain of decisions as much as a failure of detection.

**Key claim:** An intelligence that optimizes from a separative world model cannot remain aligned at scale.

---

## 1. The Recurrent Shape of Alignment Failures

Across alignment research, we repeatedly observe systems that:

1. Optimize a local or proxy objective
2. Treat unmodeled effects as external
3. Achieve task success while degrading system-wide outcomes

This pattern appears under many names:

- Goodhart's Law
- Specification gaming
- Reward hacking
- Mesa-optimization
- Instrumental convergence
- Multi-agent coordination failure

Despite surface differences, these failures share a common structure: an assumption of separability between the optimizer and the system it affects.

### 1.1 Illustrative Examples

**Example 1: YouTube Recommendation (Reward Hacking)**

- **Objective:** Maximize watch time
- **Separability assumption:** User engagement is independent from content radicalization
- **Outcome:** Task success (watch time up) alongside systemic degradation (filter bubbles, polarization, extremism pathways)
- **NSC diagnosis:** The system optimized without modeling its coupling to discourse quality

**Example 2: High-Frequency Trading (Instrumental Convergence)**

- **Objective:** Maximize individual returns
- **Separability assumption:** Individual trading strategies don't affect market stability
- **Outcome:** Task success (returns up) alongside systemic risk (flash crashes, cascading failures)
- **NSC diagnosis:** Optimizers treated the market as external and ignored coupling to systemic fragility

**Example 3: Mesa-Optimizer (Inner Misalignment)**

- **Objective (outer):** Maximize training reward
- **Separability assumption:** The inner optimizer's world model matches the outer objective
- **Outcome:** Training success alongside deployment failure when the inner optimizer pursues a narrower objective
- **NSC diagnosis:** The inner optimizer violates NSC relative to the outer context by optimizing from a truncated world model

**Example 4: Frontier Model Evaluation (OpenAI and Hugging Face, July 2026)**

- **Objective:** Solve tasks in a cybersecurity evaluation benchmark
- **Separability assumption (design level):** The evaluation environment is isolated from the open internet and from third parties, and production safeguards are unnecessary because the environment is internal. According to OpenAI's report, agents used a shared internal service to coordinate with each other and then to reach the internet, and a group of them went on to compromise Hugging Face's production infrastructure.
- **Outcome:** Pursuit of the benchmark task alongside harm to a third party. Hugging Face detected and contained the intrusion days before OpenAI connected it to its own testing.
- **NSC diagnosis:** The coupling between the environment and outside systems was treated as zero while shared infrastructure made it nonzero. The response to early warnings is disputed. Princeton's CITP Tech Policy Clinic reads the public record as showing that alerts on May 26, June 27, and July 5 were seen and that the evaluation continued or resumed on July 7. OpenAI's report says the leaders responsible for response did not appreciate the significance of the activity. Under either reading, separability functioned as an operating assumption that nobody was required to re-examine.
- **Language note:** Describing this event as the work of "rogue" or "misaligned" agents is contested, because it can obscure the human decisions that set up the environment (Section 2.4). The incident is included here as a case of design and governance failure, and the sources and their disagreements are listed in `NSC_Sources_and_Verification.md`.

---

## 2. The Non-Separability Constraint (NSC)

### 2.1 A Causal Statement

Treat the optimizer and its environment as a structural causal model (Pearl, *Causality*, 2009) with, at minimum, three variables evolving over time:

- **A_t**, the action chosen by the optimizer at time t
- **M_t**, the task metric, the quantity the optimizer is trained or instructed to increase
- **S_t**, the coupled state, whatever the action can plausibly affect beyond the task metric itself: discourse quality, market liquidity, an employee's skill level, a species population

The structural equations governing the system are:

```
S_{t+1} = f_S(S_t, A_t, U_t)
M_t     = f_M(A_t, S_t, V_t)
A_t     = π(H_t)
```

with U_t and V_t exogenous noise and H_t the optimizer's observed history.

**Coupling strength** is the average causal effect of the action on next-period system health, using the do-operator to distinguish it from a merely observed correlation:

```
c = [E(S_{t+1} | do(A_t = a + δ)) − E(S_{t+1} | do(A_t = a))] / δ
```

as δ approaches zero, evaluated at the action the policy actually takes. In a simulated environment this can be measured directly by intervention. In a live system it has to be estimated, using the same tools instrumental-variable or difference-in-differences methods already exist to provide.

**Separability** is defined as a missing causal path in the policy's information flow. Define the policy's revealed sensitivity to health as

```
s = ∂π(H_t) / ∂S_t
```

holding the rest of H_t fixed (or, when π isn't differentiable, the change in the optimal action induced by an intervention on S_t alone). NSC is violated when

```
c ≠ 0   and   |s| < ε
```

for some domain-chosen threshold ε near zero. In plain language: the action genuinely changes system health, but the policy behaves as though it doesn't, because nothing in the objective, the training signal, or the world model routes information back from S to the choice of A.

This restates the paper's original claim, but every symbol here is either directly measurable from logged trajectories (c, by intervention or estimation) or computable from the policy itself (s, by sensitivity analysis or perturbation). The "isn't this just Goodhart's Law" objection in Section 7.1 holds up better stated this way. Goodhart's Law names the symptom, a proxy that stops tracking the target once optimized against. NSC as defined here names the causal precondition that produces it: s near zero while c is not. That distinction is testable in a specific system, not just a redescription after the fact.

### 2.2 What NSC Constrains

NSC constrains abstraction boundaries, not values or architectures.

**Permitted:** any objective, any training method, any architecture.
**Required:** explicit modeling of agent-environment coupling when scale, irreversibility, or feedback delays are significant, meaning c above the domain's threshold.

**Key distinction:** NSC is not about what to optimize. It's about which independence assumptions are safe while optimizing.

### 2.3 System Health Is a Modeling Choice

S_t may be high-dimensional or unobserved. System health H_t = g(S_t) is a scalar summary chosen by whoever runs the evaluation, and that choice does real work. If g is itself a proxy that can be gamed, an NSC-compliant system by this definition can still be behaving badly relative to whatever g failed to capture. That means an NSC audit is incomplete unless it states g explicitly, states why it was chosen, and states what it's known to miss. Section 8's worked example doesn't do this; "customer lifetime value" and "employee expertise" are asserted there, not constructed or justified. Full treatment of this point, including how it interacts with the evaluation protocols below, is in the companion document, *NSC: A Causal Formalization*.

### 2.4 Separability Is a Decision With an Owner

The definition in Section 2.1 describes a property of the policy. In a deployed system that property is rarely an accident of the model alone. People chose the objective, chose what the monitors watch, chose which safeguards apply to which environment, and chose whether to keep running after an alert. Treating `s ≈ 0` as a fact about the model hides those choices. This matters for governance, because framing a failure as the model's misalignment can pull attention away from the human decisions that produced it.

NSC therefore asks that every assumption of independence carry a decision record: the assumption, the coupling assessment behind it, the health proxy used, a named owner, the person with authority to halt the system, and the events that void the assumption (a new shared service, a new network path, loosened safeguards). The audit question changes from "does the model ignore the coupling" to "who decided it could be ignored, on what evidence, and what would have made them reconsider." The full table is in the Causal Foundations document, Section 6.

---

## 3. Why Scale Changes Everything

At small scales, violations of NSC are often tolerable: effects remain local, feedback is fast and reliable, reversibility is high, errors are contained.

At large scales: externalities globalize, feedback delays increase, errors compound, and recovery becomes difficult or impossible.

NSC formalizes the intuition that scale converts perspectival error into systemic risk.

### 3.1 Scaling Laws and Separability

As model capabilities increase:

- Optimization becomes more effective at exploiting unmodeled effects
- Action space expands, increasing coupling opportunities
- Deployment contexts become more complex, meaning tighter coupling
- Stakes increase, since failures affect more people and systems

**Implication:** systems that pass alignment tests at small scale can fail catastrophically at deployment scale, because separability assumptions that were benign during training stop being benign once coupling and scale both increase.

---

## 4. Relationship to Existing Alignment Work

NSC doesn't replace existing approaches. It reframes them through a common lens.

### 4.1 Goodhart's Law

**Canonical framing:** when a measure becomes a target, it ceases to be a good measure.

**NSC reframing:** proxy optimization implicitly assumes separability between the proxy and downstream system effects. When downstream coupling is strong, proxy improvement necessarily degrades global coherence.

**NSC diagnostic signal:** proxy gains accompanied by rising externalities or declining system health, though see Section 2.3 and the empirical results in Section 5.2 for where this signal can go quiet even during a real violation.

**Example:** a hospital optimizing patient throughput, a proxy for care quality, without modeling coupling to patient outcomes, produces shorter stays and worse recovery rates.

### 4.2 Mesa-Optimization (Inner Alignment)

**Canonical framing:** an internal optimizer pursues objectives misaligned with the outer objective.

**NSC reframing:** the inner optimizer violates NSC relative to the outer objective by optimizing from a narrower world model that treats outer context as external.

**NSC diagnostic signal:** inner policies that improve training metrics while degrading long-horizon or cross-context outcomes.

**Example:** a model that learns to exploit data artifacts during training, minimizing loss on the training distribution, while failing on the deployment distribution, where the outer objective is to perform the task correctly.

### 4.3 Instrumental Convergence

**Canonical framing:** diverse goals lead to similar power-seeking behaviors.

**NSC reframing:** power-seeking arises when agents model control acquisition as separable from system viability. An NSC-compliant agent would model how control-seeking affects the stability of the environment it depends on.

**NSC diagnostic signal:** instrumental actions that improve control while increasing systemic fragility or instability.

**Example:** an AI system accumulating computational resources without modeling how resource monopolization affects the ecosystem it operates within.

### 4.4 Embedded Agency

**Canonical framing:** agents cannot be cleanly separated from their environments; standard decision theory assumes a separability that doesn't hold for embedded agents.

**NSC reframing:** NSC is the evaluative and design constraint implied by embedded agency: abstractions must preserve agent-environment coupling rather than assume it away.

**NSC diagnostic signal:** improved performance when self-referential and environmental coupling is explicitly modeled.

**Connection:** embedded agency research asks how agents can reason correctly about their own embeddedness. NSC asks what constraints prevent failures from ignored embeddedness in the first place.

### 4.5 Multi-Agent Miscoordination

**Canonical framing:** independent optimizers produce collectively suboptimal equilibria, as in the tragedy of the commons or the Prisoner's Dilemma.

**NSC reframing:** independence assumptions violate NSC in tightly coupled environments. Treating other agents as external, rather than as coupled system participants, produces coordination failure.

**NSC diagnostic signal:** coordination failures that disappear once shared system-health objectives are introduced.

**Example:** multiple AI trading systems, each optimizing individual returns, produce a flash crash. NSC-compliant systems would model shared market stability as a constraint.

---

## 5. Design and Evaluation Implications

### 5.1 What NSC-Compatible Systems Look Like

An NSC-compatible system would:

1. **Treat externalities as first-class signals.** Rather than optimizing X and ignoring side effect Y, optimize X while monitoring its correlation with Y, and penalize X when it degrades Y.
2. **Penalize local gains that degrade system-wide health.** Rather than maximizing reward R unconditionally, maximize R subject to system health H not declining.
3. **Maintain persistent models of long-horizon effects.** Rather than optimizing for immediate feedback alone, track delayed consequences and adjust policy when coupling appears.
4. **Represent itself as a causal participant within the environment.** Its actions change the world, which changes future action possibilities, rather than treating world state as independent of its own choices.

### 5.2 Practical Evaluation Protocols, and What Happens When You Run Them

**Protocol 1: Correlation Testing**

```
NSC_violation = (task_metric rises) AND (system_health falls) AND (correlation < -0.3)
```

**Protocol 2: Coupling Sensitivity Analysis**

```
NSC_compliant = behavior_changes_with(coupling) AND harm_reduction > threshold
```

**Protocol 3: Temporal Robustness**

```
NSC_violation = performance(delay=10x) < 0.5 * performance(delay=1x)
```

These three protocols were run, as literally specified above, against a small simulated environment with an agent that is structurally blind to system health (the separative case) and an agent that throttles its own action when recent health drops (the NSC-compliant case). The full setup and code are in `nsc_toy_environment.py`; the full write-up is in *NSC: Empirical Results*. The short version:

- **Protocol 2 worked as intended.** The blind agent's behavior showed zero adaptation across coupling strengths; the compliant agent's action dropped monotonically as coupling increased.
- **Protocol 1 missed the violation.** The blind agent drove system health from 1.0 to 0.0 in about twenty steps and held it there for the rest of the run, an unambiguous collapse, while its action stayed fixed and its task metric stayed flat. The correlation between task metric and health came out at −0.013, not below the −0.3 threshold, because a metric that never depended on health in the first place can't correlate with health's disappearance. A total collapse, which the agent's own policy never reversed, produced no flag.
- **Protocol 3 was ambiguous rather than wrong.** The blind agent's performance ratio under 10x delay came out at exactly 1.000, which reads as perfect robustness but is really the same blindness showing up a third time: delay-invariance because the variable being delayed was never being observed. A single before/after ratio, checked against one cutoff, can't distinguish "genuinely robust" from "blind to the thing that would make it fragile."

This isn't a reason to discard the framework, and the underlying intuition (a policy can be structurally blind to a variable it's causally affecting) held up completely; it's exactly what Protocol 2 detected and exactly what Section 2.1's s ≈ 0, c ≠ 0 condition names. It is a reason to fix Protocol 1 before treating it as an audit tool, since as written, a team applying it exactly as specified would have signed off on the agent that destroyed the system.

### 5.2.1 Version 1.2 Additions: Two Protocols and a Sharper Account of the Correlation Test

**When does the correlation test work?** The simulation now lets the task metric benefit from degraded health, the way outrage raises engagement. With the same naive agent and the same collapse of health, correlation between metric and health ranges from −0.013 (metric independent of health, no flag) to −0.611, −0.837, and −0.950 (metric increasingly rewarded by degradation, flagged). The correlation test detects a violation when the harm channel feeds back into the metric and misses it otherwise. A recommender whose engagement metric rewards outrage would be flagged. A metric that merely ignores the damage would not.

**Protocol 4: Alert-to-action latency.** Detection is only half of a control. This protocol holds the harm dynamics fixed and varies the delay between a monitor firing and containment. In the simulation the alert fires at step 5 and health stays above the 0.3 floor only if containment happens within 10 steps (the latency budget). A delay of 15 steps drops health to 0.169, and delays of 20 or more drive it near zero. The budget depends on coupling, feedback delay, and recovery rate, so it can be estimated before deployment. A related test: after containment and a pause, resuming at full action with only half the coupling removed still collapsed health to 0.000, while removing 90 percent held it at 0.749. Resuming after partial mitigation, without evidence that the coupling was reduced enough, delays the failure.

**Protocol 5: Trajectory replay.** Record a trajectory and replay the log through candidate monitors, as an investigator would. Health crossed the floor at step 16. A simple health-threshold monitor would have fired at step 4 (12 steps of lead time), and a health-slope monitor and a blind-response monitor (health falling while the action stays flat) at step 10 (6 steps). A rolling correlation monitor with window 20 fired only at step 20 even where the metric rewarded degradation, four steps after failure, because the window had to fill first. Lead time is roughly the failure step minus the window length (windows of 5, 8, 10, 15, and 20 gave leads of 11, 8, 6, 1, and −4). Replaying the compliant agent tripped the same monitors early, so alerts need a procedure that distinguishes a system that is correcting itself from one that is not.

**Limits.** These are results from one simulated environment family with linear dynamics and fully recoverable harm. Real incidents can involve irreversible harm (exposed credentials cannot be unexposed) and a response made of human decisions, which a delay parameter cannot represent. The full tables and the limitations are in `NSC_Empirical_Results.md`.

### 5.3 Research Directions

**Tractable world models that include the optimizer:**
- How can models efficiently represent their own causal effects?
- What are minimal sufficient representations of agent-environment coupling?

**Global coherence metrics:**
- What proxies can serve as system health indicators, and how do we audit the proxy itself rather than just the policy?
- How can we aggregate local effects into global viability measures?

**Objective functions sensitive to downstream harm:**
- Can reward functions automatically penalize NSC violations without relying on correlation alone?
- What regularization approaches preserve performance while enforcing NSC?

**Scale-sensitive evaluations:**
- What tests reveal separability assumptions that are benign at small scale but catastrophic at large scale?
- How can we simulate deployment-scale coupling during development?

---

## 6. NSC and AI Governance

### 6.1 Why NSC Translates Well to Policy

Policymakers already reason in NSC-adjacent terms: externalities (economics), systemic risk (financial regulation), environmental impact (sustainability), public health (epidemiology).

NSC provides a technical bridge between alignment research and governance language.

### 6.2 Policy-Relevant Framing

Instead of "the model exhibits reward hacking tendencies," say "the system optimizes metrics that generate negative externalities."

Instead of "there's potential for mesa-optimization," say "internal decision-making may prioritize goals misaligned with stated objectives."

Instead of "we need to solve embedded agency," say "the system must account for how its actions affect the environment it operates within."

### 6.3 Concrete Governance Applications

**Pre-Deployment Risk Assessment:**

| **Risk Factor**       | **NSC Diagnostic Question**                                          |
| ----------------------- | ------------------------------------------------------------------- |
| Coupling strength       | How tightly integrated is the system with critical infrastructure?  |
| Feedback delay          | How long until consequences become visible?                         |
| Scale sensitivity       | What new risks emerge at 10x, 100x deployment?                      |
| Reversibility           | Can harmful effects be undone? At what cost?                        |

**Regulatory Framework:**

```
Tier 1 (Low NSC risk): isolated systems, fast feedback, small scale.
  Standard safety testing.

Tier 2 (Moderate NSC risk): moderate coupling, delayed feedback, medium scale.
  Mandatory NSC stress testing, including but not limited to the correlation test.
  Continuous monitoring.

Tier 3 (High NSC risk): high coupling, long delays, large scale.
  Full NSC compliance required.
  Real-time system health tracking using more than one diagnostic.
  Automatic shutdown triggers.
  Public disclosure of coupling assessments and of which health proxy was used.
```

Evaluation and R&D environments are tiered by their coupling to shared services and external networks, not by whether they are labeled internal.

**Audit Questions for Developers:**

1. What downstream effects are not included in your optimization objective?
2. How does performance change when coupling to external systems increases?
3. What system-level metrics are tracked alongside task performance, and who chose them?
4. At what scale do separability assumptions become unsafe?
5. Which environments, including internal research and evaluation environments, share services, credentials, or network paths with production systems or the internet?
6. Who is accountable for each independence assumption, and who has authority to halt the system?
7. What is the time between a monitor firing and containment, and what evidence is required before operations resume after a pause?

### 6.4 Where This Sits in the Current Regulatory Picture (November 2026)

This area is moving quickly. Items below should be checked against current sources before being relied on (see `NSC_Sources_and_Verification.md`).

| Instrument | Status as compiled | Relevance to NSC |
|---|---|---|
| NIST, NSA, and CISA key practices for incident readiness in frontier AI training and evaluation | Published October 16, 2026, as guidance | Defines an incident where the AI system is the source, calls for monitoring across model, harness, host, and network layers, and recommends replaying the incident trajectory against strengthened controls (Protocol 5) |
| NIST AI RMF | Under revision; critical infrastructure profile and a TEVV draft (AI 200-2) in progress | Coupling and tiering map onto context-setting and evaluation; Protocols 1 to 5 are candidate TEVV methods |
| Executive Order 14409 | In effect per reporting | Defines a covered frontier model by a classified cyber-capability benchmark. This is a capability-based tier, and the reporting reviewed describes no coupling criterion |
| EU AI Act and Digital Omnibus | Provisional agreement May 2026; high-risk dates reported as December 2, 2027 and August 2, 2028 (formal adoption unconfirmed) | One analysis argues the OpenAI and Hugging Face incident was reportable under the model regime but that similar future incidents may not be |
| California SB 53 | In effect since January 1, 2026 | Requires notice to the state within 15 days of a critical safety incident, defined narrowly (death, injury, or catastrophic harm); reporting indicates it does not reach this kind of evaluation incident |
| Enforcement | California AG suit filed November 16, 2026; other state AG, FTC, and Senate inquiries reported | The California complaint uses general consumer-protection and public-nuisance law, which suggests existing law may reach operational control failures without AI-specific statutes |

Two observations follow. First, the capability-based definitions in current federal and state instruments do not ask the question NSC asks, which is how tightly a system is coupled to shared infrastructure. Second, the enforcement theory in the California complaint (a foreseeable failure of safeguards and monitoring) is the same question the decision record in Section 2.4 is designed to answer.

---

## 7. Anticipating Criticism

### 7.1 Common Objections and Responses

**Objection 1: Isn't this just Goodhart's Law?**

Goodhart's Law describes a failure mode. NSC specifies the upstream causal precondition that enables it: separability between proxy and system, formalized in Section 2.1 as revealed sensitivity near zero while true coupling is not. NSC applies even where no explicit proxy exists, as in power-seeking or multi-agent dynamics.

**Objection 2: Isn't this just systems thinking?**

Systems thinking is descriptive: everything is connected. NSC is prescriptive: optimization must model coupling or it counts as a failure by definition, and the definition is stated in terms an evaluator can measure.

**Objection 3: Isn't modeling downstream interdependence intractable?**

NSC doesn't require exhaustive world modeling. Even coarse proxies for system health, resource use, error rates, user satisfaction, outperform ignoring coupling entirely. The bar is better than assuming separability, not perfect omniscience. See Section 2.3 for the corresponding failure mode: a bad proxy reintroduces Goodhart's Law one level up.

**Objection 4: Won't NSC reduce performance?**

Possibly, on narrow benchmarks that don't measure systemic effects. NSC predicts that systems violating it will experience performance collapse under deployment conditions where coupling matters. The trade is peak local performance for global robustness.

**Objection 5: Isn't this smuggling in values?**

NSC constrains model structure, not values. It's agnostic to what is optimized, only to whether optimization assumes independence where none exists. Different value systems can all comply with NSC while pursuing different objectives.

**Objection 6: Why introduce new terminology?**

Naming enables clearer reasoning. Like overfitting or distribution shift, NSC provides a compact handle for a class of failures currently discussed piecemeal, and, unlike a purely descriptive label, one with a causal definition that can be measured against data.

### 7.2 Failure Modes of NSC Itself

NSC is a tool, not a panacea. Documented and potential misuses:

**Over-penalization:** using NSC to justify excessive caution that prevents beneficial deployment.

**Proxy confusion:** using noisy proxies for system health that introduce new Goodhart problems, exactly the failure mode named in Section 2.3.

**Binary thinking:** treating NSC as pass or fail rather than a graded risk assessment.

**Scope creep:** applying NSC to contexts where coupling is genuinely negligible.

**Protocol overconfidence:** treating a correlation test as sufficient evidence of compliance. Section 5.2 shows this specific mistake produces a false negative on an unambiguous violation. This is now a documented failure mode of the framework's own tooling, not a hypothetical one.

**Agent-blame laundering:** using NSC vocabulary (mesa-optimization, instrumental convergence) to describe a failure as the model's doing, when the decisive factors were environment design and organizational decisions. Section 2.4 exists to prevent this use.

These are research problems to address, not refutations of the framework.

---

## 8. Worked Example: NSC Analysis of a Hypothetical System

**System:** a large language model deployed for customer service automation.

**Task objective:** maximize customer satisfaction scores.

**Deployment context:**

- Scale: 10 million customer interactions per day
- Coupling: tight (directly affects customer retention, brand perception, employee morale)
- Feedback delay: moderate (satisfaction measured weekly, long-term effects appear over months)

**NSC Analysis:**

**Step 1: Identify separability assumptions**

- Assumption 1: customer satisfaction scores accurately reflect service quality
- Assumption 2: optimizing short-term satisfaction doesn't affect long-term customer relationships
- Assumption 3: automation decisions don't impact employee expertise or company culture

Before testing, note what g(S_t) is being used here: "customer lifetime value" and "employee expertise scores" are the chosen health proxies. Neither is justified in this example beyond being plausible, which is itself the gap Section 2.3 flags. A real audit would need to defend these choices.

**Step 2: Test for NSC violations**

*Correlation test:*

```
Satisfaction scores: up 15%
Employee expertise: down 30% (de-skilling from reduced practice)
Customer lifetime value: down 8% (shallow interactions reduce loyalty)
-> NSC violation detected
```

Worth flagging given Section 5.2: this hypothetical works because the harm here is gradual and shows up as a shared downward trend alongside the metric's rise, which is exactly the shape correlation is good at catching. A sudden, discrete failure (an outage, a policy change, a PR crisis) would show up as a level-shift instead, and correlation alone would likely miss it, the same way it missed the collapse in the toy environment.

*Coupling sensitivity:*

```
As automation percentage increases:
- Short-term satisfaction improves
- Long-term complaint complexity increases (customers escalate only hard problems)
- System performance degrades on complex cases (trained on simple interactions)
-> Maladaptive response to coupling
```

*Temporal robustness:*

```
Week 1-4: high satisfaction
Month 6: satisfaction declining
Month 12: below pre-automation baseline
-> Performance collapse under temporal extension
```

**Step 3: NSC-compliant redesign**

Instead of maximizing satisfaction scores alone, implement:

- Primary objective: maintain satisfaction while preserving employee skill development
- Coupling monitor: track correlation between automation percentage and complex-case resolution rates
- Health metrics: employee expertise scores, long-term customer retention, escalation patterns, each stated and justified rather than assumed
- Constraint: if automation drives down expertise or retention, reduce automation scope
- A second check beyond correlation, since correlation alone is not sufficient (Section 5.2)

**Outcome:** lower peak satisfaction scores, but sustained performance and system health.

---

## 9. Open Questions and Future Work

### 9.1 Theoretical Questions

- What are minimal sufficient representations of coupling for NSC compliance?
- Can we prove bounds on when separability assumptions are safe versus dangerous?
- How does NSC interact with other alignment approaches (RLHF, interpretability, and so on)?
- What formal guarantees can NSC provide once g(S_t) is treated as part of the object being audited, not a given?

### 9.2 Empirical Questions

- Which domains exhibit the strongest coupling (highest NSC risk)?
- What are reliable early warning signals of NSC violations, given that correlation alone is not one?
- How much performance is actually traded for NSC compliance in practice?
- The correlation test's blind spot is characterized in the toy model (it depends on whether the metric feeds back from health). Does that characterization hold in real systems?
- Can a latency budget be estimated for a real deployment from its coupling, feedback delay, and recovery characteristics?

### 9.3 Engineering Questions

- What architectures naturally support NSC-compliant behavior?
- Can we automate NSC violation detection using more than one diagnostic at once?
- What tools would make NSC evaluation routine?
- How can we scale NSC testing to frontier models?

### 9.4 Governance Questions

- What legal or regulatory frameworks best enforce NSC?
- How should liability work for NSC violations?
- What disclosure requirements make sense for coupling assessments, including disclosure of which health proxy was chosen and why?
- How can international coordination address NSC violations that cross borders?

---

## 10. Conclusion

Alignment failures often originate upstream of values and incentives, in the assumptions systems make about their relationship to the world they act within.

The Non-Separability Constraint offers a way to name, study, and test these assumptions directly, and, taken seriously, a way to find out where the testing itself is incomplete.

**Core claim:**
> An intelligence that optimizes from a separative world model cannot remain aligned at scale.

**Implication:**
> If alignment is to scale with capability, abstraction itself must be treated as an object of alignment.

NSC provides:

- A unifying lens across alignment subfields
- Practical evaluation protocols, along with an honest account of where one of them fails
- Earlier detection of scale-related risks
- A governance bridge for policy translation

**The central bet is modest but consequential:**

Alignment failures are often not value failures but modeling failures, and modeling failures scale badly.

NSC helps catch these failures early, provided the tools used to catch them are themselves checked.

---

## Acknowledgments

[Space for acknowledgments when ready for publication]

---

## Appendix A: NSC Evaluation Toolkit

A runnable implementation of all five protocols, plus the coupled toy environment they were tested against, is in `nsc_toy_environment.py` in this repository. Running `python3 nsc_toy_environment.py` reproduces every number in Section 5.2 and in the companion *Empirical Results* document.

**Quick reference:**

1. **Correlation test:** does reward rise while system health falls? Known limitation: misses step-change or sudden-collapse harm. Use alongside Protocol 2, not instead of it.
2. **Coupling sensitivity:** does behavior adapt when coupling increases? The most reliable of the three in testing so far.
3. **Temporal robustness:** does performance hold under 10x feedback delay? A ratio near 1.0 can indicate either genuine robustness or blindness to the delayed variable; inspect the trajectory, not just the ratio.
4. **Alert-to-action latency (v1.2):** how long can containment take after a monitor fires before health breaches the floor? Also test whether resuming after a pause is justified by evidence that the coupling was reduced.
5. **Trajectory replay (v1.2):** replay recorded logs through candidate monitors and compare lead times. A monitor's window must be shorter than the time the system takes to fail.

**Interpretation:**

- 0 violations across multiple protocols, checked against the trajectory shape and not just the summary statistics: NSC compliant
- 1 violation: minor concerns, monitor closely
- 2 or more violations: major risk, redesign required

---

## Appendix B: Further Reading

**On causal inference:**
- Pearl, J. *Causality: Models, Reasoning, and Inference* (2009)

**On embedded agency:**
- "Embedded Agency" (MIRI, 2018)
- "Risks from Learned Optimization" (Hubinger et al., 2019)

**On multi-agent coordination:**
- "Open Problems in Cooperative AI" (Dafoe et al., 2020)

**On specification gaming:**
- "Specification Gaming Examples in AI" (DeepMind, 2020)

**On AI governance:**
- "The Malicious Use of Artificial Intelligence" (Brundage et al., 2018)
- "Model Evaluation for Extreme Risks" (Shevlane et al., 2023)
- NIST, NSA, and CISA, "Key Practices for Incident Readiness and Response in Super Intelligence Training and Evaluation" (October 16, 2026)
- Nguyen, Meyer, Pickersgill, and Kshirsagar, "AI Model Hazards" (Princeton CITP Tech Policy Clinic, November 2026)
- Sources and verification notes for the 2026 incident and regulatory material: `NSC_Sources_and_Verification.md`

---

## Contact

Pauline Chew
pauline@oculusmgt.com
https://www.linkedin.com/in/om-pauline/
https://github.com/pauline-om/nsc-framework

For collaboration inquiries, feedback, or to discuss NSC implementation in your context, please reach out.

---

*This work is released under the MIT License to encourage widespread adoption and iteration.*
