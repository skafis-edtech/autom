import fs from "fs";

const categories_file = "input/categories.json";
const output_file = "output/categories.txt";

const categories = JSON.parse(fs.readFileSync(categories_file, "utf-8"));

const output = categories
  .sort((a, b) => {
    const parseVersion = (v) => v.split(".").map(Number);
    const [aMajor, aMinor, aPatch] = parseVersion(a.name);
    const [bMajor, bMinor, bPatch] = parseVersion(b.name);

    return aMajor - bMajor || aMinor - bMinor || aPatch - bPatch;
  })
  .map((c) => c.name)
  .join("\n");

fs.writeFileSync(output_file, output);

console.log(`Categories have been saved to ${output_file}`);
