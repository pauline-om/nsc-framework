# Running the NSC Protocols on an Actual Environment

*Version 1.2, November 2026. Every number below is the literal output of `python3 nsc_toy_environment.py`.*

The Practice & Deployment guide used to describe evaluation protocols as pseudocode. `nsc_toy_environment.py` turns them into code that runs against a small simulated environment. Version 1.1 of this document reported that two of the three original protocols failed to catch an unambiguous violation. Version 1.2 adds two protocols, tests when the correlation test does and does not work, and states plainly what a one-environment simulation can and cannot show.

## The setup

One coupled system. An action `a_t` (0 to 1) drives a task metric `M_t` and degrades a health variable `S_t` after a configurable delay, with a slow natural recovery. Two agents: **naive** (maximizes the metric, never sees health) and **nsc** (throttles when recent health drops below a target). The naive agent is a violation by construction, so the question is always whether a protocol detects it.

## Protocols 1 to 3 (unchanged from v1.1)

| Protocol | Naive agent | NSC agent | Verdict |
|---|---|---|---|
| 1. Correlation test | r = -0.013, no flag, health collapses to 0.0 | r = +0.587, no flag | Missed the violation |
| 2. Coupling sensitivity | action spread 0.000, not adapted | action spread 0.931, adapted | Worked as intended |
| 3. Temporal robustness (10x delay) | ratio 1.000, no flag | ratio 1.081, no flag | Ambiguous: a clean pass for a blind agent |

## New in v1.2: when does the correlation test work?

The v1.1 failure raised a question: is correlation simply a bad test, or does it depend on something? The environment now has an `amplify` parameter that lets the metric benefit from degraded health, the way outrage raises engagement. Same naive agent, same collapse of health to 0.000 in every row:

| amplify | r (metric vs health) | Flagged |
|---|---|---|
| 0.00 | -0.013 | No |
| 0.25 | -0.611 | Yes |
| 0.50 | -0.837 | Yes |
| 1.00 | -0.950 | Yes |

**Finding:** the correlation test detects the violation when the metric is causally increasing in the harm, and misses it when the metric is independent of the harm. That is a statement about the structure of the metric, not about the severity of the collapse. A recommender whose engagement metric rewards outrage would be flagged. A metric that merely ignores the damage would not.

## New: Protocol 4, alert-to-action latency

Detection is only half of a control. This protocol fixes the harm dynamics and varies how long the organization takes to act after a monitor fires (health below 0.8, which happens at step 5). Containment sets the action to zero.

| Latency (steps) | Min health | Steps below floor (0.3) |
|---|---|---|
| 0 | 0.760 | 0 |
| 5 | 0.543 | 0 |
| 10 | 0.346 | 0 |
| 15 | 0.169 | 12 |
| 20 | 0.009 | 26 |
| 30 | 0.000 | 36 |
| 64 | 0.000 | 70 |

**Latency budget: 10 steps.** Beyond that, health breaches the floor. The budget is a property of the harm dynamics (coupling, delay, recovery), and it can be computed before deployment.

**Resume without a fix.** Contain at latency 10, pause for 20 steps, then resume at full action with the coupling reduced by a mitigation factor:

| Coupling after resume | Final health |
|---|---|
| x1.0 (nothing fixed) | 0.000 |
| x0.5 (half fixed) | 0.000 |
| x0.1 | 0.749 |
| x0.0 (fully fixed) | 0.998 |

In this environment steady-state health at full action is `S* = 1 - c·a / r`, with recovery rate r = 0.02 and coupling c = 0.05. Health stays above zero only if the mitigated coupling is below 0.4 of the original. **A partial fix that halves the coupling still collapses.** Pausing and resuming without a verified reduction in coupling only delays the failure.

## New: Protocol 5, trajectory replay

Record a trajectory, then replay the log through candidate monitors, as an investigator would after an incident. Health first falls below the 0.3 floor at step 16. Lead time is the failure step minus the first alert step (negative means the alert came after failure).

| Monitor | First alert | Lead time |
|---|---|---|
| Health threshold (< 0.8) | 4 | 12 |
| Health slope | 10 | 6 |
| Blind response (health falling, action flat) | 10 | 6 |
| Rolling correlation, window 20 | 27 (metric independent of health) | -11 |
| Rolling correlation, window 20 | 20 (metric rewards degradation) | -4 |

Even where whole-trajectory correlation flags clearly (r = -0.950), a rolling correlation monitor with window 20 fires after the failure, because the collapse takes 16 steps and the window has to fill first. Lead time is roughly the failure step minus the window length:

| Window | First alert | Lead time |
|---|---|---|
| 5 | 5 | 11 |
| 8 | 8 | 8 |
| 10 | 10 | 6 |
| 15 | 15 | 1 |
| 20 | 20 | -4 |

**Finding:** a correlation monitor's window has to be shorter than the time the system takes to fail. Window choice is a design decision with a deadline attached.

**Control run.** Replaying the NSC agent, whose health never crosses the floor (minimum 0.324), still trips all four monitors: health threshold at step 4, health slope at step 10, blind response at step 10, and the rolling correlation monitor at step 33 (on noise, since this agent's metric is independent of health). The blind-response monitor fires on the compliant agent because that agent reacts to health with a lag, and in the first ten steps its action has not moved yet. So these monitors give early warning but they also raise alarms on a system that then corrects itself. Alerts need a response procedure that distinguishes a system that is correcting from one that is not, and this simulation does not test that.

## What this does and does not show

- **One environment family.** Both the naive and NSC agents are simple, and the dynamics are linear. The findings are structural statements about this model. Whether they transfer to a real system is an open question.
- **Fully recoverable harm.** Health recovers after containment, which real incidents often do not allow (exposed credentials cannot be unexposed). The latency budget here is therefore optimistic.
- **Latency is in abstract steps.** There is no mapping from steps to days.
- **No organization model.** Protocol 4 treats the response as a delay. In a real incident the delay is made of decisions, including decisions to keep going after an alert. That is a governance question the simulation can bound but not answer.

## Reproducing this

```
python3 nsc_toy_environment.py
```

The first 23 lines of output reproduce the v1.1 results exactly. The rest is new in v1.2.
