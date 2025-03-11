# PDF and Markdown data extraction

## Script list

### Generate problems.json from problems.md

`python3 gen_problems_json.py` - from problems.md and answers.md takes \n(\d+)\. numbers and cuts them into problems.json with problemText and answerText but no categories (just unsorted ID).

`python3 gen_problems_json_final.py` - from problems.md, answer.md, cats.json, class.txt makes problems.json (with all the problemText, answerText and categories according to class.txt).

### Cut pdf into images

`python3 pdf_to_images.py` - from input.pdf makes temp/page\_{num}.png images.

`python3 num_stripe_insp.py` - from temp/page\_{num}.png images makes output/mat11-{num}.png math problem images. Finds the problem numbers (to know where to cut) by inspecting black color (ignores blue) darkness in a specified dimensions vertical stripe.

### Generate cat.json from cat.txt

`python3 gen_cats_json.py` - makes json file out of leaf categories (\d+\.\d+\.\d+\.)

### Helper for manual checking of problems.md and answer.md

`python3 validate_content_md.py` - checks for in order numbering of problems in \n(\d+)\. format.

## Workflow examples

### From PDF make importable data

INPUT: PDF with problems and answers, MD with same problems and answers.

OUTPUT: JSON with categories, JSON with problems and answers, PNGs of problems and answers.

1. Have PDF OCRed to markdowns and separated into problem and answer parts in `input/` folder: `mat11.md`, `mat11.pdf`, `mat11ats.md`, `mat11ats.pdf`.
2. Have categories listed and assigned to problems in txt files in `input/` folder: `class.txt`, `cats.txt`.
3. Make PNGs of problems and answers:
   1. PDF -> pages PNGs. Produces `temp/page_{num}.png`.
   2. Pages PNGs -> problem/answer PNGs (according to problem number "stripe"). Produces `output/mat11-{num}.png`.
4. Make JSON with categories. Produces `cats.json`.
5. Make JSON with problems and answers and linked images:
   1. Check if MD files are in good format (the problem numbers) and manually fix.
   2. Run the "final" gen_problems script. Produces `output/problems.json`.
6. Review the images and see if the number of problems is the same in all outputs and if the image naming is good.
