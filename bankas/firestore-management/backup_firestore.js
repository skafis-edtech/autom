import admin from "firebase-admin";
import fs from "fs";
import env from "dotenv";

env.config({ path: ".env.not-secret" });

const SDK_FILE_PATH = process.env.SDK_FILE_PATH;
const BACKUP_DIR_PATH = "output/backup";
const serviceAccount = JSON.parse(fs.readFileSync(SDK_FILE_PATH, "utf8"));

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

async function backupCollection(collectionName) {
  const snapshot = await db.collection(collectionName).get();
  const data = [];

  snapshot.forEach((doc) => {
    data.push({ id: doc.id, ...doc.data() });
  });

  const jsonString = JSON.stringify(data, null, 2);

  const fileDirectory = `${BACKUP_DIR_PATH}/firestore`;

  if (!fs.existsSync(fileDirectory)) {
    fs.mkdirSync(fileDirectory, { recursive: true });
  }
  fs.writeFileSync(
    `${fileDirectory}/${collectionName}-backup-${new Date().toISOString()}.json`,
    jsonString
  );
  console.log(`Backup of ${collectionName} completed successfully.`);
}

const validCollections = [
  "categories",
  "problems",
  "users",
  "sources",
  "meta",
  "testai2_executions",
  "testai2_gradings",
  "testai2_templates",
  "testai2_takes",
];

const args = process.argv.slice(2); // Skip the first two arguments (node and script name)

if (args.length > 0) {
  const collectionName = args[0];
  if (validCollections.includes(collectionName)) {
    backupCollection(collectionName).catch(console.error);
  } else {
    console.error(`Error: '${collectionName}' is not a valid collection name.`);
    console.error(`Valid collection names are: ${validCollections.join(", ")}`);
  }
} else {
  // No CLI argument provided, backup all collections
  Promise.all(validCollections.map(backupCollection))
    .then(() => console.log("All collections backed up successfully."))
    .catch(console.error);
}
