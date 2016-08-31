#!/usr/bin/env python
""" functions to handle maxcluster output"""

import sys
from pprint import pprint as pp


class MaxCluster(object):
    def __init__(self, file_name):
        index = file_name.rfind('/') if '/' in file_name else 0
        self.path = file_name[:index]
        self._data = self.parse_output(file_name)
    
    def parse_output(self, file_name):
        """returns the file as a dictionary [cluster] = list_of_members"""
        file = open(file_name)
        d = dict()
        for i in file:
            l = i.split()
	    cluster  = int(l[4])
	    name = l[5]
	    if cluster not in d.keys():
	        d[cluster]=list()
	    d[cluster].append(name)
        return d

    def get_cluster(self, number):
        return self._data[number]

    def save_each_cluster(self):
        """saves a list for each cluster with its members"""
        for cluster in self._data.keys():
	    open('c_' + cluster, 'w').writelines(
               pdb + '\n' for pdb in self._data[cluster])
