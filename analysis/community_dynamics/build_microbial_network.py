#!/usr/bin/env python3
import biom
from collections import defaultdict
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os

os.makedirs('analysis/community_dynamics', exist_ok=True)

# 1. Load closed-reference table 54502 and Deblur ASV 91 table
t = biom.load_table('data/microbiome/study_10863/BIOM/54502/otu_table.biom')
obs_meta = t.metadata(axis='observation')

# Define target genera
target_taxa = {
    'Aspergillus': 'ASV_91',
    'Pseudomonas': 'g__Pseudomonas',
    'Stenotrophomonas': 'g__Stenotrophomonas',
    'Achromobacter': 'g__Achromobacter',
    'Haemophilus': 'g__Haemophilus',
    'Staphylococcus': 'g__Staphylococcus',
    'Prevotella': 'g__Prevotella',
    'Veillonella': 'g__Veillonella',
    'Streptococcus': 'g__Streptococcus',
    'Fusobacterium': 'g__Fusobacterium',
    'Porphyromonas': 'g__Porphyromonas',
    'Bulleidia': 'g__Bulleidia',
    'Actinomyces': 'g__Actinomyces',
    'Rothia': 'g__Rothia'
}

taxa_indices = {}
for name, tag in target_taxa.items():
    if name == 'Aspergillus':
        continue
    idx_list = []
    for i, m in enumerate(obs_meta):
        tax = ';'.join(m.get('taxonomy', []))
        if tag in tax:
            idx_list.append(i)
    taxa_indices[name] = idx_list

# Load ASV 91
t_deblur = biom.load_table('data/microbiome/study_10863/BIOM/129335/all.biom')
asv91_seq = t_deblur.ids(axis='observation')[91]
deblur_sample_ids = list(t_deblur.ids(axis='sample'))
deblur_asv91 = t_deblur.data(asv91_seq, axis='observation')
deblur_sums = t_deblur.sum(axis='sample')
deblur_dict = {s: (int(deblur_asv91[i]), int(deblur_sums[i])) for i, s in enumerate(deblur_sample_ids)}

sample_ids = t.ids(axis='sample')

# Build sample x taxon abundance matrix
sample_data = []
valid_samples = []

for s in sample_ids:
    if 'Blank' in s or 'PBS' in s or s.startswith('10863.Sp'):
        continue
    col = t.data(s, axis='sample')
    tot = col.sum()
    if tot < 500:
        continue
        
    row = {}
    for name, indices in taxa_indices.items():
        row[name] = col[indices].sum() / tot
        
    # Aspergillus from Deblur
    if s in deblur_dict:
        c, deb_tot = deblur_dict[s]
        row['Aspergillus'] = c / deb_tot if deb_tot > 0 else 0.0
    else:
        row['Aspergillus'] = 0.0
        
    sample_data.append(row)
    valid_samples.append(s)

df_abund = pd.DataFrame(sample_data, index=valid_samples)
print(f'Constructed abundance matrix for {len(df_abund)} valid depth samples and {df_abund.shape[1]} key taxa.')

# 2. Compute pairwise Spearman correlation matrix and p-values
taxa_names = list(df_abund.columns)
n_taxa = len(taxa_names)

edges = []
for i in range(n_taxa):
    for j in range(i + 1, n_taxa):
        t1, t2 = taxa_names[i], taxa_names[j]
        r, p = spearmanr(df_abund[t1], df_abund[t2])
        edges.append({
            'taxon1': t1,
            'taxon2': t2,
            'spearman_rho': r,
            'p_value': p
        })

edge_df = pd.DataFrame(edges)
# FDR correction (Benjamini-Hochberg)
_, p_adj, _, _ = multipletests(edge_df['p_value'], method='fdr_bh')
edge_df['fdr_p_adj'] = p_adj

edge_df.to_csv('analysis/community_dynamics/microbial_correlation_edges.csv', index=False)
print('Wrote microbial_correlation_edges.csv')

