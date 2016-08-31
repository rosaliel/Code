"""handling MSA"""

from Bio import AlignIO

def parse_MSA(file_name, format = 'fasta'):
    alignment = AlignIO.read(file_name, format)
    return alignment

def write_MSA(alignment, file_name, format):
    """writes alignment object to file_name with the wanted format"""
    AlignIO.write(alignment, file_name, format)

def convert_format(file_name, s_format, e_format):
    try:
        alignment = parse_MSA(file_name, s_format)
	write_MSA(alignment, '{}.{}'.format(file_name, e_format), e_format)
    except:
        print 'bad file name or format'

def get_columns(alignment, c_start, c_end):
    return alignment[:, (c_start - 1):c_end]

def real_index_to_aligned(seq, index):
    """returns the index in the python sequence (first index is 0)"""
    return get_index_map(seq)[index]

def get_index_map(seq):
    """returns a dictionary mapping real indices (starting from one) to the
    aligned ones (starting from zero): [real] = aligned_index
    """
    index_map = dict()
    count = 0
    for i in range(len(seq)):
        aa = seq[i]
        if aa != '-':
	    count += 1
	    index_map[count] = i
    return index_map
