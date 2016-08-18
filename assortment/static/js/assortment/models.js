/**
 * Created by Matthias on 11/04/2016.
 */

import {MiniSignal} from 'bower_components/mini-signals/src/index';

import {SubscribeAble} from 'js/tools/tools';

import dummy_data from 'json/assortment/dummy_db'

import { AssortmentRenderer,
  ProductRenderer,
  AndProductRenderer,
  OrProductRenderer } from 'js/assortment/render';

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
    this.name = name;
    this.value_type = value_type;
    this.labels = new Set();
    this.values = new Map();
    this.assortment = None;
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

  set_assortment(assortment) {
    this.assortment = assortment
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

export class BaseArticle extends SubscribeAble {
  /**
   * @param {Number}                id
   * @param {String}                name
   * @param {Number}                amount
   * @param {Branch}                branch
   * @param {Array<Label>}          labels
   */
  constructor(id, name, amount, branch, labels) {
    super();
    this.id = id;
    this.name = name;
    if(amount !== undefined)
      this._amount = amount;
    this.branch = branch;
    this.labels = labels;
    try {
      this.branch.add_product(this);
      this.labels.forEach(
        (label) =>
          label.add_product(this));
    } catch (e) {

    }
    this.assortment = null;
  }

  fire_event(event){
    this.signal.fire_event(event);
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

  get amount_str() {
    const am = this.amount;
    if (am === 0) {
      return 'none'
    } else if (am < 4) {
      return 'low'
    } else if (am < 10) {
      return 'medium'
    }
    return 'high'
  }

  get renderer() {
    throw Error();
  }

  set_assortment(assortment) {
    this.assortment = assortment
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
        products[__json.id] = new (BaseArticle.to_class(__json.type))(
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

  get amount() {
    return this._amount
  }

  get renderer() {
    return ProductRenderer;
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

  get renderer() {
    return AndProductRenderer;
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

  get renderer() {
    return OrProductRenderer;
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
   * @param {Number} id
   */
  constructor(name, parent_id, id) {
    this.name = String(name);
    this.id = id;
    this.parent_id = parent_id;
    this.parent = null; // reference to the parent tag.
    this._products = [];
    this._children = [];
    this.assortment = null;
    this.value = new Set();
    this._value = new Set();
  }

  get children() {
    return this._children.filter(
      this.assortment.filter_branches
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  get products() {
    return this._products.filter(
      this.assortment.filter_products
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  /**
   * @param {Array<Branch>}         branches: A sparse array of tags, with id as their index.
   */
  post_init(branches) {
    this.parent = branches[this.parent_id];
    if (this.parent) {
      this.parent.add_child(this);
    }
  }

  /**
   * @param {BaseArticle}           product
   */
  add_product(product) {
    this._products.push(product);
  }

  /**
   * @param {Branch}                branch
   */
  add_child(branch) {
    this._children.push(branch);
  }

  set_assortment(assortment) {
    this.assortment = assortment
  }

  /**
   * @param {Array<{id: Number, name: String, parent_id: Number}>} branch_json
   * @returns {Array<Branch>}
   */
  static generate_list(branch_json) {
    let branches = [];

    for (const __json of branch_json) {
      if (__json !== undefined && typeof __json === "object") {
        branches[__json.id] = new Branch(__json.name, __json.parent_id, __json.id)
      } else {
      }
    }

    for (const branch of branches) {
      // this part is needed to get the tree working:
      // Tree lookup with indexes is less efficient than direct pointers,
      // so we switch the numbers to pointers.
      if (branch)
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
 * @prop {String}                   name
 * @prop {String}                   title
 */
export class Assortment {
  /**
   * @param {HTMLElement}           element
   * @param {Array<Product>}        products
   * @param {Array<Branch>}         branches
   * @param {Array<Label>}          labels
   * @param {Array<LabelType>}      label_types
   */
  constructor(element, products=[], branches=[], labels=[], label_types=[]) {
    this.rootElement = element;
    this.name = element.getAttribute('article-tree');
    this.title = element.dataset.title;
    this.query = '';

    this._branches = branches;
    this._branches.forEach((br) => br ? br.set_assortment(this) : void 0);

    this.label_types = label_types;
    this.label_types.forEach((lt) => lt ? lt.set_assortment(this) : void 0);
    this.labels = labels;

    this._products = products;
    this._products.forEach((pr) => pr ? pr.set_assortment(this) : void 0);

    this.filter_branches = (br) => this.branches_set.has(br);
    this.filter_products = (pr) => this.product_set.has(pr);

    this.product_set = new Set(this._products);
    this.branches_set = new Set(this._branches);

    this.dom = domChanger(AssortmentRenderer, element, true);
    let t1 = performance.now();
    this.dom.update(this);
    let t2 = performance.now();
    console.log(`rendering took ${t2 - t1} ms`)
  }

  get branches() {
    return this._branches.filter(
      this.filter_branches
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  get products() {
    return this._products.filter(
      this.filter_products
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  /**
   * @param {Element}                                                      domelement
   * @param {Array<{name: String, tag: Number, label_ids: Array<Number>}>} product_protos
   * @param {Array<{id: Number, name: String, parent_id: Number}>}         branch_protos
   * @param {Array<{
   *            id: Number,
   *            name: String,
   *            type: String,
   *            value_type: String,
   *            labels: {
   *              id: Number,
   *              value: String|Number
   *            }
   *          }>}                                                          label_type_protos
   * @returns {Assortment}
   */
  static generate(domelement, product_protos, branch_protos, label_type_protos) {
    let [label_types, labels] = LabelType.generate_list(label_type_protos);
    const branches = Branch.generate_list(branch_protos);
    const products = Product.generate_list(product_protos, labels, branches);
    const assortment = new Assortment(domelement, products, branches, labels, label_types);
    console.log(assortment);
    return assortment;
  }

  /**
   * @param {Element} domelement
   */
  static create_from_element(domelement){
    let t1 = performance.now();
    if(domelement.dataset.apiEndpoint == "dummy") {
      let label_types = dummy_data.label_types;
      let tags = dummy_data.branches;
      let products = dummy_data.products;

      return Assortment.generate(domelement, products, tags, label_types);
    } else {

      var assortment_api_endpoint = domelement.dataset.apiEndpoint;
      axios.get(`/api/assortment/${assortment_api_endpoint}`)
        .then((response) => {
          var label_types = response.data.label_types;
          var tags = response.data.branches;
          var products = response.data.products;

          Assortment.generate(domelement, products, tags, label_types);
        }).catch(
        (error) => console.error(error)
      )
    }
    let t2 = performance.now();
    console.log(`starting took ${t2 - t1} ms`);
  }

  add_render(branch) {
    if (!branch || this.branches_set.has(branch)) return;
    this.branches_set.add(branch);
    this.add_render(branch.parent);
  }

  /**
   * @param query
   */
  search(query) {
    let t1 = performance.now();
    let strings = [...(new Set(query.split(' ')))];
    this._branches.forEach(
      (br) => {
        if (br) {
          br._value = new Set(
            strings.filter(
              (str) => br.name.match(str)
            )
          );// create a set of all matches it has found, and store it
          br.value = new Set(br._value)
        }
      }
    );
    this._branches.forEach(
      (br) => {
        if (br)
          br._children.forEach(
            (b) => br._value.forEach(
              (v) => b.value.add(v)
            )
          )
      }
    );
    this._branches.forEach(
      (br) => {
        if (br)
          br._products.forEach(
            (p) => p._value = new Set(br.value)
          )
      }
    );
    this._products.forEach(
      (pr) => {
        if (pr) {
          strings.forEach(
            (str) => {
              if (pr.name.match(str))
                pr._value.add(str)
            }
          )
        }
      }
    );
    let go_products = this._products.filter(
      (pr) => pr ? pr._value.size == strings.length : false
    );
    this.product_set = new Set(go_products);
    this.branches_set = new Set();
    go_products.forEach(
      (pr) => this.add_render(pr.branch)
    );
    let t2 = performance.now();
    this.dom.update(this, query.length > 3);
    let t3 = performance.now();
    console.log(`querying took ${t2 - t1} ms, rendering took ${t3 - t2} ms`);

    /*this.query = query;
     axios.get(window.swipe.global.api.assortment)*/

  }
}
