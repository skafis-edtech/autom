import admin from "firebase-admin";
import fs from "fs";
import path from "path";
import env from "dotenv";

env.config({ path: ".env.not-secret" });

const SDK_FILE_PATH = process.env.SDK_FILE_PATH;
const BACKUP_DIR_PATH = "output/backup";
const STORAGE_BUCKET = process.env.STORAGE_BUCKET;

const serviceAccount = JSON.parse(fs.readFileSync(SDK_FILE_PATH, "utf8"));

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: STORAGE_BUCKET,
});

const storage = admin.storage().bucket();

async function backupFolder(folderName) {
  const folderPath = path.join(
    BACKUP_DIR_PATH,
    "storage",
    folderName + "-" + new Date().toISOString().replace(/:/g, "-")
  );

  // Ensure the backup directory exists
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
  }

  const [files] = await storage.getFiles({ prefix: `${folderName}/` });

  if (files.length === 0) {
    console.log(`No files found in ${folderName}`);
    return;
  }

  for (const file of files) {
    if (file.name.endsWith("/")) {
      console.log(`Skipping directory placeholder: ${file.name}`);
      continue;
    }

    const destination = path.join(
      folderPath,
      file.name.replace(`${folderName}/`, "")
    );

    const fileDirectory = path.dirname(destination);

    if (!fs.existsSync(fileDirectory)) {
      fs.mkdirSync(fileDirectory, { recursive: true });
    }

    await file.download({ destination });
    console.log(`Successfully downloaded: ${file.name}`);
  }

  console.log(`Backup of ${folderName} completed successfully.`);
}

const validFolders = ["problems", "answers"];
const args = process.argv.slice(2);

async function backupStorage() {
  try {
    if (args.length > 0) {
      const folderName = args[0];
      if (validFolders.includes(folderName)) {
        await backupFolder(folderName);
      } else {
        console.error(`Error: '${folderName}' is not a valid storage folder.`);
        console.error(`Valid storage folders are: ${validFolders.join(", ")}`);
      }
    } else {
      await Promise.all(validFolders.map(backupFolder));
      console.log("All storage folders backed up successfully.");
    }
  } catch (error) {
    console.error("Error backing up storage:", error);
  }
}

backupStorage();
