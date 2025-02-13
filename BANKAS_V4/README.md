# Automatisation to upload math problemsets to bankas.skafis.lt

bankas v4 is a version of bankas.skafis, which is good to use for "business customers".

## Running scripts

### Generate problems.json from problems.md

`python3 gen_problems_json.py` - from problems.md and answers.md takes \n(\d+)\. numbers and cuts them into problems.json with problemText and answerText but no categories (just unsorted ID).

`python3 gen_problems_json_final.py` - from problems.md, answer.md, cats.json, class.txt makes problems.json (with all the problemText, answerText and categories according to class.txt).

### Cut pdf into images

`python3 pdf_to_images.py` - from input.pdf makes temp/page_{num}.png images.

`python3 pix_insp.py` - from temp/page_{num}.png images makes output/mat11-{num}.png math problem images. Finds the problem numbers (to know where to cut) by inspecting black color (ignores blue) darkness in a specified dimensions vertical stripe. 

### Generate cat.json from cat.txt

`python3 gen_cats_json.py` - makes json file out of leaf categories (\d+\.\d+\.\d+\.)

### Helper for manual checking of problems.md and answer.md

`python3 validate_content_md.py` - checks for in order numbering of problems in \n(\d+)\. format.