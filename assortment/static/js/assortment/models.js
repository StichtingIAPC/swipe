/**
 * Created by Matthias on 11/04/2016.
 */

import {SubscribeAble} from 'js/tools/tools'
import {FilterSet} from './filters';

/**
 * @class {LabelType}                                   LabelType
 * @prop {string}                                       name
 * @prop {string}                                       value_type
 * @prop {Set<Label>}                                   labels
 * @prop {Map<string|number, Label>}                    values
 */
export class LabelType {
  /**
   * @param {string} name
   * @param {string} value_type
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
   *    id: number,
   *    name: string,
   *    type: string,
   *    value_type: string
   *  }>} label_type_json
   * @returns {Array<LabelType>}
   */
  static generate_list(label_type_json) {
    let label_types = [];

    for (let i = 0; i < label_type_json.length; i++) {
      let __json = label_type_json[i];

      if (__json !== 'undefined' && typeof(__json) === "object") {
        label_types[__json.id] = new LabelType(__json.name, __json.value_type);
      }
    }

    return label_types;
  }
}

/**
 * @type {string}
 */
LabelType.MATCHER = '([a-zA-Z0-9]+)'; // currently only alphanumericals are supported as label names

/**
 * @class {Label}                   Label
 * @prop {string}                   value
 * @prop {LabelType}                label_type
 * @prop {Set<Product>}           products
 */
export class Label {
  /**
   * @param {string}                value
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

  /**
   * @param {Array<{value: string, type: string, id: number}>}  label_json
   * @param {Array<LabelType>}                                  label_types
   * @returns {Array<Label>}
   */
  static generate_list(label_json, label_types) {
    let labels = [];

    for (let i = 0; i < label_json.length; i++) {
      let __json = label_json[i];
      if (__json !== 'undefined' && typeof(__json) === "object") {
        let type = label_types[__json.type];
        let label = new Label(__json.value, type);
        labels[__json.id] = label;
        type.register(label);
      }
    }

    return labels;
  }
}

/**
 * @type {string}
 */
Label.DIVIDER = ':';

/**
 * @type {string}
 */
Label.VALUE_MATCHER = '(.+)';

/**
 * @type {string}
 */
Label.MATCHER = LabelType.MATCHER + Label.DIVIDER + Label.VALUE_MATCHER;

class BaseArticle extends SubscribeAble {
  /**
   * @param {number}                id
   * @param {string}                name
   * @param {number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, amount, branch, labels) {
    this.id = id;
    this.name = name;
    this.amount = amount;
    this.branch = branch;
    this.labels = labels;

    this.branch.add_product(this);
    this.labels.forEach(
      (label, index) =>
        label.add_product(this));
  }

  /**
   * @param {string} name
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
 * @prop {number}                   id
 * @prop {string}                   name
 * @prop {number}                   price
 * @prop {number}                   amount
 * @prop {Tag}                      branch
 * @prop {Array<Label>}             labels
 */
export class Product extends BaseArticle {
  /**\
   * @param {number}                id
   * @param {string}                name
   * @param {number}                price
   * @param {number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, price, amount, branch, labels) {
    super(id, name,amount, branch, labels);
    this.price = price;
  }

  /**
   * @param {Array<{
   *    type: string,
   *    id: number,
   *    name: string,
   *    price: ?number,
   *    amount: ?number,
   *    branch: number,
   *    label_ids: Array<number>,
   *    contained_products: ?Array<number>,
   *    components: ?Array<{product: number, amount: number}>
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
   * @param {number} id
   * @param {string} name
   * @param {number} price
   * @param {null} amount
   * @param {Branch} branch
   * @param {Array<Label>} labels
   * @param {Array<{product: number, amount: number}>} components
   */
  constructor(id, name, price, amount=null, branch, labels, components) {
    super(id, name, amount, branch, labels);
    this.price = price;
    this.contained_products = [];
    components.forEach(
      (component) -> this.contained_products.push(
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
      (component) -> component.product = assortment.products[component.product]
    );
  }

  /**
   * @returns {number}
   */
  get amount() {
    let min_amount = Infinity;
    this.contained_products.forEach(
      (component) -> min_amount = Math.min(
        min_amount,
        component.product.amount / component.amount
      )
    );
    return min_amount;
  }
}

export class OrProduct extends BaseArticle {
  /**
   * @param {number} id
   * @param {string} name
   * @param {null} price
   * @param {null} amount
   * @param {Branch} branch
   * @param {Array<Label>} labels
   * @param {Array<number>} contained_products
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
      (id) -> assortment.products[id]
    )
  }

  /**
   * @returns {number}
   */
  get amount() {
    let amount = 0;
    this.contained_products.forEach((product) -> amount += product.amount);
    return amount;
  }
}

/**
 * @type {string}
 */
Product.MATCHER = '(.+)';

/**
 * @class {Branch}                  branch
 * @prop {string}                   name
 * @prop {Element}                  node
 * @prop {number}                   parent_id
 * @prop {?Tag}                     parent
 * @prop {Array<Product>}           products
 * @prop {Array<Tag>}               children
 */
export class Branch extends RenderAble {
  /**
   *
   * @param {string} name
   * @param {number} parent_id
   */
  constructor(name, parent_id) {
    super();
    this.name = string(name);
    this.node = null; // this is a reference to the DOMElement that represents
                      // the branch in the tree generated from this tag.
    this.parent_id = parent_id;
    this.parent = null; // reference to the parent tag.
    this.products = [];
    this.children = [];
  }

