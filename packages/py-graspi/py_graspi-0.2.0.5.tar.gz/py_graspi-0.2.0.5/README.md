# py-graspi
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kkevinmartinezz/kaggle_PyGraspi/3d7bf5df17b015612ab1b8261c63d0bbb00a268f?urlpath=lab%2Ftree%2Fpygraspi-test.ipynb)

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from some meta-vertices to all specified vertices
  -  Provide a list of descriptors
  -  Graph visualization


## Getting Started
### Testing Py-Graspi Online
To run an existing test notebook to explore the capabilities of Py-Graspi,

[![Check out this kaggle notebook](https://img.shields.io/badge/Open_Kaggle_Notebook-green)](https://www.kaggle.com/code/elyuzz/pygraspi-test)

To create your own notebook and use the py-graspi package
1. Open [Google Colab](https://colab.research.google.com/).
2. In the notebook, install Py-Graspi by running the following command:
   ```python
   !pip install py-graspi
   ```
3. Import the py-graspi package by running this command in the notebook:
   ```python
   import py_graspi as ig
   ```
4. Run any py-graspi function you wish to use as described in the [To Test Algorithms section](#to-test-algorithms)


## Installation
### Manual Installation of Py-Graspi
Follow these steps to manually install the Py-Graspi package.

1. After opening a new project in your preferred IDE, activate the virtual environment for your project by running this command:
   - On Windows (Command Prompt):
     ```cmd
     .\.venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source ./.venv/bin/activate
     ```

2. Clone the project repository by running this command:

   **Note: You must have Git installed on your system**
   ```bash
   git clone https://github.com/owodolab/py-graspi.git
   ```
   If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git

3. Navigate to the Py-Graspi project directory by running this command:
   ```bash
   cd py-graspi/
   ```

4. Install the py-graspi module from PyPI by running this command:

   **Note: You must have Python and pip installed onto your system**
   ```bash
   pip install py-graspi
   ```

5. Verify that the module has been installed correctly by ensuring that the following command DOES NOT give you a "Package not found" error.
   ```bash
   pip show py-graspi
   ```
   
   If you do not have Python installed, please visit: https://www.python.org/downloads/

   If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/

   If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/ 

6. Once installed, import the package to utilize it in your project
   ```python
   import py_graspi as ig
   ```
7. To learn how to use and run graph algorithms in your project files, [Go to the Test Algorithms section in the README](#to-test-algorithms)
  
8. To run test files on the command line and view the output, [Go to the Testing From Command Line section of the README](#testing-from-command-line)



### Script Installation of Py-Graspi
1. Clone the project repository by running this command:

   **Note: You must have Git installed on your system**
   ```bash
   git clone https://github.com/owodolab/py-graspi.git
   ```
   If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git
   
2. Run the following script to set up and activate the virtual environment and install the py-graspi package:
   ```
   python py-graspi/startup.py
   ```
3. Verify that the module has been installed correctly by ensuring that the last output line on the command line says "Setup complete!" with no errors.
   If you do not have Python installed, please visit: https://www.python.org/downloads/
   

### Installation and Set-Up of Jupyter Notebook for Py-Graspi
1. After opening a new project in your preferred IDE, activate the virtual environment for your project by running this command:
   - On Windows (Command Prompt):
     ```cmd
     .\.venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source ./.venv/bin/activate
     ```

2. Clone the project repository by running this command:

   **Note: You must have Git installed on your system**
   ```bash
   git clone https://github.com/owodolab/py-graspi.git
   ```
   If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git

3. Navigate to the Py-Graspi project directory by running this command:
   ```bash
   cd py-graspi/
   ```

4. Install the py-graspi module from PyPI by running this command:
   **Note: You must have Python and pip installed onto your system**
   ```bash
   pip install py-graspi
   ```
   
5. Install jupyter notebook by running this command:
   ```
   pip install notebook
   ```
   
6. Now, open the package in Jupyter Notebook for testing by running this command:
   ```
   jupyter notebook
   ```
   A localhost jupyter notebook should open with the same directories and files as the py-graspi package.
   
  
## View Demo Videos for Py-Graspi Installation, Notebook Setup, and Testing via Command Line
Please visit this link: https://drive.google.com/drive/folders/1AECLQXII4kmcBiQuN86RUYXvJG_F9MMq?usp=sharing
### Videos
* **py_graspi_installation**: How to install Py-Graspi and run basic commands.
* **py_graspi_notebook**: How to utilize our prebuilt notebook to run basic commands of Py-Graspi.
* **py_graspi_command_line**: How to print out Py-Graspi's calculations of connected components, descriptors, visualizations of graph, etc of provided input files via command line.

## Testing from Command Line

Now that we have cloned the REPO lets talk about testing.

In this GitHub Repo, you can find test files in the data directory or the 2D-testFile and 3D-testFile directories.
Inside these directories, some files hold information about either 2d or 3d graphs based on the directory name. 
When running from command lines you will need to know the complete pathname of the test file you are trying to run.

There are 2 type of input file formats: *.txt & *.graphe
### _*.txt input format:_

The command line input to run a graph creation for *.txt files will have the following format:
```
python igraph_testing.py {total pathname of test file}
```
If you have the same test directories as this GitHub Repo you should be able to run the following command line argument to output a 2D 10x10 graph.
```
python igraph_testing.py ../data/2D-testFile/testFile-10-2D.txt 
```
### _*.graphe input format:_
*.graphe input format is not that different, only extra parameter you need to input is a '-g' before the total pathname of the test file.

The command line input to run a graph creation for *.graphe files will have the following format:
````
python igraph_testing.py -g {total pathname of test file} 
````
If you have the same test directories as this GitHub Repo you should be able to run the following command line argument to output a 2D 4x3 graph.
```
python igraph_testing.py -g ../data/data_4_3.graphe
```
### _Running with Periodicity:_
We include the option of running any test case with periodicity turned on (only for .txt files). This 
is done with an added '-p' parameter. This parameter is added first before inputting the test case
format.

For example, for *.txt cases with periodicity turned on will look like the following:
```
python igraph_testing.py -p {total pathname of test file}
```
To test this out run the example test case above but with the added '-p' parameter
to turn periodicity on.

## Output of Command Line Input
As long as the inputs follow the format above and a file exists the program shall do the following:
1. Pop up window should appear, this will be the initial visualization of the graph along with red, blue, and green meta vertices.
2. Exit out of this pop up window with the top right "X" button.
3. Now a second pop up window should appear, this window will now show a visualization of the filtered version of the graph in step 1.
4. Exit out this window following same steps as step 2.
5. Make sure program exits correctly (code 0).

DISCLAIMER: if any issues occur you may not be in the right directory (src) or the test file may not exists or be poorly formatted.

## To Test Algorithms

### To **generate graphs**, call the generateGraph(_file_) function which takes in a input-file name
returns:
  - graph_Data object - The graph data. It contains the following:
      - g: graph object
      - s_2D: bool of whether the graph is 2D
      - black_vertices: list of all black vertices
      - white_vertices: list of all white vertices
      - black_green: number of edges from black to interface (green vertex)
      - black_interface_red: number of black interface vertices that has a path to top (red)
      - white_interface_blue: number of white interface vertices that has a path to bottom (blue)
      - dim: value of vertices in y direction for 2D and z direction for 3D
      - interface_edge_comp_paths: number of interface edges with complementary paths to top (red) and bottom (blue)
      - shortest_path_to_red: shortest paths from all vertices to red 
      - shortest_path_to_blue: shortest paths from all vertices to blue
      - CT_n_D_adj_An: number of black vertices in direct contact with top (red)
      - CT_n_A_adj_Ca: number of white vertices in direct contact with bottom (blue)
    ```
    g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")   # utilizing the test file found in 2D-testFiles folder as an example
    ```

### To **filter graphs**, call filterGraph(_graph_) function which takes in a graph object 
  -  can pass a graph generated by generateGraph(_file_)
  -  returns a filtered graph
    ```
g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")[0]     # utilizing the test file found in 2D-testFiles folder as an example
fg = ig.filterGraph(g)
print(f"Number of Connected Components: {len(fg.connected_components())}")
print(f"Connected Components: {fg.connected_components()}")```

### To get a dictionary of descriptors

To test if descriptors are computed correctly, you can run the following script in the terminal to check.
  -  make sure you are in the py-graspi directory after git cloning
  -  if not in directory tests, in the terminal, run the command
     ```
     cd tests
     ```
     ```
     python descriptor_testing.py ../data/data/data_0.5_2.2_001900.txt
     ```
     This will print out whether the descriptor computation is correct and should take around 10-15 seconds.

The **descriptors stored in a dictionary** can be computed by calling the function descriptors(graph_data, filename).
It takes in the graph_data_class object returned from generateGraph() and an input filename as the parameters.
      ```
      dict = ig.descriptors(graph_data,filename) 
      ```
The ** descriptors in a text file** can be computed by calling the function descriptorsToTxt(_dictionary_,_filename_)
  -  _dict_ is a dictionary of descriptors that is returned by calling ig.descriptors(...)
    ```
ig.descriptorsToTxt(dict,"descriptors_list.txt") ```


### To visualize graphs

To visualize graphs, call visualize(_graph_, _is_2D_)
  -  _graph_ is a graph object
  -  _is_2D_ is a bool of whether a graph is 2D, also a return value when _generateGraph()_ is called
    ```
g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")   # utilizing the test file found in 2D-testFiles folder as an example
ig.visualize(g, "graph")```

## Translating .plt files to .txt files
These are the steps for translating .plt files to .txt files in order to be turned into graphs.
1. Make sure you cd into the py_graspi directory.
2. All necessary functions are in the plt_to_txt.py file.
3. The command line input format for this file is as follows:
```
python plt_to_txt.py [pathname]
```
5. The file in pathname should be in the plt directory and end with the .plt extension, if not this will not work.
6. It's translated .plt file should show up in the same directory but now with a .txt extension and in .txt formatting when executed with no errors.
7. Some files have been placed in the .plt directory for testing.
8. If you wish to run an example, first delete the translated version of a .plt file if it has been created, and run the following command line input:
```
python plt_to_txt.py plt/5x4x3.plt
```
9. Make sure the translated file with .txt extension has been made and placed in the plt directory to ensure the file has been executed correctly.

## Translate Image File Into Truncated .txt File
1. Make sure you have py-graspi installed: pip install py-graspi
2. Make sure you cd into the py-graspi directory first. From there, cd into the tools then translations by running 'cd tools/translations'. 
3. The command line format to translate an image file into its truncated .txt file is as follows:
```
python img_to_txt.py {pathname of image file} {Resize calculation amount}
```
4. The "resize calculation amount" is multiplied to the X and Y axis of the original image and this will alter the size of the image's final resized .txt file. 
5. This should place both a truncated image file and truncated .txt file of the original image file into the "resized" directory. 
6. They will be named "resized_" followed by the image file name and correct extension. 
7. An example command line input that should work for this repo is as follows:
```
python img_to_txt.py ../../data/images/data_0.5_2.2_001900.png 0.15
```

## 2D & 3D Morphologies Tests
To run the 2d and 3d morphologies you will need to setup notebook and pip install the graspi_igraph package.

First you will need to git clone the current repo:
```
git clone https://github.com/owodolab/py-graspi.git
```
Then, you will need to install the igraph package:
```
pip install py-graspi
```
Install jupyter notebook in order to view the test file:
```
pip install notebook
```
Finally, you will be able to use the command:
```
jupyter notebook
```
This will bring you into the testing filing on jupyter.

Navigate to the file `graspi_igraph_notebook.ipynb` under the `notebook` directory.

On this file you will be able to run and view the 2d and 3d morphologies.

## Testing Runtime for old and new implementation
Repeat the above instructions from "2D & 3D Morphologies Tests". New tests are located in the same notebook at the bottom two.

## Running All 33 Morphologies Tests
To run the morphologies tests, first make sure you're on the `py-graspi` directory.
<br>
<br>
Run the following command to start at the py-graspi directory:
```
cd ..
```
Next, make sure you're running using bash by running the following command:
```
bash
```
Next, run the following command:
```
chmod +x run.sh
```
Finally, run the following command for .txt or .pdf generation: 
```
./run.sh <file_type>
```
Substitute `<file_type>` with either `txt` or `pdf` for the desired output type.
<br />
<br />
Example:
```
./run.sh txt
```
**Note: You should run `txt` before `pdf` to update text files and for an accurate PDF output**
## 33 Morphologies Output
After running the command, the automatic report generation will begin. 
<br />
<br /> 
The following will print when the report generation begins:
```
Generating PDF (If on pdf mode)
Generating Text Files
```
As the script is running, the following will print for which microstructure it is on
```
Executing <test_file>
```
After a few minutes, the following will print once the report has been created
```
Text Files Generated
PDF Generated (If on pdf mode)
```
## Viewing 33 Morphologies Output
### Text Files
For text files, navigate to the results directory by using the following command:
```
cd data/results
```
Use the following command to view the list of text files generated:
```
ls
```
To view the result in each file, run the following command:
```
cat <result_file_name>
```
Replace `<result_file_name>` with any of the files outputted by running `ls`
<br />
<br />
Example:
```
cat descriptors-data_0.514_2.4_000220.txt
```
### PDF
If using pdf mode, the PDF should automattically open upon completion.
<br />
<br />
If the pdf does not automatically pop up, use the following commands, making sure you're on the `py-graspi` directory:
### On Windows
```
start py_graspi/test_results.pdf
```
### On MacOS
```
open py_graspi/test_results.pdf
```
### On Linux
```
evince py_graspi/test_results.pdf
```
If evince is not installed, run this first:
```
sudo apt install evince
```

## Tortuosity HeatMap Visualization
This are the steps for visualizing tortuosity via HeatMap.
1. Make sure you cd into the py-graspi directory, then into tools then tortousity. Run cd tools/tortousity to get there. 
2. All necessary functions are in the tortuosity.py file.
3. Code necessary to visualize the tortuosity HeatMap is as follows:
```
python tortuosity.py {pathname of file}
```
4. This code will only work if the IdTortuosityBlackToRed descriptors of this file
have been found and outputted to it's corresponding file in the distances directory.
5. For now there are some file examples in this directory so an example code
to visualize a heatmap is as follows:
```
Python tortuosity.py ../../data/data/data_0.5_2.2_001900.txt 
```
6. First a tortuosity heatmap will output for Black To Red vertices.
7. Exit out of this pop up window.
8. Second a totuosity heatmap will output for White to Blue vertices.
9. Exit out of this pop up Window.
### Reading HeatMap
* A HeatMap should show up with a HeatMap Bar to the right of the HeatMap. 
* Based on current implementation, this HeatMap outputs tort values of each vertex and that value is used to color in the Heatmap based on the HeatMap Bar.
* Read the side bar to the right to understand the cyclic gradiant coloring.
* Following is the matplotlib api section for more information on this gradiant: https://matplotlib.org/stable/users/explain/colors/colormaps.html#cyclic

  
## Jupyter NoteBook to Visualize HeatMap
1. Make sure Jupyter Notebook is installed:
```
pip install jupyter
```
2. Run jupyter notebook with following command:
```
jupyter notebook
```
3. Open up `tortuosity.ipynb` under the `py_graspi` directory.
4. Click the Run tab on the top.
5. Click "Run All Cells"
6. Wait a bit and the HeatMaps of some files will be created and visualized.
   
## Mycelium Filtered Vertices Visualization
This section explains how to visualize a mycelium image by both it's white and black vertices filtered versions.
The mycelium image used is included in the "images" directory called "mycelium.png".

The following are steps on how to visualize the graph from this image.
1. Make sure you have py-graspi installed: pip install py-graspi
2. Make sure you cd into py-graspi directory first.
3. The command line format input is as follows
```
python myceliumTest.py {pathname of image file} {Resize calculation amount}
```
4. The input is the same as the translation input from image files to .txt files, it will create a new .img and .txt file for it in the "resized" directory.
5. The image input pathname must be in the "images" directory.
6. If you wish to not resize the original image just input a '1' for the Resize calculation amount, this will keep the original size.
7. Example command line input is as follows:
```
python myceliumTest.py ../../data/images/data_0.5_2.2_001900.png 0.15
```
8. This creates a truncated version of the mycelium image (for runtime purposes) and outputs the largest subgraph of the following filtered graphs:
   1. The first one is a white only vertex graph 
   2. The second one is a black only vertex graph.

## Mycelium Filtered Vertices Interactivity
1. Follow these steps to run through different interactive features after running the myceliumTest.py file
2. On the bottom left of the window, there will be some built-in mathplotlib tools in the following order: "Reset Home Button," "Undo," "Redo," "Drag and Pull Move Mode," "Zoom in Mode," "Configuration Settings," and "Save File."
3. The Reset Home Button, when clicked, will take you to the center of the graph no matter where you are. You may need to zoom out a couple of times, but if you do, you will resort back to the original graph visualization (not accounting for rotations).
4. We will not use these Redo/Undo buttons since they only work with the mathplotlib built-in functionalities and not my built-in ones so they may cause confusion.
5. The Drag and Pull Mode Button, when clicked, allows the user to hold a click on the graph and move around as desired. Make sure you are able to move around easily.
6. The Zoom In Mode will make it so you can crop out a rectangular area and it will automatically zoom into this area. This is helpful for easier massive zooms and can be used with the built-in zoom in/out buttons. Make sure you can zoom in with this functionality. 
7. The Configuration Settings will open up a window with sliders. These sliders will change the border of the graph and get rid of white space around the graph. Play with the sliders to make sure you are able to change the border fo the graph visualization. (The bottom two sliders do not affect our graph visualization in any way, recommend not to mess with these). 
8. If you wish to reset the configurations there is a "reset" button on the bottom right of this new pop up window, click this and confirm that all the settings are back to how they were originally. 
9. The Save File button works just as any other save file button. This allows to save the graph visualization into your computer files. 
10. There are also 4 buttons to the bottom right of the Graph in the following order: Zoom In, Zoom Out, Rotate CW, and Rotate CCW.
11. Pressing the Zoom In button which will zoom into the graph.
12. Pressing the Zoom Out button will zoom out the same amount as it zoomed in.
13. Pressing Rotate CW will rotate the graph by 30 degrees clockwise.
14. Pressing Rotate CCW will rotate the graph by 30 degrees counter-clockwise.


## Generate and Run Files for py-graspi API
In order to generate an API using sphinx, you need to follow the installation of py-graspi:

Cloning the repository:
```
git clone https://github.com/owodolab/py-graspi.git
```

**Make sure your current directory is py-graspi**

In order to create an API with sphinx, you need to download sphinx with this command in the command line interface:
```
pip install sphinx
```
Additional dependencies needed for installed Sphinx Extension:
```
pip install sphinxcontrib-details-directive
```
Provides additional details (dropdowns) for each submodle listed.
```
pip install sphinx_rtd_theme
```
Uses the rtf theme for the API
```
pip install --upgrade setuptools
```
Used by python to handle resources and files

In the command line interface, run this command:
```
sphinx-build -b html ./docs/source/ ./docs/ 
```
* **sphinx-build**: This is the main command for building Sphinx documentation. It generates documentation from reStructuredText (.rst) or Markdown (.md) source files.
* **-b html**: This specifies the output format. Here, -b html tells Sphinx to build the documentation in HTML format, which is typically used for web-based documentation.
* **./docs/source/**: This is the path to the source directory where Sphinx looks for the documentation source files. In this example, it’s in the source subdirectory inside docs.
* **./docs/**: This is the output directory where the built HTML files will be saved. In this example, it’s the main docs folder. After running this command, you’ll find the generated HTML files here.

In order to see the py-graspi API, run this command in the command line interface:

**FOR WINDOWS:**
```
start docs/index.html
```

**FOR MACOS:**
```
open docs/index.html
```
This would create a local view. You can see the official API on Github pages at: https://owodolab.github.io/py-graspi/
