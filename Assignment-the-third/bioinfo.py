#!/usr/bin/env python

# Author: Emma Pearce <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = "ACTGNactgn"
RNA_bases = "ACUGNacugn"

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    '''Takes the phred score line and computes the average quality score of the whole string'''
    sum = 0
    for letter in phred_score:
        sum +=(convert_phred(letter))
    return(sum/len(phred_score))

def validate_base_seq(seq, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    valid_bases = RNA_bases if RNAflag else DNA_bases
    return all([base in valid_bases for base in seq.upper()])

def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(DNA), "String contains invalid characters - are you sure you used a DNA sequence?"
    DNA = DNA.upper()
    return (DNA.count("G")+DNA.count("C"))/len(DNA)

def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list'''
    lst=sorted(lst)
    if len(lst) % 2 ==1: #if list has an odd number of elements
        middle_index = (len(lst) - 1)//2
        return lst[middle_index]
    else: #if list has even number of elements
        small_middle = int((len(lst) - 1)/2)
        median = (lst[small_middle] + lst[small_middle +1])/2
        return median

def oneline_fasta(file_in,file_out):
    '''Takes file_in (fasta file) that has multiple sequence lines per record
    goes through and combines all sequence lines into one'''
    with open(file_in, "r") as fi:
        with open(file_out,"w") as fo:
            line_num = 0
            for line in fi:
                line =line.strip('\n')
                if line_num == 0:
                    fo.write(f'{line}\n')
                elif line.startswith(">"):
                    fo.write(f'\n{line}\n')
                else:
                    fo.write(line)
                line_num +=1
            fo.write("\n")

def rev_comp(orig: str) -> str:
    orig = orig.upper()
    rev_comp = ''
    complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N':'N'}
    if validate_base_seq(orig):
        rev = orig[::-1]
        for base in rev:
            rev_comp+=complements[base]
    else:
        print("Sequence has non DNA bases")
    return rev_comp

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
    assert qual_score("EEE") == 36
    assert qual_score("#I") == 21
    assert qual_score("EJ") == 38.5
    print("You calcluated the correct average phred score")
    assert validate_base_seq("AATAGAT", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("TATUC",False) == False
    assert validate_base_seq("UCUGCU", False) == False
    print("Passed DNA and RNA tests")
    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("Correctly calculated GC content")
    assert calc_median([1,2,100]) == 2, "calc_median function does not work for odd length list"
    assert calc_median([1,2]) == 1.5, "calc_median function does not work for even length list"
    assert calc_median([1,1,1,1,1,1,1,1,1,5000]) == 1
    assert calc_median([1,2,3,4,5,6,7,13]) == 4.5
    print("Median successfully calculated")
    print("") #checking autograder things
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Autograder passed convert_phred")
    assert qual_score("A") == 32.0, "wrong average phred score for 'A'"
    assert qual_score("AC") == 33.0, "wrong average phred score for 'AC'"
    assert qual_score("@@##") == 16.5, "wrong average phred score for '@@##'"
    assert qual_score("EEEEAAA!") == 30.0, "wrong average phred score for 'EEEEAAA!'"
    assert qual_score("$") == 3.0, "wrong average phred score for '$'"
    print("Autograder passed qual_score")
    assert validate_base_seq("AATAGAT"), "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True), "Validate base seq does not work on RNA"
    assert validate_base_seq("R is the best!")==False, "Not a DNA string"
    assert validate_base_seq("aatagat"), "Validate base seq does not work on lowercase DNA"
    assert validate_base_seq("aauagau", True), "Validate base seq does not work on lowercase RNA"
    assert validate_base_seq("TTTTtttttTTT")
    print("Autograder passed validate_base_seq")
    assert calc_median([1,2,3]) == 2
    assert calc_median([5,6,7,8]) == 6.5
    assert calc_median([1,1,1,1,1,1,1,1,100]) == 1
    assert calc_median([7]) == 7
    assert calc_median([50,100]) == 75
    print("Autograder passed calc_median")
    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("Autograder passed gc_content")
    assert rev_comp('AAAAA') == 'TTTTT'
    assert rev_comp('ATGC') == 'GCAT'
    assert rev_comp('TANC') == 'GNTA'
    print("Autograder passed rev_comp")

