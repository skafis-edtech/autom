# Firestore backup and upload

## Prerequisites

Have firebase service account file `f-sdk.json`. Put it into `/secrets` folder here. Do the same with test environment service account file `test-f-sdk.json`. In JSON format store password hash parameters `test-pwd-hash-params.json` and `pwd-hash-params.json`.

## Scripts

To run on prod environment firebase, put this content in `.env.not-secret` file:

```
SDK_FILE_PATH=secrets/f-sdk.json
HASH_PARAMS_FILE=secrets/pwd-hash-params.json
STORAGE_BUCKET=bankas-skafis.appspot.com
```

To run on test environment firebase, put this content in `.env.not-secret` file:

```
SDK_FILE_PATH=secrets/test-f-sdk.json
HASH_PARAMS_FILE=secrets/test-pwd-hash-params.json
STORAGE_BUCKET=bankas-skafis-testenv.firebasestorage.app
```

### Upload

Amends, doesn't delete existing.

`node import_auth` - imports auth data (users with passwords) from `input/auth.json` file. Currently has problems with preserving passwords.

`node import_firestore problems` - imports problems data (or other entity) from `input/problems.json` or corresponding file.

`node import_storage problems` - imports images to storage from `input/images/problems/` folder or corresponding.

### Backup

`node backup_auth`

`node backup_storage problems`

`node backup_storage`

`node backup_firestore`

`node backup_firestore problems`

`node backup_firestore`

`node retrieve_emails` - puts only email list into a txt file.

All output stored in `output/` folder.

### Other

`node get_problem_categories_convenient`

Takes `problem.json` and `categories.json` files and creates `problems-categories.json` file with problem texts and category names assigned for problems.

`node get_categories_list_txt.js`

Makes categories.txt from categories.json
