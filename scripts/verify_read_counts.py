#!/usr/bin/env python3
import gzip
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

def count_fastq_reads(fastq_file):
    count = 0
    with gzip.open(fastq_file, 'rt') as f:
        for _ in f:
            count += 1
    return count // 4

def check_run(run_id, expected_count):
    fastq_file = f"fastq/{run_id}.fastq.gz"
    if not os.path.exists(fastq_file):
        return run_id, expected_count, None, False, "File missing"
    
    actual_count = count_fastq_reads(fastq_file)
    matches = (actual_count == expected_count)
    return run_id, expected_count, actual_count, matches, "OK" if matches else f"Mismatch: expected {expected_count}, got {actual_count}"

def main():
    metadata_file = "metadata/ERP109668_runs.tsv"
    runs_to_check = []
    with open(metadata_file) as f:
        header = f.readline().strip().split("\t")
        run_idx = header.index("run_accession")
        count_idx = header.index("read_count")
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            runs_to_check.append((parts[run_idx], int(parts[count_idx])))
            
    print(f"Verifying read counts for {len(runs_to_check)} FASTQ files...")
    
    mismatches = []
    completed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(check_run, r, c): r for r, c in runs_to_check}
        for future in as_completed(futures):
            run_id, exp, act, matches, msg = future.result()
            completed += 1
            if not matches:
                print(f"FAILED: {run_id} - {msg}", file=sys.stderr)
                mismatches.append((run_id, exp, act))
            if completed % 50 == 0 or completed == len(runs_to_check):
                print(f"Verified {completed}/{len(runs_to_check)} files")
                
    if mismatches:
        print(f"\n{len(mismatches)} runs had read count mismatches!", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\nAll {len(runs_to_check)} FASTQ files verified successfully against ENA read counts!")

if __name__ == "__main__":
    main()
