export PYTHONPATH=json-webcaller

cp webservices.json demo.json

for testfile in tests/*-test.py; do
	python "$testfile"
done
