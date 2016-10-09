#!/usr/bin/python

#i	j	i_id	j_id	r_sco	s_sco	prob
#65	115	65_E	115_H	1.2476	3.839	1.000

from pymol import cmd

class Gremlin(object):
    """this class parses gremlin output and can display it when running form
    pymol.
    """

    def __init__(self, file_name):
        self.path = file_name
        self.__data = self.parse_output(self.path)

    def get_data(self):
        """returns all data parsed from gremlin's output"""
        return self.__data

    def get_pairs(self):
        """returns a list of tuples of the co-evolving pairs"""
        return [cov[:2] for cov in self.__data]

    def parse_output(self, file_name):
        """returns the output as a list of tuples 
        (i, j, i_id, j_id, r_sco, s_sco,prob)
        """ 
        f = open(file_name, 'r')
        gremlin = list()
        for line in f:
            cov = line.split()
            if cov[0].strip().isdigit():
                gremlin.append(cov)
        return gremlin

    def show_sticks(self, protein):
        """shows all cov residues as sticks (not very useful...)"""
        for i in self.__data:
            cmd.show('sticks', 'resi {}+{} and {}'.format(i[0], i[1], protein))

    def show_pairs_dist(self, protein, prob_cutoff = 0.9, mode = 4):
        """shows CA distances between pair of residues having a probability >
        prob_cutoff.
        Args:
            mode: for distance function in pynol (details in pymolWiki)
            4 - CA-CA
            2 - polar interaction
        """
        pairs = [cov[:2] for cov in self.__data if 
                float(cov[-1]) >= prob_cutoff]
        self.__show_dist(pairs, protein, mode)
    
    def show_in_both(self, gremlin, protein):
        """shows only contacts that are both in this instance and in another
        Gremlin instance named gremlin
        """
        this_pairs = [cov[:2] for cov in self.__data]
        pairs = [cov[:2] for cov in gremlin.__data if cov[:2] in this_pairs]
        self.__show_dist(pairs, protein, mode = 4)

    def __show_dist(self, pairs, protein, mode):
        """shows dist between the pairs in pairs on protein with the wanted
        distance mode
        """
	for i, j in pairs:
	    sele1 = '(resi {} and name ca)'.format(i)
	    sele2 = '(resi {} and name ca)'.format(j)
	    name = 'pc_{}_{}'.format(i, j)
	    cmd.distance(name, sele1, sele2, mode = 4)
        #for i, j in pairs:
        #    sele_name = 'sele_{}_{}'.format(i, j)
        #    sele_group = 'resi {}+{} and {} and name ca'.format(i, j, protein)
        #    cmd.select(sele_name, sele_group)
        #    dist = cmd.distance(name = 'pc_{}_{}'.format(i, j),
        #                        selection1 = sele_name,
        #            selection2 = sele_name,
        #            mode = mode,
        #            label = 0)
        #cmd.delete('sele_*')
