# Step-by-step Instructions for Docking with Rosetta

## 1) Prepare Ligand library with Spartan

1. Build ligand
2. Click setup -> calculations -> conformer distribution
* with molecular mechanics and MMFF
* increase max number of conformers to 100%
* if its a large ligand, it can take hours to run
3. After running, a new window will open
4. Bottom will show number of conformers, left arrow to go through them
5. Save library as mol2
6. Also save the original ligand as a spartan file and mol2 file - just in case

[refer to video](https://www.youtube.com/watch?v=ocuT3tYeK7I) 

## 2) Use HIVE to prepare ligands for Rosetta

1. upload CL3.mol2 library conformer to HIVE
* CL3 can instead be any 3 letter/number code for a ligand, dont use 001, be creative
3. run with
```
python3 /quobyte/jbsiegelgrp/software/Rosetta_314/rosetta/main/source/scripts/python/public/generic_potential/mol2genparams.py -s CL3.mol2
```
or try
```
python3 /quobyte/jbsiegelgrp/software/Rosetta_314/rosetta/main/source/scripts/python/public/molfile_to_params.py -n CL3 -p CL3 --conformers-in-one-file CL3.mol2
```
3. will generate CL3.pdb, CL3_conformers.pdb, CL3.params files
4. download all
5. write PDB_ROTAMERS CL3_conformers.pdb at the end of your params file
   example:
   <img width="552" height="117" alt="Screenshot 2026-02-23 at 2 32 08 PM" src="https://github.com/user-attachments/assets/9f18591a-f5af-4ba0-89c3-dd282cef242e" />



## 3) Use HIVE to prepare enzyme for Rosetta

1. Acquire enzyme PDB from [Uniprot](https://www.uniprot.org/) or [RCSB PDB](https://www.rcsb.org/)
   or refer to my [Alphafold3 Submission for HIVE](https://github.com/MissMaryR/AlphaFold3-Submission-for-HIVE) to generate a PDB from AF3
2. Refer to my [Relax pdbs for Rosetta](https://github.com/MissMaryR/Relax-pdbs-for-Rosetta) to prepare your PDB



## 4) Use PyMOL to place ligand into active site

### To help guide ligand placement in the active site, try using: [Chai](https://www.chaidiscovery.com/), AF3, or [Boltz](https://github.com/jwohlwend/boltz)
* they will generate PDBs with a general ligand placement - often not close enough to catalytic residues for docking analysis but acts as a guide

1. Open relaxed PDB & ligand (CL3.pdb) in PyMOL
2. If you made a roughly docked PDB from sources above try using the [Pair fit](https://pymolwiki.org/index.php/Pair_fit) commands in PyMOL
   * also add the roughly docked PDB to the PyMOL session and align it with the relaxed PDB
   * run commands in the command line in PyMOL
   * use SHOW to show atom names on catalytic residues & ligands
   * it works by moving LIG1 (your ligand) on top of LIG2 (ligand already in active site)
   * ```
     pair_fit LIG1/ATOM1+ATOM2, LIG2/ATOM1+ATOM2
     ```
   * example code with moving CL3 (your ligand) on top of LIG2
   * ```
     pair_fit CL3/O1+C4+O3+C7, LIG2/O2_1+C3_1+O3_1+C4_1
     ```
   * keep pressing enter to move it to different positions, if several are available
   * alternatively you can adjust the number of atoms to align
   * save the session
3. Alternatively, you can use the Pair Fit method to align the ligand to a catalytic residue
   * then use editing mode in PyMOL to move the ligand into a spot that is catalytically relevant
   * it does not need to be super specific, just within a couple angstroms, the constraint file will tell rosetta where to place the ligand
   * recommend using a mouse for editing mode
5. Make sure to delete everything except the relaxed PDB and the placed ligand (CL3.pdb)
   * keep the order with relaxed PDB first and then the ligand, this matters for the pdb file
6. File -> export structure -> export molecule -> save as PDB
7. Open the saved file and make sure your ligand is at the bottom and labeled as chain X
 * if 2 ligands - X & Y


     

