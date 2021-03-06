#!/usr/bin/env python3

# adjaceancy.py
# Functions to cluster people together based on distance.

import numpy as np

def adjaceancy(riderlist):
    adj = np.empty((len(riderlist), len(riderlist)))
    for r1 in range(len(riderlist)):
        for r2 in range(r1 + 1):
            adj[r1,r2] = str(np.sqrt((riderlist[r1].get('x') - riderlist[r2].get('x'))**2 + ((riderlist[r1].get('y') - riderlist[r2].get('y'))**2)))
            adj[r2,r1] = adj[r1,r2]
            if r1 == r2:
                adj[r1,r2] = np.nan
    print(adj)
    return adj

def cluster(adj,riderlist):
    num_rid = len(adj[0])
    num_ungrp = num_rid
    clusters = []
    clus_ind = []
    clustered = False

    # intializes with each person in their own cluster, clus_ind follows the mutations of the
# adjaceancy matrix
    for i in range(num_rid):
        clus_ind.append([i])
    print(clus_ind)
    print(clusters)
    # Loop runs until all riders are in a cluster, ideally of more than 1 person
    while not clustered:
        # finds the shortest distance, stores the coordinates, and constructs values for what
        # rows and columns to removed later
        short = np.nanargmin(adj)
        A = int(short//num_ungrp)
        B = int(short%num_ungrp)
        first = np.maximum(A,B)
        second = np.minimum(A,B)

        # Grouping indices in temp that correspond to specific riders, converts to names at end
        temp =[]
        for i in clus_ind[A]:
            temp.append(i)

        for i in clus_ind[B]:
            temp.append(i)

        print(temp)

        # Removes lists that have been combined
        clus_ind.pop(first)
        clus_ind.pop(second)

        print(clusters)
   
        # creates array of values representing distance between new cluster and old clusters
        combined = []
        for i in range(num_ungrp):
            combined.append(np.maximum(adj[A][i],adj[B][i]))
        combined.pop(first)
        combined.pop(second)
        combined = np.asarray(combined)

        # Deletes the old rows and columns of the recently combined clusters
        adj = np.delete(adj,first, axis=0)
        adj = np.delete(adj,first, axis=1)
        adj = np.delete(adj,second, axis=0)
        adj = np.delete(adj,second, axis=1)
    
        # Takes combined and inserts it as the 0th row and column
        if len(temp) < 3:
            clus_ind.insert(0,temp)
            adj = np.insert(adj, 0, combined,axis=0)
            combined = np.insert(combined,0, np.nan,axis=0)
            adj = np.insert(adj, 0, combined.transpose(),axis=1)
        else:
            clusters.append(temp)
            num_ungrp -= 1
        print(clus_ind)
        print(adj)

        num_ungrp -= 1
    
        if num_ungrp <= 1:
            clustered = True
            if len(clus_ind) != 0: 
                clusters.append(clus_ind[0])
    
    # converts list of list of indices, into list of list of names
    num_clus = len(clusters)

    for i in range(num_clus):
        for j in range(len(clusters[i])):
            clusters[i][j] = riderlist[clusters[i][j]]

    return clusters



def LocGrpMatch(Groups,PickupPoints):
    for Group in Groups:
        xtot = 0
        ytot = 0
        for i in Group:
            xtot += float(i['x'])
            ytot += float(i['y'])
            xcenter = xtot/len(Group)
            ycenter = ytot/len(Group)
                                # The above finds the epicenter of the group
        FinalPickupDisp = [9999999]
        FinalPickupName = ['Filler']
                                # "empty" lists, My strategy here was to find
                                # find the net displacement of each possible
                                # pickup point to the group's epicenter.
                                # I needed both information, the total distance
                                # and the actual name of the pickup point.
                                # My strategy was to find the displacement for
                                # each point, and if that was smaller than the
                                # displacement of any other already in the list
                                # then it will be appended (i.e. the last point
                                # listed will always be the closest)
        for PickupPoint in PickupPoints:
            LocX = float(PickupPoint['x'])
            LocY = float(PickupPoint['y'])
            xdisp = LocX-xcenter
            ydisp = LocY-ycenter
            disp = xdisp**2 + ydisp**2
            if disp < min(FinalPickupDisp):
                FinalPickupDisp.append(disp)
                FinalPickupName.append(PickupPoint)
        Group.append(FinalPickupName[-1])
                                # The closest point is the last item, so I
                                # append that to the group of people. 
                                # since 'name' is a common element to both the
                                # people list and the location list, I print
                                # the 'name' elements of all the items
    return Groups

            # Group is a list of lists (the original group of people from the
            # the clustering algorithm, plus the location)      
