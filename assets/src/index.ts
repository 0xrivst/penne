export {
  pasteToFile,
  pasteLinkToQr,
  processEncryptedPaste,
} from './pasteActions';

import { handleFormSubmission } from './pasteFormHandler';

document.addEventListener('DOMContentLoaded', () => {
  const newPasteForm = document.getElementById(
    'newPasteForm'
  ) as HTMLFormElement | null;
  newPasteForm?.addEventListener('submit', handleFormSubmission);
});
