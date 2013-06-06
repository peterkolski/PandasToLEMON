import pandas as pd
import numpy as np
from pandas import DataFrame
import fileinput
import networkx as nx
import os


# ========================================================
# ========================================================

def readLGF_Nodes_DF( source ):
    mInFile = open( source ,mode='r')
    fileString = mInFile.read()
    mInFile.close()
    if '@arcs' in fileString:
        endPos = '@arcs'
    elif '@edges' in fileString:
        endPos = '@edges'
    else:
        print('No keyword \'@arcs\' or \'@edges\' found\n Wrong file format')
        return
    strDat = fileString[fileString.find('@nodes')+7:fileString.find(endPos)]
    mOutFile = open('tmp.txt',mode='w')
    mOutFile.write(strDat)
    mOutFile.close()
    mFrame = pd.read_table('tmp.txt')
    os.remove('tmp.txt')
    mFrame = mFrame.dropna( axis=1, how='all')
    return mFrame

# ========================================================
# ========================================================

def readLGF_EdgeArc_DF( source ):
    mInFile = open( source ,mode='r')
    fileString = mInFile.read()
    mInFile.close()
    if '@arcs' in fileString:
        initKey = '@arcs'
        initPos = 6
    elif '@edges' in fileString:
        initKey = '@edges'
        initPos = 7
    else:
        print('No keyword \'@arcs\' or \'@edges\' found\n Wrong file format')
        return
    strDat = fileString[fileString.find(initKey)+initPos:]
    mOutFile = open('tmp.txt',mode='w')
    mOutFile.write(strDat)
    mOutFile.close()
    mFrame = pd.read_table('tmp.txt')
    os.remove('tmp.txt')
    mFrame = mFrame.dropna( axis=1, how='all')
    return mFrame

# ========================================================
# ========================================================

def readLGF_Network( source ):
    mInFile = open( source ,mode='r')
    fileString = mInFile.read()
    mInFile.close()
    if '@arcs' in fileString:
        initKey = '@arcs'
        initPos = 6
    elif '@edges' in fileString:
        initKey = '@edges'
        initPos = 7
    else:
        print('No keyword \'@arcs\' or \'@edges\' found\n Wrong file format')
        return
    strDat = fileString[fileString.find(initKey)+initPos:]
    mOutFile = open('tmp.txt',mode='w')
    mOutFile.write(strDat)
    mOutFile.close()
    mOutFile = open('tmp2.txt',mode='w')
    for line in fileinput.input('tmp.txt'):
        if not fileinput.isfirstline():
            mOutFile.write(line)
    mOutFile.close()
    os.remove('tmp.txt')
    g = nx.read_edgelist('tmp2.txt', nodetype=int, edgetype=int, data=False )
    os.remove('tmp2.txt')
    return g

# ========================================================
# ========================================================

def DF_merge_NXfunc( df, func, colName ):
    mDF = pd.DataFrame.from_dict( func, orient='index')
    mDF.columns = [str(colName)]
    mDF = pd.merge( df , mDF, right_index=True, left_index=True)
    return mDF

# ========================================================
# ========================================================

def writeDF_LGF( fileName, NodesDF, ArcsDF ):
    file = open( fileName,'w')
    file.write('@nodes\n')
    NodesDF.to_csv( file, index=False, sep="\t")
    file.write('@arcs\n\t\t')
    for x in ArcsDF.columns[2:]:
        file.write(x)
        file.write('\t')
    file.write('\n')
    ArcsDF.to_csv( file, index=False, sep="\t", header=False)
    file.close
    return "done"