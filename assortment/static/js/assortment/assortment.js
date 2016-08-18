import {Assortment} from 'js/assortment/models';
import {onload} from 'js/tools/tools';

onload(function(ev) {
  const assortments = Array.prototype.map.call(
    document.querySelectorAll('[article-tree]'),
    function(node) {
      console.log(node);
      return Assortment.create_from_element(node);
    }
  );
  assortments[0].search('fiets');
});
// as a NodeList does not have array operations, but has (otherwise) the same
// structure as an array, we can call array's prototype methods on it. This
// would be the same as calling map on the NodeList.
