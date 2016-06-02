/**
 * Created by Matthias on 11/04/2016.
 */

import {
  Assortment,
  Branch,
  Label,
  LabelType,
  Product
} from './models'

/**
 * @class {Filter}                  Filter
 */
class Filter {
  /**
   * @param {ResultMap}             resultset
   */
  append_to(resultset) {
    // to be implemented by subclasses
  }

  /**
   * @param {ResultMap}             resultset
   */
  remove_from(resultset) {
    // to be implemented by subclass
  }

  /**
   * @param {Array<String>}         queries
   * @param {Assortment}            assortment
   */
  static generate(queries, assortment) {
    throw "This function is to be implemented by the subclass, with the same arguments"
  }

  /**
   *
   * @param {Array<String>} queries
   * @param {String} regex
   */
  static filter_queries(queries, regex) {
    var reg = new RegExp('^' + regex + '$');
    return queries.filter(q => q.matches(reg));
  }
}

/**
 * @type {string}
 */
Filter.NEGATOR = '!';

export class TagFilter extends Filter {
  /**
   * @param {Array<Branch>} tags
   * @param {Array<*>} args
   */
  constructor(tags, ...args) {
    super(...args);
    this.tags = tags;
  }

  /**
   * @param {ResultMap}             resultset
   */
  append_to(resultset) {
    for (let t of this.tags)
      resultset.tags.add(t);
  }

  /**
   * @param {ResultMap}             resultset
   */
  remove_from(resultset) {
    for (let t of this.tags)
      resultset.tags.delete(t)
  }

  /**
   * @param {Array<String>}         queries
   * @param {Assortment}            assortment
   * @returns {Array<TagFilter>}
   */
  static make_pos_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Branch.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let t of assortment.tags) {
        if (t.name.matches(q)) {
          matches.push(t);
        }
      }
      if (matches.length > 0)
        ret.push(new TagFilter(matches));
    }
    return ret;
  }

  static make_neg_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Filter.NEGATOR + Branch.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let t of assortment.tags) {
        if ((Filter.NEGATOR + t.name).matches(q)) {
          matches.push(t);
        }
      }

      if (matches.length > 0)
        ret.push(new TagFilter(matches));
    }
    return ret;
  }
}

/**
 * @class {LabelFilter}             LabelFilter
 * @prop {Array<Label>}             labels
 */
export class LabelFilter extends Filter {
  /**
   * @param {Array<Label>} labels
   * @param {Array<*>} args
   */
  constructor(labels, ...args) {
    super(...args);
    this.labels = labels;
  }

  /**
   * @param {ResultMap}             resultset
   */
  append_to(resultset) {
    for (let l of this.labels)
      resultset.labels.add(l);
  }

  /**
   * @param {ResultMap}             resultset
   */
  remove_from(resultset) {
    for (let l of this.labels)
      resultset.labels.delete(l)
  }


  /**
   * @param {Array<String>}         queries
   * @param {Assortment}            assortment
   * @returns {Array<LabelFilter>}
   */
  static make_pos_filters(queries, assortment) {
    // Lets assume that the query is done in the way of ('name:value[type]'), such as ('length:20m'), or ('socket:LGA1151[]'))
    var ret = [];
    queries = Filter.filter_queries(queries, Label.MATCHER);
    for (var query of queries) {
      var matching_labels = assortment.labels.filter(l => l.name.matches(query));
      if (matching_labels.length > 0)
        ret.push(new LabelFilter(matching_labels));
    }
    return ret;
  }

  static make_neg_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Filter.NEGATOR + Label.MATCHER);
    for (var query of queries) {
      var matches = assortment.labels.filter(l => l.name.matches(query));
      if (matches.length > 0)
        ret.push(new LabelFilter(matches))
    }
  }
}

/**
 * @class {LabelTypeFilter}         LabelTypeFilter
 */
export class LabelTypeFilter extends Filter {
  /**
   * @param {Array<LabelType>} label_types
   * @param {Array<*>} args
   */
  constructor(label_types, ...args) {
    super(...args);
    this.label_types = label_types;
  }

  /**
   * @param {ResultMap}             resultset
   */
  append_to(resultset) {
    for (let l of this.label_types)
      resultset.label_types.add(l);
  }

  /**
   * @param {ResultMap}             resultset
   */
  remove_from(resultset) {
    for (let l of this.label_types)
      resultset.label_types.delete(l)
  }

