#  High-Performance Mono Alphabetic Cipher Solver (HPMACS)

<p>It aims to identify a linguistically sound set of plain texts constructed from a valid permutations of the key for the given monoalphabetic cipher</p>

Importance
----------
### Used in
* Decipher encrypted the notes and conversations
* Identify the unknown encoding schemes in documents
* Archeology for representing ancient manuscripts in modern languages

# Algorithm HPMACS

<p>The HPMACS is the combination of the bellow mentioned algorithms</p>

* Generalized Jakobsen
* AC-3
* Backtracking with Forward Checking
* MCTS ( for ciphers with no spaces )

Necessary Libraries
-------------------
For running the code a user needs to have python 3.0. <br>
All the libraries are imported in ``crypt.utils.py`` <br>
If the user does not have them in the computer, they can install them, using pip install in the terminal. For example:

```python
pip install imparaai-montecarlo
```

Steps to Run the Code on cipher with spaces
-------------------
* Download the zip
* Extract the files
* Open the ``csp_based_word_replacement_solver.py`` file
* Change the line bellow

```python
plaintext = "your sentence goes here"
```

* Run the command ``python3 csp_based_word_replacement_solver.py``

Steps to Run the Code on cipher without spaces
-------------------
* Download the zip (with_mcts version)
* Extract the files
* Open mcts.ipynb
* change the following line

```python
cyperedText = "your cipher goes here"
```

* Run all cells



