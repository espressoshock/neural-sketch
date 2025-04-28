# ![logo dark](https://github.com/user-attachments/assets/80788604-6e25-417d-a543-70fc9991f003) Neural Sketch

**A modern, opinionated, yet highly customizable LaTeX package for crafting consistent, publication-ready diagrams.**

---

[![Version](https://img.shields.io/badge/version-v1.2.0-blue.svg)](#)
[![Made with](https://img.shields.io/badge/made%20with-LaTeX3-brightgreen.svg)](https://www.latex-project.org/)
[![TikZ Compatible](https://img.shields.io/badge/compatible-TikZ-orange.svg)](https://ctan.org/pkg/pgf)
[![l3build](https://img.shields.io/badge/built%20with-l3build-purple.svg)](https://ctan.org/pkg/l3build)
[![l3keys](https://img.shields.io/badge/configured%20with-l3keys-ff69b4.svg)](https://ctan.org/pkg/l3keys2e)
[![docs](https://img.shields.io/badge/documented%20with-l3doc-informational.svg)](https://ctan.org/pkg/l3doc)


## Overview

**Neural Sketch** is a publication-oriented diagramming toolkit for LaTeX, designed for researchers who demand both speed and polish. With opinionated defaults, a key–value API for deep customization, and a portable design philosophy, Neural Sketch collapses the typical trade‑off between configuration overhead and figure aesthetics. 

📚 **[Check the documentation](https://neural-sketch.app/)**

<br/><br/>

![nsk_preview](https://github.com/user-attachments/assets/dbe29248-8106-43e1-8dba-bc3426e9cb57)


## 🌟 Why Neural Sketch?

> **Diagrams aren’t decoration—they’re the lens readers use to see your ideas.**

- **Opinionated defaults**: Publication‑tuned styling out of the box.
- **Key–value API**: Override only what you care about.
- **Transportable**: Same source for papers, slides, and web demos.
- **Layered architecture**: Core primitives + domain‑specific dialects + raw TikZ/pgf interop.

Whether you’re mapping neural nets, flowcharts, or optimization pipelines, Neural Sketch keeps your focus on ideas, not boilerplate.


## Key Features


### ⚡ **Ease of Use**
- Intuitive, minimal-boilerplate API
- Beautiful, publication-ready defaults right out of the box
- Seamless integration with standard LaTeX environments

### 🎨 **Fine-Grained Customization**
- Extensive key–value system for effortless yet detailed adjustments
- Comprehensive styling options (colors, borders, paddings, shadows, and more)
- Fully customizable color palettes optimized for readability and aesthetic appeal

### 🛠 **Comprehensive Toolkit**
- Built-in geometric primitives: rectangles, circles, diamonds, trapeziums, etc.
- Containers and groups for logical element clustering
- Automatic bridging arcs for neat arrow routing
- Support for annotations, decorations, and conditional rendering

### 📐 **Consistent and Professional Output**
- Unified visual style designed specifically for AI/ML publications
- Smart defaults that adhere to professional standards of top-tier venues (ICLR, NeurIPS, CVPR)
- Seamless dark mode integration for presentations and digital publications

### 🌟 **Modern LaTeX3 Design**
- Built on the powerful `expl3` programming layer
- Modular and extensible architecture
- Robust, reliable, and maintainable codebase leveraging `l3build`

---

## Getting Started


Pick your installation route:

### 📦 Via CTAN

```sh
tlmgr install neural-sketch
```

### 🚀 From source

```sh
git clone https://github.com/your-org/neural-sketch.git
cd neural-sketch
l3build install
```

Then, in your LaTeX preamble:

```latex
\usepackage{neural-sketch}
\nskUseModule{*} % Load all modules (recommended for new users)
```



### 📝 **Your First Diagram**

Here's a quick example to create a simple diagram:

```latex
\begin{nskFigure}[]
  \nskBlock[text-center=First Block]
  \nskBlock[last-pos={right=}, text-center=Second Block]
\end{nskFigure}
```

---

## Documentation



Extensive documentation, examples, and best practices can be found at:

- 📚 **[Neural Sketch Documentation](https://neural-sketch.app/)**

Key documentation sections:
- [Getting Started Guide](https://neural-sketch.app/)
- [Core Components Overview](https://neural-sketch.app/docs/core/what-is-nsk)
- [Customization and Styling](https://neural-sketch.app/docs/core/palette)
- [Automatic Dark Mode](https://neural-sketch.app/docs/core/dark-mode)

---

## Contributing

Contributions, issues, and feature requests are warmly welcomed!

- **Report issues**: [Issues Tracker](https://github.com/espressoshock/neural-sketch/issues)
- **Feature Requests and Discussions**: Open a discussion in the [GitHub Discussions](https://github.com/espressoshock/neural-sketch/discussions)
- **Pull Requests**: Submit improvements via PR, following the contribution guidelines in `CONTRIBUTING.md`.
