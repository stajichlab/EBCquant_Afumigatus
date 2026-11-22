# Tripartite Surface Niche Partitioning and Deep Anaerobic Convergence Under Tobramycin

## 1. Overview
This follow-up analysis investigates the patient-by-patient community reorganization across the 10 mm depth gradient under topical tobramycin treatment in Qiita study 10863 (ERP109670).

By integrating exact Deblur 150 bp amplicon sequence variants (ASV 91 for *Aspergillus fumigatus*) with closed-reference Greengenes bacterial OTUs (table 54502), we resolve the patient-specific trajectories that were obscured by pooled cohort averages.

---

## 2. Tripartite Niche Partitioning at the Surface (Depth 1 mm, Oxic Zone)

When tobramycin is applied to the oxic surface of the mucus column, patient communities diverge into three mutually exclusive regimes:

| Regime | Patient | *A. fumigatus* (ASV 91) | *Xanthomonadaceae* / *Stenotrophomonas* | *Pseudomonas* | Dominant Taxon |
|---|---|---|---|---|---|
| **Regime 1: Fungal Bloom** | **157** | **96.28%** | 27.48%* | 16.41%* | *Aspergillus fumigatus* |
| | **146** | **95.06%** | 17.56%* | 31.11%* | *Aspergillus fumigatus* |
| | **353** | **74.50%** | 95.79%* | 0.95%* | *Aspergillus fumigatus* |
| **Regime 2: Resistant *Stenotrophomonas*** | **107** | 0.00% | **99.66%** | 0.09% | *Xanthomonadaceae* (*Stenotrophomonas*) |
| | **243** | 0.00% | **98.37%** | 0.23% | *Xanthomonadaceae* (*Stenotrophomonas*) |
| | **179** | 0.00% | **94.81%** | 4.28% | *Xanthomonadaceae* (*Stenotrophomonas*) |
| | **350** | 0.00% | **92.97%** | 0.84% | *Xanthomonadaceae* (*Stenotrophomonas*) |
| | **178** | 0.00% | **89.20%** | 9.31% | *Xanthomonadaceae* (*Stenotrophomonas*) |
| **Regime 3: Tobramycin-Resistant *Pseudomonas*** | **49** | 0.00% | 0.69% | **90.79%** | *Pseudomonas* |
| | **345** | 0.00% | 6.38% | **71.66%** | *Pseudomonas* |
| | **187** | 0.00% | 0.03% | **37.23%** | *Pseudomonas* |
| | **69** | 0.00% | 8.88% | **34.78%** | *Pseudomonas* / *Prevotella* |
| | **34** | 0.00% | 6.41% | **30.73%** | *Pseudomonas* |
| | **328** | 0.09% | 0.11% | **25.23%** | *Pseudomonas* |
| | **148** | 0.00% | 0.02% | **22.87%** | *Pseudomonas* |
| | **228** | 0.00% | 6.81% | **21.95%** | *Pseudomonas* |
| | **259** | 0.00% | 24.64% | **20.31%** | *Pseudomonas* / *Xantho* |

*(Note: In Regime 1, bacterial percentages are computed out of the remaining bacterial reads in table 54502; the Deblur total-community percentage is dominated by *Aspergillus* at 74.5–96.3%.)*

### Clinical & Ecological Interpretation
1. **Competitive Release:** When susceptible *Pseudomonas* is eradicated from the oxic surface by tobramycin, the vacated aerobic niche is captured either by eukaryotic *Aspergillus fumigatus* (Regime 1) or by intrinsically multidrug-resistant *Stenotrophomonas maltophilia* (Regime 2).
2. **Treatment Resistance:** In Regime 3 patients, *Pseudomonas* exhibits phenotypic or enzymatic resistance to tobramycin, retaining dominance (20% to 90.8%) at the surface.

---

## 3. Deep Anaerobic Convergence (Depth 10 mm, Anoxic Sanctuary)

In stark contrast to the divergent surface regimes, the deep anoxic layers (10 mm) converge across all patients into a conserved anaerobic fermentative guild:

- **Mean Total Anaerobe Relative Abundance at 10 mm:** **50.3%** (reaching up to 94.8% in individual patients).
- **Core Anaerobic Taxa:**
  - *Prevotella*: dominates in patients 259 (69.1%), 69 (69.0%), 350 (59.7%), 243 (50.5%), and 49 (40.7%).
  - *Streptococcus*: dominates in patients 353 (69.7%), 179 (51.2%), 148 (39.4%), 272 (35.6%), 107 (32.1%), 350 (31.9%), 187 (30.4%), and 243 (29.8%).
  - *Porphyromonas* & *Bulleidia*: expand up to 49.9% (patient 107).
- **Complete Elimination of Fungi at Depth:** *Aspergillus* ASV 91 drops to **0.00%** across all patients at 10 mm.

This validates the hypothesis that inhaled aminoglycosides fail to penetrate the viscous anaerobic mucus plug, providing a protected clinical reservoir for fermentative anaerobes.
