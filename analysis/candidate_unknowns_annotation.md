# Candidate Chemical Formulas and Structural Annotations for Unannotated *Aspergillus* Features (EBC-033)

## 1. Context & Motivation
In message `ebc-033`, the EBC agent analyzed 85,399 features from the WinCF reversed-phase metabolomics dataset (MSV000080397) against the 16S *Aspergillus* mitochondrial ASV 91 depth profiles. 

Two unannotated features emerged with extraordinary correlation to *A. fumigatus* reads (AUC >= 0.98) and were confirmed present in **27 of 27 *A. fumigatus* culture runs in MSV000087365**:
1. **Feature A:** *m/z* 525.2695 ([M+H]<sup>+</sup>, RT 5.01 min; sodium adduct *m/z* 547.2507; AUC = 0.992).
2. **Feature B:** *m/z* 548.2871 ([M+H]<sup>+</sup>, RT 5.59 min; sodium adduct *m/z* 570.2690; AUC = 0.989).

Neither feature currently carries a library spectrum match (MSI level 2) or accepted automated formula. Here we perform high-resolution isotope mass defect and formula generation to propose structural hypotheses.

---

## 2. Adduct Verification & Monoisotopic Masses

### Feature A:
- **[M+H]<sup>+</sup> observed:** 525.2695
- **[M+Na]<sup>+</sup> observed:** 547.2507
- **Measured Delta(Na - H):** 21.9812 Da (Theoretical: 21.9819 Da; error = **0.7 mDa**). Confirms sodium adduct assignment.
- **Monoisotopic neutral mass:** **M = 524.2622 Da**.
- Nominal mass is even (524) => **Even number of nitrogens (0, 2, 4...)** by the Nitrogen Rule.

### Feature B:
- **[M+H]<sup>+</sup> observed:** 548.2871
- **[M+Na]<sup>+</sup> observed:** 570.2690
- **Measured Delta(Na - H):** 21.9819 Da (Theoretical: 21.9819 Da; error = **0.0 mDa**). Confirms sodium adduct assignment.
- **Monoisotopic neutral mass:** **M = 547.2798 Da**.
- Nominal mass is odd (547) => **Odd number of nitrogens (1, 3, 5...)** by the Nitrogen Rule.

---

## 3. High-Resolution Formula Generation (<= 5 ppm)

### Top Formulas for Feature A (M = 524.2622, Even N):
| Formula | Theoretical Neutral | [M+H]<sup>+</sup> | Mass Error | RDBE | Plausibility & Pathway Link |
|---|---|---|---|---|---|
| **C<sub>28</sub>H<sub>36</sub>N<sub>4</sub>O<sub>6</sub>** | 524.2635 | 525.2708 | +2.45 ppm | 13.0 | **Highest (Alkaloid / DKP):** Derived from fumitremorgin core (C<sub>22</sub>H<sub>25</sub>N<sub>3</sub>O<sub>3</sub>) by addition of C<sub>6</sub>H<sub>11</sub>NO<sub>3</sub> (+145.074 Da), corresponding to an amino acid/diketopiperazine condensation. |
| **C<sub>27</sub>H<sub>40</sub>O<sub>10</sub>** | 524.2621 | 525.2694 | -0.10 ppm | 8.0 | **High (Meroterpenoid):** Highly oxygenated sesquiterpene / meroterpenoid related to pyripyropene core intermediates. |
| C<sub>31</sub>H<sub>40</sub>O<sub>5</sub>S | 524.2596 | 525.2669 | -4.87 ppm | 12.0 | Low (unlikely sulfur adduct). |

### Top Formulas for Feature B (M = 547.2798, Odd N):
| Formula | Theoretical Neutral | [M+H]<sup>+</sup> | Mass Error | RDBE | Plausibility & Pathway Link |
|---|---|---|---|---|---|
| **C<sub>30</sub>H<sub>37</sub>N<sub>5</sub>O<sub>5</sub>** | 547.2795 | 548.2867 | -0.61 ppm | 15.0 | **Highest (Quinazoline/Alkaloid):** Exact mass defect matches Fumiquinazoline A (C<sub>24</sub>H<sub>23</sub>N<sub>5</sub>O<sub>4</sub>) + C<sub>6</sub>H<sub>14</sub>O (+102.105 Da, O-hydroxyhexyl or di-isopentyl extension) or an ergopeptine-type cyclol intermediate. |
| C<sub>29</sub>H<sub>41</sub>NO<sub>9</sub> | 547.2781 | 548.2854 | -3.05 ppm | 10.0 | Moderate (mono-nitrogen meroterpenoid). |
| C<sub>22</sub>H<sub>41</sub>N<sub>7</sub>O<sub>7</sub>S | 547.2788 | 548.2861 | -1.80 ppm | 6.0 | Low (non-ribosomal peptide fragment with sulfur). |

---

## 4. Proposed Biosynthetic Connections
1. **Feature A (C<sub>28</sub>H<sub>36</sub>N<sub>4</sub>O<sub>6</sub>, RT 5.01 min):**
   - Elutes at 5.01 min, slightly earlier than Fumitremorgin C (RT 5.21 min). The presence of two additional oxygens and one nitrogen increases polarity relative to fumitremorgin, exactly consistent with the observed retention shift on reversed-phase chromatography.
   - Recommended MS2 fragment search: test for loss of *m/z* 226.123 (diketopiperazine core fragment characteristic of fumitremorgin C).
2. **Feature B (C<sub>30</sub>H<sub>37</sub>N<sub>5</sub>O<sub>5</sub>, RT 5.59 min):**
   - Elutes at 5.59 min, later than Fumiquinazoline A (RT 4.84 min) and Fumiquinazoline C (RT 4.97 min). An extension of C<sub>6</sub>H<sub>14</sub>O adds lipophilicity, matching the later retention time on C18 reversed-phase.
   - Recommended MS2 fragment search: test for diagnostic quinazoline fragment ions (*m/z* 284, *m/z* 302, *m/z* 320).
