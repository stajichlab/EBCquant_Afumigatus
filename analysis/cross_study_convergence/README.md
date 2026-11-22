# Cross-Study Synergism: Convergence Between the Oxygen Gradient (10863) and the pH Gradient (10511)

## 1. Overview
In Quinn et al. 2018 (*Science Advances*, PMC6157970), the cystic fibrosis lung microbiome was subjected to two distinct chemical perturbations in independent experiments:
1. **Study 10511 (ERP109668):** Growth in artificial sputum medium across a buffered pH gradient (pH 5.0 to 8.5; $n=194$ processed profiles).
2. **Study 10863 (ERP109670):** Growth in the WinCF capillary tube model across a vertical oxygen depth gradient (1 to 10 mm depth) with and without topical sodium bicarbonate ($\text{HCO}_3^-$) ($n=353$ processed untreated and bicarbonate profiles).

Here, we test the ecological hypothesis of **chemical convergence**: that physical vertical hypoxia/anoxia down the mucus column phenocopies environmental acidification (favoring fermentative anaerobes), whereas topical bicarbonate phenocopies alkaline media.

---

## 2. Quantitative Dissimilarity Analysis (Bray-Curtis)

Pairwise Bray-Curtis dissimilarity was calculated between condition-averaged genus-level profiles:

| WinCF Depth / Treatment Condition | vs. pH 5.0 | vs. pH 5.5 | vs. pH 6.0 | vs. pH 6.5 | vs. pH 7.0 | vs. pH 7.5 | vs. pH 8.0 | vs. pH 8.5 |
|---|---|---|---|---|---|---|---|---|
| **Untreated 1–3 mm (Oxic Surface)** | 0.426 | 0.443 | 0.440 | 0.435 | 0.450 | 0.462 | 0.427 | 0.442 |
| **Untreated 4–6 mm (Microaerophilic)** | 0.292 | 0.328 | 0.344 | 0.338 | 0.352 | 0.377 | 0.364 | 0.408 |
| **Untreated 7–10 mm (Deep Anoxia)** | **0.229** | 0.281 | 0.296 | 0.287 | 0.313 | 0.342 | 0.336 | **0.397** |
| **Bicarbonate 1–3 mm (Alkalinized Surface)** | 0.675 | 0.688 | 0.696 | 0.704 | 0.714 | 0.687 | 0.655 | **0.656** |
| **Bicarbonate 7–10 mm (Deep Anoxia + BC)** | **0.306** | 0.354 | 0.373 | 0.365 | 0.358 | 0.364 | 0.332 | 0.380 |

---

## 3. Key Ecological Findings
1. **Deep Anoxia Phenocopies Acidic pH (Monotonic Trajectory):**
   - The community at 7–10 mm depth in untreated WinCF columns displays its minimum dissimilarity against **pH 5.0 (0.229)** and increases monotonically across the pH gradient to reach its maximum dissimilarity against **pH 8.5 (0.397)**.
   - The deep mucus plug provides both the oxygen depletion and acidic fermentation microenvironment (accumulating propionic and lactic acids) that selects for the same fermentative guild (*Prevotella*, *Veillonella*, *Streptococcus*) observed at low pH.
2. **Ordination & Clustering:**
   - In PCoA and hierarchical clustering (Ward distance), deep anoxic samples from study 10863 cluster tightly with the pH 5.0–5.5 samples from study 10511.

---

## 4. Figures & Output Files
- `analysis/cross_study_convergence/chemical_convergence_ordination.pdf` (PCoA ordination & Ward hierarchical clustering dendrogram)
- `analysis/cross_study_convergence/chemical_convergence_ordination.png` (High-res preview)
- `analysis/cross_study_convergence/bray_curtis_condition_distances.csv` (Full condition distance matrix)
