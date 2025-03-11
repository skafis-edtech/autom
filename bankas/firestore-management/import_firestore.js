import admin from "firebase-admin";
import fs from "fs";
import env from "dotenv";

env.config({ path: ".env.not-secret" });

const SDK_FILE_PATH = process.env.SDK_FILE_PATH;

const serviceAccount = JSON.parse(fs.readFileSync(SDK_FILE_PATH, "utf8"));

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore(); // ✅ Now initialized before calling importCollection()

const validCollections = ["categories", "problems", "users", "sources", "meta"];
const args = process.argv.slice(2);

async function importCollection(collection, filePath) {
  const problems = JSON.parse(fs.readFileSync(filePath, "utf8"));
  const batch = db.batch();
  const collectionRef = db.collection(collection);

  problems.forEach((problem) => {
    const docRef = collectionRef.doc(problem.id);
    batch.set(docRef, problem);
  });

  await batch.commit();
  console.log(`${collection} imported successfully.`);
}

if (args.length > 0) {
  const collectionName = args[0];
  if (validCollections.includes(collectionName)) {
    importCollection(collectionName, "input/" + collectionName + ".json").catch(
      console.error
    );
  } else {
    console.error(`Error: '${collectionName}' is not a valid collection name.`);
    console.error(`Valid collection names are: ${validCollections.join(", ")}`);
    process.exit(1);
  }
} else {
  console.error("Error: No collection name provided.");
  console.error(`Valid collection names are: ${validCollections.join(", ")}`);
  process.exit(1);
}
