# Autodock Actor

* The following actor takes an input message as follows:

  _agavefile center_x center_y center_z size_x size_y size_z forcefield docking flexible_sidechain library_

  <span style="font-size:2em;">"agave://cloud.corral.work.joshuaam/ls6/autodock-collab/input/receptors/1iep_receptor.pdbqt 16 52 17 20 20 20 vina flexible THR315 /scratch/02875/docking/test/benchmarks/Enamine-HTSC/10000_set"</span>

* The actor will check if the file provided is a pdbqt or pdb file.

* The actor will download the specified file.

* The actor will verify all x,y,z coordinates, the flexible sidechain, and set the number of necessary nodes and processes.

* The actor has future functionality for submitting a job to an app if all verifications are passed.
