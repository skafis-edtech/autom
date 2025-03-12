import admin from "firebase-admin";
import fs from "fs";
import path from "path";
import env from "dotenv";

env.config({ path: ".env.not-secret" });

const SDK_FILE_PATH = process.env.SDK_FILE_PATH;
const STORAGE_BUCKET = process.env.STORAGE_BUCKET;

const serviceAccount = JSON.parse(fs.readFileSync(SDK_FILE_PATH, "utf8"));

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: STORAGE_BUCKET,
});

const storage = admin.storage().bucket();

async function uploadFolder(folderName) {
  const localFolderPath = path.join("input/images", folderName);

  if (!fs.existsSync(localFolderPath)) {
    console.error(`Error: Folder '${localFolderPath}' does not exist.`);
    return;
  }

  const files = fs.readdirSync(localFolderPath).filter((file) => {
    return fs.statSync(path.join(localFolderPath, file)).isFile();
  });

  if (files.length === 0) {
    console.log(`No files found in ${localFolderPath}`);
    return;
  }

  for (const file of files) {
    const localFilePath = path.join(localFolderPath, file);
    const storageFilePath = `${folderName}/${file}`;

    const metadata = {
      contentType: `image/${file.split(".").pop()}`,
    };

    try {
      await storage.upload(localFilePath, {
        destination: storageFilePath,
        metadata: metadata,
      });
      console.log(`Uploaded ${file} to ${storageFilePath}`);
    } catch (error) {
      console.error(`Error uploading ${file}:`, error);
    }
  }

  console.log(`Upload of ${folderName} completed successfully.`);
}

const validFolders = ["problems", "answers"];
const args = process.argv.slice(2);

async function uploadImages() {
  try {
    if (args.length > 0) {
      const folderName = args[0];
      if (validFolders.includes(folderName)) {
        await uploadFolder(folderName);
      } else {
        console.error(`Error: '${folderName}' is not a valid folder.`);
        console.error(`Valid folders are: ${validFolders.join(", ")}`);
      }
    } else {
      await Promise.all(validFolders.map(uploadFolder));
      console.log("All image folders uploaded successfully.");
    }
  } catch (error) {
    console.error("Error uploading images:", error);
  }
}

uploadImages();
