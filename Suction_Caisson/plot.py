#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:36:53 2022

@author: goharshoukat
"""
import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#from sklearn.preprocessing import MinMaxScaler

#capacity checks are implemented through functions instead of nested if else
#to avoid cluttering and make code more readable. 
plt.style.use('dark_background')

def sand_anchor(dimensions):
    #input
    #dimensions : dict : result of the designer script
     return ((dimensions['Drained bearing capacity']==True) & (
        dimensions['Eccentricity'] == True))


def sand_foundation(dimensions):
    #input
    #dimensions : dict : result of the designer script
     return ((dimensions['Drained bearing capacity']==True) & (dimensions['Sliding']==True))

def clay_anchor(dimensions):
    return ((dimensions['Undrained bearing capacity']==True) & (
       dimensions['Eccentricity'] == True))

def clay_foundation(dimensions):
    return ((dimensions['Undrained bearing capacity']==True) & (dimensions['Sliding']==True))

def operate(dimensions, option):
    op = {
        'sand_anchor' : sand_anchor,
        'sand_foundation' : sand_foundation,
        'clay_anchor' : clay_anchor,
        'clay_foundation' : clay_foundation
        }
    option = op.get(option)
    return (option(dimensions))

    
def plot(dimensions, soil_type, foundation_type = 'anchor'):
    #Input
    #dimensions : pd.DataFrame : df of the relevent diensions and their
    #soil_type  : str          : lower case string, either sand or clay
    #foundation_type : str     : lower case string, anchor or foundation

    #commented out the scatter plot weighted size averageing code. 
    
    #Mc = np.reshape(np.array(dimensions['M']), (-1, 1))
    #scalar = MinMaxScaler(feature_range=(0.1, 1))
    #dimensions['M_resc'] = scalar.fit_transform(Mc) * 50
    dimensions['installation'] = (dimensions['Suction limit'] == True) & (
        dimensions['Self-weight installation'] == True) 
    
    
    #use dict and .get to run selection structures instead of nested if else
    dimensions['capacity'] = operate(dimensions, soil_type + '_' + foundation_type)
    
# =============================================================================
#     if soil_type == 'sand':
#         dimensions['capacity'] = (dimensions['Drained bearing capacity'] == True) & (
#             dimensions['Sliding'] == True) 
#     
#     else:
#         dimensions['capacity'] = (dimensions['Undrained bearing capacity'] == True) & (
#             dimensions['Sliding'] == True)
#             
# =============================================================================
        


    plt.rcParams.update({'font.size': 13.5})
    #Input
    #dimensions : pd.DataFrame : df of the relevent diensions and their
    #respective checks
    plt.figure()
    
    plt.scatter( dimensions['D'] , dimensions['L'],color = 'black')#, s=  dimensions['M_resc'])
        #Plot the results
    
    #insufficient capacity and uninstallable

    
    #sufficient capacitty and installable
    allTrue = dimensions[(dimensions['installation']==True) & 
                              (dimensions['capacity']==True)]
    plt.scatter(allTrue['D'], allTrue['L'], color = 'green', label = 'Sufficient Capacity, Installable')#,  s= allTrue['M_resc'])


    #sufficient capacity and uninstallable
    bearingTrue = dimensions[(dimensions['installation']==False) & 
                              (dimensions['capacity']==True)]
    plt.scatter(bearingTrue['D'], bearingTrue['L'], color = 'blue',
                label = 'Sufficient capacity, Non-installable')#,  s= bearingTrue['M_resc'])
    
    
    #insufficient capacity and installable
    installTrue = dimensions[(dimensions['installation']==True) & 
                              (dimensions['capacity']==False)]
    plt.scatter(installTrue['D'],  installTrue['L'], color = 'orange',
                label = 'Insufficient capacity, Installable')#, s= installTrue['M_resc'])
    
    allFalse = dimensions[(dimensions['installation']==False) & 
                          (dimensions['capacity']==False)]

    plt.scatter(allFalse['D'], allFalse['L'],  color = 'red', 
                label = 'Insufficient capacity, Non-Installable')#, s= allFalse['M_resc'])
    

    plt.ylabel('Length [m]') #user defined lengths
    plt.xlabel('Diameter [m]') #user defined diameter
    plt.legend(bbox_to_anchor=(1, 1))
    plt.title('Suction Installed Caisson {} Design Space'.format(
        foundation_type))
    plt.axis('scaled')
    #plt.gca().set_aspect('equal', adjustable='box')