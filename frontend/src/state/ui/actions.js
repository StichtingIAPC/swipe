export const ARE_YOU_SURE_ACTION = 'UI/areYouSure';
export const TOAST_ACTION = 'UI/toast';

/**
 *
 * @param action An action to spawn if the user presses OK
 * @param text The text to ask the user.
 * @param successText What to say to the user after he presses OK. Empty string for no dialog
 * @param failureText What to say to the user after he presses cancel. Empty string for no dialog
 * @returns {{type: string, action: *, text: string, successText: string, failureText: string}}
 */
export const areYouSureAction = (action, text,successText="", failureText="") => ({type: ARE_YOU_SURE_ACTION, action, text, successText, failureText});

/**
 *
 * @param text What to say to the user. Giving an empty string results in no toast.
 * @returns {{type: string, text: string}}
 */
export const toastAction = (text) => ({type: TOAST_ACTION, text});
