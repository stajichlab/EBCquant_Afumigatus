#!/usr/bin/env python3
import biom
from collections import defaultdict
import pandas as pd
import numpy as np

# 1. Load closed-reference OTU table 54502
t = biom.load_table('data/microbiome/study_10863/BIOM/54502/otu_table.biom')
obs_meta = t.metadata(axis='observation')

otu_to_group = {}
for oid, m in zip(t.ids(axis='observation'), obs_meta):
    tax = ';'.join(m.get('taxonomy', []))
    if 'Pseudomonas' in tax or 'f__Pseudomonadaceae' in tax:
        otu_to_group[oid] = 'Pseudomonas_group'
    elif 'Stenotrophomonas' in tax or 'f__Xanthomonadaceae' in tax:
        otu_to_group[oid] = 'Xanthomonadaceae_Stenotrophomonas'
    elif 'Prevotella' in tax:
        otu_to_group[oid] = 'Prevotella'
    elif 'Streptococcus' in tax:
        otu_to_group[oid] = 'Streptococcus'
    elif 'Veillonella' in tax:
        otu_to_group[oid] = 'Veillonella'
    elif 'Porphyromonas' in tax or 'Bulleidia' in tax or 'Fusobacterium' in tax:
        otu_to_group[oid] = 'Other_Anaerobes'
    elif 'f__mitochondria' in tax:
        otu_to_group[oid] = 'Mitochondria'
    else:
        otu_to_group[oid] = 'Other_Bacteria'

# Also load Deblur ASV 91 table
t_deblur = biom.load_table('data/microbiome/study_10863/BIOM/129335/all.biom')
asv91_seq = t_deblur.ids(axis='observation')[91]
deblur_sample_ids = list(t_deblur.ids(axis='sample'))
deblur_asv91 = t_deblur.data(asv91_seq, axis='observation')
deblur_sums = t_deblur.sum(axis='sample')
deblur_dict = {s: (int(deblur_asv91[i]), int(deblur_sums[i])) for i, s in enumerate(deblur_sample_ids)}

sample_ids = t.ids(axis='sample')

# Analyze TB samples across depths 1 to 10 mm
records = []
for s in sample_ids:
    if '.TB.' not in s:
        continue
    parts = s.split('.')
    pt = parts[1]
    dp = parts[3]
    if not dp.isdigit():
        continue
    dp = int(dp)
    
    col = t.data(s, axis='sample')
    tot_bac = col.sum()
    if tot_bac == 0:
        continue
        
    counts = defaultdict(float)
    for oid, c in zip(t.ids(axis='observation'), col):
        if c > 0:
            counts[otu_to_group[oid]] += c
            
    # Deblur ASV 91
    asv91_c, asv91_tot = deblur_dict.get(s, (0, 0))
    afum_pct = (asv91_c / asv91_tot * 100) if asv91_tot > 0 else 0.0
    
    rec = {
        'patient': pt,
        'depth_mm': dp,
        'afum_asv91_pct': afum_pct,
        'xantho_steno_pct': (counts['Xanthomonadaceae_Stenotrophomonas'] / tot_bac) * 100,
        'pseudomonas_pct': (counts['Pseudomonas_group'] / tot_bac) * 100,
        'prevotella_pct': (counts['Prevotella'] / tot_bac) * 100,
        'streptococcus_pct': (counts['Streptococcus'] / tot_bac) * 100,
        'other_anaerobes_pct': (counts['Other_Anaerobes'] / tot_bac) * 100,
        'total_bac_reads': int(tot_bac),
        'total_deblur_reads': int(asv91_tot)
    }
    records.append(rec)

tb_df = pd.DataFrame(records).sort_values(['patient', 'depth_mm'])
tb_df.to_csv('analysis/community_dynamics/tobramycin_bacterial_dynamics_detailed.csv', index=False)
print(f'Wrote {len(tb_df)} tobramycin depth records.')

# Print surface (1 mm) patient categorization
tb_surface = tb_df[tb_df['depth_mm'] == 1].sort_values('afum_asv91_pct', ascending=False)
print('\n=== Surface Oxic Layer (1 mm) Regime Classification Under Tobramycin ===')
categories = []
for _, r in tb_surface.iterrows():
    if r['afum_asv91_pct'] > 50:
        regime = 'Regime 1: Aspergillus Bloom'
    elif r['xantho_steno_pct'] > 50:
        regime = 'Regime 2: Stenotrophomonas/Xantho Bloom'
    elif r['pseudomonas_pct'] > 20:
        regime = 'Regime 3: Resistant Pseudomonas'
    else:
        regime = 'Regime 4: Mixed / Other'
    categories.append(regime)
tb_surface['regime'] = categories
print(tb_surface[['patient', 'regime', 'afum_asv91_pct', 'xantho_steno_pct', 'pseudomonas_pct', 'prevotella_pct', 'streptococcus_pct']].to_string(index=False))

# Deep anoxic layer (10 mm) summary
tb_deep = tb_df[tb_df['depth_mm'] == 10].copy()
tb_deep['anaerobes_total_pct'] = tb_deep['prevotella_pct'] + tb_deep['streptococcus_pct'] + tb_deep['other_anaerobes_pct']
print('\n=== Deep Anoxic Layer (10 mm) Anaerobic Convergence Under Tobramycin ===')
print(tb_deep[['patient', 'afum_asv91_pct', 'pseudomonas_pct', 'prevotella_pct', 'streptococcus_pct', 'other_anaerobes_pct', 'anaerobes_total_pct']].to_string(index=False))
mean_anaerobes = tb_deep["anaerobes_total_pct"].mean()
print(f'Mean total anaerobe % at 10 mm: {mean_anaerobes:.1f}%')
