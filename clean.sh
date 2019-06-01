echo "cleaning temp files"
rm .temp_files/*
echo "cleaning logs"
rm logs/*
echo "cleaning pycache files"
rm -Rdf `find -iname __pycache__`
echo "cleaning dot files"
rm *.dot
# echo "cleaning images"
# rm *.svg