  /**
   * @param {Array<Branch>}            tags: A sparse array of tags, with id as their index.
   */
  post_init(tags) {
    this.parent = tags[this.parent_id];
    this.parent.add_child(this);
  }

  /**
   * @param {Product}               product
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
   * @param {Array<{id: number, name: string, parent_id: number}>} tag_json
   * @returns {Array<Branch>}
   */
  static generate_list(tag_json) {
    let tags = [];

    for (let i = 0; i < tag_json.length; i++) {
      let __json = tag_json[i];

      if (__json !== 'undefined' && typeof(__json) === "object") {
        tags[__json.id] = new Branch(__json.name, __json.parent_id)
      }
    }

    for (let tag of tags)
      tag.post_init(tags);

    return tags;
  }
}

/**
 * @type {string}
 */
Branch.MATCHER = '[a-zA-Z0-9]+';

/**
 * @class Assortment
 * @prop {string}                   query
 * @prop {Array<Tag>}               tags
 * @prop {Array<Label>}             labels
 * @prop {Array<LabelType>}         label_types
 * @prop {FilterSet}                filter
 */
export class Assortment {
  /**
   * @param {HTMLElement}           element
   * @param {Array<Product>}        products
   * @param {Array<Branch>}         tags
   * @param {Array<Label>}          labels
   * @param {Array<LabelType>}      label_types
   */
  constructor(element, products, tags, labels, label_types) {
    super();
    this.name = element.dataset.name;
    this.rootElement = element;
    this.query = '';
    this.tags = tags;
    this.labels = labels;
    this.label_types = label_types;
    this.products = products;
    this.filter = new FilterSet(this.query, this);
  }

  /**
   *
   * @param {Array<{name: string, tag: number, label_ids: Array<number>}>}        product_protos
   * @param {Array<{id: number, name: string, parent_id: number}>}                tag_protos
   * @param {Array<{value: string, type: string, id: number}>}                    label_protos
   * @param {Array<{id: number, name: string, type: string, value_type: string}>} label_type_protos
   * @returns {Assortment}
   */
  static generate(product_protos, tag_protos, label_protos, label_type_protos) {
    let label_types = LabelType.generate_list(label_type_protos);
    let labels = Label.generate_list(label_protos, label_types);
    let tags = Branch.generate_list(tag_protos);
    let products = Product.generate_list(product_protos, labels, tags);
    return new Assortment(products, tags, labels, label_types);
  }

  /**
   * @param query
   */
  search(query) {
    this.filter.update(query);
  }
}
