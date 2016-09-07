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

/**
 * The functions in this file are the renderers for domChanger, for various
 * aspects of the Assortment, like products, branches etc.
 */

/**
 * @param emit
 * @param refresh
 * @returns {{render: renderer, hwrender: hwrender}}
 *
 * Partial renderer for product descriptions
 */
function ProductDescription(emit, refresh) {
  /**
   * @type {?BaseArticle}
   */
  return {
    render: renderer,
    hwrender: hwrender
  };
  function renderer(product) {
    let name_dict = draggable('product', product);
    name_dict.class = 'name';
    name_dict.editable = 'false';
    `
    <div class='product-description>
      <span draggable class='name' editable='false'>{{product.name}}</span>
      <span class='amount {{product.amount_str}}'>{{product.amount}}</span>
      <span class='spacer'></span>
      <span class='price'>{{product.price}}</span>
    </div>
    `
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
}

/**
 * @param emit
 * @param refresh
 * @returns {{render: renderer}}
 * Gets rendered in place of items when there are no items in an Branchlist.
 */
function NoItems(emit, refresh) {
  return {
    render: renderer
  };

  function renderer() {
    `
    <div class='tree-list tree-list-info'>
      {% trans 'no contained items' %}
    </div>
    `
    return [
      'div', {
        class: 'tree-list tree-list-info'
      },
      _('no contained items')
    ]
  }
}

/**
 * @param {String} unique_name
 * @param {Boolean} active
 * @returns {*[]}
 *
 * This inserts the toggle option into the article tree. Usage: easy, and no JS
 * required.
 */
function insert_toggle(unique_name, active) {
  `
  <input type='checkbox' class='opening-mechanism' id='{{unique_name}}'
         hidden='true' checked='{{ active }}'>
  <label for='{{unique_name}}' class='opening_mechanism'></label>
  `
  return [
    [
      'input', {
        type: 'checkbox',
        class: 'opening-mechanism',
        id: unique_name,
        hidden: 'true',
        checked: active
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
 *
 * Renderer for normal Products
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
    `
    <div class='product'>
      {% include ProductDescription %}
    </div>
    `
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
 *
 * Renderer for AndProducts
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
    `
    <div class='product and-product'>
      {% include insert_toggle(prefix + '-product-' + andproduct.id) %}
      {% include ProductDescription with product=andproduct %}
      {% include BranchList with products=andproduct.contained_products %}
    </div>
    `
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
 *
 * Renderer for OrProducts
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
    `
    <div class='product or-product'>
      {% include insert_toggle(prefix + '-product-' + orproduct.id) %}
      {% include ProductDescription with product=orproduct %}
      {% include BranchList with products=orproduct.contained_products %}
    </div>
    `
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
 *
 * Renderer for Branches
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
    `
    <div class='branch'>
      {% include insert_toggle(prefix + '-branch-' + branch.id) %}
      <div class="branch-description">
        <span class="name">{{branch.name}}</span>
      </div>
      {% include BranchList with children=branch.children products=branch.products %}
    </div>
    `
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
 *
 * Renders a list of branches and/or products.
 * Used in Branches and And or OrProducts
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
    `
      <div class='tree-list'>
        {% for branch in branches %}{% include BranchRenderer with branch=branch %}{% endfor %}
        {% for product in products %}{% include product.renderer() with product=product %}{% endfor %}
      </div>
    `
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
 *
 * Renderer for Assortments
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
    `
    <div class='assortment-tree'>
      <div class="assortment-header">
        <div class="description">
          {{ assortment.title }}
        </div>
        <div class="search-box">
          <input type="search" id='{{assortment.name}}-search-box'
                 oninput="oninput" placeholder="{% trans 'Search' %}"
                 value='{{ assortment.query }}'>
        </div>
      </div>
      {% include BranchList with branches= *rootbranches* %}
    </div>
    `
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
