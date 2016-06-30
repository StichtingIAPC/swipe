/**
 * Created by Matthias on 11/04/2016.
 */

import {MiniSignal} from 'bower_components/mini-signals/src/index';

import {SubscribeAble} from 'js/tools/tools';

import {AssortmentRenderer} from './render';

/**
 * @class {LabelType}                                   LabelType
 * @prop {String}                                       name
 * @prop {String}                                       value_type
 * @prop {Set<Label>}                                   labels
 * @prop {Map<String|Number, Label>}                    values
 */
export class LabelType {
  /**
   * @param {String} name
   * @param {String} value_type
   */
  constructor(name, value_type) {
    super();
    this.name = name;
    this.value_type = value_type;
    this.labels = new Set();
    this.values = new Map();
  }

  /**
   * @param {Label} label
   */
  register(label) {
    this.labels.add(label);
    this.values.set(label.value, label);
  }

  /**
   * @param {Array<{
   *    id: Number,
   *    name: String,
   *    type: String,
   *    value_type: String
   *    labels: Array<{id: Number, value: String|Number}>
   *  }>} label_type_json
   * @returns {Array<LabelType>}
   */
  static generate_list(label_type_json) {
    let label_types = [];
    let labels = [];

    for (const __json of label_type_json) {
      if (__json !== undefined && typeof __json === "object") {
        const id = __json.id;
        label_types[id] = new LabelType(__json.name, __json.value_type);
        for (const __label of __json.labels) {
          labels[__label.id] = new Label(__label.value, label_types[id]);
        }
      }
    }

    return label_types;
  }
}

/**
 * @type {String}
 */
LabelType.MATCHER = '([a-zA-Z0-9]+)'; // currently only alphanumericals are supported as label names

/**
 * @class {Label}                   Label
 * @prop {String}                   value
 * @prop {LabelType}                label_type
 * @prop {Set<Product>}           products
 */
export class Label {
  /**
   * @param {String}                value
   * @param {LabelType}             type
   */
  constructor(value, type) {
    super();
    this.value = value;
    this.label_type = type;
    this.products = new Set();
  }

  /**
   * @param {Product}               product
   */
  add_product(product) {
    this.products.add(product);
  }

  /**
   * @param {Product}               product
   * @returns {Boolean}
   */
  has_product(product) {
    return this.products.has(product);
  }
}

/**
 * @type {String}
 */
Label.DIVIDER = ':';

/**
 * @type {String}
 */
Label.VALUE_MATCHER = '(.+)';

/**
 * @type {String}
 */
Label.MATCHER = LabelType.MATCHER + Label.DIVIDER + Label.VALUE_MATCHER;

class BaseArticle extends SubscribeAble {
  /**
   * @param {Number}                id
   * @param {String}                name
   * @param {Number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, amount, branch, labels) {
    this.id = id;
    this.name = name;
    this.amount = amount;
    this.branch = branch;
    this.labels = labels;

    this.click = new MiniSignal();
    this.change = new MiniSignal();

    this.branch.add_product(this);
    this.labels.forEach(
      (label, index) =>
        label.add_product(this));
  }

  /**
   * @param {String} name
   * @returns {class<BaseArticle>}
   */
  static to_class(name){
    return {
      'OrProductType': OrProduct,
      'AndProductType': AndProduct,
      'ArticleType': Product
    }[name];
  }
}

/**
 * @class {Product}                 Product
 * @prop {Number}                   id
 * @prop {String}                   name
 * @prop {Number}                   price
 * @prop {Number}                   amount
 * @prop {Tag}                      branch
 * @prop {Array<Label>}             labels
 */
export class Product extends BaseArticle {
  /**\
   * @param {Number}                id
   * @param {String}                name
   * @param {Number}                price
   * @param {Number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, price, amount, branch, labels) {
    super(id, name,amount, branch, labels);
    this.price = price;
  }

  /**
   * @param {Array<{
   *    type: String,
   *    id: Number,
   *    name: String,
   *    price: ?Number,
   *    amount: ?Number,
   *    branch: Number,
   *    label_ids: Array<Number>,
   *    contained_products: ?Array<Number>,
   *    components: ?Array<{product: Number, amount: Number}>
   *      }>} product_json
   * @param {Array<Label>}          labels
   * @param {Array<Branch>}         branches
   * @returns {Array<Product>}
   */
  static generate_list(product_json, labels, branches) {
    let products = [];

    for (let i = 0; i < product_json.length; i++) {
      let __json = product_json[i];

      if (__json !== 'undefined' && typeof(__json) === "object") {
        products[__json.id] = new BaseArticle.to_class[__json.type](
          __json.id,
          __json.name,
          __json.price,
          __json.amount,
          branches[__json.branch],
          __json.label_ids.filter(id => labels[id]).map(id => labels[id]),
          __json.contained_products || __json.components
        )
      }
    }

    return products;
  }
}

export class AndProduct extends BaseArticle {
  /**
   * @param {Number} id
   * @param {String} name
   * @param {Number} price
   * @param {null} amount
   * @param {Branch} branch
   * @param {Array<Label>} labels
   * @param {Array<{product: Number, amount: Number}>} components
   */
  constructor(id, name, price, amount=null, branch, labels, components) {
    super(id, name, amount, branch, labels);
    this.price = price;
    this.contained_products = [];
    components.forEach(
      (component) => this.contained_products.push(
        {product: component.product|0, amount: component.amount}
      )
    );
  }

