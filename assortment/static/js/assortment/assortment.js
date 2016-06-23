import {Assortment} from './models';

const assortments = Array.prototype.map.call(
  document.querySelectorAll('[article-tree]'),
  node -> Assortment.create_from_element(node)
);
// as a NodeList does not have array operations, but has (otherwise) the same
// structure as an array, we can call array's prototype methods on it. This
// would be the same as calling map on the NodeList.