  /**
   * @param {Array<String>}         queries
   * @param {Assortment}            assortment
   * @returns {Array<LabelTypeFilter>}
   */
  static make_pos_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, LabelType.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let l of assortment.label_types) {
        if (l.name.matches(q)) {
          matches.push(l);
        }
      }

      if (matches.length > 0) {
        ret.push(new LabelTypeFilter(matches));
      }
    }
    return ret;
  }

  static make_neg_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Filter.NEGATOR + LabelType.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let l of assortment.label_types) {
        if (('!' + l.name).matches(q)) {
          matches.push(l);
        }
      }

      if (matches.length > 0) {
        ret.push(new LabelTypeFilter(matches));
      }
    }
    return ret;
  }
}

/**
 * @class {ProductFilter}           ProductFilter
 * @prop {Array<Product>}           products
 */
export class ProductFilter extends Filter {
  /**
   * @param products
   * @param {Array<*>} args
   */
  constructor(products, ...args) {
    super(...args);
    this.products = products;
  }

  /**
   * @param {ResultMap}             resultset
   */
  append_to(resultset) {
    for (let l of this.products)
      resultset.products.add(l);
  }

  /**
   * @param {ResultMap}             resultset
   */
  remove_from(resultset) {
    for (let l of this.products)
      resultset.products.delete(l)
  }

  /**
   * @param {Array<String>}         queries
   * @param {Assortment}            assortment
   * @returns {Array<ProductFilter>}
   */
  static make_pos_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Product.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let p of assortment.products) {
        if (p.name.matches(q)) {
          matches.push(p);
        }
      }

      if (matches.length > 0) {
        ret.push(new ProductFilter(matches));
      }
    }
    return ret;
  }

  static make_neg_filters(queries, assortment) {
    var ret = [];
    queries = Filter.filter_queries(queries, Filter.NEGATOR + Product.MATCHER);
    for (var q of queries) {
      var matches = [];

      for (let p of assortment.products) {
        if (p.name.matches(q)) {
          matches.push(p)
        }
      }

      if (matches.length > 0) {
        ret.push(new ProductFilter(matches))
      }
    }
  }
}

/**
 * @class {FilterSet} FilterSet
 * @prop {String}                   query
 * @prop {Assortment}               assortment
 */
export class FilterSet {
  constructor(query, assortment) {
    this.assortment = assortment;
    this.update(query);
  }

  /**
   * @param {String}                query
   */
  update(query) {
    var queries = FilterSet.tokenify(query);
    this.queries = queries;
    this.tagfilters = TagFilter.make_pos_filters(queries, this.assortment);
    this.labelfilters = LabelFilter.make_pos_filters(queries, this.assortment);
    this.label_typefilters = LabelTypeFilter.make_pos_filters(queries, this.assortment);
    this.productfilters = ProductFilter.make_pos_filters(queries, this.assortment);

    this.neg_tagfilters = TagFilter.make_neg_filters(queries, this.assortment);
    this.neg_labelfilters = LabelFilter.make_neg_filters(queries, this.assortment);
    this.neg_label_typefilters = LabelTypeFilter.make_neg_filters(queries, this.assortment);
    this.neg_productfilters = ProductFilter.make_neg_filters(queries, this.assortment);
  }

  static tokenify(query) {
    return query.split(' ').filter(s => s !== ''); // break up the query at spaces, and filter out all the empty strings.
  }

  /**
   * @returns {ResultMap}
   */
  generate_result() {
    let result = new ResultMap(this.assortment);
    this.tagfilters.forEach((tag_filter, index) => tag_filter.append_to(result));
    this.neg_tagfilters.forEach((neg_tag_filter, index) => neg_tag_filter.remove_from(result));
    this.labelfilters.forEach((labelfilter, index) => labelfilter.append_to(result));
    this.neg_labelfilters.forEach((labelfilter, index) => labelfilter.remove_from(result));
    this.label_typefilters.forEach((label_typefilter, index) => label_typefilter.append_to(result));
    this.neg_label_typefilters.forEach((label_typefilter, index) => label_typefilter.remove_from(result));
    this.productfilters.forEach((productfilter, index) => productfilter.append_to(result));
    this.neg_productfilters.forEach((productfilter, index) => productfilter.remove_from(result));
    return result;
  }
}

/**
 * @class {ResultMap}               ResultSet
 * @prop {Map<Tag, Number>}         tags
 * @prop {Map<Label, Number>}       labels
 * @prop {Map<LabelType, Number>}   label_types
 * @prop {Map<Product, Number>}     products
 */
export class ResultMap {
  /**
   * @param {Assortment}            assortment
   */
  constructor(assortment) {
    this.tags = new Map();
    this.labels = new Map();
    this.label_types = new Map();
    this.products = new Map();
  }
}