  /**
   * @param {Assortment} assortment
   */
  post_init(assortment) {
    super.post_init();
    this.contained_products = this.contained_products.forEach(
      (component) => component.product = assortment.products[component.product]
    );
  }

  /**
   * @returns {Number}
   */
  get amount() {
    let min_amount = Infinity;
    this.contained_products.forEach(
      (component) => min_amount = Math.min(
        min_amount,
        component.product.amount / component.amount
      )
    );
    return min_amount;
  }
}

export class OrProduct extends BaseArticle {
  /**
   * @param {Number} id
   * @param {String} name
   * @param {null} price
   * @param {null} amount
   * @param {Branch} branch
   * @param {Array<Label>} labels
   * @param {Array<Number>} contained_products
   */
  constructor(id, name, price=null, amount=null, branch, labels, contained_products) {
    super(id, name, amount, branch, labels);
    this.contained_products = contained_products;
  }

  /**
   * @param {Assortment} assortment
   */
  post_init(assortment) {
    super.post_init();
    this.contained_products = this.contained_products.map(
      (id) => assortment.products[id]
    )
  }

  /**
   * @returns {Number}
   */
  get amount() {
    let amount = 0;
    this.contained_products.forEach((product) => amount += product.amount);
    return amount;
  }
}

/**
 * @type {String}
 */
Product.MATCHER = '(.+)';

/**
 * @class {Branch}                  branch
 * @prop {String}                   name
 * @prop {Element}                  node
 * @prop {Number}                   parent_id
 * @prop {?Tag}                     parent
 * @prop {Array<Product>}           products
 * @prop {Array<Tag>}               children
 */
export class Branch {
  /**
   *
   * @param {String} name
   * @param {Number} parent_id
   */
  constructor(name, parent_id) {
    super();
    this.name = String(name);
    this.node = null; // this is a reference to the DOMElement that represents
                      // the branch in the tree generated from this tag.
    this.parent_id = parent_id;
    this.parent = null; // reference to the parent tag.
    this.products = [];
    this.children = [];
  }

  /**
   * @param {Array<Branch>}         tags: A sparse array of tags, with id as their index.
   */
  post_init(tags) {
    this.parent = tags[this.parent_id];
    this.parent.add_child(this);
  }

  /**
   * @param {BaseArticle}           product
   */
  add_product(product) {
    this.products.push(product);
  }

  /**
   * @param {Branch}                   tag
   */
  add_child(tag) {
    this.children.push(tag);
  }

  /**
   * @param {Array<{id: Number, name: String, parent_id: Number}>} branch_json
   * @returns {Array<Branch>}
   */
  static generate_list(branch_json) {
    let branches = [];

    for (const __json of branch_json) {
      if (__json !== undefined && typeof __json === "object") {
        branches[__json.id] = new Branch(__json.name, __json.parent_id)
      }
    }

    for (const branch of branches) {
      // this part is needed to get the tree working:
      // Tree lookup with indexes is less efficient than direct pointers,
      // so we switch the numbers to pointers.
      branch.post_init(branches);
    }

    return branches;
  }
}

/**
 * @type {String}
 */
Branch.MATCHER = '[a-zA-Z0-9]+';

/**
 * @class Assortment
 * @prop {String}                   query
 * @prop {Array<Branch>}            branches
 * @prop {Array<Label>}             labels
 * @prop {Array<LabelType>}         label_types
 */
export class Assortment {
  /**
   * @param {HTMLElement}           element
   * @param {Array<Product>}        products
   * @param {Array<Branch>}         branches
   * @param {Array<Label>}          labels
   * @param {Array<LabelType>}      label_types
   */
  constructor(element, products, branches, labels, label_types) {
    super();
    this.rootElement = element;
    this.name = element.dataset.name;
    this.query = '';
    this.branches = branches;
    this.labels = labels;
    this.label_types = label_types;
    this.products = products;

    this.dom = domUpdater(AssortmentRenderer, element.firstElementChild);
    this.dom.update(this);
  }

  /**
   * @param {Element}                                                             domelement
   * @param {Array<{name: String, tag: Number, label_ids: Array<Number>}>}        product_protos
   * @param {Array<{id: Number, name: String, parent_id: Number}>}                tag_protos
   * @param {Array<{
   *            id: Number,
   *            name: String,
   *            type: String,
   *            value_type: String,
   *            labels: {
   *              id: Number,
   *              value: String|Number
   *            }
   *          }>} label_type_protos
   * @returns {Assortment}
   */
  static generate(domelement, product_protos, tag_protos, label_type_protos) {
    let [label_types, labels] = LabelType.generate_list(label_type_protos);
    let tags = Branch.generate_list(tag_protos);
    let products = Product.generate_list(product_protos, labels, tags);
    return new Assortment(domelement, products, tags, labels, label_types);
  }

  /**
   * @param {Element} domelement
   */
  static create_from_element(domelement){
    var assortment_api_endpoint = domelement.dataset.apiEndpoint;
    axios.get(`/api/assortment/${assortment_api_endpoint}`)
      .then((response) => {
        var label_types = response.data.label_types;
        var tags = response.data.tags;
        var products = response.data.products;

        Assortment.generate(domelement, products, tags, label_types);
      }).catch(
        (error) => console.error(error)
      )
  }

  /**
   * @param query
   */
  search(query) {
    this.query = query;
    axios.get(window.swipe.global.api.assortment)
  }
}
