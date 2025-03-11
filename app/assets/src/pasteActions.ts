import { renderSVG } from 'uqr';

import { decryptPaste } from './crypto';

const pasteToFile = (title: string, contents: string): void => {
  const fileContents = `${title}\n\n${contents}`;

  const url = URL.createObjectURL(
    new Blob([fileContents], { type: 'text/plain;charset=utf-8' })
  );

  const link = document.createElement('a');
  link.href = url;
  link.download = `${title}.txt`;
  link.click();
  URL.revokeObjectURL(url);
};

const pasteLinkToQr = (): void => {
  const qrCodeContainer = document.getElementById('qr-code-container');

  if (!qrCodeContainer) throw new Error('SVG element is not on page');

  qrCodeContainer.classList.remove('d-none');
  const svg = renderSVG(window.location.href);
  qrCodeContainer.innerHTML = svg;
};

const processEncryptedPaste = (title: string, text: string): void => {
  const { decryptedTitle, decryptedText } = decryptPaste(title, text);

  if (decryptedTitle && decryptedText) {
    const titleElement = document.getElementById('pasteTitle');
    const contentsElement = document.getElementById('pasteContents');

    if (titleElement && contentsElement) {
      titleElement.innerText = decryptedTitle;
      contentsElement.innerText = decryptedText;
    }
  }
};

export { pasteLinkToQr, pasteToFile, processEncryptedPaste };
