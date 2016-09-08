import {Assortment} from 'js/assortment/models';
import {onload} from 'js/tools/tools';

onload(function(ev) {
  // make sure that window.swipe.assortments is available
  window.swipe = window.swipe ? window.swipe : {};
  window.swipe.assortments = {};

  // create an assortment for every object that has the `article-tree`-attribute
  Array.prototype.forEach.call(
    document.querySelectorAll('[article-tree]'),
    function(node) {
      console.log(node);
      let assort = Assortment.create_from_element(node);
      window.swipe.assortments[assort.name] = assort;
    }
  );
});
// as a NodeList does not have array operations, but has (otherwise) the same
// structure as an array, we can call array's prototype methods on it. This
// would be the same as calling map on the NodeList.