# Significant edges (|rho| >= 0.20 and FDR <= 0.01)
sig_edges = edge_df[(edge_df['fdr_p_adj'] <= 0.01) & (edge_df['spearman_rho'].abs() >= 0.20)].sort_values('spearman_rho')
print(f'\nFound {len(sig_edges)} significant edges (|rho| >= 0.20, FDR <= 0.01):')
print('Top Negative (Competitive Exclusion):')
print(sig_edges.head(8)[['taxon1', 'taxon2', 'spearman_rho', 'fdr_p_adj']].to_string(index=False))
print('\nTop Positive (Co-occurrence Guilds):')
print(sig_edges.tail(8)[['taxon1', 'taxon2', 'spearman_rho', 'fdr_p_adj']].to_string(index=False))

# 3. Network Visualization with NetworkX
G = nx.Graph()

# Assign guild colors to nodes
guild_map = {
    'Aspergillus': ('Fungus', '#E41A1C'), # Red
    'Pseudomonas': ('Aerobic Pathogen', '#377EB8'), # Blue
    'Stenotrophomonas': ('Aerobic Pathogen', '#377EB8'),
    'Achromobacter': ('Aerobic Pathogen', '#377EB8'),
    'Haemophilus': ('Facultative Pathogen', '#984EA3'), # Purple
    'Staphylococcus': ('Facultative Pathogen', '#984EA3'),
    'Prevotella': ('Fermentative Anaerobe', '#4DAF4A'), # Green
    'Veillonella': ('Fermentative Anaerobe', '#4DAF4A'),
    'Streptococcus': ('Fermentative Anaerobe', '#4DAF4A'),
    'Fusobacterium': ('Fermentative Anaerobe', '#4DAF4A'),
    'Porphyromonas': ('Fermentative Anaerobe', '#4DAF4A'),
    'Bulleidia': ('Fermentative Anaerobe', '#4DAF4A'),
    'Actinomyces': ('Fermentative Anaerobe', '#4DAF4A'),
    'Rothia': ('Facultative Commensal', '#FF7F00') # Orange
}

for node in taxa_names:
    guild, col = guild_map.get(node, ('Other', 'gray'))
    G.add_node(node, guild=guild, color=col)

edge_colors = []
edge_widths = []
for _, r in sig_edges.iterrows():
    u, v = r['taxon1'], r['taxon2']
    rho = r['spearman_rho']
    G.add_edge(u, v, weight=abs(rho), rho=rho)

plt.figure(figsize=(12, 10), dpi=300)
pos = nx.spring_layout(G, k=0.8, seed=42)

# Draw edges
pos_edges = [(u, v) for u, v, d in G.edges(data=True) if d['rho'] > 0]
neg_edges = [(u, v) for u, v, d in G.edges(data=True) if d['rho'] < 0]

pos_weights = [G[u][v]['weight'] * 4.5 for u, v in pos_edges]
neg_weights = [G[u][v]['weight'] * 4.5 for u, v in neg_edges]

nx.draw_networkx_edges(G, pos, edgelist=pos_edges, width=pos_weights, edge_color='#2b83ba', alpha=0.75)
nx.draw_networkx_edges(G, pos, edgelist=neg_edges, width=neg_weights, edge_color='#d7191c', style='dashed', alpha=0.75)

# Draw nodes
node_cols = [G.nodes[n]['color'] for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=node_cols, node_size=1800, edgecolors='black', linewidths=1.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='white')

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Fungi (Aspergillus)', markerfacecolor='#E41A1C', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Aerobic Pathogens (Pseudomonas, Stenotrophomonas)', markerfacecolor='#377EB8', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Fermentative Anaerobes (Prevotella, Veillonella...)', markerfacecolor='#4DAF4A', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Facultative Taxa (Streptococcus, Haemophilus...)', markerfacecolor='#984EA3', markersize=12),
    Line2D([0], [0], color='#2b83ba', lw=2.5, label='Positive Co-occurrence (rho >= +0.20)'),
    Line2D([0], [0], color='#d7191c', lw=2.5, linestyle='--', label='Competitive Exclusion (rho <= -0.20)')
]
plt.legend(handles=legend_elements, loc='upper left', frameon=True, fontsize=10)

plt.title('Microbial Interaction & Niche Exclusion Network in CF Mucus\n(Study 10863; n = 502 depth samples; FDR <= 0.01)', fontsize=13, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('analysis/community_dynamics/microbial_interaction_network.pdf')
plt.savefig('analysis/community_dynamics/microbial_interaction_network.png')
print('Successfully saved microbial interaction network figure!')
