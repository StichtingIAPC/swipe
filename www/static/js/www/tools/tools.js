/**
 * Created by Matthias on 11/04/2016.
 */
import Signal from 'bower_components/mini-signals/src/index'

export class SubscribeAble {
  constructor(){
    this.signal = new Signal();
    this.signal.add(this.onChange)
  }

  onChange(){}
}

export class RenderAble extends SubscribeAble {
  constructor(){
    super();
  }
}
