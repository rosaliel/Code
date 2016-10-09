#!/usr/bin/env python
""" functions to handle maxcluster output"""

import sys
from pprint import pprint as pp


class MaxCluster(object):
    def __init__(self, file_name):
        index = file_name.rfind('/') if '/' in file_name else 0
	self.path = file_name[:index]
	self.__data = self.parse_output(file_name)
    
    def parse_output(self, file_name):
        """returns the file as a dictionary [cluster] = list_of_members"""
        file = open(file_name)
        d = dict()
        start_line = 'INFO  : Item     Cluster'
	end_line = 'INFO  : ======================================'
	flag = False
	for line in file:
	    if start_line in line:
	        flag = True
	    elif flag and (end_line in line):
		break
	    elif flag:
	        cluster = int(line.split()[4])
		name = line.split()[5]
		if cluster not in d.keys():
		    d[cluster] = list()
		d[cluster].append(name)
        return d
    
    def get_cluster(self, number):
        return self.__data[number]

    def save_each_cluster(self):
        """saves a list for each cluster with its members"""
        for cluster in self.__data.keys():
	    open('c_' + cluster, 'w').writelines(
               pdb + '\n' for pdb in self.__data[cluster])

    def filter_best_energy(self):
        """filters from each cluster the best energy structure and returns a
	list of this structures' names
	"""
	best_e = list()
	for cluster in self.__data.keys():
	    if len(self.__data[cluster]) == 1:
	        best_e.append((cluster, self.__data[cluster][0]))
	    else:
	        scores = []
		for i in self.__data[cluster]:
		    pdb = open(i).readlines()
		    line = (filter(lambda x: ~x.find('pose'), pdb)[0]).strip()
		    scores.append(float(line.split()[-1]))
                best_e.append((cluster,
		             self.__data[cluster][scores.index(min(scores))]))
	return best_e
		            
