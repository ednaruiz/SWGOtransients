import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def read_xrt_lc(file, verbose = False):
    file = open(file,"r")

    Time = []
    Time_d = []
    Time_u = []

    Flux = []
    Flux_u = []
    Flux_d = []
    Index = []
    Index_u = []
    Index_d = []

    read_xrtgamma = False
    read_xrtflux = False
    read_batflux = False
    read_batgamma = False

    for line in file:

        if line == "READ TERR 1 2\n" or line == "NO NO NO NO NO NO\n":
            if (verbose) : print("Skipping "+line)
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False


        elif (read_xrtgamma):
            vals = [float(vv) for vv in line.split()]
            Time.append(vals[0])
            Time_u.append(vals[1])
            Time_d.append(abs(vals[2]))
            Index.append(vals[3])
            Index_u.append(vals[4])
            Index_d.append(abs(vals[5]))

        elif (read_xrtflux):
            vals = [float(vv) for vv in line.split()]
            Flux.append(vals[3])
            Flux_u.append(vals[4])
            Flux_d.append(abs(vals[5]))


        elif line == "! xrtpcgamma\n" or line == "! xrtwtslewgamma\n" or line == "! xrtwtgamma\n" or line == "! xrtpcgamma\n":
            if (verbose) : print("Reading XRT-PC indexes")
            read_xrtgamma = True
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False

        elif line == "! batSNR4flux\n" or line == "! batSNR5gamma\n":
            if (verbose) : print("Skipping BAT flux")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False

        elif line == "! batSNR4gamma\n" or line == "! batSNR5flux\n":
            if (verbose) : print("Skipping BAT gamma")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False

        elif line == "! xrtpcflux_nosys\n" or line == "! xrtwtslewflux\n" or line == "! xrtwtflux\n" or line == "! xrtpcflux\n":
            if (verbose) : print("Now reading XRT flux")
            read_xrtgamma = False
            read_xrtflux = True
            read_batflux = False
            read_batgamma = False

    if (verbose) : print(" ")
    if (verbose) : print("Done!")
    df = pd.DataFrame()

    df["Time"] = Time
    df["Time_u"] = Time_u
    df["Time_d"] = Time_d
    df["Flux"] = Flux
    df["Flux_u"] = Flux_u
    df["Flux_d"] = Flux_d
    df["Index"] = Index
    df["Index_u"] = Index_u
    df["Index_d"] = Index_d

    return df


def read_bat_lc(file, verbose = False):
    file = open(file,"r")

    Time = []
    Time_d = []
    Time_u = []

    Flux = []
    Flux_u = []
    Flux_d = []
    Index = []
    Index_u = []
    Index_d = []

    read_xrtgamma = False
    read_xrtflux = False
    read_batflux = False
    read_batgamma = False

    for line in file:

        if line == "READ TERR 1 2\n" or line == "NO NO NO NO NO NO\n":
            if (verbose) : print("Skipping "+line)
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False


        elif (read_batgamma):
            vals = [float(vv) for vv in line.split()]
            Time.append(vals[0])
            Time_u.append(vals[1])
            Time_d.append(abs(vals[2]))
            Index.append(vals[3])
            Index_u.append(vals[4])
            Index_d.append(abs(vals[5]))

        elif (read_batflux):
            vals = [float(vv) for vv in line.split()]
            Flux.append(vals[3])
            Flux_u.append(vals[4])
            Flux_d.append(abs(vals[5]))


        elif line == "! xrtpcgamma\n" or line == "! xrtwtslewgamma\n" or line == "! xrtwtgamma\n" or line == "! xrtpcgamma\n":
            if (verbose) : print("Skipping XRT-PC indexes")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False

        elif line == "! batSNR6flux\n" or line == "! batSNR7flux\n" or line == "! batSNR4flux\n" or line == "! batSNR5flux\n" or line == "! batTIMEDEL0.064flux\n" or line == "! allbatTIMEDEL0.064flux\n":
            if (verbose) : print("Reading BAT flux")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = True
            read_batgamma = False

        elif line == "! batSNR6gamma\n" or line == "! batSNR7gamma\n" or line == "! batSNR4gamma\n" or line == "! batSNR5gamma\n" or line == "! batTIMEDEL0.064gamma\n" or line == "! allbatTIMEDEL0.064gamma\n":
            if (verbose) : print("Reading BAT gamma")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = True

        elif line == "! xrtpcflux_nosys\n" or line == "! xrtwtslewflux\n" or line == "! xrtwtflux\n" or  line == "! xrtpcflux\n":
            if (verbose) : print("Skipping reading XRT flux")
            read_xrtgamma = False
            read_xrtflux = False
            read_batflux = False
            read_batgamma = False
    if (verbose) : print(" ")
    if (verbose) : print("Done!")
    df = pd.DataFrame()

    df["Time"] = Time
    df["Time_u"] = Time_u
    df["Time_d"] = Time_d
    df["Flux"] = Flux
    df["Flux_u"] = Flux_u
    df["Flux_d"] = Flux_d
    df["Index"] = Index
    df["Index_u"] = Index_u
    df["Index_d"] = Index_d

    return df


def plot_xrt(df, axes, **style):

    if axes == []:
        fig = plt.figure(figsize=(5,4.5))
        ax1 = fig.add_axes((.15,.3,.8,.5))

        ax1.set_ylabel(r'Energy flux (erg cm$^{-2}$ s$^{-1}$)', fontsize = 8)

        ax1.tick_params('both',which = 'both',direction = 'in',bottom = True, top =True, right = True, left = True,grid_linestyle = '--', grid_alpha = 0.5)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        locmaj = mpl.ticker.LogLocator(base=10,  numticks=11)
        ax1.yaxis.set_major_locator(locmaj)
        locmin = mpl.ticker.LogLocator(base=10.0, subs=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
                                       numticks=100)
        ax1.yaxis.set_minor_locator(locmin)
        ax1.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        ax1.grid()

        ax2 = fig.add_axes((.15,.15,.8,.15))


        ax2.set_ylabel("Photon\nindex", labelpad = 10, fontsize = 8)
        ax2.set_xlabel(r"Time since T$_0$ trigger (s)", fontsize = 8)
        ax2.tick_params('both',which = 'both',direction = 'in',bottom = True, top =True,right = True, left = True, grid_linestyle = '--')
        ax2.set_xscale('log')

        ax2.grid()

        ax1.errorbar(df["Time"], df["Flux"], xerr = df["Time_u"], yerr = df["Flux_u"], **style)
        ax2.errorbar(x = df['Time'], y = df['Index'], xerr = df['Time_u'], yerr = df["Index_u"], **style)
        #ax1.errorbar(df["Time"], df["Flux"], xerr = df["Time_u"], **style)
        #ax2.errorbar(x = df['Time'], y = df['Index'], xerr = df['Time_u'], **style)


    else:
        print("axes provided")
        ax1 = axes[0]
        ax2 = axes[1]

        #ax1.errorbar(df["Time"], df["Flux"], xerr = df["Time_u"], **style)
        #ax2.errorbar(x = df['Time'], y = df['Index'], xerr = df['Time_u'], **style)

        ax1.errorbar(df["Time"], df["Flux"], xerr = df["Time_u"], yerr = df["Flux_u"], **style)
        ax2.errorbar(x = df['Time'], y = df['Index'], xerr = df['Time_u'], yerr = df["Index_u"], **style)

    return ax1,ax2
