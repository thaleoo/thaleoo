<div align="center">

<img src="assets/banner.svg" alt="Thaleo Osorio — Mathematics · Computational Physics · Systems Programming · Cryptography" width="100%"/>

<br/>

<a href="https://www.linkedin.com/in/jj-osorio"><img src="https://img.shields.io/badge/LinkedIn-jj--osorio-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0d1117" alt="LinkedIn"/></a>
<a href="https://orcid.org/0009-0000-0240-7005"><img src="https://img.shields.io/badge/ORCID-0009--0000--0240--7005-A6CE39?style=for-the-badge&logo=orcid&logoColor=white&labelColor=0d1117" alt="ORCID"/></a>
<img src="https://img.shields.io/badge/UNAL-La%20Paz%2C%20Colombia-ff7a45?style=for-the-badge&labelColor=0d1117" alt="Universidad Nacional de Colombia, La Paz"/>
<img src="https://img.shields.io/badge/%23-KnowledgeMustBeFree-58c4dc?style=for-the-badge&labelColor=0d1117" alt="#KnowledgeMustBeFree"/>

<br/><br/>

<a href="#-numerical-experiments"><img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=3000&pause=1000&color=FF7A45&center=true&vCenter=true&width=640&lines=Simulating+phase+transitions+with+Monte+Carlo;Building+end-to-end+encryption+in+Rust;Chasing+the+zeros+of+%CE%B6(s);Understanding+%3E+applying;%23KnowledgeMustBeFree" alt="Typing animation"/></a>

</div>

---

## `$ cat about.md`

I'm **Thaleo Osorio** (academically **Juan J. Osorio-Díaz**), a Biological Engineering undergraduate at the **Universidad Nacional de Colombia, La Paz campus** — and an aspiring interdisciplinary researcher and software developer.

My degree is biological; my obsession is **the mathematics and computation underneath natural phenomena**. I want to understand how things work at a fundamental level, build the tools to investigate them, and eventually contribute original ideas to science and technology.

A typical loop for me: study a mathematical model → implement the simulation in **Rust** → analyse it in **Python** → document the whole experiment, reproducibly, in **Typst**.

```rust
pub struct Thaleo {
    pub degree:    &'static str,          // "Biological Engineering @ UNAL"
    pub thinks_in: [&'static str; 4],     // math, physics, CS, engineering
    pub builds_in: [&'static str; 3],     // Rust, Python, Typst
    pub principle: &'static str,          // "Understanding > applying"
}

impl Thaleo {
    pub fn goal(&self) -> &str {
        "Researcher and educator: contribute knowledge, make rigour accessible."
    }
}
```

---

## 🧭 Research interests

<table>
<tr>
<td width="33%" valign="top">

### ∑ Mathematics
- Real & complex analysis
- **Analytic number theory** — ζ(s), the Riemann Hypothesis
- Infinite series & convergence
- Special functions
- (Numerical) linear algebra
- Differential equations
- Mathematical methods for physics

</td>
<td width="33%" valign="top">

### ⚛ Physics
- Statistical mechanics
- **Phase transitions & critical phenomena**
- Computational & condensed-matter physics
- Quantum mechanics
- Nonlinear & classical dynamical systems
- Emergent behaviour from simple rules

</td>
<td width="33%" valign="top">

### 🔐 Computing & security
- **Systems programming in Rust**
- Scientific computing & algorithms
- Cryptographic engineering
- **Post-quantum cryptography**
- Secure messaging protocols
- ML systems, AI security, software provenance

</td>
</tr>
</table>

---

## 🔬 Numerical experiments

> Every animation on this page is generated from my own code — no stock GIFs. The scripts live in [`scripts/`](scripts/) so anyone can reproduce them.

<table>
<tr>
<td width="50%" valign="top">

<img src="assets/ising.gif" alt="2D Ising model annealed through the critical temperature" width="100%"/>

