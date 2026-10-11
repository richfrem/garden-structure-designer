# Third-Party Licenses & Attribution

`garden-structure-designer` integrates external open-source tools and libraries to deliver precision CAD output, structural physics analysis, and document compilation.

---

## 1. CADCraft (vendor/cadcraft)

- **Upstream Project**: [CADCraft](https://github.com/storytold/cadcraft)
- **Copyright**: (c) 2026 ArtCraft Team and the CADCraft contributors.
- **License**: Dual-licensed under the **MIT License** or the **Apache License, Version 2.0**, at your option (`vendor/cadcraft/LICENSE-MIT`, `vendor/cadcraft/LICENSE-APACHE`).
- **Trademarks**: The ArtCraft name, wordmark, and logos are trademarks of the ArtCraft Team and are not covered by the MIT/Apache-2.0 license (`vendor/cadcraft/docs/brand/LICENSE-brand.txt`).
- **Integration**: Linked as a Git submodule at `vendor/cadcraft` pinned to commit `54ea5e743a29acd8f3178cfaa82fb74a38c2de72`. Used to compile the headless `cadcraft-cli` binary (`vendor/cadcraft/target/release/cadcraft-cli`) for CAD drawing verification and exchange.
- **Source Code**: Source is included directly in this repository via the submodule (`git submodule update --init --recursive`) and upstream at https://github.com/storytold/cadcraft.

### Transitive Component: acadrust
- **Project**: [acadrust](https://github.com/hakanaktt/acadrust)
- **License**: **Mozilla Public License 2.0 (MPL-2.0)**
- **Usage**: Used unmodified as a separate Rust library crate (`crates/dwg`) by CADCraft for DWG reading and writing.
- **Source Code**: Available from crates.io and at https://github.com/hakanaktt/acadrust under the terms of the MPL 2.0.

---

## 2. Python Ecosystem & Core Libraries

- **ezdxf**: [ezdxf](https://github.com/mozman/ezdxf) - MIT License. Used for DXF generation, entity auditing, block parsing, and XDATA validation.
- **build123d**: [build123d](https://github.com/gumyr/build123d) - Apache License 2.0. Parametric 3D CAD modeling.
- **OpenCV**: [OpenCV](https://opencv.org/) - Apache License 2.0. Visual smoke testing and computer vision heuristics.
- **Playwright**: [Playwright](https://playwright.dev/) - Apache License 2.0. Headless Chromium rendering for drawing verification.
- **ReportLab**: [ReportLab](https://www.reportlab.com/) - BSD License. Architectural PDF compilation.
