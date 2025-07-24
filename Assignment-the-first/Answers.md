# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | bio_r1 | 101 | 33 |
| 1294_S1_L008_R2_001.fastq.gz | index_r1 | 8 | 33 |
| 1294_S1_L008_R3_001.fastq.gz | index_r2 | 8 | 33 |
| 1294_S1_L008_R4_001.fastq.gz | bio_r2 | 101 | 33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. **YOUR ANSWER HERE**
    3. **YOUR ANSWER HERE**
    
## Part 2
1. Define the problem

When multiple samples are sequenced in one run on Illimina, each sample gets its own barcode to identify it. After sequencing, the biological reads and their barcodes are outputted to four fastq files (one for each read).  Each forward and reverse read should have matching indexes. For example, if read 1 is matched with barcode A, read 2 should also have been matched with barcode A. During sequencing some barcodes will be low quality, not found in our known barcodes, or will become mismatched for their reads (Ex: r1 = barcode A and r2 = barcode F). If any of these things happen we need to output them to their own fastq files and appropriately label them.

2. Describe output

The script should output multiple fastq files. There should be two fastqs per matching indexes (barcode A with barcode A for corresponding reads). There should also be two files for every mismatched set of barcodes (A with C for example). Finally, there should also be two files for every unknown barcode pair or barcode pair that falls below the quality score cutoff.
Additionally, there should be several text outputs to the script. These include the number of matched barcode pair reads (total and by each pair) (total = just a number, each pair maybe a figure). There should also be the number of mismatched barcodes (can also do the number per each mismatched pair in a figure). Lastly, there should be the number of unknown reads (can also make a figure for each unknown pair).

3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode

pseudocode can be found [here](./psudocode_demultiplexing.txt)

5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

def rev_comp(seq: string) -> string:
	'''takes a DNA sequence and returns the reverse compliment'''
	return rev_comp
Input: ACTGCTGATC
Expected output: GATCAGCAGT
