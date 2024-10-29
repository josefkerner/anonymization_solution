# anonymization solution
This solution parses and anonymizes source documents for RAG AI use cases

## Installation
0. install python 3.9 or higher
1. Clone the repository
2. Install the required packages using the following command:
```bash
pip install -r requirements.txt
```
4. place the source documents in the `data` folder
5. change location to root of the project
```bash
cd anonymization_solution
```
6. export the env var PYTHONPATH in the root of the project
```bash
set PYTHONPATH=. 
or export PYTHONPATH=. (for linux and mac users)
```
7. download the spacy model
```bash
python -m spacy download en_core_web_lg
```
7. Run the following command to start the application:
```bash
python src/main.py
```
8. The anonymized documents will be saved in the `results` folder in txt format