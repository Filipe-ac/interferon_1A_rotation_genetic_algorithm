import numpy as np
from random import random
import os
from time import time


#function the add a number if a folder already exist
#ex: if 'foo' is in the folder, it will return 'foo_1'
def adjust_name(nome):
    'adiciona numero se ja existe um arquivo com o nome'
    nome1 = nome
    n = 0
    while True:
        if nome1 not in os.listdir():
            break
        else:
            n += 1
            nome1 = nome.split('.')[0]+'_%i'%n
            for i in nome.split('.')[1:]:
                nome1 += '.' + i
    return nome1

def import_data(nome, titulo = False,
                troca_virgula = True,
                convert = True,
                separador = None):
    ''' Old funtion to read a matrix for a file'''
    a = open(nome)
    l = a.readlines()[titulo:]
    a.close()

    if len(l) == 0:
        return ([],[])

    j = 0
    if titulo == False:
        
        while True:
            coluna = l[j].strip('\n').strip('\t').split(separador)
            try:
                eval(coluna[0])
                break
            except:
                j += 1

    mat = []
    colunas = len(l[j].strip('\n').strip('\t').split(separador))
    for i in range(colunas):
        mat.append([])
        
    #x,y,extras = [],[],[]
    for i in l[j:]:
        i = i.strip('\n').strip('\t').split(separador)
            
        try:
            for n in range(len(i)):
                if convert == True:
                    if troca_virgula == True and 'ne(' not in i[n]:
                        mat[n].append(eval(i[n].replace(',','.')))
                    else:
                        mat[n].append(eval(i[n]))
                else:
                    mat[n].append(i[n])
        except:
            return mat


    return mat

def save_data(nome,*args):
    '''Function to save data to a given file'''
    arq = open(nome,'w')
    s = ''
    tamanho = len(args[0])
    for p in range(tamanho):
        
        for i in args:
            
            s += str(i[p]) + '\t'
        s += '\n'
    arq.write(s)
    arq.close()

