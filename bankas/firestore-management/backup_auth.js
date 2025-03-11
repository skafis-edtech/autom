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

async function exportUsers() {
  const users = [];
  let nextPageToken;

  do {
    const listUsersResult = await admin.auth().listUsers(1000, nextPageToken);
    listUsersResult.users.forEach((userRecord) => {
      users.push(userRecord.toJSON());
    });
    nextPageToken = listUsersResult.pageToken;
  } while (nextPageToken);

  const fileDirectory = `${BACKUP_DIR_PATH}/auth`;

  if (!fs.existsSync(fileDirectory)) {
    fs.mkdirSync(fileDirectory, { recursive: true });
  }

  // Save the users to a JSON file
  fs.writeFileSync(
    `${fileDirectory}/users-${new Date().toISOString()}.json`,
    JSON.stringify(users, null, 2)
  );
  console.log("Exported", users.length, "users");
}

exportUsers().catch((error) => console.error("Error exporting users:", error));
