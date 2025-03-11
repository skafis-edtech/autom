import admin from "firebase-admin";
import fs from "fs";
import env from "dotenv";

env.config({ path: ".env.not-secret" });

const SDK_FILE_PATH = process.env.SDK_FILE_PATH;
const HASH_PARAMS_FILE = process.env.HASH_PARAMS_FILE;

const INPUT_FILE_PATH = "input/auth.json";

// Initialize Firebase Admin SDK
const serviceAccount = JSON.parse(fs.readFileSync(SDK_FILE_PATH, "utf8"));
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

// Read hash parameters
const hashParams = JSON.parse(fs.readFileSync(HASH_PARAMS_FILE, "utf8"));

// Read users JSON file
const users = JSON.parse(fs.readFileSync(INPUT_FILE_PATH, "utf8"));

// Convert users to Firebase format
const formattedUsers = users
  .filter((user) => user.email && user.passwordHash)
  .map((user) => ({
    uid: user.uid,
    email: user.email,
    emailVerified: user.emailVerified || false,
    passwordHash: Buffer.from(user.passwordHash, "base64"),
    salt: Buffer.from(user.passwordSalt || "", "base64"),
    disabled: user.disabled || false,
  }));

// Batch import users
async function importUsers() {
  if (formattedUsers.length === 0) {
    console.error("No valid users found to import.");
    return;
  }

  try {
    const result = await admin.auth().importUsers(formattedUsers, {
      hash: {
        algorithm: hashParams.algorithm,
        key: Buffer.from(hashParams.base64_signer_key, "base64"),
        rounds: hashParams.rounds,
        memoryCost: hashParams.mem_cost,
        saltSeparator: Buffer.from(hashParams.base64_salt_separator, "base64"),
      },
    });

    console.log(`Successfully imported ${result.successCount} users.`);
    if (result.failureCount > 0) {
      console.error(`${result.failureCount} users failed to import.`);
      result.errors.forEach((err) => {
        console.error(
          `Error for user ${formattedUsers[err.index].email}:`,
          err.error
        );
      });
    }
  } catch (error) {
    console.error("Error importing users:", error);
  }
}

importUsers();
