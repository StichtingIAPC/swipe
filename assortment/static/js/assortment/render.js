/**
 * Created by Matthias on 11/04/2016.
 */

import {Product, Branch} from './models';

/**
 * @callback Emit
 */

/**
 * @callback Refresh
 */

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderProduct}}
 * @constructor
 */
function ProductRenderer(emit, refresh) {
  return {
    render: renderProduct
  };

  /**
   * @callback renderProduct
   * @param {Product} product
   * @returns {*[]}
   */
  function renderProduct(product){
    return [
      'div', {
        class: 'product-description'
      },
      [
        'p', product.amount
      ], [
        'span', {}, product.name
      ], [
        'span', {}, product.price
      ]
    ]
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderAndProduct}}
 * @constructor
 */
function AndProductRenderer(emit, refresh) {
  return {
    render: renderAndProduct
  };

  /**
   * @callback renderAndProduct
   * @param {AndProduct} andproduct
   * @returns {*[]}
   */
  function renderAndProduct(andproduct){
    return [
      'div', {},
      [
        'div',
        {
          class: 'product-description and-product'
        },
        [ 'span', { class: 'product-amount' }, andproduct.amount ],
        [ 'span', { class: 'product-name' }, andproduct.name ],
        [ 'span', { class: 'product-price' }, andproduct.price]
      ],
      [
        'div',
        {
          class: 'product-list'
        },
        andproduct.contained_products.map(
          (component) -> [
            'div',
            {},
            [ 'span', { class: 'product-amount' }, component.amount ],
            [ 'span', { class: 'product-name' }, component.product.name ],
            [ 'span', { class: 'product-price' }, component.product.price]
          ]
        )
      ]
    ];
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {renderOrProduct}
 */
function OrProductRenderer(emit, refresh) {
  return {
    render: renderOrProduct,
    cleanup: cleanUpOrProductRenderer
  };

  /**
   * @callback renderOrProduct
   * @param {OrProduct} orproduct
   * @returns {*[]}
   */
  function renderOrProduct(orproduct) {

    return [
      'div', {},
      [
        'div',
        {
          class: 'product-description or-product'
        },
        [ 'span', { class: 'product-amount' }, orproduct.amount ],
        [ 'span', { class: 'product-name' }, orproduct.name ],
        [ 'span', { class: 'product-price' }, orproduct.price]
      ],
      [
        'div',
        {
          class: 'product-list'
        },
        orproduct.contained_products.map(
          (component) -> [
            'div',
            {},
            [ 'span', { class: 'product-amount' }, component.amount ],
            [ 'span', { class: 'product-name' }, component.product.name ],
            [ 'span', { class: 'product-price' }, component.product.price]
          ]
        )
      ]
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
function BranchRenderer(emit, refresh) {
  return {
    render: renderBranch
  };

  /**
   * @callback renderBranch
   * @param {Branch} branch
   * @returns {*[]}
   */
  function renderBranch(branch) {
    return [
      'div', {
        branch: branch.name,
        class: 'open'
      },
      [
        'div',
        {
          class: 'branch-header'
        },
        [ 'span', { class: 'branch-icon' }],
        [ 'p', {}, branch.name ]
      ],
      [
        'div',
        {
          class: 'branch-content'
        },
        [BranchList, branch.children],
        [ProductList, branch.products]
      ]
    ]
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderProductList}}
 */
function ProductList(emit, refresh) {
  return {
    render: renderProductList
  };

  /**
   * @callback renderProductList
   * @param {Array<Product>} products
   * @returns {*[]}
   */
  function renderProductList(products) {
    return [
      'ul', {
        'class': 'product-list'
      },
      products.map(
        (product) -> [
          'li', {},
          [product.renderer, product]
        ]
      )
    ];
  }
}

/**
 * @param {Emit} emit
 * @param {Refresh} refresh
 * @returns {{render: renderBranchList}}
 */
function BranchList(emit, refresh) {
  return {
    render: render
  };

  /**
   * @callback renderBranchList
   * @param {Array<Branch>} branches
   * @returns {*[]}
   */
  function renderBranchList(branches) {
    return [
      'ul', {
        'class': 'branch-list'
      },
      branches.map(
        (branch) -> [
          'li', {},
          [BranchRenderer, branch]
        ]
      )
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
   * @returns {*[]}
   */
  function renderAssortment(assortment) {
    return __super.render(assortment.branches.filter((branch) => branch.parent !== null));
  }
}
