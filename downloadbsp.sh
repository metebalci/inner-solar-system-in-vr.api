u=https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/$1/$2.bsp
python -m jplephem excerpt 2020/1/1 2030/1/1 $u $2.bsp
