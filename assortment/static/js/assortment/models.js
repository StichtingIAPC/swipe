/**
 * Created by Matthias on 11/04/2016.
 */

import {
  SubscribeAble,
  RenderAble
} from 'js/www/tools/tools';

import {FilterSet} from './filters';

/**
 * @class {LabelType}                                   LabelType
 * @prop {String}                                       name
 * @prop {String}                                       value_type
 * @prop {Array<Label>}                                 labels
 * @prop {(Object<String,Label>|Object<Number,Label>)}  values
 */
export class LabelType extends SubscribeAble {
  /**
   * @param {String} name
   * @param {String} value_type
   */
  constructor(name, value_type) {
    super();
    this.name = name;
    this.value_type = value_type;
    this.labels = [];
    this.values = {};
  }

  /**
   * @param label {Label}
   */
  register(label) {
    this.labels.push(label);
    this.values[label.value] = label;
  }

  /**
   * @param {Array<{id: Number, name: String, type: String, value_type: String}>} label_type_json
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
 * @type {String}
 */
LabelType.MATCHER = '([a-zA-Z0-9]+)'; // currently only alphanumericals are supported as label names

/**
 * @class {Label}                   Label
 * @prop {String}                   value
 * @prop {LabelType}                label_type
 * @prop {Array<Product>}           products
 */
export class Label extends RenderAble {
  /**
   * @param {String}                value
   * @param {LabelType}             type
   */
  constructor(value, type) {
    super();
    this.value = value;
    this.label_type = type;
    this.products = [];
  }

  /**
   * @param {Product}               product
   */
  add_product(product) {
    this.products.push(product);
  }

  /**
   * @param {Product}               product
   * @returns {boolean}
   */
  has_product(product) {
    return this.products.includes(product);
  }

  /**
   * @param {Array<{value: String, type: String, id: Number}>}  label_json
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

/**
 * @class {Product}                 Product
 * @prop {Number}                   id
 * @prop {String}                   name
 * @prop {Number}                   price
 * @prop {Number}                   amount
 * @prop {Tag}                      branch
 * @prop {Array<Label>}             labels
 */
export class Product extends RenderAble {
  /**\
   * @param {Number}                id
   * @param {String}                name
   * @param {Number}                price
   * @param {Number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, price, amount, branch, labels) {
    super();
    this.id = id;
    this.name = name;
    this.price = price;
    this.amount = amount;
    this.branch = branch;

    this.labels = labels;
    this.branch.add_product(this);
    this.labels.forEach((a, i) => a.add_product(this));
  }

  /**
   * @param {Array<{id: Number, name: String, price: Number, branch: Number, label_ids: Array<Number>}>} product_json
   * @param {Array<Label>}          labels
   * @param {Array<Branch>}         tags
   * @returns {Array<Product>}
   */
  static generate_list(product_json, labels, tags) {
    let products = [];

    for (let i = 0; i < product_json.length; i++) {
      let __json = product_json[i];

      if (__json !== 'undefined' && typeof(__json) === "object") {
        products[__json.id] = new Product(
          __json.id,
          __json.name,
          __json.price,
          __json.amount,
          tags[__json.branch],
          __json.label_ids.filter(id => labels[id]).map(id => labels[id])
        )
      }
    }

    return products;
  }
}

/**
 * @type {string}
 */
Product.MATCHER = '.+';

/**
 * @class {Branch}                  branch
 * @prop {String}                   name
 * @prop {Element}                  node
 * @prop {Number}                   parent_id
 * @prop {?Tag}                     parent
 * @prop {Array<Product>}           products
 * @prop {Array<Tag>}               children
 */
export class Branch extends RenderAble {
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
   * @param {Array<{id: Number, name: String, parent_id: Number}>} tag_json
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
 * @prop {String}                   query
 * @prop {Array<Tag>}               tags
 * @prop {Array<Label>}             labels
 * @prop {Array<LabelType>}         label_types
 * @prop {FilterSet}                filter
 */
export class Assortment extends SubscribeAble {
  /**
   * @param {Array<Product>}        products
   * @param {Array<Branch>}            tags
   * @param {Array<Label>}          labels
   * @param {Array<LabelType>}      label_types
   */
  constructor(products, tags, labels, label_types) {
    super();
    this.query = '';
    this.tags = tags;
    this.labels = labels;
    this.label_types = label_types;
    this.products = products;
    this.filter = new FilterSet(this.query, this);
  }

  /**
   *
   * @param {Array<{name: String, tag: Number, label_ids: Array<Number>}>}        product_protos
   * @param {Array<{id: Number, name: String, parent_id: Number}>}                tag_protos
   * @param {Array<{value: String, type: String, id: Number}>}                    label_protos
   * @param {Array<{id: Number, name: String, type: String, value_type: String}>} label_type_protos
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
