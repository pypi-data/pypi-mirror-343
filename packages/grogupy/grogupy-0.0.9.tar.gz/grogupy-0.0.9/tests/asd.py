################################################################################
#                                 Input files
################################################################################
# input folder and file
infolder = "../benchmarks/Cr3"
infile = "Cr3.fdf"
################################################################################
#                            Convergence parameters
################################################################################
# kset should be at leas 100x100 for 2D diatomic systems
kset = [1, 1, 1]
# eset should be 100 for insulators and 1000 for metals
eset = 100
# esetp should be 600 for insulators and 10000 for metals
esetp = 600
# emin None sets the minimum energy to the minimum energy in the eigfile
emin = None
# emax is at the Fermi level at 0
emax = 0
# the bottom of the energy contour should be shifted by -5 eV
emin_shift = -5
# the top of the energy contour can be shifted to the middle of the gap for
# insulators
emax_shift = 0.5
################################################################################
#                                 Orientations
################################################################################
# usually the DFT calculation axis is [0, 0, 1]
scf_xcf_orientation = [0, 0, 1]
# the reference directions for the energy derivations
ref_xcf_orientations = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# matlabmode is only for testing purposes
matlabmode = False
################################################################################
#                      Magnetic entity and pair definitions
################################################################################
# magnetic entities and pairs can be defined automatically from the cutoff
# radius and magnetic atoms
setup_from_range = True
radius = 20
atomic_subset = "Cr"
kwargs_for_mag_ent = dict(l=2)
################################################################################
#                                Memory management
################################################################################
# maximum number of pairs per loop, reduce it to avoid memory overflow
max_pairs_per_loop = 100000
# in low memory mode we discard some temporary data that could be useful for
# interactive work
low_memory_mode = True
################################################################################
#                                 Solution methods
################################################################################
# sequential solver is better for large systems
greens_function_solver = "Parallel"
# the calculation of J and K from the energy derivations, either Fit or Grogupy
exchange_solver = "Fit"
anisotropy_solver = "Fit"
################################################################################
#                                   Output files
################################################################################
# either total or local, which controls if only the magnetic
# entity's magnetic monent or the whole atom's magnetic moment is printed
# used by all output modes
out_magentic_moment = "total"

# save the magnopy file
save_magnopy = True
# precision of numerical values in the magnopy file
magnopy_precision = None
# add the simulation parameters to the magnopy file as comments
magnopy_comments = True

# save the Uppsala Atomistic Spin Dynamics software input files
# uses the outfolder and out_magentic_moment
save_UppASD = True

# save the pickle file
save_pickle = True
"""
The compression level can be set to 0,1,2,3. Every other value defaults to 3.
0. This means that there is no compression at all.

1. This means, that the keys "_dh" and "_ds" are set
   to None, because othervise the loading would be dependent
   on the sisl version

2. This contains compression 1, but sets the keys "Gii",
   "Gij", "Gji", "Vu1" and "Vu2" to [], to save space

3. This contains compression 1 and 2, but sets the keys
   "hTRS", "hTRB", "XCF" and "H_XCF" to None, to save space
"""
pickle_compress_level = 3

# output folder, for example the current folder
outfolder = infolder
# outfile name
outfile = f"{infile.split('.')[0]}_kset_{'_'.join(map(str, kset))}_eset_{eset}_{anisotropy_solver}"
################################################################################
################################################################################