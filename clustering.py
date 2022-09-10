"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import time
import random
import simpleplot
import codeskulptor
import alg_cluster as clust

codeskulptor.set_timeout(2000)


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    leng = len(cluster_list)
    min_list = [(float("inf"), -1, -1)]
    dummy_list = list(cluster_list)
    list_i = [ind_i for ind_i in range(leng - 1)]
    for ind_i in list_i:
        for ind_j in range(ind_i + 1, leng):
            temp = pair_distance(list(dummy_list), ind_i, ind_j)
            if temp[0] < min_list[-1][0]:
                min_list = [temp]
            elif temp[0] == min_list[-1][0]:
                min_list.append(temp)
    random.shuffle(min_list)
    return min_list[0]



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    n_leng = len(cluster_list)
    dummy_list = list(cluster_list)
    if n_leng <= 3:
        return slow_closest_pair(dummy_list)
    else:
        m_leng = int(n_leng / 2)
        left_tup = fast_closest_pair(dummy_list[:m_leng])
        right_tup = fast_closest_pair(dummy_list[m_leng:])
        ret_tup = min(left_tup, (right_tup[0], right_tup[1] + m_leng, right_tup[2] + m_leng))
        mid_value = 0.5 * (dummy_list[m_leng - 1].horiz_center() + dummy_list[m_leng].horiz_center())
        return min(ret_tup, closest_pair_strip(dummy_list, mid_value, ret_tup[0]))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    s_list = []
    for ind_i in range(len(cluster_list)):
        if abs(cluster_list[ind_i].horiz_center() - horiz_center) < half_width:
            s_list.append((cluster_list[ind_i].vert_center(), ind_i))
    s_list.sort()
    k_leng = len(s_list)
    ret_tup = (float("inf"), -1, -1)
    for ind_u in range(k_leng):
        for ind_v in range(ind_u + 1, min(ind_u + 3, k_leng - 1) + 1):
            ret_tup = min(ret_tup, pair_distance([cluster_list[s_list[ind_u][1]], cluster_list[s_list[ind_v][1]]], 0, 1))
    return ret_tup



######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    set_c = list(cluster_list)
    while len(set_c) > num_clusters:
        dummy_list = list(set_c)
        dummy_list.sort(key = lambda cluster: cluster.horiz_center())
        pair = fast_closest_pair(dummy_list)
        dummy_list[pair[1]].merge_clusters(dummy_list[pair[2]])
        set_c.remove(dummy_list[pair[2]])
    return set_c


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    dummy_list = list(cluster_list)
    dummy_list.sort(key = lambda cluster: cluster.total_population(), reverse = True)
    mu_list = [(dummy_list[cluster_ind].horiz_center(), dummy_list[cluster_ind].vert_center()) for cluster_ind in range(num_clusters)]
    while num_iterations > 0:
        num_iterations -= 1
        set_c = [clust.Cluster(set([]), center[0], center[1], 0, 0) for center in mu_list]
        for ind_j in range(len(cluster_list)):
            dist_list = [(((mu_list[index][0] - cluster_list[ind_j].horiz_center()) ** 2 + (mu_list[index][1] - cluster_list[ind_j].vert_center()) ** 2) ** 0.5, index) for index in range(len(mu_list))]
            dist_list.sort()
            set_c[dist_list[0][1]].merge_clusters(cluster_list[ind_j])
        for ind_f in range(len(mu_list)):
            mu_list[ind_f] = (set_c[ind_f].horiz_center(), set_c[ind_f].vert_center())
    return set_c

def gen_center_list(n):
    center_list = []
    n_value = [-1, 1]
    while n > 0:
        n -= 1
        random.shuffle(n_value)
        value = random.random() * n_value[0]
        if value not in center_list:
            center_list.append(value)
    return center_list

def gen_random_clusters(num_clusters):
    x_list = gen_center_list(num_clusters)
    y_list = gen_center_list(num_clusters)
    cluster_list = []
    while num_clusters > 0:
        num_clusters -= 1
        cluster_list.append(clust.Cluster(set([]), x_list[num_clusters], y_list[num_clusters], 0, 0))
    return cluster_list

#obj1 = clust.Cluster(set([0]), 2, 2, 100, 0.3)
#obj2 = clust.Cluster(set([1]), -2, 2, 200, 0.2)
#obj3 = clust.Cluster(set([2]), -2, -2, 400, 0.1)
#obj4 = clust.Cluster(set([3]), 2, -2, 200, 0.1)

#obj5 = clust.Cluster(set([4]), 100, 100, 200, 0.1)
#obj6 = clust.Cluster(set([5]), 100, 60, 200, 0.1)
#obj7 = clust.Cluster(set([6]), 60, 100, 300, 0.1)
#obj8 = clust.Cluster(set([7]), 60, 60, 200, 0.1)

#s = [obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8]

#print kmeans_clustering(s, 4, 1)


# simpleplot.plot_lines('Slow vs Fast Efficiency', 1000, 600, 'No. of Initial Clusters', 'Running Time', [slow_data, fast_data], False, ['slow_closest_pair', 'fast_closest_pair'])
