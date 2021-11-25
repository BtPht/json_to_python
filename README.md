# json_to_python
Generates python code to handle a given JSON file

### TODO:
- Add tests:
    * all the single types
    * single string of single type
    * flat dictionary

### ROADMAP:
- Add parsing json from file
- Add option to use :
    * json data as default values
    * empty defaults (str="", int=0)
    * no defaults at all
- Add option to merge similar classes :
    * not at all
    * based on type and name of attributes (more difficult that it seems)
- Handle command line options
    * -f input file
    * -o output file
    * --type=atts/serializers
    * --auto-format (using black)