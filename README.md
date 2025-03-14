# penne

> Simple pastebin with server- and client-side encryption

## Features

- Small and fast with no JS frameworks.
- Server-side encryption with [AES-GCM-SIV](https://eprint.iacr.org/2017/168.pdf).
- Optional client-side encryption with [XChaCha20Poly1305](https://www.cryptopp.com/wiki/XChaCha20Poly1305) from a zero-dependencies [@noble/ciphers](https://www.npmjs.com/package/@noble/ciphers) library.
- Expiring anonymous pastes, no registration required.
- Sign up for an account to create and manage non-expiring pastes.

## Running development environment

### Installing dependencies

> Note: GCC must be installed in the host system.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt && pip install -r requirements-dev.txt
```

### Environment variables

| Variable                             | Description/Notes                                                                                                                                                                                                    |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FLASK_SECRET_KEY                     | A secret key for signing session cookie. See [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) for instructions on generating.                                                    |
| BASE_API_KEY                         | Firebase API key. Called `apiKey` in Firebase SDK config.                                                                                                                                                            |
| BASE_AUTH_DOMAIN                     | Firebase auth domain. Called `authDomain` in Firebase SDK config.                                                                                                                                                    |
| BASE_DB_URL                          | Firebase database URL. Called `databaseURL` in Firebase SDK config.                                                                                                                                                  |
| BASE_BUCKET                          | Firebase storage bucket. Called `storageBucket` in Firebase SDK config.                                                                                                                                              |
| FIREBASE_PROJECT_ID                  | Firebase project ID. Can be retrieved from project settings or Firebase SDK config as `projectId`.                                                                                                                   |
|                                      | Values for `BASE_API_KEY`, `BASE_AUTH_DOMAIN`, `BASE_DB_URL`, `BASE_BUCKET`, and `FIREBASE_PROJECT_ID` variables are obtained by creating a Firebase project and going Project settings > General.                   |
| FIREBASE_PRIVATE_KEY                 | Private key for Firebase service account. Obtained by going to Project settings > Service accounts and clicking Generate new private key. From that file, copy the value of `private_key` _without_ quotation marks. |
| FIREBASE_PRIVATE_KEY_ID              | Key ID for Firebase service account. Obtained from the file with the private key from above.                                                                                                                         |
| FIREBASE_CLIENT_EMAIL                | Firebase client email. Obtained from the file with the private key from above.                                                                                                                                       |
| FIREBASE_CLIENT_ID                   | Firebase client ID. Obtained from the file with the private key from above.                                                                                                                                          |
| FIREBASE_AUTH_PROVIDER_X509_CERT_URL | Obtained from the file with the private key from above.                                                                                                                                                              |
| FIREBASE_CLIENT_X509_CERT_URL        | Obtained from the file with the private key from above.                                                                                                                                                              |
| ENCRYPTION_KEY                       | Key that will be used for server-side AES-GCM-SIV encryption. See below for generating instructions.                                                                                                                 |

One way to generate a random key for server-side encryption is as follows. The `cryptography` package must be installed in the environment.

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
import base64
print(base64.b64encode(AESGCMSIV.generate_key(bit_length=256)))
```

Copy resulting value, omitting the `b` and paste it into `ENCRYPTION_KEY` environment variable.

### Starting development server with Flask

```
flask --app penne --debug run
```

### Building CSS and JS with Webpack in watch mode

```
cd assets
npm run watch
```

## Production deployment

Clone the repository.

```sh
git clone git@github.com:0xrivst/penne.git
```

Build frontend assets.

```sh
npm ci && npm run prod
```

Copy built assets into `dist` directory.

Install dependencies.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install waitress
```

And serve the app.

```sh
waitress-serve --listen 0.0.0.0:5000 --call penne:create_app
```
