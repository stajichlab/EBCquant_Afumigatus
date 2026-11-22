#!/usr/bin/env python3
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

def convert_sra(run_id, scratch_dir):
    sra_path = f"sra/{run_id}/{run_id}.sra"
    out_gz = f"fastq/{run_id}.fastq.gz"
    
    if os.path.exists(out_gz) and os.path.getsize(out_gz) > 0:
        return run_id, True, "already exists"
    
    if not os.path.exists(sra_path):
        return run_id, False, f"Missing SRA file: {sra_path}"
    
    cmd = [
        "parallel-fastq-dump",
        "--sra-id", sra_path,
        "--threads", "2",
        "--outdir", "fastq",
        "--split-3",
        "--gzip",
        "--tmpdir", scratch_dir
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            return run_id, False, f"Error: {res.stderr}"
        if not os.path.exists(out_gz):
            return run_id, False, f"Output file not found: {out_gz}"
        return run_id, True, "OK"
    except Exception as e:
        return run_id, False, str(e)

def main():
    scratch_dir = os.environ.get("SCRATCH", "/tmp")
    os.makedirs("fastq", exist_ok=True)
    
    with open("metadata/ERP109668_runs.tsv") as f:
        header = f.readline().strip().split("\t")
        run_idx = header.index("run_accession")
        runs = [line.strip().split("\t")[run_idx] for line in f if line.strip()]
    
    print(f"Total runs to convert: {len(runs)}")
    
    completed = 0
    errors = []
    # 2 concurrent jobs x 2 threads = 4 cores
    with ProcessPoolExecutor(max_workers=2) as executor:
        future_to_run = {executor.submit(convert_sra, r, scratch_dir): r for r in runs}
        for future in as_completed(future_to_run):
            run_id, success, msg = future.result()
            completed += 1
            if success:
                if completed % 25 == 0 or completed == len(runs):
                    print(f"Progress: {completed}/{len(runs)} runs processed")
            else:
                print(f"Failed {run_id}: {msg}", file=sys.stderr)
                errors.append((run_id, msg))
                
    if errors:
        print(f"\n{len(errors)} runs failed conversion!")
        sys.exit(1)
    else:
        print("\nAll runs converted successfully.")

if __name__ == "__main__":
    main()
