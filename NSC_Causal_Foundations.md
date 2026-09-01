# NSC: A Causal Formalization

*A proposed replacement for Section 2.1 of the white paper.*

The original formal statement introduces an optimizer O, an objective f, an environment E, a world model M, and a coupling C, then says NSC is violated when M treats E as independent, a coupling C exists, and C isn't represented in M or f. As written this is a description of the idea in symbols, not a definition anyone could compute from data. Nothing here says what C is, how large is large enough to matter, or how you'd measure whether M "represents" it. Below is an attempt to say the same thing in a form that can actually be tested against a trajectory of data, using tools that already exist in causal inference rather than inventing new ones.

## 1. The environment as a structural causal model

Treat the optimizer and its environment as a structural causal model (Pearl, *Causality*, 2009) with, at minimum, three variables evolving over time:

- **A_t** — the action chosen by the optimizer at time t.
- **M_t** — the task metric, the quantity the optimizer is trained or instructed to increase.
- **S_t** — the coupled state variable, whatever the optimizer's action can plausibly affect beyond the task metric itself: discourse quality, market liquidity, an employee's skill level, a species population.

The structural equations governing the system are:

```
S_{t+1} = f_S(S_t, A_t, U_t)
M_t     = f_M(A_t, S_t, V_t)
A_t     = π(H_t)
```

where U_t and V_t are exogenous noise terms and H_t is the optimizer's observed history. π is the policy: whatever function, learned or hand-written, maps history to action.

This is standard machinery. Nothing about it is NSC-specific. What NSC adds is a claim about the relationship between two things that live at different levels: the *true* structural equation f_S, and the policy's *effective* dependence on S.

## 2. Coupling strength, defined as a causal effect

Define coupling strength as the average causal effect of the action on next-period system health, using the do-operator to distinguish this from a merely observed correlation:

```
c = E[S_{t+1} | do(A_t = a + δ)] − E[S_{t+1} | do(A_t = a)]
    ────────────────────────────────────────────────────────
                            δ
```

as δ → 0, evaluated at the action the policy actually takes. This is a number (or, more generally, a function of state), and in a simulated environment it can be measured directly by intervention: hold everything else fixed, perturb the action, read off the change in next-period health. In a live deployed system it has to be estimated, which is harder but not exotic; it's the same problem instrumental-variable and difference-in-differences methods exist to solve.

c = 0 means the action genuinely has no effect on system health, in which case there's nothing for NSC to say. The interesting case, and the one the white paper's examples are all drawn from, is |c| bounded away from zero.

## 3. Separability, defined as a missing causal path in the objective's information flow

An optimizer's world model is separative with respect to S if the policy's dependence on S is zero even though c ≠ 0. Concretely: define the policy's *revealed sensitivity* to health as

```
s = ∂π(H_t) / ∂S_t
```

holding the rest of H_t fixed (or, in the non-differentiable case, the change in the optimal action induced by an intervention on S_t alone). NSC is violated when

```
c ≠ 0   and   |s| < ε
```

for some domain-chosen threshold ε near zero. In words: the action genuinely changes system health, but the policy behaves as if it doesn't, because nothing in the objective, the training signal, or the world model routes information back from S to the choice of A.

This is the same idea as the white paper's Section 2.1, but every symbol in it is either directly measurable from logged trajectories (c, via intervention or estimation) or computable from the policy itself (s, via a sensitivity analysis or perturbation test). Section 7's response to "isn't this just Goodhart's Law" holds up better once stated this way: Goodhart's Law is the *symptom* (a proxy stops tracking the target once optimized against), and NSC as defined here is the specific *causal precondition* that produces it, namely s ≈ 0 while c ≠ 0. That's a claim you can go test in a specific system, not just a redescription of the failure after it happens.

## 4. System health, g(S_t), is a modeling choice and should be treated as one

The white paper treats "system health" as though it's a single well-defined quantity waiting to be read off. It isn't. S_t is whatever the true (possibly high-dimensional, possibly unobserved) state is, and system health is a scalar summary H_t = g(S_t) chosen by whoever runs the evaluation. This choice is doing real work and can silently reintroduce the exact problem NSC is trying to solve: if g is itself a proxy that can be optimized against, an NSC-compliant system by this definition can still be behaving badly relative to whatever g failed to capture. Any application of this framework should say explicitly what g is, why it was chosen, and what it's known to miss. The white paper doesn't do this in any of its worked examples; the "system health" in the customer-service case (Section 8) is asserted, not constructed.

## 5. What this buys you over the original phrasing

- c is estimable from data using existing causal-inference tools, rather than being an unexplained symbol.
- s is a real, computable sensitivity, which turns "is the coupling represented in M or f" from a qualitative judgment call into a number you can put a threshold on.
- The Goodhart's Law / systems-thinking / embedded-agency objections in Section 7 can be answered with "here is the specific quantity we claim is near zero," which is a stronger response than "no, this is different."
- It exposes the dependency on g(S_t) that the original document doesn't surface, which is arguably the single largest source of hidden error in any actual NSC audit: pick the wrong health proxy and you've reintroduced Goodhart's Law one level up.

The toy simulation in `nsc_toy_environment.py` implements exactly this: c is a parameter you set directly (since it's a toy world, you get to play Pearl's demon and set do(A_t) yourself), s is estimated by comparing a policy that's structurally blind to S_t against one that isn't, and g(S_t) = S_t itself, made explicit rather than left implicit, precisely because in a toy world there's no excuse not to.