class rotation:
    '''Class to implement the genetic algorithm for optimize
    the rotation of interferon beta-1a medication'''

    
    def __init__(self,n_pop = 100,
                 n_worst = 10,
                 n_best = 50,
                 p_mutation = 0.01,
                 p_couple = 0.5,
                 n_points = 100,
                 points = 'circle',
                 plots = True,
                 verbose = False,
                 algorithm = 'minimum',
                 name = 'interferon_rotation',
                 points_to_exclude = []):
            

        #algorithm:
        
        #minimum = normal case
        #rebif = rebif problemw

        self.verbose = verbose
        self.random = random
        self.n_points = n_points
        self.n_pop = n_pop
        self.n_worst = n_worst
        self.n_best = n_best
        self.p_couple = p_couple
        self.p_mutation = p_mutation
        self.n = np.arange(n_points)
        self.algorithm = algorithm
        self.plots = plots
        

        self.lista = []

        self.lista_posicoes = [i for i in range(1,self.n_points-1)]
        self.distancia_no_tempo = []


        self.tempo = 0

        if points in ['sphere','sphere','circle']:
            #built in geometries
            self.cria_points(points)

        else:
            #load from file]
            arq = open(points);m = arq.readlines();arq.close()
            m = [i.strip('\n').strip().split('\t') for i in m]
            self.points = np.array(m).astype('float')

            #exclude points
            if len(points_to_exclude) != 0:
                self.points = np.delete(self.points,np.array(points_to_exclude)-1,0)
            
            self.n_points = self.points.shape[0]
            
            
        self.pasta_atual = os.getcwd()
        name = adjust_name(name)
        self.pasta = self.pasta_atual + '/' + name
            
        os.mkdir(name)
        os.chdir(self.pasta)
            
        
        self.cria_individuo_monte_carlo()
        self.arq_distancias = open('distancias','a')
        self.ordena_lista()
        a = open('points','w')
        a.write(str(self.points))
        a.close()


        self.arq_distancias = open('distancias','a')
        

        self.melhor = self.lista[0]
        self.menor_distancia = self.lista_distancias[0]



    def cria_points(self,points):
        #if it is a list
        
        if type(points) != str:
            self.points = points
            
        if points == 'sphere': #esfera
            theta = np.random.random(self.n_points)*2*np.pi
            phi = np.random.random(self.n_points)*np.pi
            self.points = np.array([np.cos(theta)*np.sin(phi),
                        np.sin(theta)*np.sin(phi),
                        np.cos(phi)]).transpose()

            self.theta = theta; self.phi = phi
            
        elif points == 'spiral': #spiral
            #theta = np.linspace(0,np.pi,self.n_points)
            phi = np.linspace(0,8*np.pi,self.n_points)
            z = np.linspace(0,9,self.n_points)
            self.points = np.array([np.cos(phi),
                                     np.sin(phi),
                                     z]).transpose()

        elif points == 'circle':
            phi = np.linspace(0,2*np.pi,self.n_points+1)
            z = np.zeros(self.n_points)
            self.points = np.array([np.cos(phi[:-1]),
                                     np.sin(phi[:-1]),
                                     z]).transpose()
            
    def plot_points(self,points = None):
        
        if type(points) == type(None):
            points = self.points

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x,y,z = points.transpose()
        ax.plot(x,y,z,'o')
        ax.plot([points[0][0]],[points[0][1]],[points[0][2]],
               'o', color = 'black')
        
        return fig,ax
                
            

    def cria_individuo_monte_carlo(self):

        #create the necessary arrays of random numbers
        l2 = np.random.random([self.n_pop-len(self.lista),self.n_points-1])
        
        #use the index of sorted list as the new solution
        l2 = l2.argsort(); l2 += 1
        #insert the incial and final position
        l2 = np.insert(l2,0,0,1); l2 = np.insert(l2,l2.shape[1],0,1)
  
        self.lista += l2.tolist()

    def ordena_lista(self):

        #separate the position coordinates
        x,y,z = self.points.transpose()

        #create a matrix with the organized positions for each
        #solution

        mpos = np.array(self.lista)

        x = x[mpos]; y = y[mpos]; z = z[mpos]

        if self.algorithm == 'rebif':

            tau = 6
            exp = lambda x,t: x*np.exp(-t/tau)
            
            #create a matrix with the euclidian distancies between all coordinates

            distancias = np.sqrt((x-np.append(x[:,1:],x[:,:1],axis = 1))**2 + \
                          (y-np.append(y[:,1:],y[:,:1],axis = 1))**2 + \
                          (z-np.append(z[:,1:],z[:,:1],axis = 1))**2)

            distancias2 = exp(np.sqrt((x-np.append(x[:,2:],x[:,:2],axis = 1))**2 + \
                          (y-np.append(y[:,2:],y[:,:2],axis = 1))**2 + \
                          (z-np.append(z[:,2:],z[:,:2],axis = 1))**2),1)

            distancias3 = exp(np.sqrt((x-np.append(x[:,3:],x[:,:3],axis = 1))**2 + \
                          (y-np.append(y[:,3:],y[:,:3],axis = 1))**2 + \
                          (z-np.append(z[:,3:],z[:,:3],axis = 1))**2),5)

            #sum distancie between last two neighbors

            distancias = distancias + distancias2 + distancias3


            sums = np.sum(distancias,axis = 1)
        
            distancias = sums**(-1)
            

        else:
            
            #create a matrix with the euclidian distancies between all coordinates
            distancias = np.sqrt((x-np.append(x[:,1:],x[:,:1],axis = 1))**2 + \
                          (y-np.append(y[:,1:],y[:,:1],axis = 1))**2 + \
                          (z-np.append(z[:,1:],z[:,:1],axis = 1))**2)

            #sum the total distances
            distancias = np.sum(distancias,axis = 1)   

        
        #reorganize the list of solutions with the best solutions
        positions = distancias.argsort()
        self.lista = mpos[positions].tolist()
        distancias = distancias[positions]
        self.lista_distancias = distancias
        
        if 'menor_distancia' in self.__dict__ and distancias[0] < self.menor_distancia:
            self.menor_distancia = distancias[0]
            self.melhor = self.lista[0].copy()
            self.mudou_melhor = True
        else:
            self.mudou_melhor = False
            
        
        self.salva(self.lista,self.lista_distancias,self.mudou_melhor,self.tempo,self.plots)
        

        self.distancia_no_tempo.append(distancias[0])
            
    def salva(self,lista,distancias,mudou_melhor,tempo, plots):

        self.arq_distancias.write('%i\t%s\n'%(tempo,distancias[0]))
        self.arq_distancias.flush()
        
        arq = open('lista','w')
        arq.write(str(lista))
        arq.close()

        save_data('melhor',np.array(lista[0])+1)

        self.distancia_no_tempo.append(distancias[0])
        self.arq_distancias.write('%i\t%s\n'%(tempo,distancias[0]))
        self.arq_distancias.flush()

        if mudou_melhor == True and plots == True:
            fig,ax = self.plot_points(points = self.points)
            fig,ax = self.plot_melhor(l = self.melhor)
            #print(p)
            ax.set_title('%i'%self.tempo)
            fig.savefig('_tmp%05d'%self.tempo)
            #print(p)

    def plot_melhor(self,l = None):

        fig,ax = self.plot_points()
        pos = 0
        if l == None:
            l = self.melhor
        while pos < len(l)-1:
            c1 = l[pos]
            c2 = l[pos+1]
            #print(p)
            ax.plot([self.points[c1][0],self.points[c2][0]],
                   [self.points[c1][1],self.points[c2][1]],
                      [self.points[c1][2],self.points[c2][2]])
            pos += 1

        return fig,ax


    
    def mutacao(self):

        #create a list of random numbers and decide which one will suffer a mutation
        lr = np.random.random(len(self.lista))
        bm = lr <= self.p_mutation
        self.lista = np.array(self.lista)
        #matriz with the solutions signed to suffer a mutation
        mutations = self.lista[np.where(bm == 1)[0]] #sum +1 to avoid mutate the best solution
        
        unchanged = self.lista[np.where(bm == 0)[0]]

        #separate in change 2 types of mutations
        lr = np.random.random(mutations.shape[0])
        bm = lr <= 0.5

        change = mutations[np.where(bm == 1)]
        invert = mutations[np.where(bm == 0)]

        self.change = change; self.invert = invert

        #create lists with random positions (from 1 to the -2 element, in order to dont change the first point)
        p1,p2 = (np.random.random([2,change.shape[0]])*(len(self.lista_posicoes))).astype('int') + 1
        positions = np.arange(change.shape[0])
        
        #change
        
        #get the values as copies and substitute in their positions
        values_p1 = change[positions,p1]
        values_p2 = change[positions,p2]
        change[positions,p1] = values_p1; change[positions,p2] = values_p2

        self.unchanged = unchanged
        #invert
         #i just realise that it is not necessary to create a random position for each solution,
         #since everthing is random so. I will keep the change option that way, because i learn some numpy stuff
         #and wante to keep that as a reference. Plus, i dont think it will slow the performance too mutch.

        
        invert[:,p1[0]:p2[0]] = np.flip(invert[:,p1[0]:p2[0]], axis = 1)

        #recriate the list
        lista = np.insert(unchanged,0,change,0)
        lista = np.insert(lista,0,invert,0)



        self.lista = lista.tolist()
        return

        
    def cruzamento(self):
        self.lista = np.array(self.lista)

        #decide if it will couple
        mask = np.random.random(len(self.lista)) <= self.p_couple
        partner1 = np.where(mask == 1)[0]

        #list of partners
        partner2 = np.floor(self.n_pop*np.random.random(partner1.shape[0])).astype('int64')

        #points to exchange

        p1 = int(1 + random()*(self.n_points-1))
        p2 = int(1 + random()*(self.n_points-1))


        #change the atributes between these two points among the two solutions
        for p in np.arange(min(p1,p2),max(p1,p2)+1):

            self.listac = self.lista.copy()
        
            v1 = self.lista[partner1,p]
            v2 = self.lista[partner2,p]
            
            #l1 = v1.reshape((v1.shape[0],1))

            l2 = v2.reshape((v2.shape[0],1))
            p1o = np.argwhere(self.lista[partner1]==l2).transpose()[1]

            
            
            
            #p2o = np.argwhere(self.lista[partner2]==l1).transpose()[1]

            self.lista[partner1,p] = v2
            self.lista[partner1,p1o] = v1
            

        self.lista = self.lista.tolist()  
    def iteration(self, numero = 100):


        if self.tempo == 0 and self.plots == True:
            fig,ax = self.plot_points()
            fig,ax = self.plot_melhor()           
            ax.set_title('%i'%self.tempo)
            fig.savefig('_tmp%05d'%0)
        
        for num in range(numero):
            
            self.tempo += 1
            melhor = self.melhor.copy()

            self.cruzamento()
            
            self.mutacao()
            self.lista[-1] = melhor
            
            self.ordena_lista()

            lista_nova = self.lista[:self.n_best]
            lista_nova += self.lista[self.n_pop - self.n_worst:]
            self.lista = lista_nova.copy()
            self.cria_individuo_monte_carlo()

            

            self.ordena_lista()
            
            #print(time()-t,'parte 2')
            
            if self.verbose == True:
                print(numero - num,self.tempo)
            else:
                if (self.tempo)%1000 == 0:
                    print(self.tempo,self.tempo,'best = ',self.lista_distancias[0])
     

    def plt(self):
        try:
            fig,ax = plt.subplots()
            l = import_data('distancias')[0]
            ax.plot([i for i in range(len(l))],
                   l)
            ax.set_ylabel('Generations'),
            ax.set_xlabel('Objective Function')
            fig.savefig('dxg')
            fig.show()

            return fig,ax
        except:
            pass

    def test_circle(self):

        x,y,z = self.points.transpose()

        distancias = np.sqrt((x-np.append(x[1:],x[:1]))**2 + \
                          (y-np.append(y[1:],y[:1]))**2 + \
                          (z-np.append(z[1:],z[:1]))**2)

            #sum the total distances
        distancias = np.sum(distancias)

        print(distancias)
        
        t = time()
        self.iteration(1)
        while abs(self.menor_distancia-2*np.pi) > 0.1:
            self.iteration(1)

            if self.tempo >= 10000000:
                return 'Not converge'
        return time()-t

    def test_temp(self,tempo = 10):
        t = time()
        while time()-t < 10:
            self.iteration(1)
        return self.menor_distancia

    def evaluete_of(self,genes):
        'Evaluate the objective function for a given list of genes'
        
        #separate the position coordinates
        x,y,z = self.points.transpose()

        #create a matrix with the organized positions for each
        #solution

        mpos = np.array(genes)-1

        x = x[mpos]; y = y[mpos]; z = z[mpos]

            
        
        tau = 6
        exp = lambda x,t: x*np.exp(-t/tau)
        
        #create a matrix with the euclidian distancies between all coordinates

        distancias = np.sqrt((x-np.append(x[1:],x[:1]))**2 + \
                      (y-np.append(y[1:],y[:1]))**2 + \
                      (z-np.append(z[1:],z[:1]))**2)

        distancias2 = exp(np.sqrt((x-np.append(x[2:],x[:2]))**2 + \
                      (y-np.append(y[2:],y[:2]))**2 + \
                      (z-np.append(z[2:],z[:2]))**2),1)

        distancias3 = exp(np.sqrt((x-np.append(x[3:],x[:3]))**2 + \
                      (y-np.append(y[3:],y[:3]))**2 + \
                      (z-np.append(z[3:],z[:3]))**2),5)

        #sum distancie between last two neighbors

        distancias = distancias + distancias2 + distancias3


        sums = np.sum(distancias)
    
        distancias = sums**(-1)

        return distancias

    
            

