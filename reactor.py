import os
import subprocess
from agavepy.actors import get_context, get_client
from reactors.utils import Reactor, agaveutils
from agavepy.agave import Agave


def fileDownload(r):

    print(r.client)
    print(r.context)
    print(agaveutils.from_agave_uri(uri='agave://cloud.corral.work.joshuaam/ls6/autodock-collab/input/receptors/1iep_receptor.pdbqt'))
    print(f'-----------------------------')
    storage = 'cloud.corral.work.joshuaam'
    mpath = '/ls6/autodock-collab/input/receptors/1iep_receptor.pdbqt'
    mfile = agaveutils.agave_download_file(agaveClient=r.client,agaveAbsolutePath=mpath,systemId=storage,localFilename='1iep_receptor.pdbqt')
    if mfile is None:
        print("Failed")
    else:
        print("Downloaded")

    f = open('1iep_receptor.pdbqt','r')
    print(f.read())

def main():
    r = Reactor()
    fileDownload(r)    
    context = get_context()
    message = context['raw_message']
    paramlist = message.split(' ')
    print(paramlist)

    print("Actor received message: {}".format(message))

    # Usually, one would perform some input validation before submitting
    # a job to a Tapis App. Here, we simply validate that the path looks
    # like a Tapis/Agave URI

    protein = paramlist[0]
    center_x = float(paramlist[1])
    center_y = float(paramlist[2])
    center_z = float(paramlist[3])
    size_x = float(paramlist[4])
    size_y = float(paramlist[5])
    size_z = float(paramlist[6])

    assert (size_x <= 30 and size_y <= 30 and size_z <=30), "box size is outside the bounds (30)" 
    assert protein.startswith('agave://')
    assert (protein.endswith('.pdb') or protein.endswith('.pdbqt')), "Please provide a .pdb or .pdbqt file"
   
    print(f'{message} was accepted')

    # Get an active Tapis client
    #client = get_client()
   

"""
   # Using our Tapis client, submit a job to Tapis App eho-fastqc-0.11.9
   body = {
      "name": "fastqc-test",
      "appId": "eho-fastqc-0.11.9",
      "archive": False,
      "inputs": {
         "fastq": "agave://eho.work.storage/{}".format(os.path.basename(fastq_uri))
      }
   }
   response = client.jobs.submit(body=body)
   print("Successfully submitted job {} to Tapis App {}".format(response['id'], 
response['appId']))
"""

if __name__ == '__main__':
    main()
