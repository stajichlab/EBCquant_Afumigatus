#!/usr/bin/env python3
import os
import subprocess
from Bio import SeqIO
from Bio.Seq import Seq

# Sputum ASV 91 (150 bp)
sputum_asv = 'TACGTAGAAGACTAGTGTTAGTCATCTTTATTAGGTTTAAAGGGTACCTAGACGGTAAATTAAACTCTAAATGAGTACTTTTTTACTAGAGTTTTATGTGAGAAGGAAGAATTTCTGGAGTAGTGATGAAATACCTTGATACCAGAAGGA'

# We know that in A. fumigatus, the 515f flank is: GTGCCAGCAGTCGCGGTAA
# followed immediately by the 150 bp ASV.
# Let's verify by blasting the 150 bp ASV against all_genomes_db with task blastn, evalue 1e-2.

cmd = [
    'blastn',
    '-task', 'blastn',
    '-db', 'analysis/mito_phylogeny/all_genomes_db',
    '-query', 'analysis/mito_phylogeny/asv91_query.fa',
    '-outfmt', '6 sseqid sstart send length pident evalue sstrand qstart qend',
    '-evalue', '1e-2'
]
res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)

# Parse BLAST hits
hits = {}
for line in res.stdout.strip().split('\n'):
    if not line:
        continue
    parts = line.split('\t')
    sseqid = parts[0]
    sstart, send = int(parts[1]), int(parts[2])
    length = int(parts[3])
    pident = float(parts[4])
    sstrand = parts[6]
    qstart, qend = int(parts[7]), int(parts[8])
    
    # We want the best hit per genome covering the query
    if sseqid not in hits or length > hits[sseqid]['length']:
        hits[sseqid] = {
            'sstart': sstart,
            'send': send,
            'length': length,
            'pident': pident,
            'sstrand': sstrand,
            'qstart': qstart,
            'qend': qend
        }

print(f'V4 homologous hits found in {len(hits)} genomes')

genome_dict = {rec.id: str(rec.seq) for rec in SeqIO.parse('analysis/mito_phylogeny/all_genomes.fasta', 'fasta')}

v4_entries = [('CF_sputum_ASV91', sputum_asv)]

for gid, h in sorted(hits.items()):
    seq = genome_dict[gid]
    strand = h['sstrand']
    
    # We want the 150 bp region starting from the homologous 5' position
    s1, s2 = h['sstart'], h['send']
    if strand == 'plus':
        # If query started at qstart, adjust start
        adj_start = s1 - (h['qstart'] - 1)
        sub = seq[adj_start - 1 : adj_start - 1 + 150]
    else:
        adj_start = s1 + (h['qstart'] - 1)
        sub = seq[adj_start - 150 : adj_start]
        sub = str(Seq(sub).reverse_complement())
    
    if len(sub) == 150:
        v4_entries.append((gid, sub))
        pident = h['pident']
        print(f'  {gid}: len={len(sub)}, identity={pident}%, strand={strand}')
    else:
        print(f'  WARNING: {gid} subseq len={len(sub)}')

with open('analysis/mito_phylogeny/v4_150bp.fasta', 'w') as out:
    for name, s in v4_entries:
        out.write(f'>{name}\n{s}\n')

print(f'\nWrote {len(v4_entries)} sequences to analysis/mito_phylogeny/v4_150bp.fasta')
