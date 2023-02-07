# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 08:37:54 2022

@author: aldis
"""

class Node:
    def __init__(self, content, code):
        """
        initialises Node object instance

        Parameters
        ----------
        content : any type
            content that the node represents.
        code : int
            to help with saving a node-space (nodes and their neighbors) to a file and
            retrieving it.

        Returns
        -------
        None.

        """
        self.node_code = code
        self.content = content
        self.neighbors = []
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        
class Point:
    def __init__(self, content):
        """
        initiates an instance of Point object.

        Parameters
        ----------
        content : list
            3d cartesian coordinates.

        Returns
        -------
        None.

        """
        self.x = content[0]
        self.y = content[1]
        self.z = content[2]
    
    def distance(self, point_2):
        """
        distance between points

        Parameters
        ----------
        point_2 : Point
            The point to which distance is to be foud.

        Returns
        -------
        float
        Distance between the 2 points.

        """
        x1, y1, z1 = self.x, self.y, self.z
        x2, y2, z2 = point_2.x, point_2.y, point_2.x
        
        return((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5
    
    def closest(self, points):
        """
        returns the point belonging to list points that is closest to self

        Parameters
        ----------
        points : list 
            contains objects of type Point.

        Returns
        -------
        Point
            the point closest to self.

        """
        distances = []
        for point in points:
            distances.append(self.distance(point))
        return points[distances.index(min(distances))]
    
    def __str__(self):
        return "(" + str(self.x) +  "," + str(self.y) +  "," +  str(self.z) + ")"
        


class Space_3d:
    """Representation of a finite 3D space"""
    def __init__(self, max_x, max_y, max_z, min_x = 0, min_y = 0, min_z = 0):
        """
        

        Parameters
        ----------
        max_x : int
            defines the upper limit of x axis.
        max_y : int
            defines the upper limit of y axis.
        max_z : int
            defines the upper limit of z axis.
        min_x : int, optional
            defines the lower limit of x axis. The default is 0.
        min_y : int, optional
            defines the lower limit of y axis. The default is 0.
        min_z : int, optional
            defines the lower limit of z axis. The default is 0.

        Returns
        -------
        None.

        """
        self.x_list = list(range(min_x, max_x+1))
        self.y_list = list(range(min_y, max_y+1))
        self.z_list = list(range(min_z, max_z+1))    
        
        for i in [self.x_list, self.y_list, self.z_list]:
            if not i:
                self.x_list, self.y_list, self.z_list= [], [], []
                break
        
    def get_octants(self, point):
        """
        Divies self into 8 octant spaces about point

        Parameters
        ----------
        point : Point
            The octants are centered st this point.

        Returns
        -------
        octants : list
            list of spaces that each represent one octant.

        """
        index_x = self.x_list.index(point.x)
        index_y = self.y_list.index(point.y)
        index_z = self.z_list.index(point.z)
        
        octants = []
        
        for i in [self.x_list[0:index_x], self.x_list[index_x:]]:
            for j in [self.y_list[0:index_y], self.y_list[index_y:]]:
                for k in [self.z_list[0:index_z], self.z_list[index_z:]]:
                    octants.append(Space_3d(max(i), max(j), max(k), min(i), min(j), min(k)))
        return octants
    
    def is_empty(self):
        """
        

        Returns
        -------
        bool
            True if space is null, else False.

        """
        if self.x_list == []:
            return True
        return False
    
    def is_point_in_space(self, point):
        """
        To check if point lies in the space

        Parameters
        ----------
        point : Point
            point to check.

        Returns
        -------
        bool
            True if point is in space, else False.

        """
        if not point.x in self.x_list:
            return False
        if not point.y in self.y_list:
            return False
        if not point.z in self.z_list:
            return False
        return True
        
    def points_in_space(self, points):
        """
        returns list of point objects in the list points that lie in the space. 

        Parameters
        ----------
        points : list
            list of Point objects.

        Returns
        -------
        result : list
            list of Point objects.

        """
        result = []
        for point in points:
            if self.is_point_in_space(point):
                result.append(point)
                
        return result
    
    def __str__(self):
        return "X: " + str(self.x_list) + "Y: " + str(self.y_list) + "Z: " + str(self.z_list)

class Search_3d:
    def __init__(self, content, max_x, max_y, max_z, min_x = 0, min_y = 0, min_z = 0):
        """
        

        Parameters
        ----------
        content : list
            list of tup/list of length three, the cartesian coordinates of set of points 
            to be searched.
        max_x : int
            defines the upper limit of x axis.
        max_y : int
            defines the upper limit of y axis.
        max_z : int
            defines the upper limit of z axis.
        min_x : int, optional
            defines the lower limit of x axis. The default is 0.
        min_y : int, optional
            defines the lower limit of y axis. The default is 0.
        min_z : int, optional
            defines the lower limit of z axis. The default is 0.

        Returns
        -------
        None.

        """
        self.space = Space_3d(max_x, max_y, max_z, min_x, min_y, min_z)
        
        self.content = []
        for i in content:
            self.content.append(Point(content))
    
    
    
    def init_node_space(self):
        """
        intialises node space from the content

        Returns
        -------
        None.

        """
        try:
            self.nodes
        except:
            self.nodes = []
            for i in self.content:
                self.nodes.append(Node(i, len(self.nodes)))
            
            for node in self.nodes:
                for octant in self.space.get_octants(node.content):
                    node.add_neighbor(node.content.closest(octant.points_in_space(self.content)))
        
        return

    def search_nearest_neighbor(self, goal, start = None):
        """
        greedy searches the node space to find the closest existing node to goal node.

        Parameters
        ----------
        goal : Node
            goal Node to which the nearest existing node is to be found.
        start : Node, optional
            The node to start searching from. The default is None.

        Returns
        -------
        Node
            Existing Node that is closest to goal Node.

        """
        
        if not start:
            start = self.nodes[0]
        
        if start == goal:
            return start
        
        elif start == goal.closest([start].join(start.neighbors)):
            return start
        
        else:
            return self.search_nearest_neighbor(goal, goal.closest(start.neighbors.append(start)))
    
    
    
                
            
        
    

    
    
    