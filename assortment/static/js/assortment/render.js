/**
 * Created by Matthias on 11/04/2016.
 */

import {Product, Branch} from './models';

/**
 * @param {Function} emit
 * @param {Function} refresh
 * @constructor
 */
function ProductRenderer(emit, refresh) {
  function render(product){
    return [
      'div', {},
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

function AndProductRenderer(emit, refresh) {
  /**
   * @param {AndProduct} andproduct
   * @returns {*[]}
   */
  function render(andproduct){
    return [
      'div', {},
      [
        'div',
        {
          class: 'product-description'
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

function OrProductRenderer(emit, refresh) {
  /**
   * @param {OrProduct} orproduct
   */
  function render(orproduct) {
    return [
      'div', {},
      [
        'div',
        {
          class: 'product-description'
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
}

function BranchRenderer(emit, refresh) {
  return {
    render: render
  };

  /**
   * @param {Branch} branch
   */
  function render(branch) {
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

function ProductList(emit, refresh) {
  return {
    render: render
  };
  /**
   * @param {Array<Product>} products
   * @returns {*[]}
   */
  function render(products) {
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

function BranchList(emit, refres) {
  return {
    render: render
  };

  /**
   * @param {Array<Branch>} branches
   */
  function render(branches) {
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
