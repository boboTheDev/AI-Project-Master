# UI Starting Conventions

Use these checks when a project has no more specific approved design rule. They are quality prompts, not a universal visual style.

- Make the primary task, information hierarchy, and next action clear. Use the project's terminology and real content shape.
- Design material empty, loading, success, validation, permission, and error states with a recovery path where relevant.
- Keep interactive controls keyboard reachable, visibly focused, labeled, and usable without color alone. Respect reduced motion preferences when motion is present.
- Inspect representative narrow and wide layouts and the input modes that matter to the product. Avoid assuming a single screenshot proves responsiveness or interaction.
- Reuse approved tokens and components; introduce a new visual rule only when the existing system cannot express the needed behavior coherently.
- Choose visual density, typography, color, imagery, and motion from the audience and task. Do not force a fashionable aesthetic or fabricate product claims and data.
- Record UI review findings with route, viewport, state, evidence, severity, and owning layer. Retain captures under `.project/ui/` only when they help owner review or future comparison; transient captures can remain outside durable project memory.
- Keep a prototype handoff clear about approved versus draft source revisions, synthetic data, simulated actions, and states that could not be rendered. Recheck the same state after a UI implementation fix.
