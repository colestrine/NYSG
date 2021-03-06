# Jupyter Notebooks

## Tutorial
1. First check your Python installation version. Make sure it is the latest python version, python 3.7.6. You can check this with the command in your terminal or powershell
    ```bash
    python3 --version
    ```
    
    It should say:
    ```bash
    Python 3.7.6
    ```
    Versions of Python3 beyond 3.7.6 might be ok, but some of the dependencies
    might have to be manually upgraded or more dependencies installed.
2. Next install Python's package manager pip. Run the command below:
    In Linux/MacOS
    ```bash
    python3 -m pip install --user --upgrade pip
    ```
    Windows:
    ```bash
    py -m pip install --upgrade pip
    ```
3. Install venvm, the virtual environment in which you can develop and see your code running
    In Linux/MacOS
    ```bash
    python3 -m pip install --user virtualenv
    ```
    Windows:
    ```bash
    py -m pip install --user virtualenv
    ```
4. Now create your virtual environment:
    In Linux/MacOS
    ```bash
    python3 -m venv env
    ```
    Windows:
    ```bash
    py -m venv env
    ```
    You can replace env with any other name you want.
5. Start your environment:
    In Linux/MacOS
    ```bash
    source env/bin/activate
    ```
    Windows:
    ```bash
    .\env\Scripts\activate
    ```
    Everytime you want to develop on the notebook, remember to open the environment again. 
6. In your environment, load in the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
7. To add further dependencies that are Python packages, run
    ```bash
    pip install package_name
    ```
    where package_name is the package you want. For instance, if you want package numpy, run this command:
    ```bash
    pip install numpy
    ```
8. To freeze dependencies into the requirements.txt for future use:
    ```bash
    pip freeze > requirements.txt
    ```
    This will save the dependencies you currently are developing with for other people to use with exactly the same packages and versions.
9. To launch Jupyter Notebook in the virtual environment, run this command:
    ```bash
    jupyter notebook
    ```
    A browser should open, allowing you to see different files. Click and Open the file titled Programming Tutorial, which you can work on interactively
10. To close the Jupyter Notebook, close the browser page, then go back tou your terminal and run the command ctrl - C to terminate, and enter Y for yes
11. To leave the virtual environment, run this command in your virtual environment
    ```bash
    deactivate
    ```
    This returns you back to your terminal.
12. To start using the notebook, follow the commands above. You should be able to start the Notebook and begin learning how to program in Python. 

To start using the notebook, follow the commands above. You should be able to start the Notebook and begin learning how to program in Python.  The instructions to use the notebook are in the Notebook file you just opened. 
        
As a quick summary: The notebook has cells you can click on. These cells are the rectangular partitions on the webpage. Click the arrow to activate and run the cell. A response is displayed under as the response. 

You add new cells: in the upper left corner is a button with a (+) plus sign to add a cell. Go to the cell you want to add under, click on the add button, and a cell will occur underneath. 

You can also delete cells. There is again a button in the top bar to delete a cell.

If your notebook somehow crashes, close the window, and restart using the process below.

Don't skip cells! This can cause unintended errors or crashes. Cells evaluate at the order they are run, so skipping cells changes the intended running order. You can imagine what kind of issues this could cause...

If you skip a cell, go back to the cell you skipped and run it, then run the remainder of the cells you skipped ahead on after, in descending order down the page.

Source: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/