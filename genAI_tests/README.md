Trying to use copilot to make unit tests for demultiplexing.

## Prompts:

### To make 4 input fastq files:
I want to make unit tests for demultiplexing. These should be four files all in fastq format. In AI_test1_r1.fastq, there should be four records, each with a read length of 101 bases. In AI_test1_r2.fastq  there should be four records with sequences only 8 based long. The quality scores in for each each base in each record should be Is except for the last record where the quality scores for each base should be 0s. AI_test1_r3.fastq should be a copy of AI_test1_r2.fastq except the second sequence in AI_test1_r3.fastq should be the same as the first sequence in AI_test1_r2.fastq. Finally there should be AI_test1_r4.fastq. AI_test1_r4.fastq should have four records each with a read length of 101 bases. Can you make these files?

Note: Looks good, not the most creative sequences for the biological reads

### To make known barcodes file:
