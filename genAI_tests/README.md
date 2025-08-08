Trying to use copilot to make unit tests for demultiplexing.

**Important**: Could not ever get it to make the correct read 1 and read 4 files.

## Prompts:

### To make 4 input fastq files:
I want to make unit tests for demultiplexing. These should be four files all in fastq format. In AI_test1_r1.fastq, there should be four records, each with a read length of 101 bases. In AI_test1_r2.fastq  there should be four records with sequences only 8 based long. The quality scores in for each each base in each record should be Is except for the last record where the quality scores for each base should be 0s. AI_test1_r3.fastq should be a copy of AI_test1_r2.fastq except the second sequence in AI_test1_r3.fastq should be the same as the first sequence in AI_test1_r2.fastq. Finally there should be AI_test1_r4.fastq. AI_test1_r4.fastq should have four records each with a read length of 101 bases. Can you make these files?

Note: AI can't count! It kept giving me different lengths of sequences even if I specificed for each record how many bases I wanted. At one point I asked copilot to just output 101 Gs and it gave me 213, or 99, or 97.

### To make known barcodes file:

Now I would like to make one file called AI_known_barcodes that has 5 tab separated columns. Column one should be sample followed by group, treatment, index, and index sequence. There should be three rows after the header that has the first three barcodes from AI_test1.r2.fastq. The barcodes should be under the index sequence column. The other three columns can be random strings. Can you make this file?

Note: Looks good


### Overall thoughts:

It was definitely pretty easy to make the files, not as easy to make them correct. The AI really struggled with making the correct lengths of reads. I've realized it just fully can't count (especially for all Ts and Gs for some reason).  
