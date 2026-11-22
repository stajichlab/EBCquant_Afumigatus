# Microbial Interaction & Niche Exclusion Network in CF Mucus (Study 10863)

## 1. Overview
Pairwise Spearman rank correlation analysis with Benjamini-Hochberg false discovery rate (FDR) control was conducted across $n = 558$ valid WinCF depth samples in study 10863. 

The network formally defines the microbial modules that govern the cystic fibrosis airway ecosystem:
1. **The Classic Aerobic Pathogens:** *Pseudomonas*, *Stenotrophomonas*, *Achromobacter*.
2. **The Opportunistic Filamentous Fungus:** *Aspergillus fumigatus* (ASV 91).
3. **The Fermentative Anaerobic Guild:** *Prevotella*, *Veillonella*, *Streptococcus*, *Fusobacterium*, *Porphyromonas*, *Bulleidia*, *Actinomyces*.

---

## 2. Strongest Significant Interactions (FDR $\le 0.01$, $|\rho| \ge 0.20$)

### A. Competitive Mutual Exclusion (Negative Edges)
Aerobic pathogens (*Pseudomonas* and *Stenotrophomonas*) display pervasive, highly significant negative correlations with the fermentative anaerobic guild:
- **`Pseudomonas` vs. `Streptococcus`:** $\rho = -0.5004$ ($p_{\text{adj}} = 2.42 \times 10^{-35}$)
- **`Pseudomonas` vs. `Bulleidia`:** $\rho = -0.4253$ ($p_{\text{adj}} = 5.89 \times 10^{-25}$)
- **`Stenotrophomonas` vs. `Actinomyces`:** $\rho = -0.3491$ ($p_{\text{adj}} = 8.96 \times 10^{-17}$)
- **`Pseudomonas` vs. `Veillonella`:** $\rho = -0.3174$ ($p_{\text{adj}} = 5.97 \times 10^{-14}$)
- **`Pseudomonas` vs. `Fusobacterium`:** $\rho = -0.3168$ ($p_{\text{adj}} = 6.55 \times 10^{-14}$)
- **`Stenotrophomonas` vs. `Streptococcus`:** $\rho = -0.3010$ ($p_{\text{adj}} = 1.31 \times 10^{-12}$)
- **`Pseudomonas` vs. `Actinomyces`:** $\rho = -0.2958$ ($p_{\text{adj}} = 3.33 \times 10^{-12}$)
- **`Stenotrophomonas` vs. `Veillonella`:** $\rho = -0.2660$ ($p_{\text{adj}} = 5.05 \times 10^{-10}$)

### B. Anaerobic Guild Co-occurrence (Positive Edges)
The fermentative anaerobes form a tightly interconnected mutualistic module:
- **`Veillonella` + `Actinomyces`:** $\rho = +0.6203$ ($p_{\text{adj}} = 1.13 \times 10^{-58}$)
- **`Actinomyces` + `Rothia`:** $\rho = +0.5125$ ($p_{\text{adj}} = 4.95 \times 10^{-37}$)
- **`Prevotella` + `Bulleidia`:** $\rho = +0.5092$ ($p_{\text{adj}} = 1.15 \times 10^{-36}$)
- **`Fusobacterium` + `Bulleidia`:** $\rho = +0.4868$ ($p_{\text{adj}} = 2.81 \times 10^{-33}$)
- **`Streptococcus` + `Bulleidia`:** $\rho = +0.4796$ ($p_{\text{adj}} = 2.90 \times 10^{-32}$)
- **`Veillonella` + `Fusobacterium`:** $\rho = +0.4584$ ($p_{\text{adj}} = 3.13 \times 10^{-29}$)
- **`Haemophilus` + `Fusobacterium`:** $\rho = +0.4398$ ($p_{\text{adj}} = 9.79 \times 10^{-27}$)
- **`Streptococcus` + `Porphyromonas`:** $\rho = +0.4301$ ($p_{\text{adj}} = 1.58 \times 10^{-25}$)

### C. *Aspergillus fumigatus* Dynamics
- Positively associates with *Staphylococcus* ($\rho = +0.2907$, $p_{\text{adj}} = 7.91 \times 10^{-12}$) and *Porphyromonas* ($\rho = +0.2237$, $p_{\text{adj}} = 2.17 \times 10^{-7}$).
- Inversely correlates with *Haemophilus* ($\rho = -0.1112$, $p_{\text{adj}} = 0.012$) and *Pseudomonas* ($\rho = -0.0986$, $p_{\text{adj}} = 0.027$).

---

## 3. Network Architecture & Deliverables
- `analysis/community_dynamics/microbial_interaction_network.pdf` (Publication-ready network figure)
- `analysis/community_dynamics/microbial_interaction_network.png` (High-resolution preview)
- `analysis/community_dynamics/microbial_correlation_edges.csv` (Complete edge list with raw and FDR-adjusted $p$-values)