def distancia(n):
    from funcoes import cosg,sing
    delta_theta = 360/n
    dist = 0
    for i in range(n):
        dist += ((cosg((n+1)*delta_theta) - cosg(n*delta_theta))**2 + \
                 (sing((n+1)*delta_theta) - sing(n*delta_theta))**2)**0.5
    return dist

def test_circle():
             
    a = rotation(n_pop = 100, n_worst = 10, n_best = 20,
                 p_mutation = 0.7, p_couple = 0.7,
                 n_points = 30,points = 'circle',plots = True,
                 verbose = False,algorithm = 'rebif',name = 'test_circle',
                 points_to_exclude = [])
    a.iteration(1000000)

def compara_manual():
    lista_manual = [5,26,3,21,1,8,23,7,20,18,10,22,30,25,9,4,2,6,19,17,11,24]
    
    para_excluir = []
    for i in range(1,31):
        if i not in lista_manual:
            para_excluir.append(i)
            
    a = rotation(n_pop = 100, n_worst = 10, n_best = 20,
                 p_mutation = 0.7, p_couple = 0.7,
                 n_points = 30,points = 'circle',plots = True,
                 verbose = False,algorithm = 'rebif',name = 'compara_com_manual',
                 points_to_exclude = para_excluir)
    a.iteration(100000)

    
    print(a.menor_distancia,a.evaluete_of(lista_manual))
    
    
