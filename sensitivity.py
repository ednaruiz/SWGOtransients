import numpy as np
from scipy.interpolate import RegularGridInterpolator
import pandas as pd



class HAWCSensi:
    '''

    '''
    energy = [0.17782794,0.56234133,1.77827941,5.62341325,17.7827941,56.23413252] #in TeV
    zenith = [0.,10.,20.,30.,40.,50.] #degrees
    time = [np.log10(1.0),np.log10(100.)]
    zenith_name = ["0deg","10deg","20deg","30deg","40deg","50deg"]

    def __init__(self):
        self.one_second = self.read_data("./sensi_1s.txt")
        self.houndred_second = self.read_data("./sensi_100s.txt")
        self.sensi_interpolate = self.build_interpolation_function()



    def read_data(self,file):
        #read the data into a pandas dataframe
        df = pd.read_csv(file, sep = '\t', header = None)
        #assign the name of each column here and add the energy column
        #each column is in erg cm-2 s-1
        df.columns = ["50deg","40deg","30deg","20deg","10deg","0deg"] #it is inverted respect to self.zenith_name, thats why I need to "rewrite" this one here

        df["Energy"] = self.energy #units of TeV
        df["Emin"] = [0.1,0.31622777,1.,3.16227766,10.,31.6227766] #units of TeV
        df["Emax"] = [0.31622777,1.,3.16227766,10.,31.6227766,100.] #units of TeV

        #Since these are values in E2dnde erg cm-2 s-1 and I want dnde
        for icol in ["50deg","40deg","30deg","20deg","10deg","0deg"]:
            #the two 1.602 is to convert the energy from TeV to erg
            df[icol] = df[icol]/ (df["Energy"]*df["Energy"]*1.602*1.602) #now we will have units of erg-1 cm-2 s-1

        df["Edown"] = df["Energy"]-df["Emin"]
        df["Eup"] = df["Emax"]-df["Energy"]

        return df

    def f(self,x,y,z):
        return 0

    def build_interpolation_function(self):

        data = np.zeros((len(self.zenith),len(self.energy),len(self.time)))


        for i in range(len(data)): #i will iterate in zenith
            for j in range(len(data[i])): #j in energy
                for k in range(len(data[i,j])): #k iterates in time
                    if k == 0:
                        a = self.one_second[self.zenith_name[i]][self.one_second["Energy"] == self.energy[j]].values[0]
                    if k == 1:
                        a = self.houndred_second[self.zenith_name[i]][self.houndred_second["Energy"] == self.energy[j]].values[0]

                    data[i,j,k] = a

        return RegularGridInterpolator((self.zenith,self.energy,self.time), data, bounds_error = False, fill_value = None)

    def interpolate(self, z, e, t):
        #since the interpolation does not work given the limiation of the methods here
        #and we are somehow between the background and signal dominated
        #I prefer to use a direct scaling such that the two time points
        #match what we know from the curves
        #For your given zenith
        #I make here a simple linear scaling between (x1,y1) ie sensi at energy E,1second
        #and sensi at (x2,y2) ie sensi at E and time 100 seconds
        y1 = np.log10(self.sensi_interpolate([z,e,self.time[0]])[0])
        y2 =np.log10(self.sensi_interpolate([z,e,self.time[1]])[0])
        x1, x2 = self.time[0],self.time[1]

        slope = (y1-y2)/(x1-x2)

        y = slope* (np.log10(t)-x1) + y1

        return np.power(10,y)

    def sensitivity_vs_time(self,zenith, emin, emax, times):
        #"times" is a numpy array of times
        #eg using tc:
        #ti = 10**np.arange(-1,3.5,.5)
        #tf = 10**np.arange(-.5,4,.5)
        #tc = (tf+ti)/2
        nbins = 30
        e_bins = np.logspace(np.log10(emin),np.log10(emax),nbins) #in TeV

        s_vs_time = []
        for it in times:
            per_time = []
            #here we apply a simple geometrical integration of the curve \int_emin^_emax S(E)xExdE where S(E) is the sensitivity
            for ie in e_bins:
                per_time.append(self.interpolate(zenith,ie,it)*ie*1.6) #convert to erg
            s_vs_time.append(np.sum( np.array(per_time)* (emax-emin)*1.6/float(nbins))    ) #convert to erg

        #will return an array of lenght equalt to the times array
        return s_vs_time
