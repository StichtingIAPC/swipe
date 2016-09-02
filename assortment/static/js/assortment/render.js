/**
 * Created by Matthias on 11/04/2016.
 */

import {Product, OrProduct, AndProduct, Branch, BaseArticle} from 'js/assortment/models';
import _ from 'js/tools/translations'
import {draggable, droppable} from 'js/tools/tools'

/**
 * @callback Emit
 */

/**
 * @callback Refresh
 */

function ProductDescription(emit, refresh) {
  /**
   * @type {BaseArticle?}
   */
  return {
    render: renderer,
    hwrender: hwrender
  };
  function renderer(product) {
    let name_dict = draggable('product', product);
    name_dict.class = 'name';
    name_dict.editable = 'false';
    return [
      'div', {
        class: 'product-description'
      },
      [
        'span',
        name_dict,
        `${product.name}`
      ],
      [
        'span', {
          class: `amount ${product.amount_str}`
        },
        `${product.amount ? product.amount : 0}`
      ],
      [
        'span', {
          class: 'spacer'
        }
      ],
      [
        'span', {
          class: 'price'
        },
        `${product.price.toFixed(2)}`
      ]
    ]
  }

  /**
   * @param {Element} node
   * @param {BaseArticle} article
   */
  function hwrender(node, article) {
    let nspan, aspan, sspan, pspan;
    if (node !== null && node !== undefined && node.tagName == 'div') {
      if (node.classList.contains('product-description')) {
        const l = node.childNodes;
        nspan = l[0];
        aspan = l[1];
        sspan = l[2];
        pspan = l[3];
      } else {
        node.className = 'product-description';
        while (node.firstChild) {
          node.removeChild(node.firstChild);
        }
      }
    } else {
      node = node ? node : document.createElement('div');
      node.classList.length = 0;
      node.classList.add('product-description');

      nspan = document.createElement('span');
      nspan.classList.add('name');
      nspan.appendChild(document.createTextNode(product.name));

      aspan = document.createElement('span');
      aspan.classList.add('amount');
      aspan.classList.add(product.amount_str);
      aspan.appendChild(document.createTextNode(product.amount ? product.amount : String(0)));

      sspan = document.createElement('span');
      sspan.classList.add('spacer');

      pspan = document.createElement('span');
      pspan.classList.add('price');
      pspan.appendChild(document.createTextNode(product.price.toFixed(2)));

      node.appendChild(nspan).appendChild(aspan).appendChild(sspan).appendChild(pspan);

    }
  }
}

function NoItems(emit, refresh) {
  return {
    render: renderer
  };

  function renderer() {
    return [
      'div', {
        class: 'tree-list tree-list-info'
      },
      _('no contained items')
    ]
  }
}

function insert_toggle(unique_name, active) {
  return [
    [
      'input', {
        type: 'checkbox',
        class: 'opening-mechanism',
        id: unique_name,
        hidden: 'true',
        checked: active ? true : false
      }
    ],
    [
      'label', {
        for: unique_name,
        class: 'opening-mechanism'
      }
    ]
  ]
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderProduct}}
 * @constructor
 */
export function ProductRenderer(emit, refresh) {
  return {
    render: renderProduct
  };

  /**
   * @callback renderProduct
   * @param {Product} product
   * @param {Boolean} open
   * @param {String} prefix
   * @returns {*[]}
   */
  function renderProduct(product, open, prefix){
    return [
      'div', {
        class: 'product'
      },
      [ProductDescription, product]
    ]
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderAndProduct}}
 * @constructor
 */
export function AndProductRenderer(emit, refresh) {
  return {
    render: renderAndProduct
  };

  /**
   * @callback renderAndProduct
   * @param {AndProduct} andproduct
   * @param {Boolean} open
   * @param {String} prefix
   * @returns {*[]}
   */
  function renderAndProduct(andproduct, open, prefix){
    return [
      'div', {
        class: `product and-product`
      },
      insert_toggle(`${prefix}-product-${andproduct.id}`, open),
      [ProductDescription, andproduct],
      [BranchList, [], andproduct.contained_products, open]
    ];
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {renderOrProduct}
 */
export function OrProductRenderer(emit, refresh) {
  return {
    render: renderOrProduct,
    cleanup: cleanUpOrProductRenderer
  };

  /**
   * @callback renderOrProduct
   * @param {OrProduct} orproduct
   * @param {Boolean} open
   * @param {String} prefix
   * @returns {*[]}
   */
  function renderOrProduct(orproduct, open, prefix) {
    return [
      'div', {
        class: `product or-product`
      },
      insert_toggle(`${prefix}-product-${orproduct.id}`, open),
      [ProductDescription, orproduct],
      [BranchList, [], orproduct.contained_products, open, prefix]
    ];
  }

  /**
   *
   */
  function cleanUpOrProductRenderer() {

  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @param {String} prefix
 * @returns {{render: renderBranch}}
 */
export function BranchRenderer(emit, refresh, prefix) {
  return {
    render: renderBranch
  };

  /**
   * @callback renderBranch
   * @param {Branch} branch
   * @param {Boolean} open
   * @param {String} prefix
   * @returns {*[]}
   */
  function renderBranch(branch, open, prefix) {
    return [
      'div', {
        branch: branch.name,
        class: `branch`
      },
      insert_toggle(`${prefix}-branch-${branch.id}`, open),
      [
        'div', {
          class: 'branch-description'
        },
        [
          'span', {
            class: 'name'
          },
          `${branch.name}`
        ]
      ],
      [BranchList, branch.children, branch.products, open, prefix]
    ]
  }
}


/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderBranchList}}
 */
function BranchList(emit, refresh) {
  return {
    render: renderBranchList
  };

  /**
   * @callback renderBranchList
   * @param {Array<Branch>} branches
   * @param {Array<Product>} products
   * @param {Boolean} open
   * @param {String} prefix
   * @returns {*[]}
   */
  function renderBranchList(branches, products, open, prefix) {
    if (branches.length + products.length === 0) {
      return [NoItems];
    }
    return [
      'div', {
        'class': 'tree-list'
      },
      branches.length > 0 ? branches.map(
        (branch) => [BranchRenderer, branch, open, prefix]
      ) : [],
      products.length > 0 ? products.map(
        (product) => [product.renderer, product, open, prefix]
      ): []
    ]
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderAssortment}}
 */
export function AssortmentRenderer(emit, refresh) {
  /**
   * @type {{render: renderBranchList}}
   */
  return {
    render: renderAssortment
  };

  /**
   * @param {Assortment} assortment
   * @param {Boolean} open
   * @returns {*[]}
   */
  function renderAssortment(assortment, open) {
    /**
     * @param {Event} event
     */
    function oninput(event) {
      assortment.search(event.target.value);
    }
    return [
      'div', {
        class: 'assortment-tree'
      },
      [
        'div', {
          class: 'assortment-header'
        },
        [
          'div', {
            class: 'description'
          },
          `${assortment.title}`
        ],
        [
          'div', {
            class: 'search-box'
          },
          [
            'input', {
              type: 'search',
              id: `${assortment.name}-search-box`,
              oninput: oninput,
              placeholder: _('Search'),
              value: `${assortment.query}`
            }
          ]
        ]
      ],
      [BranchList, assortment.branches.filter(a => a.parent && !a.parent.parent), [], open, assortment.name]
    ]
  }
}
