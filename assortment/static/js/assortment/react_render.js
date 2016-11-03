function toggle_insert(identifier, active) {
  return [
    <input
      type="checkbox"
      class="opening-mechanism"
      id={identifier}
      checked={active}/>,
    <label
      for={identifier}
      class="opening_mechanism"/>
  ]
}


export class ProductDescription extends React.Component {
  constructor({product}) {
    super({product});
    this.product = product;
  }

  get_amount_class() {
    return `amount ${this.product.amount_str}`
  }

  render() {
    return (
      <div class="product-description">
        <span draggable class="name" editable="false">{this.product.name}</span>
        <span class={this.get_amount_class()}>{this.product.amount}</span>
        <span class="spacer"/>
        <span class="price">{this.product.price}</span>
      </div>
    );
  }
}

export class ProductRenderer extends React.Component {
  constructor({product}) {
    super({product});
    this.product = product;
  }

  render() {
    return (
      <div class="product">
        <ProductDescription product={this.product}/>
      </div>
    )
  }
}

export class AndProductRenderer extends React.Component {
  constructor({andproduct, open, prefix}) {
    super({andproduct, open, prefix});
    this.product = andproduct;
    this.open = open;
    this.prefix = prefix;
  }

  render() {
    return (
      <div class="product and-product">
        {toggle_insert(`${this.prefix}-product-${this.product.id}`, this.open)}
        <ProductDescription product={this.product}/>
        <BranchList
            open={this.open}
            prefix={this.prefix}
            branches={[]}
            products={this.product.products}/>
      </div>
    )
  }
}

export class OrProductRenderer extends React.Component {
  constructor({orproduct, open, prefix}) {
    super({orproduct, open, prefix});
    this.product = orproduct;
    this.open = open;
    this.prefix = prefix;
  }

  render() {
    return (
      <div class="product or-product">
        {toggle_insert(`${this.prefix}-product-${this.product.id}`, this.open)}
        <ProductDescription product={this.product}/>
        <BranchList
            open={this.open}
            prefix={this.prefix}
            branches={[]}
            products={this.product.products}/>
      </div>
    )
  }
}

export class BranchRenderer extends React.Component {
  constructor({branch, open, prefix}) {
    super({branch});
    this.branch = branch;
    this.open = open;
    this.prefix = prefix;
  }

  render() {
    return (
      <div class="branch">
        {toggle_insert(`${this.prefix}-branch-${this.branch.id}`, this.open)}
        <div class="branch-description">
          <span class="name">{this.branch.name}</span>
        </div>
        <BranchList
            open={this.open}
            prefix={this.prefix}
            branches={this.branch.branches}
            products={this.branch.products}/>
      </div>
    )
  }
}


export class NoItems extends React.Component {
  render() {
    return (
      <div class="tree-list tree-list-info">
        {'no contained items'}
      </div>
    )
  }
}


export class BranchList extends React.Component {
  constructor({branches, products}) {
    super({branches, products});
    this.branches = branches;
    this.products = products;
  }

  render() {
    if (this.branches.length + this.products.length === 0)
      return <NoItems/>;

    const branches = this.branches.map(
      (branch) =>
        <BranchRenderer
            key={'branch_' + branch.id}
            branch={branch}/>);

    const products = this.products.map(
      (product) =>
        <product.renderer
            key={'product_' + product.id}
            product={product}/>);

    return (
      <div class="tree-list">
        {branches}
        {products}
      </div>
    )
  }
}

export class AssortmentRenderer extends React.Component {
  constructor({assortment, open}) {
    super();
    this.assortment = assortment;
    this.open = open;
  }

  on_input(event) {
    this.assortment.search(event.target.value);
  }

  render() {
    return (
      <div class="assortment-tree">
        <div class="assortment-header">
          <div class="description">
            {this.assortment.title}
          </div>
          <div class="search-box">
            <input
                type="search"
                id={this.assortment.name + '-search-box'}
                oninput={this.on_input}
                placeholder="search"
                value={this.assortment.query}/>
          </div>
        </div>
        <BranchList open={this.open} prefix={this.assortment.name} branches={this.assortment.branches.filter(a => a.parent && !a.parent.parent)} products={[]}/>
      </div>
    )
  }
}