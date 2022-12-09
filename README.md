<p align="center">
    <img src="assets/QuickCheckLogo.svg"
        height="50">
</p>

---


<a href="https://www.djangoproject.com/" alt="Flutter"><img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" /></a> 
<a href="https://github.com/tonydoesathing/quickcheck-backend/releases" alt="Figma"><img src="https://img.shields.io/github/v/release/tonydoesathing/quickcheck-backend" /></a>
<a href="https://github.com/tonydoesathing/quickcheck-backend" alt="Figma"><img src="https://img.shields.io/github/last-commit/tonydoesathing/quickcheck-backend" /></a> 

[QuickCheck](https://github.com/tonydoesathing/quickcheck) is a cross-platform application for teachers that assists in rapid formative assessment so they can focus more on teaching and less on organization. This project provides the networked synchronization required to run [QuickCheck](https://github.com/tonydoesathing/quickcheck).

## Setup
Ensure that you're using Python3.
Run `python -m venv .env` in the source directory, and then `.env/Scripts/activate`, `python -m pip install -r requirements.txt`, and `python manage.py migrate`, in that order. It should create the database.

## Running
Simply run `python ./manage.py runserver`

## Generating UML diagram
Run `python manage.py graph_models -a -g --dot -o quickcheck-backend.dot`; this will export a GraphViz .dot file.
Ensure that you have GraphViz enabled.
Run `dot.exe -Tpng quickcheck-backend.dot -o quickcheck-backend-uml.png`