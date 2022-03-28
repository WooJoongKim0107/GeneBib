These codes covers the second half of our work, which includes:
	1. Generation of time-series of hits 
		<./src/TimeSeries/time_series.py>
	2. Finding the debut years 
		<./src/TimeSeries/debut.py>
	3. Classify genes (growing, non-growing, growth-slowed, ...)
		<./src/TimeSeries/pattern.py>
	4. Calculating share
		<./src/Share/share.py>
	5. Find the fraction of categories (genetic tools, medical science, etc) among debuted genes.
		<./src/Share/portion.py>
	6. Finding the fitting parameters of the model to describe the debut time-series
		<./src/fitting.py> and <./src/Fitting/...>

All the codes are written in Python 3.8.10 and list of all libraries and their versions installed in my Python project can be found at the very end of this file.

All the raw data shown in the text can be found on <./pdata/plots/> and <./pdata/supple_plots/>. 
Processes to generate those data can be found <./src/Plot/data.py>, <./src/Plot/supple_data.py> and the python codes imported from those.

To reproduce all the results,
	1. Move to <./src/TimeSeries/__init__.py> and modify the "base_dir" as the absolute path of GeneBib project.
	2. Run <./src/update_TimeSeries.py>
	3. Run <./src/update_Shares.py>
	4. Run <./src/update_Fitting.py>
	5. Run <./src/update_Plot.py>

I tried to avoid any external libraries and to use only standard libraries as much as possible. All non-standard libraries used are:
	1. more_itertools (any version >= 8.0.0)
		https://pypi.org/project/more-itertools/
	2. numpy (any version >= 1.18.0)
		https://numpy.org/
	3. pandas (any version >= 1.0.0)
		https://pandas.pydata.org/
	4. scipy (any version >= 1.7.0)
		https://scipy.org/
	5. matplotlib (any version >= 3.1)
		https://matplotlib.org/
	6. mpmath (any version >= 1.2)
		https://mpmath.org/

	All those libraries can be installed using pip. If any conflicts, follow the installation instructions that each official homepage provides.
	
	Our work is not version specific unless Python version is >= 3.8, and any latest version of those libraries produce proper results (checked 2022/March/15th).
	
	I recommend using the latest possible version of those libraries. If the versions of those libraries are of concern, run <./src/demo.py> to compare the results generated using your system and their expected outputs. The demo will take less than an hour on normal desktop computer and probably less than 10 minutes on any recent computer systems.
	
Installation of Python >= 3.8 can be found:
	https://www.python.org/

Installation of Python and all the libraries used will take less than an hour on normal desktop computer. Probably less than 30 minutes on any recent computer systems.

--------------------<Installed packages>--------------------------
# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0# Name                    Version                   Build  Channel
backcall                  0.2.0              pyhd3eb1b0_0
blas                      1.0                         mkl
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_2
colorama                  0.4.4              pyhd3eb1b0_0
console_shortcut          0.1.1                         4
cycler                    0.10.0                   py38_0
decorator                 5.1.0              pyhd3eb1b0_0
dill                      0.3.3              pyhd3eb1b0_0
freetype                  2.10.4               hd328e21_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 ha925a31_3
intel-openmp              2021.2.0           haa95532_616
ipython                   7.29.0           py38hd4e2768_0
jedi                      0.18.0           py38haa95532_1
jpeg                      9b                   hb83a4c4_2
kiwisolver                1.3.1            py38hd77b12b_0
libpng                    1.6.37               h2a8f88b_0
libtiff                   4.2.0                hd0e1b90_0
llvmlite                  0.36.0           py38h34b8924_4
lz4-c                     1.9.3                h2bbff1b_0
matplotlib                3.3.4            py38haa95532_0
matplotlib-base           3.3.4            py38h49ac443_0
matplotlib-inline         0.1.2              pyhd3eb1b0_2
mkl                       2021.2.0           haa95532_296
mkl-service               2.3.0            py38h2bbff1b_1
mkl_fft                   1.3.0            py38h277e83a_2
mkl_random                1.2.1            py38hf11a4ad_2
more-itertools            8.7.0              pyhd3eb1b0_0
mpmath                    1.2.1                    pypi_0    pypi
numba                     0.53.1           py38hf11a4ad_0
numpy                     1.20.2           py38ha4e8547_0
numpy-base                1.20.2           py38hc2deb75_0
olefile                   0.46                       py_0
openssl                   1.1.1m               h2bbff1b_0
pandas                    1.2.4            py38hd77b12b_0
parso                     0.8.3              pyhd3eb1b0_0
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    8.2.0            py38h4fa10fc_0
pip                       21.1.1           py38haa95532_0
powerlaw                  1.4.6                    pypi_0    pypi
prompt-toolkit            3.0.20             pyhd3eb1b0_0
pygments                  2.10.0             pyhd3eb1b0_0
pyparsing                 2.4.7              pyhd3eb1b0_0
pyqt                      5.9.2            py38ha925a31_4
python                    3.8.10               hdbf39b2_7
python-dateutil           2.8.1              pyhd3eb1b0_0
pytz                      2021.1             pyhd3eb1b0_0
qt                        5.9.7            vc14h73c81de_0
scipy                     1.6.2            py38h66253e8_1
setuptools                52.0.0           py38haa95532_0
sip                       4.19.13          py38ha925a31_0
six                       1.15.0           py38haa95532_0
sqlite                    3.35.4               h2bbff1b_0
tbb                       2020.3               h74a9793_0
tk                        8.6.10               he774522_0
tornado                   6.1              py38h2bbff1b_0
traitlets                 5.1.1              pyhd3eb1b0_0
tzdata                    2020f                h52ac0ba_0
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wcwidth                   0.2.5              pyhd3eb1b0_0
wheel                     0.36.2             pyhd3eb1b0_0
wincertstore              0.2                      py38_0
xz                        5.2.5                h62dcd97_0
zlib                      1.2.11               h62dcd97_4
zstd                      1.4.5                h04227a9_0
