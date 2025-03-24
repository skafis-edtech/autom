import fs from "fs";
const problems_file="input/problems.json"
const categories_file="input/categories.json"
const output_file="output/problems-categories.json"

const problems = JSON.parse(fs.readFileSync(problems_file, 'utf-8'));
const categories = JSON.parse(fs.readFileSync(categories_file, 'utf-8'));

const categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]));

const output = problems
  .filter(p => p.problemText && p.skfCode)
  .map(p => ({
    problemText: p.problemText,
    categories: (p.categories || []).map(id => categoryMap[id]).filter(Boolean),
    skfCode: p.skfCode
  }))
  .sort((a, b) => {
    const numA = parseInt(a.skfCode.replace(/\D/g, ''), 10);
    const numB = parseInt(b.skfCode.replace(/\D/g, ''), 10);
    return numA - numB;
  });

fs.writeFileSync(output_file, JSON.stringify(output, null, 2));
