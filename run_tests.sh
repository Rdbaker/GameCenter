i=0
limit=$1
for meth in $(grep "def"  tests/views/test_api.py | grep -v "setUp" | grep -v "tearDown" | awk '{print $2;}' | awk -F\( '{print $1}'); do
    if [ $i -lt $limit ]; then
        py.test --verbose tests/views/test_api.py::APIViewsTest::$meth
        i=$((i+1))
    fi
done