**2D Ising model.** A 150×150 lattice annealed from the paramagnetic phase through T<sub>c</sub> = 2/ln(1+√2) ≈ 2.269 with Metropolis checkerboard updates. Domains grow and the magnetisation is compared against Onsager's exact solution — the lag behind the curve is real finite-time relaxation, not a bug.

</td>
<td width="50%" valign="top">

<img src="assets/lorenz.gif" alt="Lorenz attractor with two nearby initial conditions diverging" width="100%"/>

**Lorenz attractor.** Two trajectories that start 10⁻⁵ apart, integrated with RK4. They trace the same strange attractor but separate exponentially — deterministic chaos and sensitive dependence on initial conditions in one picture.

</td>
</tr>
<tr>
<td width="50%" valign="top">

<img src="assets/zeta.gif" alt="Riemann zeta function traced along the critical line" width="100%"/>

**ζ(½ + it).** The Riemann zeta function traced along the critical line for 0 ≤ t ≤ 42. Each time the curve passes through the origin we hit a non-trivial zero (14.1347…, 21.0220…, …). This is the object at the centre of my analytic number theory roadmap.

</td>
<td width="50%" valign="top">

### What's next on the bench
- [ ] Finite-size scaling & critical exponents for Ising (Rust core, Python analysis)
- [ ] Wolff cluster algorithm vs. Metropolis near T<sub>c</sub>
- [ ] Site percolation and the spanning threshold
- [ ] Brownian motion & diffusion
- [ ] Time-dependent Schrödinger equation (split-step Fourier)

**Workflow**

```mermaid
flowchart LR
  A[Model<br/>math] --> B[Simulate<br/>Rust]
  B --> C[Analyse<br/>Python]
  C --> D[Document<br/>Typst]
  D -. new questions .-> A
```

</td>
</tr>
</table>

---

## 🛠 Projects

### 🔑 [Cista](https://github.com/thaleoo/cista) — local, encrypted password manager &nbsp; ![Rust](https://img.shields.io/badge/Rust-0d1117?style=flat-square&logo=rust&logoColor=ff7a45) ![status](https://img.shields.io/badge/status-active-3fb950?style=flat-square&labelColor=0d1117)

<img src="assets/cista-demo.gif" alt="Cista terminal demo: init, add, list, health, raw vault bytes" width="800"/>

Your credentials live in a single `*.cista` file — without the master password it's just bytes. Educational, but built with real cryptographic practice rather than toy implementations:

| Layer | Choice |
|---|---|
| Key derivation | **Argon2id** (64 MiB, 3 iterations) |
| Encryption | **XChaCha20-Poly1305** AEAD, file header authenticated as AAD |
| Secrets in memory | `secrecy` + `zeroize` — wiped on drop; best-effort `mlockall`, core dumps disabled |
| UX | CLI + REPL session + Ratatui TUI, auto-lock, clipboard auto-clear, password health (zxcvbn) |
| Architecture | Cargo workspace: `cista-core` · `cista-cli` · `cista-tui` |

> *Demo above uses the real `cista` binary output; only the typing is animated.*

<br/>

<table>
<tr>
<td width="50%" valign="top">

