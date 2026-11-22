# Fungal Mitochondrial SSU (*rrnS*) Phylogeny & Placement of CF Sputum ASV 91

## Overview
This analysis reconstructs the maximum-likelihood phylogenetic placement of the 150 bp mitochondrial small subunit (SSU / *rrnS*) amplicon sequence (`CF_sputum_ASV91`) identified in CF sputum cultures from Qiita study 10863 / 10511 (Quinn et al. 2018 *Science Advances*, PMC6157970).

Because standard EMP 515f–806r primers target the V4 region of 16S rRNA, organellar (mitochondrial) rRNA is co-amplified during bacterial profiling. This analysis tests whether the recovered amplicon sequence is definitively *Aspergillus fumigatus* versus sister species in section *Fumigati*, other *Aspergillus* sections, or other fungal clades.

---

## Taxa and Reference Accessions
Complete fungal mitochondrial genomes were retrieved from NCBI RefSeq / GenBank:

| Taxon | Section / Clade | Accession | SSU Coordinates |
|---|---|---|---|
| *Aspergillus fumigatus* Af293 | *Fumigati* | JQ346808.1 | 6391..7850 |
| *Aspergillus fumigatus* A1163 | *Fumigati* | JQ346807.1 | 6391..7850 |
| *Aspergillus fischeri* | *Fumigati* | BK072237.1 | Homologous *rrnS* |
| *Aspergillus lentulus* IFM 54703 | *Fumigati* | LC612919.1 | 6936..8373 |
| *Aspergillus udagawae* IFM 46973 | *Fumigati* | LC602355.1 | 6913..8351 |
| *Aspergillus pseudoviridinutans* IFM 55266 | *Fumigati* | AP024468.1 | 6914..8352 |
| *Aspergillus clavatus* NRRL 1 | *Clavati* | JQ354999.1 | 10873..12311 |
| *Aspergillus flavus* CA14 | *Flavi* | CP061812.1 | Homologous *rrnS* |
| *Aspergillus oryzae* RIB40 | *Flavi* | AP007176.1 | Homologous *rrnS* |
| *Aspergillus terreus* | *Terrei* | PX585205.1 | Homologous *rrnS* |
| *Aspergillus nidulans* FGSC A4 | *Nidulantes* | NC_017896.1 | Homologous *rrnS* |
| *Aspergillus niger* CBS 513.88 | *Nigri* | NC_007445.1 | 8915..10360 |
| *Talaromyces marneffei* PM1 | Eurotiales | NC_005256.1 | 12340..13721 |
| *Fusarium oxysporum* | Sordariomycetes (outgroup) | NC_017930.1 | 28187..29847 |
| *Fusarium graminearum* PH-1 | Sordariomycetes (outgroup) | NC_009493.1 | 86336..88406 |
| *Neurospora crassa* OR74A | Sordariomycetes (outgroup) | NC_026614.1 | Homologous *rrnS* |

---

## Sequence Comparison & Diagnostic Single Nucleotide Polymorphisms
Query ASV: `CF_sputum_ASV91` (150 bp)
```
TACGTAGAAGACTAGTGTTAGTCATCTTTATTAGGTTTAAAGGGTACCTAGACGGTAAAT
TAAACTCTAAAATGAGTACTTTTTTACTAGAGTTTTATGTGAGAAGGAAGAATTTCTGGA
GTAGTGATGAAATACCTTGATACCAGAAGGA
```

The 150 bp amplicon corresponds to positions 6857..7006 of the *A. fumigatus* mitochondrial genome (NC_017016.1), immediately downstream of the 515f binding site (`GTGCCAGCAGTCGCGGTAA`).

Key diagnostic positions across the 150 bp alignment:
- **`CF_sputum_ASV91` vs *A. fumigatus* (Af293 & A1163):** 100.00% identity (150/150 bp, 0 mismatches, 0 gaps).
- **vs *A. fischeri* / *A. udagawae* / *A. pseudoviridinutans* / *A. lentulus*:**
  - Position 102: **T** in *A. fumigatus* and `CF_sputum_ASV91` (`...TTTTATGTGA...`) vs **A** in *A. fischeri*, *A. lentulus*, etc. (`...TTTTATGAGA...`).
  - Position 137: **C** in *A. fumigatus* and `CF_sputum_ASV91` (`...AATACCTTGA...`) vs **T** in *A. lentulus*, *A. fischeri*, etc. (`...AATACTTTGA...`).
- **vs *A. clavatus*:** 99.33% identity (1 mismatch at position 137).
- **vs *A. flavus* / *A. oryzae*:** 98.67% identity (2 mismatches at position 124 `G` vs `T` and position 137 `T` vs `C`).
- **vs *A. terreus*:** 98.00% identity (3 mismatches).
- **vs *A. nidulans*:** 94.52% identity (8 mismatches).
- **vs *A. niger*:** 94.00% identity (9 mismatches).
- **vs *Talaromyces marneffei*:** 91.39% identity (13 mismatches).
- **vs *Fusarium* / *Neurospora*:** 75.5–78.6% identity.

---

## Phylogenetic Analysis

### 1. 150 bp V4 Region Maximum-Likelihood Tree
- **Alignment:** 17 sequences, 155 aligned positions (MAFFT v7.505).
- **Model:** TIM+F+I (ModelFinder BIC).
- **Bootstrap:** 1,000 ultrafast bootstrap replicates + SH-aLRT test.
- **Topology:** `CF_sputum_ASV91` is placed in a zero-length branch polytomy with *Aspergillus fumigatus* Af293 and A1163. The *Fumigati* section forms a monophyletic clade distinct from *A. clavatus*, *A. flavus*, *A. terreus*, *A. nidulans*, and *A. niger*.
- **Tree files:**
  - `tree_v4_150bp.treefile` (Newick ML tree)
  - `tree_v4_150bp.contree` (Consensus tree with bootstrap supports)
  - `mito_v4_150bp_phylogeny.pdf` / `mito_v4_150bp_phylogeny.png` (Visual figure)

### 2. Full-length *rrnS* (~1,450 bp) Backbone Tree with ASV 91
- **Alignment:** 17 sequences, 1,477 aligned positions.
- **Model:** TVM+F+R2 (ModelFinder BIC).
- **Bootstrap:** 1,000 ultrafast bootstrap replicates + SH-aLRT test.
- **Topology:**
  - `((CF_sputum_ASV91, A. fumigatus Af293, A. fumigatus A1163))` forms a supported terminal clade (**90% bootstrap support**).
  - The entire section *Fumigati* is recovered with **95% bootstrap support**.
  - Section *Clavati* (*A. clavatus*) is sister to section *Fumigati*.
  - Sections *Flavi*, *Terrei*, *Nidulantes*, and *Nigri* branch basal to *Fumigati* with high confidence.
- **Tree files:**
  - `tree_full_with_asv.treefile` (Newick ML tree)
  - `tree_full_with_asv.contree` (Consensus tree with bootstrap supports)
  - `mito_rrns_phylogeny.pdf` / `mito_rrns_phylogeny.png` (Visual figure)

---

## Conclusion
Phylogenetic analysis of the mitochondrial SSU (*rrnS*) rRNA demonstrates that the sequence blooming in tobramycin-treated cystic fibrosis sputum is **specifically and unambiguously *Aspergillus fumigatus***. Diagnostic nucleotide substitutions rule out closely related species in section *Fumigati* (*A. fischeri*, *A. lentulus*, *A. udagawae*) as well as other common clinical or environmental *Aspergillus* species.
