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
 * @callback Filter
 * @param {Product} product
 * @returns {Boolean}
 *
 * A filter used to filter the products before the products are put into the
 * assortment.
 */

/**
 * @class {Object}                                      LabelType
 * @prop {String}                                       name
 * @prop {String}                                       value_type
 * @prop {Set<Label>}                                   labels
 * @prop {Map<String|Number, Label>}                    values
 *
 * A label type. Has no use yet, but it's nice to have in front.
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
   *
   * Register a label value to the label type
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
   *
   * create an array of label types from the json-array of proto-labeltypes
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
 * @class {Object}                  Label
 * @prop {String}                   value
 * @prop {LabelType}                label_type
 * @prop {Set<Product>}           products
 *
 * A label, which has a value and an label type.
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
   *
   * Add the product to the label's product registry
   */
  add_product(product) {
    this.products.add(product);
  }

  /**
   * @param {Product}               product
   * @returns {Boolean}
   *
   * Returns whether or not the product has the label. (label has the product)
   */
  has_product(product) {
    return this.products.has(product);
  }
}

/**
 * @type {String}
 *
 * label divider. not currenly in use, but may be used for local search purposes
 */
Label.DIVIDER = ':';

/**
 * @type {String}
 *
 * Label value matcher. Not in use, but for local search
 */
Label.VALUE_MATCHER = '(.+)';

/**
 * @type {String}
 *
 * local search again
 */
Label.MATCHER = LabelType.MATCHER + Label.DIVIDER + Label.VALUE_MATCHER;

/**
 * @class {Object} BaseArticle
 * @prop {Number} id
 * @prop {String} name
 * @prop {Number} amount
 * @prop {Branch} branch
 * @prop {Array<Label>} labels
 * @prop {?Assortment} assortment
 */
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

  get amount() {
    return this._amount;
  }

  /**
   * @param {Event} event
   */
  fire_event(event){
    this.signal.fire_event(event);
  }

  /**
   * @param {String} name
   * @returns {class<BaseArticle>}
   *
   * Get the class related to the name of the class.
   */
  static to_class(name){
    return {
      'OrProductType': OrProduct,
      'AndProductType': AndProduct,
      'ArticleType': Product
    }[name];
  }

  /**
   * @returns {String}
   *
   * Get a string which represents the stock amount, like
   * {high | medium | low | none}
   */
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

  /**
   * @param assortment
   *
   * Set the product's assortment
   */
  set_assortment(assortment) {
    this.assortment = assortment
  }
}

/**
 * @class {BaseArticle}             Product
 * @prop {Number}                   id
 * @prop {String}                   name
 * @prop {Number}                   price
 * @prop {Number}                   amount
 * @prop {Tag}                      branch
 * @prop {Array<Label>}             labels
 *
 * A normal product
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
    this.value = new Set();
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
   *
   * generate products from json
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

  /**
   * @returns {ProductRenderer}
   *
   * Get the rendering function of this product type
   */
  get renderer() {
    return ProductRenderer;
  }
}

/**
 * @class {BaseArticle} AndProduct
 * @prop {Number} price
 * @prop {Array<{product: Product, amount: Number}>} contained_products
 *
 * The JS representation of an And product
 */
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
   *
   * Post-init hook to finalize the data.
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

  /**
   * @returns {AndProductRenderer}
   *
   * get the renderer of this product type
   */
  get renderer() {
    return AndProductRenderer;
  }
}

