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
  console.log(func);
  if (document.readyState === 'complete') {
    func([{}])
  } else {
    execute_on_load.push(func);
  }
}
window.onload = function(){
  for(let func of execute_on_load) {
    func.apply(this, arguments);
  }
};

let drag_identifiers = new WeakMap();

export function draggable(type, identifier) {
  drag_identifiers[identifier] =
}

export function droppable(types, func, args, kwargs) {
  return {}

  function onDrop(event) {
    event.
  }
}