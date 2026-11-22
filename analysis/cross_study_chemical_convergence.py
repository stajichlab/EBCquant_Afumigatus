#!/usr/bin/env python3
import biom
from collections import defaultdict
import numpy as np
import pandas as pd
from scipy.spatial.distance import braycurtis
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.manifold import MDS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import os

os.makedirs('analysis/cross_study_convergence', exist_ok=True)

# 1. Helper to extract genus profile from BIOM
def extract_genus_table(biom_path):
    t = biom.load_table(biom_path)
    obs_meta = t.metadata(axis='observation')
    sample_ids = t.ids(axis='sample')
    
    otu_to_genus = {}
    for oid, m in zip(t.ids(axis='observation'), obs_meta):
        tax = m.get('taxonomy', [])
        g = 'Unclassified'
        for item in tax:
            if item.startswith('g__') and len(item) > 3:
                g = item[3:]
                break
            elif item.startswith('f__') and len(item) > 3:
                g = item
        otu_to_genus[oid] = g
        
    genus_profiles = {}
    for s in sample_ids:
        col = t.data(s, axis='sample')
        tot = col.sum()
        if tot < 500: # filter low read depth
            continue
        g_counts = defaultdict(float)
        for oid, c in zip(t.ids(axis='observation'), col):
            if c > 0:
                g_counts[otu_to_genus[oid]] += c / tot
        genus_profiles[s] = g_counts
    return genus_profiles

print('Loading Study 10511 (pH gradient)...')
p10511 = extract_genus_table('data/microbiome/study_10511/BIOM/4006/otu_table.biom')

print('Loading Study 10863 (Oxygen/Depth/Bicarbonate)...')
p10863 = extract_genus_table('data/microbiome/study_10863/BIOM/54502/otu_table.biom')

# 2. Categorize conditions
condition_samples = defaultdict(list)

# Study 10511 conditions by pH
for s, g_dict in p10511.items():
    m = re.search(r'[pP][hH]\.?([0-9\.]+)', s)
    if m:
        ph_val = float(m.group(1))
        cond = f'pH_{ph_val:.1f}'
        condition_samples[cond].append(g_dict)

# Study 10863 conditions by treatment and depth
for s, g_dict in p10863.items():
    parts = s.split('.')
    if len(parts) >= 3 and parts[2] == 'BC':
        dp = parts[3].split('.')[0] if len(parts) > 3 else 'NA'
        if dp.isdigit():
            d = int(dp)
            if 1 <= d <= 3:
                condition_samples['Bicarbonate_1-3mm'].append(g_dict)
            elif 4 <= d <= 6:
                condition_samples['Bicarbonate_4-6mm'].append(g_dict)
            elif 7 <= d <= 10:
                condition_samples['Bicarbonate_7-10mm'].append(g_dict)
    elif len(parts) >= 3 and parts[2] not in ['TB', 'BC'] and not parts[1].startswith('Sp') and 'Blank' not in s:
        # untreated depth is in parts[2]
        dp = parts[2].split('.')[0]
        if dp.isdigit():
            d = int(dp)
            if 1 <= d <= 3:
                condition_samples['Untreated_1-3mm'].append(g_dict)
            elif 4 <= d <= 6:
                condition_samples['Untreated_4-6mm'].append(g_dict)
            elif 7 <= d <= 10:
                condition_samples['Untreated_7-10mm'].append(g_dict)

print('\nConditions and sample counts:')
for cond, slist in sorted(condition_samples.items()):
    print(f'  {cond}: {len(slist)} samples')

# 3. Calculate mean genus abundance per condition
all_genera = set()
for slist in condition_samples.values():
    for g_dict in slist:
        all_genera.update(g_dict.keys())

all_genera = sorted(list(all_genera))

cond_means = {}
for cond, slist in sorted(condition_samples.items()):
    arr = np.zeros((len(slist), len(all_genera)))
    for i, g_dict in enumerate(slist):
        for j, g in enumerate(all_genera):
            arr[i, j] = g_dict.get(g, 0.0)
    cond_means[cond] = arr.mean(axis=0)

cond_names = sorted(list(cond_means.keys()))
mean_matrix = np.array([cond_means[c] for c in cond_names])

# 4. Compute pairwise Bray-Curtis distance matrix
dist_mat = np.zeros((len(cond_names), len(cond_names)))
for i in range(len(cond_names)):
    for j in range(len(cond_names)):
        dist_mat[i, j] = braycurtis(mean_matrix[i], mean_matrix[j])

dist_df = pd.DataFrame(dist_mat, index=cond_names, columns=cond_names)
dist_df.to_csv('analysis/cross_study_convergence/bray_curtis_condition_distances.csv')
print('\nWrote bray_curtis_condition_distances.csv')

# Print key convergence comparisons
print('\n=== Key Chemical Convergence Comparisons ===')
d1 = dist_df.loc["Untreated_7-10mm", "pH_5.0"]
d2 = dist_df.loc["Untreated_7-10mm", "pH_8.5"]
d3 = dist_df.loc["Untreated_1-3mm", "pH_8.5"]
d4 = dist_df.loc["Bicarbonate_1-3mm", "pH_8.5"]
d5 = dist_df.loc["Bicarbonate_1-3mm", "pH_5.0"]
print(f'Deep Anoxia (Untreated 7-10mm) vs pH 5.0: {d1:.3f}')
print(f'Deep Anoxia (Untreated 7-10mm) vs pH 8.5: {d2:.3f}')
print(f'Surface Oxic (Untreated 1-3mm) vs pH 8.5: {d3:.3f}')
print(f'Surface Bicarbonate (1-3mm) vs pH 8.5:    {d4:.3f}')
print(f'Surface Bicarbonate (1-3mm) vs pH 5.0:    {d5:.3f}')

# 5. Ordination & Hierarchical Clustering Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel A: PCoA / Metric MDS
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
coords = mds.fit_transform(dist_mat)

ax = axes[0]
colors = []
for c in cond_names:
    if 'pH' in c:
        colors.append('coral')
    elif 'Bicarbonate' in c:
        colors.append('purple')
    else:
        colors.append('royalblue')

ax.scatter(coords[:, 0], coords[:, 1], c=colors, s=140, edgecolors='black', zorder=3)
for i, c in enumerate(cond_names):
    ax.annotate(c, (coords[i, 0], coords[i, 1] + 0.015), fontsize=9, fontweight='bold', ha='center')

ax.set_title('A. PCoA Ordination of Microbial Communities\n(pH Gradient vs. Oxygen Depth Gradient)', fontsize=12, fontweight='bold')
ax.set_xlabel('PCoA Axis 1', fontsize=11, fontweight='bold')
ax.set_ylabel('PCoA Axis 2', fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

# Panel B: Hierarchical Clustering Dendrogram
ax = axes[1]
from scipy.spatial.distance import squareform
cond_condensed = squareform(dist_mat)
Z = linkage(cond_condensed, method='ward')
dendrogram(Z, labels=cond_names, ax=ax, orientation='right', color_threshold=0.5)
ax.set_title('B. Hierarchical Clustering (Ward Distance)', fontsize=12, fontweight='bold')
ax.set_xlabel('Bray-Curtis Dissimilarity Distance', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('analysis/cross_study_convergence/chemical_convergence_ordination.pdf')
plt.savefig('analysis/cross_study_convergence/chemical_convergence_ordination.png')
print('Successfully saved chemical convergence ordination plots!')