/**
 * @class {BaseArticle} OrProduct
 * @prop {Array<>} contained_products
 */
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
 * @class {Object}                  Branch
 * @prop {String}                   name
 * @prop {Element}                  node
 * @prop {Number}                   parent_id
 * @prop {?Tag}                     parent
 * @prop {Array<Product>}           _products
 * @prop {Array<Branch>}            _children
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
  }

  /**
   * Gets the currently active children (as filtered required by it's assortment)
   * @returns {Array<Branch>}
   */
  get children() {
    return this._children.filter(
      this.assortment.filter_branches
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  /**
   * Gets the currently active products (as filtered required by it's assortment)
   * @returns {Array<BaseArticle>}
   */
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

  /**
   * @param assortment
   *
   * Set the assortment for this Branch
   */
  set_assortment(assortment) {
    this.assortment = assortment
  }

  /**
   * @param {Array<{id: Number, name: String, parent_id: Number}>} branch_json
   * @returns {Array<Branch>}
   *
   * Generate a list of branches from a json format.
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
 *
 * Not used, but is useful for e.g. offline sorting
 */
Branch.MATCHER = '[a-zA-Z0-9]+';

/**
 * @class {Object}                  Assortment
 * @prop {String}                   query
 * @prop {Array<Branch>}            branches
 * @prop {Array<Label>}             labels
 * @prop {Array<LabelType>}         label_types
 * @prop {String}                   name
 * @prop {String}                   title
 *
 * The main assortment wrapper.
 */
export class Assortment {
  /**
   * @param {HTMLElement}           element
   * @param {Array<Product>}        products
   * @param {Array<Branch>}         branches
   * @param {Array<Label>}          labels
   * @param {Array<LabelType>}      label_types
   * @param {Array<Filter>}         filters
   */
  constructor(element, products=[], branches=[], labels=[], label_types=[], filters=[]) {
    this.rootElement = element;
    this.name = element.getAttribute('article-tree');
    this.title = element.dataset.title;
    this.query = element.dataset.search;

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

    this.filters = filters;

    // Bind the assortment to it's DOM node using domChanger
    this.dom = domChanger(AssortmentRenderer, element, true);
    // initiate the assortment by searching for the specified term or ' '
    // (which does nothing)
    this.search(element.dataset.search || " ");
  }

  /**
   * @returns {Array<Branch>}
   */
  get branches() {
    return this._branches.filter(
      this.filter_branches
    ).sort(
      (a, b) => a.name.localeCompare(b.name)
    );
  }

  /**
   * @returns {Array<BaseArticle>}
   * Get the enclosed products when filtered by the assortment filter
   */
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
   * @param {Array<Filter>}                                                filters
   * @returns {Assortment}
   */
  static generate(domelement, product_protos, branch_protos, label_type_protos, filters) {
    let [label_types, labels] = LabelType.generate_list(label_type_protos);
    const branches = Branch.generate_list(branch_protos);
    const products = Product.generate_list(product_protos, labels, branches);
    const assortment = new Assortment(domelement, products, branches, labels, label_types, filters);
    console.log(assortment);
    return assortment;
  }

  /**
   * @param {Element} domelement
   *
   * Create an assortment from the properties specified by the html element
   */
  static create_from_element(domelement){
    let t1 = performance.now();

    let preset_filters = [];
    if (domelement.dataset.inStore !== undefined)
      preset_filters.push((p) => p.amount > 0);

    if(domelement.dataset.apiEndpoint == "dummy") {
      let label_types = dummy_data.label_types;
      let tags = dummy_data.branches;
      let products = dummy_data.products;

      return Assortment.generate(domelement, products, tags, label_types, preset_filters);
    } else {

      var assortment_api_endpoint = domelement.dataset.apiEndpoint;
      axios.get(`/api/assortment/${assortment_api_endpoint}`)
        .then((response) => {
          var label_types = response.data.label_types;
          var tags = response.data.branches;
          var products = response.data.products;

          Assortment.generate(domelement, products, tags, label_types, preset_filters);
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
   * @param {Branch} branch
   * @param {Array<RegExp>} query
   * @param {Set<RegExp>} found
   * Search the article branch on how many products match the search query
   */
  recursive_search_with_found(branch, query, found) {
    branch.value = new Set(found);
    query.forEach((q) => branch.name.match(q)? branch.value.add(q) :undefined);
    branch._products.forEach((p) => this.search_with_values(p, query, branch.value));
    branch._children.forEach((c) => this.recursive_search_with_values(c, query, branch.value));
  }

  /**
   * @param {BaseArticle} product
   * @param {Array<RegExp>} query
   * @param {Set<RegExp>} found
   * Search the product on how much it matches the search
   */
  search_with_found(product, query, found) {
    product.value = new Set(found);
    query.forEach((q) => product.name.match(q)? product.value.add(q) :undefined);
  }

  /**
   * @param {String} query
   * Search the assortment on products, and display it in the dom.
   */
  search(query) {
    this.query = query;
    let t1 = performance.now();
    let vals = [...(new Set(query.split(' ')))];
    let regexes = vals.map((str) => new RegExp(str, "gui"));
    this.recursive_search_with_values(
      this._branches.find(
        (br) => br !== undefined && !br.parent // = root node
      ), regexes, new Set()
    );
    let go_products = this._products.filter(
      (pr) => pr !== undefined && pr.value.size == regexes.length
    );
    for (let filter of this.filters) {
      go_products = go_products.filter(filter);
    }
    this.product_set = new Set(go_products);
    this.branches_set = new Set();
    go_products.forEach(
      (pr) => this.add_render(pr.branch)
    );
    let t2 = performance.now();
    this.dom.update(this, this.query.length > 3);
    let t3 = performance.now();
    console.log(`querying took ${t2 - t1} ms, rendering took ${t3 - t2} ms`);

    /*this.query = query;
     axios.get(window.swipe.global.api.assortment)*/

  }

  /**
   * refresh the DOM
   */
  refresh() {
    this.dom.update(this, this.query.length > 3)
  }
}
