#Make a directory for each interpreter
#rm -r python-ref python-dev
#mkdir python-ref python-dev

#Download the python source code into python-ref
#hg clone https://hg.python.org/cpython python-ref

#Add timing instrumentation
cd python-ref
patch Objects/listobject.c ../timing-instrumentation.diff
cd ../

#Create the patched version in python-dev
cp -r python-ref/. python-dev
cd python-dev
patch Objects/listobject.c ../fastsort.diff
cd ../

#Build the two interpreters
for dir in python*; do
    cd $dir
    ./configure --enable-optimizations
    make
    cd ../
done
