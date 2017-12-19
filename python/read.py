import re
import numpy as np

class Read:

    def __init__(self, source):
        self.source = source
    
    
    def out(self):

        def is_F(x):
            return x[0] == 'f'

        def is_V(x):
            if x[0] == 'v':
                if x[1] == ' ':
                    return True
                return False
    
        open_file = open(self.source, 'r')
        read_file = open_file.readlines()
        open_file.close
        
        list_F = filter(is_F, read_file)
        list_V = filter(is_V, read_file)

        l_f = []
        for n in list_F:
            l_f.append(list(x - 1 for x in map(int, re.split(r'[/\s]', n)[1:7:2])))
        l_f = np.array(l_f)

        vertex = []
        for n in list_V:
            vertex.append(list(map(float, re.split(r'\s', n)[1:4])))
        vertex = np.array(vertex)

        x= []
        b = [1, 1 ,1] 
        for n in l_f:
            a = []
            for m in n:
                a.append(vertex[m])
            a = np.array(a)
            x.append(np.linalg.solve(a, b))

        return vertex, l_f, x        
    
