#!/usr/bin/python

import argparse
import decimal
from scipy.stats.kde import gaussian_kde
import numpy

def main():

    print "Four Square ics to AMS geospatial parser"
    
    #set and get command line args
    parser = argparse.ArgumentParser(description='Parse 4sq ics data\
                                                   into AMS geospatial')
    parser.add_argument('foursquare_ics',
                         metavar='filename', 
                         type=argparse.FileType('r'),
                         help='filename of four squre data - must be in\
                         ICS format')
    args = parser.parse_args()
    
    # read in ics file
    lines = args.foursquare_ics.readlines()
    
    #we're only interested in GEO co-ordinates, ie lines starting with GEO
    geo = []
    for i, line in enumerate(lines):
        if lines[i].startswith("GEO"):
            geo.append(line[4:len(line)].rstrip())
    
    #narrow down co-ords to AMS specific co-ords - within the A10 ring
    """
    most east - https://maps.google.nl/?ll=52.345027,4.841108&spn=0.007669,0.021136&t=m&z=16
    most west - https://maps.google.nl/?ll=52.373759,4.974124&spn=0.001916,0.005284&t=m&z=18
    most south - https://maps.google.nl/?ll=52.328468,4.913657&spn=0.007671,0.021136&t=m&z=16
    most north - https://maps.google.nl/?ll=52.425068,4.888594&spn=0.003827,0.010568&t=m&z=17
    
    E 4.841
    W 4.974
    S 52.328
    N 52.425
    
    latitude = 52
    longtitude = 4
    """
    maxNorth = 52.425
    maxEast  = 4.841
    maxSouth = 52.328
    maxWest  = 4.974
    
    ams_coords = []
    for i, item in enumerate(geo):
        latitude = float(item.split(";")[0])
        longtitude = float(item.split(";")[1])
        
        #check that the GEO co-ord is within our catchment area
        if latitude < maxNorth and latitude > maxSouth:
            if longtitude < maxWest and longtitude > maxEast:
                #and store as a tuple
                ams_coords.append((latitude, longtitude))
        
    print "There have been %i checkins in Amsterdam" % len(ams_coords)
    
    #reduce lat+long down to 3 decimal places
    for i, coord in enumerate(ams_coords):
        ams_coords[i] =(round(decimal.Decimal(coord[0]),3),
                        round(decimal.Decimal(coord[1]),3))
        
    #establish le grid, filled with zeros
    """
    grid is 
    X x Y
    width x height
    columns x rows
    (maxWest - maxEast) x (maxNorth - maxSouth)
    minus 1 for each - zero indexed buggery
    = [96] x [132]
    """
    grid = [[2 for x in range(96)] for y in range(132)]
    
    #cycle through the list of coords and +1 the relevant 'grid position'
    for i, coord in enumerate(ams_coords):
        #get position relative to .425 for latitude values
        gridX = 425 - int((coord[0] - int(coord[0])) * 1000)
        #get position relative to .974 for latitude values
        gridY = 974 - int((coord[1] - int(coord[1])) * 1000)
        grid[gridY][gridX] = grid[gridY][gridX] + 1
        
    #normalise ALL the ranges
    #find larget value
    largest = 0.0
    for gridRow in grid:
        for item in gridRow:
            if item > largest:
                largest = float(item)
    
    print "Largest value is %i" % largest
    
    #divide all values by largest
    #multiply each value by our 'range' factor
    rangeFactor = 15.0;
    
    for i, gridRow in enumerate(grid):
        for j, item in enumerate(gridRow):
            result = (float(item) / largest) * rangeFactor
            grid[i][j] = result
        
    #mangle data with gaussian_kde
    #for ever X line
    for i, gridRow in enumerate(grid):
        print gridRow
        nparray = numpy.array(gridRow)
        print nparray
        pdf = gaussian_kde(nparray)
        for j, item in enumerate(gridRow):
            grid[i][j] = pdf(j);
    
    #output data
    outputFile = open('foursquare.dat','w+')
    
    for gridRow in grid:
        for item in gridRow:
            outputFile.write('%f ' % item)
        outputFile.write("\n")

if __name__ == "__main__":
    main()
