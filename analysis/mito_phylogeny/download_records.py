#!/usr/bin/env python3
import time
import urllib.request
import re
import os

accessions = {
    # Section Fumigati
    'Aspergillus_fumigatus_A1163': 'NC_017016.1',
    'Aspergillus_fumigatus_Af293': 'JQ346808.1',
    'Aspergillus_fischeri_NRRL181': 'NC_016860.1',
    'Aspergillus_lentulus_IFM54703': 'LC612919.1',
    'Aspergillus_udagawae_IFM46973': 'LC602355.1',
    'Aspergillus_pseudoviridinutans_IFM55266': 'AP024468.1',
    
    # Section Clavati
    'Aspergillus_clavatus_NRRL1': 'NC_016859.1',
    
    # Section Flavi
    'Aspergillus_flavus_NRRL3357': 'NC_026850.1',
    'Aspergillus_oryzae_RIB40': 'NC_009945.1',
    
    # Section Nigri
    'Aspergillus_niger_CBS513.88': 'NC_007445.1',
    
    # Section Terrei
    'Aspergillus_terreus_NIH2624': 'NC_007449.1',
    
    # Section Nidulantes
    'Aspergillus_nidulans_FGSC_A4': 'NC_001224.1',
    
    # Other Eurotiales
    'Penicillium_rubens_Wisconsin54-1255': 'NC_022467.1',
    'Penicillium_digitatum_Pd1': 'NC_014691.1',
    'Penicillium_brasilianum_MG11': 'NC_034870.1',
    'Penicillium_solitum_TX01': 'NC_034914.1',
    'Talaromyces_marneffei_PM1': 'NC_005256.1',
    
    # Onygenales
    'Histoplasma_capsulatum_G186AR': 'NC_009880.1',
    'Coccidioides_immitis_RS': 'NC_005251.1',
    'Blastomyces_dermatitidis_ATCC18188': 'NC_023772.1',
    
    # Sordariomycetes
    'Fusarium_graminearum_PH-1': 'NC_009493.1',
    'Fusarium_oxysporum': 'NC_017930.1',
    'Neurospora_crassa_OR74A': 'NC_026614.1',
    
    # Basidiomycota outgroup
    'Cryptococcus_neoformans': 'NC_001615.1'
}

os.makedirs('analysis/mito_phylogeny/gb_records', exist_ok=True)

for name, acc in accessions.items():
    dest = f'analysis/mito_phylogeny/gb_records/{name}.gb'
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        continue
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={acc}&rettype=gb&retmode=text'
    print(f'Fetching {name} ({acc})...')
    retries = 3
    while retries > 0:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Bioinformatics Pipeline)'})
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode('utf-8')
            with open(dest, 'w') as out:
                out.write(text)
            print(f'  Saved {dest}')
            break
        except Exception as e:
            print(f'  Error: {e}, retrying...')
            time.sleep(2)
            retries -= 1
    time.sleep(0.5)

print('All records fetched.')