import argparse
p = argparse.ArgumentParser()
p.add_argument('-b',help = 'fraction of best individuals to keep',default = 20,type = int)
p.add_argument('-w',help = 'fraction of worst individuals to keep',default = 10, type = int)
p.add_argument('-e',help = 'points to exclude',default = '',type = str)
p.add_argument('-n',help = 'folder name',default = 'interferon_rotation',type = str)
p.add_argument('-m',help = 'mutation probabilitie',default = 0.7,type = float)
p.add_argument('-c',help = 'couple probabilitie',default = 0.7,type = float)
p.add_argument('-p',help = 'points coordinates - see documantation',default = 'coordinates',type = str)
p.add_argument('-a',help = 'algorithm type - see documantation',default = 'rebif',type = str)
p.add_argument('-v',help = 'verbose (0 or 1)',default = 0,type = bool)
p.add_argument('-plots',help = 'Generate plots',default = 0,type = bool)
p.add_argument('-np',help = 'number of points - see documantation',default = 30,type = int)
p.add_argument('-npop',help = 'population number',default = 100,type = int)
p.add_argument('-i',help = 'number of iterations',default = 50000,type = int)

args = p.parse_args()

if args.e == '':
    args.e = []
else:
    args.e = args.e.strip('[').strip(']')
    if ',' in args.e:
        args.e = [int(i) for i in args.e.split(',')]
    else:
        args.e = [int(i) for i in args.e.split()]

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
except:
    args.plots = 0

a = rotation(n_pop = args.npop, n_worst = args.w, n_best = args.b,
             p_mutation = args.m, p_couple = args.c,
             n_points = args.np,points = args.p,plots = args.plots,
             verbose = args.v,algorithm = args.a,name = args.n,
             points_to_exclude = args.e)

a.iteration(args.i)
