#!/usr/bin/python 


def get_atoms_list(prot):
    """returns resi list of prot"""
    res = {'residues':[]}
    cmd.iterate(prot, 'residues.append(resv)',space=res)
    prot_res = sorted( list( set( res['residues'])))
    return prot_res

def index2resi(prot, ids):
    """converts indices list to the correct residue number of prot.
    Args:
    	prot - name of a loaded protein
    	ids - list of indices
    returns a list of tuples (index, resi)
    """
    all_ids = '+'.join(str(i) for i in ids)
    res = {'res_i':[]}
    cmd.iterate('(index {} and {})'.format(all_ids, prot), 
                'res_i.append((index, resv))', 
    	        space = res)
    return res['res_i']
    	
def get_alignment( mobile, target):
    """alignes mobile to target (both are loaded protein's names).
    returns the alignment object - list of lists of pairs of tuples:
    [ (prot_a, index), (prot_b, index)]
    """
    cmd.select('ca_mobile', '{} and name CA'.format(mobile))
    cmd.select('ca_target', '{} and name CA'.format(target))
    aln_object = 'aln_{}_{}'.format(mobile, target)
    cmd.align(mobile, target, object = aln_object)
    raw_aln = cmd.get_raw_alignment(aln_object)
    return raw_aln

def atom_aln2resi_aln(raw_aln, target_ind = 1):
    """converts a raw_aln (parsed alignment object) to a dictionary mapping 
    aligned residues between the target and the mobile protein.
    Args:
    target index - 0 if target's atoms are the first tuple of every list in 
    	       raw_aln, else 1
    returns a dictionary [ target residue ] = mobile residue
    """
    target_resi = index2resi(prot = raw_aln[0][target_ind][0], 
                             ids = [i[target_ind][1] for i in raw_aln])
    mobile_resi = index2resi(prot = raw_aln[0][1 ^ target_ind][0], 
                             ids = [i[1 ^ target_ind][1] for i in raw_aln])
    resi_pairs = dict()
    for i in raw_aln:
    	target_r = filter(lambda x: x[0] == i[target_ind][1], 
    	                  target_resi)[0][1]
    	mobile_r = filter(lambda x: x[0] == i[1 ^ target_ind][1], 
    	                  mobile_resi)[0][1]
    	if ((target_r in resi_pairs.keys()) 
    	   and (mobile_r != resi_pairs[target_r])):
    	    print 'conflict: target={:5<} mobile1={:5<} mobile2={:5<}'.format(
	              target_r, 
		      resi_pairs[target_r], 
		      mobile_r)
    	else:
    		resi_pairs[target_r] = mobile_r
    return resi_pairs	
    
def remove_aligned_residues(mobile, target, remove_target = 1):
    """
    mobile - name of protein to align to target
    target - target protein
    remove_target - 1 for deleting aligned target residues, else 0
    aligns mobile to target, maps the aligned residues and removes them
    """
    raw_aln = get_alignment(mobile, target)
    index_target = 0 if raw_aln[0][0][0] == target else 1 # alignment object doesn't keep sending order
    residue_map = atom_aln2resi_aln(raw_aln, index_target)
    print residue_map
    for res_target in residue_map.keys():
        if remove_target:
    	    cmd.remove('resi {} and {}'.format(res_target, target))
    	cmd.remove('resi {} and {}'.format(residue_map[res_target], mobile))
