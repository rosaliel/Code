#!/usr/bin/python 
from pymol import cmd

def get_alignment( mobile, target):
    """alignes mobile to target (both are loaded protein's names).
    returns the alignment object - list of lists of pairs of tuples:
    [ (prot_a, index), (prot_b, index)]
    """
    cmd.select('ca_mobile', mobile + ' and name CA')
    cmd.select('ca_target', target + ' and name CA')
    aln_object = 'aln_%s_%s' %(mobile, target)
    cmd.align(mobile, target, object = aln_object)
    raw_aln = cmd.get_raw_alignment(aln_object)
    return raw_aln

def index2resi(prot, ids):
    """converts indices list to the correct residue number of prot.
    Args:
        prot - name of a loaded protein
        ids - list of indices
    returns a list of tuples (index, resi)
    """
    all_ids = '+'.join(str(i) for i in ids)
    res = {'res_i':[]}
    cmd.iterate('(index '+ all_ids +' and '+ prot +')', 
                'res_i.append((index, resv))', 
                space = res)
    return res['res_i']    
    
# def atom_aln2resi_aln(raw_aln, target_ind = 1):
    # """converts a raw_aln (parsed alignment object) to a dictionary mapping 
    # aligned residues between the target and the mobile protein.
    # Args:
    # target index - 0 if target's atoms are the first tuple of every list in 
               # raw_aln, else 1
    # returns a dictionary [ target residue ] = mobile residue
    # """
    # target_resi = index2resi(prot = raw_aln[0][target_ind][0], 
                             # ids = [i[target_ind][1] for i in raw_aln])
    # mobile_resi = index2resi(prot = raw_aln[0][1 ^ target_ind][0], 
                             # ids = [i[1 ^ target_ind][1] for i in raw_aln])
    # resi_pairs = dict()
    # for i in raw_aln:
        # # X_r is the index's residue in X in the current position in raw_aln
        # target_r = filter(lambda x: x[0] == i[target_ind][1], 
                          # target_resi)[0][1]
        # mobile_r = filter(lambda x: x[0] == i[1 ^ target_ind][1], 
                          # mobile_resi)[0][1]
        # if ((target_r in resi_pairs.keys()) 
               # and (mobile_r != resi_pairs[target_r])):          
              # print 'conflict: target=', target_r
              # print 'mobile1=', resi_pairs[target_r], 'mobile2=', mobile_r
        # else:
            # resi_pairs[target_r] = mobile_r
    # return resi_pairs    

    
def atom_aln2resi_aln(raw_aln, target_ind = 1):
    """converts a raw_aln (parsed alignment object) to a dictionary mapping 
    aligned residues between the target and the mobile protein.
    Args:
    target index - 0 if target's atoms are the first tuple of every list in 
               raw_aln, else 1
    returns a dictionary [ target residue ] = mobile residue
    """
    target_name = raw_aln[0][target_ind][0]
    mobile_name = raw_aln[0][1 ^ target_ind][0]
    resi_pairs = dict()
    for i in raw_aln:
        # X_r is the index's residue in X in the current position in raw_aln
        target_r = index2resi(prot=target_name, ids=[i[target_ind][1]])[0][1]
        mobile_r = index2resi(prot=mobile_name, 
                              ids=[i[1 ^ target_ind][1]])[0][1]
        if ((target_r in resi_pairs.keys()) 
               and (mobile_r != resi_pairs[target_r])):          
              print 'conflict: target=', target_r
              print 'mobile1=', resi_pairs[target_r], 'mobile2=', mobile_r
        else:
            resi_pairs[target_r] = mobile_r
    return resi_pairs 