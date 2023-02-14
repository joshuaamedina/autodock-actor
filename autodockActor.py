import os
import subprocess
from agavepy.actors import get_context, get_client
from reactors.utils import Reactor, agaveutils
from agavepy.agave import Agave

libraries = {
    "Enamine-PC": "/scratch/02875/docking/test/Enamine-PC/Enamine-PC/test_sets/test",
    "Enamine-AC": "/scratch/02875/docking/test/benchmarks/Enamine-AC/10000_set",
    "Enamine-HTSC": "/scratch/02875/docking/test/benchmarks/Enamine-HTSC/10000_set",
    "ZINC-in-trials": "/scratch/02875/docking/test/benchmarks/ZINC-in-trials/10000_set",
    "ZINC-fragments": "/scratch/02875/docking/test/benchmarks/ZINC-fragments/10000_set"
}

def fileDownload(r,filename):

    storage, mpath, localFilename = agaveutils.from_agave_uri(uri=filename)
    mpath = mpath + '/' + localFilename
    mfile = agaveutils.agave_download_file(agaveClient=r.client,agaveAbsolutePath=mpath,systemId=storage,localFilename=localFilename)
    if mfile is None:
        print("Failed")
    else:
        print("Downloaded")

def setParallelism(library):
    nodes = 1
    processes = 32
    maxRunTime = "03:00:00"

    if library == "Enamine-PC":
        nodes = 1 
        processes = 32
        maxRunTime = "00:05:00"
    if library == "Enamine-HTSC":
        nodes = 10 
        processes = 320
        maxRunTime = "02:00:00"
    if library == "ZINC-in-trials":
        nodes = 2 
        processes = 64
        maxRunTime = "04:00:00"        

    return nodes, processes, maxRunTime
        
def main():
    r = Reactor()
    context = get_context()
    message = context['raw_message']
    paramlist = message.split(' ')
    print("Actor received message: {}".format(message))

    # Parse all parameters from the actor's message

    protein = paramlist[0]
    newProtein = protein.split('/')
    position = len(newProtein) - 1
    filename = newProtein[position]

    center_x = float(paramlist[1])
    center_y = float(paramlist[2])
    center_z = float(paramlist[3])
    size_x = float(paramlist[4])
    size_y = float(paramlist[5])
    size_z = float(paramlist[6])
    forcefield = paramlist[7]
    docking = paramlist[8]

    flexible = False
    if docking == "rigid":
        flexible = False
    elif docking == "flexible":
        flexible = True
        sidechains = paramlist[9].split('_')
    library = paramlist[10]

    # Check the bounds of our box
    # Check the file passed is an agave link
    # Check the file passed ends with .pdb or .pdbqt

    for size in [size_x,size_y,size_z]:
        assert (size <= 30 and size >= 1), "box size is outside the bounds (1-30)" 
    assert protein.startswith('agave://')
    assert (protein.endswith('.pdb') or protein.endswith('.pdbqt')), "Please provide a .pdb or .pdbqt file"

    # Pass the Reactor instance and file to fileDownload to be downloaded for processing.
    # Pass the library to setParallelism to get appropriate # of Nodes and Processes.
    
    nodes, processes, maxRunTime = setParallelism(library)
    fileDownload(r,protein)

    # Prepare receptor to pdbqt
    '''
    if(protein.endswith('.pdb')):
        subprocess.run(["prepare_receptor {filename}"],shell=True)
        filename = filename.split('.')[0]
        filename = filename + '.pdbqt'
    '''

    # If our file is appropriate, create our center bounds
    # Check the user's provided bounds
    # Check the user's provided flexible sidechain

    if(protein.endswith('.pdbqt')):
        all_sidechains = []
        xbounds = []
        ybounds = []
        zbounds = []
        with open(filename, 'r') as r:
            line = r.readline()
            while line:
                line = r.readline()
                if line.startswith('ATOM'):
                    xbounds.append(float(line.split()[6]))
                    ybounds.append(float(line.split()[7]))
                    zbounds.append(float(line.split()[8]))
                    all_sidechains.append(line.split()[3] + line.split()[5])
        if flexible == True:
            for sidechain in sidechains:
                assert (sidechain in all_sidechains), "Please provide valid flexible sidechain names, separated by underscores (e.g. THR315_GLU268)"
        assert(min(xbounds)) <= center_x <= (max(xbounds)), "Center x coordinate is not within bounds"            
        assert(min(ybounds)) <= center_y <= (max(ybounds)), "Center y coordinate is not within bounds"
        assert(min(zbounds)) <= center_z <= (max(zbounds)), "Center z coordinate is not within bounds"
    
    print("We would continue to job submission here with : ", nodes, " nodes and " , processes, " processes!")

'''
    #Get an active Tapis client
    client = get_client()
    body = {
        "name": "Autodock-Vina-Actor",
        "appId": "Autodock-Vina-1.2.3",
        "batchQueue": "normal",
        "maxRunTime": maxRunTime,
        "memoryPerNode": "1GB",
        "nodeCount": nodes,
        "processorsPerNode": processes,
        "archive": False,
        "inputs": {
            "receptor": "{protein}"
        },
        "parameters": {
            "center_x": center_x,
            "center_y": center_y,
            "center_z": center_z,
            "size_x": size_x,
            "size_y": size_y,
            "size_z": size_z,
            "forcefield": forcefield,
            "docking": docking,
            "library": libraries[library],
            "top_n_scores": 5
            "sidechains": paramlist[9]
        }
    }

    response = client.jobs.submit(body=body)
    print("Successfully submitted job {} to Tapis App {}".format(response['id'], response['appId']))
'''

if __name__ == '__main__':
    main()
