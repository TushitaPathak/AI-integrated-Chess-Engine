#  Chess Engine (Flask + CLI)

This project is a **custom chess engine** built using `python-chess` and Flask.
It supports both:

*  **Web Interface (Flask)** – Play in your browser
*  **Command Line Interface (CLI)** – Play directly in terminal

---

##  Features

* Minimax algorithm with Alpha-Beta pruning
* Quiescence search for improved move evaluation
* Interactive web UI
* Terminal-based chess with a clean board display
* Move validation using SAN (Standard Algebraic Notation)

---

## Requirements

* Python 3.x
* Install dependencies:

```bash
pip install flask python-chess
```

---

## Running the Project

###  1. Run Web Version (Flask)

Start the Flask server:

```bash
python chess_engine_8_3.py
```

Then open your browser and go to:

```
http://localhost:5000
```

---

###  2. Run CLI Version (Terminal Chess)

Run the program with the `cli` argument:

```bash
python chess_engine_8_3.py cli
```
in order to locate the cli file ,Find where your file actually is (likely in Downloads or a project folder).

Then in terminal:

(cd path_to_your_file)

Example:

cd Downloads
---

##  How to Play (CLI Mode)

* You play as **White**
* Enter moves using **Standard Algebraic Notation (SAN)**:

  * `e4`
  * `Nf3`
  * `O-O` (castling)
* The engine will respond automatically

Example:

```
Your move (>>>): e4
Engine plays: e5
```

---

##  Project Structure

```
chess_engine_8_3.py   # Main file (Flask + CLI + Engine)
```

---

## How It Works

* The engine uses:

  * **Minimax Algorithm**
  * **Alpha-Beta Pruning**
  * **Piece-Square Tables**
* CLI and Web modes share the **same engine logic**

---

##  Modes Summary

| Mode | Command                          | Description         |
| ---- | -------------------------------- | ------------------- |
| Web  | `python chess_engine_8_3.py`     | Runs Flask server   |
| CLI  | `python chess_engine_8_3.py cli` | Runs terminal chess |
