/**
 * Created by Matthias on 11/04/2016.
 */
import Signal from 'bower_components/mini-signals/src/index'

export class SubscribeAble {
  constructor(){
    this.signal = new Signal();
    this.signal.add(this.onChange);
  }

  onChange(){}
}

let execute_on_load = [];

export function onload(func) {
  execute_on_load.push(func);
}

document.onload = function(){
  for(let func in execute_on_load) {
    func.apply(this, arguments);
  }
};
