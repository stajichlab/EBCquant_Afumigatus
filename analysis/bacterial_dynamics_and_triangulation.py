#!/usr/bin/env python3
import biom
import numpy as np
import pandas as pd
import re
import os

os.makedirs('analysis/community_dynamics', exist_ok=True)

# 1. Load BIOM table 54502 (671 samples)
table = biom.load_table('data/microbiome/study_10863/BIOM/54502/otu_table.biom')
sample_ids = table.ids(axis='sample')
obs_ids = table.ids(axis='observation')
obs_meta = table.metadata(axis='observation')
sample_sums = table.sum(axis='sample')

# Define target taxonomic groups
target_genera = {
    'Pseudomonas': 'g__Pseudomonas',
    'Stenotrophomonas': 'g__Stenotrophomonas',
    'Streptococcus': 'g__Streptococcus',
    'Prevotella': 'g__Prevotella',
    'Veillonella': 'g__Veillonella',
    'Fusobacterium': 'g__Fusobacterium',
    'Mitochondria': 'f__mitochondria'
}

genus_mask = {}
for g, tag in target_genera.items():
    matching_indices = []
    for i, m in enumerate(obs_meta):
        tax_str = ';'.join(m.get('taxonomy', []))
        if tag in tax_str:
            matching_indices.append(i)
    genus_mask[g] = matching_indices

# Also get exact A. fumigatus ASV 91 counts from 129335 table for comparison
table_deblur = biom.load_table('data/microbiome/study_10863/BIOM/129335/all.biom')
asv91_seq = table_deblur.ids(axis='observation')[91]
deblur_sample_ids = list(table_deblur.ids(axis='sample'))
deblur_asv91_counts = table_deblur.data(asv91_seq, axis='observation')
deblur_sample_sums = table_deblur.sum(axis='sample')
deblur_asv91_dict = {
    s: (int(deblur_asv91_counts[i]), int(deblur_sample_sums[i]))
    for i, s in enumerate(deblur_sample_ids)
}

# 2. Extract per-sample abundances
sample_rows = []
for i, s in enumerate(sample_ids):
    tot = sample_sums[i]
    if tot == 0:
        continue
    
    # Parse metadata from sample id: 10863.<patient>.<depth/treatment>
    parts = s.split('.')
    rest = parts[1:]
    
    patient = 'unknown'
    treatment = 'unknown'
    depth = 'NA'
    
    if len(rest) == 1:
        if rest[0].startswith('Sp'):
            patient = rest[0][2:]
            treatment = 'sputum'
        elif 'Blank' in rest[0] or 'PBS' in rest[0]:
            patient = 'control'
            treatment = 'control'
        else:
            patient = rest[0]
            treatment = 'unknown'
    elif len(rest) == 2:
        patient = rest[0]
        treatment = 'untreated'
        depth_str = rest[1]
        depth_m = re.match(r'^(\d+)', depth_str)
        depth = int(depth_m.group(1)) if depth_m else np.nan
    elif len(rest) >= 3:
        patient = rest[0]
        if rest[1] in ['TB', 'BC']:
            treatment = 'tobramycin' if rest[1] == 'TB' else 'bicarbonate'
            depth_str = rest[2]
            depth_m = re.match(r'^(\d+)', depth_str)
            depth = int(depth_m.group(1)) if depth_m else np.nan
        else:
            treatment = rest[1]
            depth = rest[2]
            
    col_data = table.data(s, axis='sample')
    row = {
        'sample_name': s,
        'patient': patient,
        'treatment': treatment,
        'depth_mm': depth,
        'total_reads': int(tot)
    }
    
    for g, indices in genus_mask.items():
        g_reads = int(col_data[indices].sum())
        row[f'{g}_reads'] = g_reads
        row[f'{g}_rel_abund'] = g_reads / tot
        
    # Add exact deblur ASV 91
    if s in deblur_asv91_dict:
        asv_c, asv_tot = deblur_asv91_dict[s]
        row['afum_asv91_reads'] = asv_c
        row['afum_asv91_rel_abund'] = asv_c / asv_tot if asv_tot > 0 else 0.0
    else:
        row['afum_asv91_reads'] = 0
        row['afum_asv91_rel_abund'] = 0.0
        
    sample_rows.append(row)

df = pd.DataFrame(sample_rows)
df.to_csv('analysis/community_dynamics/study_10863_community_profiles.csv', index=False)
print(f'Wrote {len(df)} sample community profiles.')

# 3. Load MSV000081456 fumitremorgin C peak area
ftc_df = pd.read_csv('EBC-KT/analyses/Fumitremorgin-C/MSV000081456_feature578_per_run.csv')
# run format: 157Tb1_170805032247.mzML or 107Tb1.mzML
# Extract patient and depth:
ftc_rows = []
for _, r in ftc_df.iterrows():
    run_name = r['run']
    m = re.match(r'^(\d+)Tb(\d+)', run_name)
    if m:
        pt = m.group(1)
        dp = int(m.group(2))
        ftc_rows.append({
            'patient': pt,
            'depth_mm': dp,
            'ftc_peak_area': r['peak_area'],
            'ftc_detected': r['detected']
        })

ftc_clean = pd.DataFrame(ftc_rows)

# Merge with tobramycin samples
tb_df = df[(df['treatment'] == 'tobramycin') & (df['depth_mm'].isin(range(1, 11)))].copy()
tb_df['depth_mm'] = tb_df['depth_mm'].astype(int)
merged = pd.merge(tb_df, ftc_clean, on=['patient', 'depth_mm'], how='inner')
merged.to_csv('analysis/community_dynamics/microbiome_metabolome_merged_depth.csv', index=False)
print(f'Merged {len(merged)} sample depth points with MSV000081456 metabolomics.')

# 4. Compute summary of community structure across treatments and depths
mean_profiles = df[df['treatment'].isin(['untreated', 'tobramycin', 'bicarbonate']) & df['depth_mm'].isin(range(1, 11))].groupby(
    ['treatment', 'depth_mm']
)[['Pseudomonas_rel_abund', 'Stenotrophomonas_rel_abund', 'afum_asv91_rel_abund', 'Streptococcus_rel_abund', 'Prevotella_rel_abund', 'Veillonella_rel_abund']].mean().reset_index()

mean_profiles.to_csv('analysis/community_dynamics/depth_stratification_summary.csv', index=False)
print('Wrote depth_stratification_summary.csv')

# Print summary table
print('\n=== Mean Relative Abundances Across Depths under Tobramycin ===')
tb_summary = mean_profiles[mean_profiles['treatment'] == 'tobramycin']
print(tb_summary.to_string(index=False))
