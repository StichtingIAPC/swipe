/**
 * Created by Matthias on 11/04/2016.
 */

import {Product, OrProduct, AndProduct, Branch} from 'js/assortment/models';
import _ from 'js/tools/translations'

/**
 * @callback Emit
 */

/**
 * @callback Refresh
 */

function ProductDescription(emit, refresh) {
  return {
    render: renderer
  };
  function renderer(product) {
    return [
      'div', {
        class: 'product-description'
      },
      [
        'span', {
          class: 'name'
        },
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
        hidden: 'true'
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
  const __super = BranchList(emit, refresh);

  return {
    render: renderAssortment
  };

  /**
   * @param {Assortment} assortment
   * @param {Boolean} open
   * @returns {*[]}
   */
  function renderAssortment(assortment, open) {
    return __super.render(
      assortment.branches.filter((branch) => !branch.parent),
      [],
      open,
      assortment.name
    );
  }
}
