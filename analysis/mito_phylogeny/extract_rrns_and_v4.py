#!/usr/bin/env python3
import glob
import os
import subprocess
from Bio import SeqIO
from Bio.Seq import Seq

# 1. Query: A. fumigatus rrnS full length (1437 bp)
ref_rrns_fa = 'analysis/mito_phylogeny/ref_rrns_full.fasta'

# ASV 91 (150 bp from CF sputum)
asv91_seq = 'TACGTAGAAGACTAGTGTTAGTCATCTTTATTAGGTTTAAAGGGTACCTAGACGGTAAATTAAACTCTAAATGAGTACTTTTTTACTAGAGTTTTATGTGAGAAGGAAGAATTTCTGGAGTAGTGATGAAATACCTTGATACCAGAAGGA'

v4_records = []
full_records = []

# Add ASV 91
v4_records.append(('CF_sputum_ASV91', asv91_seq))

# Prepare a single FASTA with all mitochondrial genomes
genomes_file = 'analysis/mito_phylogeny/all_genomes.fasta'
with open(genomes_file, 'w') as out:
    for gfile in sorted(glob.glob('analysis/mito_phylogeny/fasta_genomes/*.fa')):
        name = os.path.basename(gfile).replace('.fa', '')
        for rec in SeqIO.parse(gfile, 'fasta'):
            out.write(f'>{name}\n{str(rec.seq)}\n')
            break

print('Created all_genomes.fasta. Building BLAST DB...')
subprocess.run(['makeblastdb', '-in', genomes_file, '-dbtype', 'nucl', '-out', 'analysis/mito_phylogeny/all_genomes_db'], check=True)

# 1. BLAST full rrnS
print('Blasting full rrnS against all genomes...')
cmd = [
    'blastn',
    '-db', 'analysis/mito_phylogeny/all_genomes_db',
    '-query', ref_rrns_fa,
    '-outfmt', '6 qseqid sseqid sstart send length pident evalue sstrand',
    '-max_target_seqs', '100'
]
res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)

best_hits = {}
for line in res.stdout.strip().split('\n'):
    if not line:
        continue
    parts = line.split('\t')
    sseqid = parts[1]
    sstart = int(parts[2])
    send = int(parts[3])
    length = int(parts[4])
    pident = float(parts[5])
    sstrand = parts[7]
    
    if sseqid not in best_hits or length > best_hits[sseqid]['length']:
        best_hits[sseqid] = {
            'sstart': sstart,
            'send': send,
            'length': length,
            'pident': pident,
            'sstrand': sstrand
        }

print(f'Found full rrnS hits in {len(best_hits)} genomes')

# Load genomes into dict
genome_dict = {rec.id: str(rec.seq) for rec in SeqIO.parse(genomes_file, 'fasta')}

for gid, h in sorted(best_hits.items()):
    seq = genome_dict[gid]
    strand = h['sstrand']
    s1, s2 = min(h['sstart'], h['send']) - 1, max(h['sstart'], h['send'])
    subseq = seq[s1:s2]
    if strand == 'minus':
        subseq = str(Seq(subseq).reverse_complement())
    full_records.append((gid, subseq))

# 2. BLAST 150 bp ASV 91 to get exact homologous 150 bp V4 region from every genome
with open('analysis/mito_phylogeny/asv91_query.fa', 'w') as out:
    out.write(f'>asv91\n{asv91_seq}\n')

cmd_v4 = [
    'blastn',
    '-db', 'analysis/mito_phylogeny/all_genomes_db',
    '-query', 'analysis/mito_phylogeny/asv91_query.fa',
    '-outfmt', '6 qseqid sseqid sstart send length pident evalue sstrand',
    '-max_target_seqs', '100'
]
res_v4 = subprocess.run(cmd_v4, stdout=subprocess.PIPE, text=True, check=True)

best_v4_hits = {}
for line in res_v4.stdout.strip().split('\n'):
    if not line:
        continue
    parts = line.split('\t')
    sseqid = parts[1]
    sstart = int(parts[2])
    send = int(parts[3])
    length = int(parts[4])
    pident = float(parts[5])
    sstrand = parts[7]
    
    if sseqid not in best_v4_hits or length > best_v4_hits[sseqid]['length']:
        best_v4_hits[sseqid] = {
            'sstart': sstart,
            'send': send,
            'length': length,
            'pident': pident,
            'sstrand': sstrand
        }

print(f'Found V4 hits in {len(best_v4_hits)} genomes')

for gid, h in sorted(best_v4_hits.items()):
    seq = genome_dict[gid]
    strand = h['sstrand']
    s1, s2 = min(h['sstart'], h['send']) - 1, max(h['sstart'], h['send'])
    subseq = seq[s1:s2]
    if strand == 'minus':
        subseq = str(Seq(subseq).reverse_complement())
    v4_records.append((gid, subseq))

# Write FASTA files
with open('analysis/mito_phylogeny/rrns_v4_dataset.fasta', 'w') as out:
    for name, s in v4_records:
        out.write(f'>{name}\n{s}\n')

with open('analysis/mito_phylogeny/rrns_full_dataset.fasta', 'w') as out:
    for name, s in full_records:
        out.write(f'>{name}\n{s}\n')

print(f'Wrote {len(v4_records)} sequences to rrns_v4_dataset.fasta')
print(f'Wrote {len(full_records)} sequences to rrns_full_dataset.fasta')
