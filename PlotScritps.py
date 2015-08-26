# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:38:51 2015

common types of plots that require specialized construction

@author: jonesad
"""


def spectra(lnpaEnergies, lsSpecies, llsJPi, sPath='', fSparse=0.05, nSpc=20):
    '''
        Input is a list of the numpy arrays of energies and a list of names for
        the species, and a list of the spins and parities for each level.
        Output is a spectra plot where all the species are labeled on the
        xaxis. If a path is given save the plot there otherwise show the plot.
    '''
    if len(lsSpecies) != len(lnpaEnergies):
        print ('Error: ', len(lsSpecies), 'labels found. For',
               len(lnpaEnergies), 'spectra.')
        return []
    if fSparse < 0 or fSparse > 0.5:
        print ('Error fSparse is:', fSparse,
               'but thevalid range is 0<fSparse<0.5')
    from matplotlib import pyplot as plt
    import numpy as np
    fig, ax = plt.subplots()
    ax.set_xlim([0, len(lsSpecies) + fSparse])
    tickray = np.array(range(len(lsSpecies))) + 0.5
    ax.xaxis.set_ticks(tickray)
    Emax = ''
    Emin = ''
    for nIdx, npaEnergies in enumerate(lnpaEnergies):
        if Emax != '':
            temp = float(np.max(npaEnergies))
            if temp > Emax:
                Emax = temp
        else:
            Emax = np.max(npaEnergies)
        if Emin != '':
            temp = np.min(npaEnergies)
            if temp < Emin:
                Emin = temp
        else:
            Emin = np.min(npaEnergies)
    Erng = Emax - Emin
    ax.set_ylim([Emin - fSparse * Erng, Emax + fSparse * Erng])
    ax.set_xticklabels(lsSpecies)
    for nIdx, npaEnergies in enumerate(lnpaEnergies):
        rhs = nIdx + (1 - fSparse)
        targets = [(rhs, y) for y in npaEnergies]
        stack = ax.transData.transform(targets)
        labels = llsJPi[nIdx]
        npaEnergies.sort()
        stack, labels = stackLabels(stack, labels, nSpc)
        stack = [(x + nSpc, y) for (x, y) in stack]
        arrowprops = dict(arrowstyle="-", connectionstyle="arc3", color='k')
        for nlIdx, fE in enumerate(npaEnergies):
            ax.plot([nIdx + fSparse, nIdx + (1 - fSparse)], [fE, fE],
                    color='b')
            ax.annotate(labels[nlIdx], xy=(nIdx + (1 - fSparse), fE),
                        textcoords='figure pixels', xytext=stack[nlIdx],
                        arrowprops=arrowprops)
    if sPath != '':
        plt.savefig(sPath)
    else:
        plt.show()


def stackLabels(stack, labels, nSpc):
    import numpy
    stack = numpy.array(stack)
    newLab = [l for (s, l) in sorted(zip(stack[:, 1], labels))]
    newstack = numpy.sort(stack, axis=0)
    for nJIdx in range(len(stack)):
        if nJIdx > 0 and newstack[nJIdx][1] - newstack[nJIdx - 1][1] < nSpc:
            newstack[nJIdx][1] = newstack[nJIdx - 1][1] + nSpc
    return newstack, newLab

import numpy as np
en = []
lab = []
jpi = []

for nidx in range(4):
    en.append(np.random.uniform(-10, 0, 4))
    lab.append('$^{' + str(16 + nidx) + '}$O')
    jpi.append([str(num)+'$^+$' for num in range(4)])
    sparit = []
#fname = 'test'
spectra(en, lab, jpi, '', fSparse=0.2)
