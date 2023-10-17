# Volodrone

<img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"
     alt="Markdown Python icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;

> Simple drone simulation app written in python.

### Requirements

- Python 3.9

### Usage

- It is advised to work in a virtual environment. Create one using the following command:

```
python3 -m venv venv
```

Activating **venv**:

- Windows OS: `./venv/Scripts/activate`
- Unix/Mac OS: `source venv/bin/activate`

Install the required packages into the newly created venv:

```
pip install -r requirements.txt
```

To start the simulation edit commands and mock data in main.py and run the terminal:

```
python main.py
```

To start unit tests run:

```
pytest -v .
```
