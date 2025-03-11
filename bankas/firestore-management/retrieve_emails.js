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

async function exportEmails() {
  const emails = [];
  let nextPageToken;

  do {
    const listUsersResult = await admin.auth().listUsers(1000, nextPageToken);
    listUsersResult.users.forEach((userRecord) => {
      if (userRecord.email) {
        // Ensure the email exists
        emails.push(userRecord.email);
      }
    });
    nextPageToken = listUsersResult.pageToken;
  } while (nextPageToken);

  const fileDirectory = `${BACKUP_DIR_PATH}/auth`;
  if (!fs.existsSync(fileDirectory)) {
    fs.mkdirSync(fileDirectory, { recursive: true });
  }
  // Save the emails to a TXT file
  fs.writeFileSync(
    `${fileDirectory}/emails-${new Date().toISOString()}.txt`,
    emails.join("\n")
  );
  console.log("Exported", emails.length, "emails");
}

exportEmails().catch((error) =>
  console.error("Error exporting emails:", error)
);
