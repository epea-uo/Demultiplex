#!/usr/bin/env python

#to run (with this data specifically)
# python demultiplex.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz
# -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz
# -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz
# -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz
# -b /projects/bgmp/shared/2017_sequencing/indexes.txt
# -c 33

# TEST runs:
# python demultiplex.py -r1 /projects/bgmp/epea/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/zipped/test_r1.fastq.gz
# -r2 /projects/bgmp/epea/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/zipped/test_r2.fastq.gz
# -r3 /projects/bgmp/epea/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/zipped/test_r3.fastq.gz 
# -r4 /projects/bgmp/epea/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/zipped/test_r4.fastq.gz 
# -b /projects/bgmp/epea/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/zipped/test_known_barcodes
# -c 33

import bioinfo
import matplotlib.pyplot as plt
import gzip
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="A program to demultiplex data")
    parser.add_argument("-r1", "--read1_file", help="R1 input file", required=True)
    parser.add_argument("-r2", "--read2_file", help="R2 input file", required=True)
    parser.add_argument("-r3", "--read3_file", help="R3 input file", required=True)
    parser.add_argument("-r4", "--read4_file", help="R4 input file", required=True)
    parser.add_argument("-c", "--cutoff", help="Qscore cut off",type = int, required=True)
    parser.add_argument("-b", "--barcodes", help="File with known barcodes", required=True)
    return parser.parse_args()

args = get_args()
r1=args.read1_file
r2=args.read2_file
r3=args.read3_file
r4=args.read4_file
cutoff=args.cutoff

with open(args.barcodes, "r") as barcodes_file:
    lines = barcodes_file.readlines()
    barcode_lines = lines[1:]
    known_barcodes = [line.strip().split("\t")[-1] for line in barcode_lines]

dual_pairs_counts = dict()
mismatched_pairs_count = dict()
unknown_pairs_count = dict()

barcode_counter = 0
header_1 = ""
header_2 = ""
barcode_1 = ""
barcode_2 = ""
seq1 =""
seq2 = ""

barcode_files_dict = dict()
for i in known_barcodes:
    barcode_files_dict[i] = (open(f'{i}_r1.fastq', "w"), open(f'{i}_r2.fastq', "w"))

with (gzip.open(r1, "r") as r1, gzip.open(r2,"r") as r2,
      gzip.open(r3, "r") as r3, gzip.open(r4, "r") as r4,
      open("unknown_r1.fastq", "w") as unknown_r1,
      open ("unknown_r2.fastq", "w") as unknown_r2,
      open("index_hopped_r1.fastq", "w") as hopped_r1,
      open("index_hopped_r2.fastq", "w") as hopped_r2):
    for line_r2 in r2:
        line_r3 = r3.readline()
        line_r1 = r1.readline()
        line_r4 = r4.readline()
        line_r2 = line_r2.decode("utf-8").strip('\n')
        line_r3 = line_r3.decode("utf-8").strip('\n')
        line_r1 = line_r1.decode("utf-8").strip('\n')
        line_r4 = line_r4.decode("utf-8").strip('\n')
        barcode_counter+=1
        if barcode_counter % 4 == 1:
            header_1 = line_r1
            header_2 = line_r4
        if barcode_counter % 4 == 2:
            barcode_1 = line_r2
            barcode_2 = bioinfo.rev_comp(line_r3)
            seq1 = line_r1
            seq2 = line_r4
        if barcode_counter % 4 == 0:
            # Time to catch all unknown and low quality barcodes
            if (barcode_1 not in known_barcodes or barcode_2 not in known_barcodes
                or bioinfo.qual_score(line_r2) < cutoff
                or bioinfo.qual_score(line_r3) < cutoff):
                if f'{barcode_1}-{barcode_2}' not in unknown_pairs_count:
                    unknown_pairs_count[f'{barcode_1}-{barcode_2}'] = 1
                else:
                    unknown_pairs_count[f'{barcode_1}-{barcode_2}'] += 1
                unknown_r1.write(f'{header_1} {barcode_1}-{barcode_2}\n')
                unknown_r1.write(f'{seq1}\n')
                unknown_r1.write(f'+\n')
                unknown_r1.write(f'{line_r1}\n')
                unknown_r2.write(f'{header_2} {barcode_1}-{barcode_2}\n')
                unknown_r2.write(f'{seq2}\n')
                unknown_r2.write(f'+\n')
                unknown_r2.write(f'{line_r4}\n')
            # Catching all the index hopped reads
            elif barcode_1 != barcode_2:
                if f'{barcode_1}-{barcode_2}' not in mismatched_pairs_count:
                    mismatched_pairs_count[f'{barcode_1}-{barcode_2}'] = 1
                else:
                    mismatched_pairs_count[f'{barcode_1}-{barcode_2}'] += 1
                hopped_r1.write(f'{header_1} {barcode_1}-{barcode_2}\n')
                hopped_r1.write(f'{seq1}\n')
                hopped_r1.write(f'+\n')
                hopped_r1.write(f'{line_r1}\n')
                hopped_r2.write(f'{header_2} {barcode_1}-{barcode_2}\n')
                hopped_r2.write(f'{seq2}\n')
                hopped_r2.write(f'+\n')
                hopped_r2.write(f'{line_r4}\n')
            # Catching all correctly matched reads!
            elif barcode_1 == barcode_2:
                if f'{barcode_1}-{barcode_2}' not in dual_pairs_counts:
                    dual_pairs_counts[f'{barcode_1}-{barcode_2}'] = 1
                else:
                    dual_pairs_counts[f'{barcode_1}-{barcode_2}'] += 1
                barcode_files_dict[barcode_1][0].write(f'{header_1} {barcode_1}-{barcode_2}\n')
                barcode_files_dict[barcode_1][0].write(f'{seq1}\n')
                barcode_files_dict[barcode_1][0].write(f'+\n')
                barcode_files_dict[barcode_1][0].write(f'{line_r1}\n')
                barcode_files_dict[barcode_1][1].write(f'{header_2} {barcode_1}-{barcode_2}\n')
                barcode_files_dict[barcode_1][1].write(f'{seq2}\n')
                barcode_files_dict[barcode_1][1].write(f'+\n')
                barcode_files_dict[barcode_1][1].write(f'{line_r4}\n')


for i in barcode_files_dict: # close all the files for the matched reads
    barcode_files_dict[i][0].close()
    barcode_files_dict[i][1].close()

total_reads = sum(dual_pairs_counts.values())+ sum(mismatched_pairs_count.values()) + sum(unknown_pairs_count.values())

print(f'Total number of matched reads:', sum(dual_pairs_counts.values()))
for barcode in dual_pairs_counts:
    print(f'Percent of {barcode} in matched reads:', dual_pairs_counts[barcode]/sum(dual_pairs_counts.values())*100, f'%')
    print(f'Percent of {barcode} in all reads:', dual_pairs_counts[barcode]/total_reads*100, f'%')

plt.figure(figsize=(10, 6))
#plt.yscale("log")
plt.bar(dual_pairs_counts.keys(), dual_pairs_counts.values())
plt.title("Number of matched reads")
plt.xlabel("barcode")
plt.ylabel("Number of matched reads")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f"hist_matched_reads")
print("Look at hist_matched_reads.png for cool figure")

print(f'Total number of index hopped reads:', sum(mismatched_pairs_count.values()))
print(f'Total number of unknown reads:', sum(unknown_pairs_count.values()))
