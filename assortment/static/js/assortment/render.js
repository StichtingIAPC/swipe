/**
 * Created by Matthias on 11/04/2016.
 */

import {Product, Branch} from './models';

class Renderer {
  constructor(){}

  renderAsList(){}

  renderAsTile(){}

  renderAsBranch(){}

  update(){}
}

/**
 * @class {ProductRenderer} ProductRenderer
 * @prop {Product}    product
 */
export class ProductRenderer extends Renderer {
  /**
   * @param {Product} product
   */
  constructor(product){
    super();
    this.product = product;
    this.product.signal.add(this.update);
  }

  renderAsList(){
    return [
      'li', {
        'class': 'something',
        'id': this.product.id
      }, [
        'div', {

        },
        this.product.name,
        this.product.price,
        this.product.amount
      ]
    ];
  }

  renderAsTile(){
    return [
      'div', {},
      this.product.amount,
      this.product.name,
      this.product.price
    ]
  }

  renderAsBranch(){
    return [
      'div', {},
      this.product.amount,
      this.product.name,
      this.product.price
    ]
  }

  update(){};

}

/**
 * @class {BranchRenderer} BranchRenderer
 * @prop {Branch} branch
 */
export class BranchRenderer extends Renderer {
  /**
   * @param {Branch} branch
   */
  constructor(branch){
    super();
    this.branch = branch;
    this.branch.signal.add(this.update)
  }

  update(){

  }
}