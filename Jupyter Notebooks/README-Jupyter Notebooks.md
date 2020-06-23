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
6. In your environment, load in the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
7. To leave, run this command in your virtual environment
    ```bash
    deactivate
    ```

Source: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/