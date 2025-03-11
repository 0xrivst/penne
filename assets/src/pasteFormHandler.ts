import { encryptPaste } from './crypto';

import type { EncryptedData } from './types';

export const handleFormSubmission = function (
  this: HTMLFormElement,
  event: Event
): void {
  event.preventDefault();

  const formData = new FormData(this);
  let pasteTitle = formData.get('pasteName') as string;
  pasteTitle = pasteTitle.length === 0 ? 'Unnamed' : pasteTitle;
  const pasteText = formData.get('pasteText') as string;

  const e2eeChecked = formData.get('e2ee') !== null;
  let keyEncoded: string | undefined;

  if (e2eeChecked) {
    const {
      keyEncoded: key,
      titleEncrypted,
      textEncrypted,
    }: EncryptedData = encryptPaste(pasteTitle, pasteText);

    formData.set('pasteName', titleEncrypted);
    formData.set('pasteText', textEncrypted);
    keyEncoded = key;
  }

  fetch(this.action, {
    method: this.method,
    body: formData,
  })
    .then((response: Response) => {
      if (response.ok) {
        window.location.href =
          e2eeChecked && keyEncoded
            ? `${response.url}?k=${keyEncoded}`
            : response.url;
      }
      if (response.status === 401) {
        alert('Nuh-uh!');
      }
    })
    .catch((error: Error) => {
      console.error(error);
    });
};
