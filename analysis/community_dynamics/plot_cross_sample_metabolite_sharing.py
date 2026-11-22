#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('analysis/community_dynamics', exist_ok=True)

# 1. Load thresholded patient table (MSV000080397, 556 runs)
df = pd.read_csv('EBC-KT/analyses/Quinn2018_recapitulation/patient_table_thresholded.csv')

# Focus on the core Aspergillus metabolites under the strict 5% of q99 threshold
core_compounds = [
    'fumitremorgin C',
    'fumiquinazoline A',
    '444.17 (fumiquinazoline C?)',
    'fumigaclavine C',
    'fumiquinazoline F',
    'festuclavine',
    'festuclavine(2)',
    'pyripyropene A',
    'tobramycin'
]

df_strict = df[(df['criterion'] == '5%q99') & (df['compound'].isin(core_compounds))].copy()

# Create patient x compound matrix for Toby and NT
fig, axes = plt.subplots(1, 2, figsize=(16, 9), dpi=300)

for idx, (trt, title) in enumerate([('Toby', 'A. Tobramycin Treatment (Toby)'), ('NT', 'B. Untreated Control (NT)')]):
    sub = df_strict[df_strict['treatment'] == trt]
    piv = sub.pivot(index='subject', columns='compound', values='sum').fillna(0)
    # reindex columns to match order
    existing_cols = [c for c in core_compounds if c in piv.columns]
    piv = piv[existing_cols]
    
    # Sort subjects so positive patients are at top, then controls at bottom
    all_subjects = list(piv.index)
    cf_pts = [s for s in all_subjects if not s.startswith('C')]
    controls = [s for s in all_subjects if s.startswith('C')]
    
    # Sort CF patients by total positive runs across core compounds
    cf_sorted = sorted(cf_pts, key=lambda s: piv.loc[s, [c for c in existing_cols if c != 'tobramycin']].sum(), reverse=True)
    sorted_subjects = cf_sorted + sorted(controls)
    piv = piv.loc[sorted_subjects]
    
    ax = axes[idx]
    sns.heatmap(piv, annot=True, fmt='d', cmap='YlOrRd', vmin=0, vmax=10, cbar=idx==1, cbar_kws={'label': 'Positive Runs (out of 10)'}, ax=ax, linewidths=0.5, linecolor='lightgray')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Specialized Metabolite', fontsize=11, fontweight='bold')
    ax.set_ylabel('Patient / Subject ID', fontsize=11, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9)

plt.suptitle('Cross-Sample Metabolite Sharing Across 18 CF Patients and 4 Healthy Controls\n(MSV000080397; 556 runs; threshold >= 5% of 99th percentile intensity)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/community_dynamics/cross_sample_metabolite_sharing.pdf')
plt.savefig('analysis/community_dynamics/cross_sample_metabolite_sharing.png')
print('Successfully saved cross_sample_metabolite_sharing figure!')
