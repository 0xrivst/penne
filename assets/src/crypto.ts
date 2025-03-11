import { xchacha20poly1305 } from '@noble/ciphers/chacha';
import {
  utf8ToBytes,
  bytesToUtf8,
  bytesToHex,
  hexToBytes,
} from '@noble/ciphers/utils';
import { randomBytes, managedNonce } from '@noble/ciphers/webcrypto';

import type { EncryptedData, DecryptedData } from './types';

const initChacha = (key: Uint8Array) => {
  return managedNonce(xchacha20poly1305)(key);
};

const encryptPaste = (title: string, text: string): EncryptedData => {
  const key = randomBytes(32);
  const keyEncoded = bytesToHex(key);
  const chacha = initChacha(key);

  const titleEncrypted = bytesToHex(chacha.encrypt(utf8ToBytes(title)));
  const textEncrypted = bytesToHex(chacha.encrypt(utf8ToBytes(text)));

  return { keyEncoded, titleEncrypted: titleEncrypted, textEncrypted };
};

const decryptPaste = (title: string, text: string): DecryptedData => {
  try {
    const key = hexToBytes(
      new URLSearchParams(window.location.search).get('k') || ''
    );
    const decryptedTitle = bytesToUtf8(
      initChacha(key).decrypt(hexToBytes(title))
    );
    const decryptedText = bytesToUtf8(
      initChacha(key).decrypt(hexToBytes(text))
    );
    return { decryptedTitle, decryptedText };
  } catch (error) {
    console.log(error);
    return { decryptedTitle: undefined, decryptedText: undefined };
  }
};

export { encryptPaste, decryptPaste };
