export PYTHONPATH=json-webcaller

cp webservices.json.example demo.json

for testfile in tests/*-test.py; do
	python "$testfile"
done
