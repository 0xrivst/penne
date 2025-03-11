export interface EncryptedData {
  keyEncoded: string;
  titleEncrypted: string;
  textEncrypted: string;
}

export interface DecryptedData {
  decryptedTitle: string | undefined;
  decryptedText: string | undefined;
}

export interface PasteContent {
  title: string;
  contents: string;
}