### 💬 Atrio
**End-to-end encrypted terminal messenger** · ![Rust](https://img.shields.io/badge/Rust-0d1117?style=flat-square&logo=rust&logoColor=ff7a45) ![wip](https://img.shields.io/badge/status-in%20development-ff7a45?style=flat-square&labelColor=0d1117)

Secure communication without depending on centralised commercial services.
- **X3DH** key agreement + **Double Ratchet**
- **Ed25519** identities · **X25519** key exchange
- Async networking · **Ratatui** TUI
- Next: post-quantum KEMs, optional Tor transport

</td>
<td width="50%" valign="top">

### 🎞 Animath
**Programmable mathematical animation** · ![Rust](https://img.shields.io/badge/Rust-0d1117?style=flat-square&logo=rust&logoColor=ff7a45) ![concept](https://img.shields.io/badge/status-design-a58bff?style=flat-square&labelColor=0d1117)

Making mathematical communication *programmable, precise and reproducible*.
- Geometric constructions & typeset expressions
- Function plots and physical vector fields
- Scientific diagrams and animated explanations

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧲 Computational Physics
**Numerical experiments collection** · ![Rust](https://img.shields.io/badge/Rust-0d1117?style=flat-square&logo=rust&logoColor=ff7a45) ![Python](https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=58c4dc) ![Typst](https://img.shields.io/badge/Typst-0d1117?style=flat-square&logo=typst&logoColor=239dad)

Theory → implementation → numerical results → interpretation. Centred on the 2D Ising model: Monte Carlo, critical temperature, finite-size scaling and universality.

</td>
<td width="50%" valign="top">

### 🧠 ADNI · MCI → Alzheimer's
**Clinical ML / data analysis** · ![Python](https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=58c4dc) ![pandas](https://img.shields.io/badge/pandas-0d1117?style=flat-square&logo=pandas&logoColor=e6edf3)

Academic project on the Alzheimer's Disease Neuroimaging Initiative: longitudinal clinical data, missing-value analysis, statistical testing, EDA and ML-ready preprocessing to study progression from mild cognitive impairment.

</td>
</tr>
</table>

### 🌱 Synapse — open knowledge & student research
An initiative for students to be **active contributors** to research and technology, not passive consumers: open-source projects, collaborative research and shared academic resources. **#KnowledgeMustBeFree**

---

## 🗺 Roadmap · analytic number theory

```mermaid
flowchart LR
  CA[Complex analysis] --> DS[Dirichlet series]
  DS --> EP[Euler products]
  EP --> AC[Analytic continuation]
  AC --> FE[Functional equation]
  FE --> LF[L-functions]
  LF --> RH((Riemann<br/>Hypothesis))
```

Learning these rigorously — as one connected structure rather than isolated curiosities.

---

## 🧰 Toolbox

<div align="center">

<img src="https://skillicons.dev/icons?i=rust,python,bash,linux,fedora,git,github,latex,md&theme=dark" alt="Rust, Python, Bash, Linux, Fedora, Git, GitHub, LaTeX, Markdown"/>

<br/><br/>

![Typst](https://img.shields.io/badge/Typst-239DAD?style=flat-square&logo=typst&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Cargo](https://img.shields.io/badge/Cargo-000000?style=flat-square&logo=rust&logoColor=white)
![Ratatui](https://img.shields.io/badge/Ratatui-1f2328?style=flat-square&logo=rust&logoColor=white)
![Zsh](https://img.shields.io/badge/Zsh-F15A24?style=flat-square&logo=zsh&logoColor=white)

</div>

| Area | Tools |
|---|---|
| **Daily drivers** | Rust · Python · Bash · Fedora Linux · Zsh · Git · terminal-first workflow |
| **Science stack** | NumPy · pandas · statistical analysis · numerical simulation · data visualisation |
| **Writing** | Typst for research notes & papers · LaTeX · Markdown |
| **Actively learning** | Cryptographic engineering · post-quantum crypto · ML systems · embedded electronics |

---

## ⚖️ How I work

| Principle | In practice |
|---|---|
| **Rigour** | Mathematical correctness, evidence and well-founded arguments. |
| **Understanding** | I want to know how a tool is built, why it works and where it breaks — not just how to call it. |
| **Reproducibility** | If others can't inspect and rerun it, it isn't finished. |
| **Craftsmanship** | Clean architecture, maintainable code, honest documentation. |
| **Open knowledge** | Open source, accessible resources, collaborative learning. |

<details>
<summary><b>Beyond the terminal</b></summary>
<br/>

Electronics & DIY engineering · embedded systems · robotics & human–machine interaction · astronomy & astrophysics · chess · calisthenics · minimalist, functional design · open hardware.

</details>

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/thaleoo/thaleoo/output/snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/thaleoo/thaleoo/output/snake.svg"/>
  <img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/thaleoo/thaleoo/output/snake.svg"/>
</picture>

<br/>

<sub><i>Understanding, constructing and exploring systems through mathematics, science and computation.</i></sub>

</div>
