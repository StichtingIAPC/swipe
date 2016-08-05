/**
 * Created by Matthias on 04/08/2016.
 */

export default function translate(str) {
  try {
    return window.swipe.translations[str];
  } catch (e) {
    return `[${str}]`;
  }
}