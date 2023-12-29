
python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

mkdir dataSet
mkdir recognizer

python3 datasetCreator.py
python3 trainer.py
python3 detector.py
