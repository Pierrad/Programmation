import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController) {

  }
  Counter1 = 0;
  Counter2 = 0;
  Counter3 = 0;
  Counter4 = 0;
  Counter5 = 0;

  public Count1(){
    this.Counter1 = this.Counter1 + 1;
  }

  public Count2(){
    this.Counter2 = this.Counter2 + 1;
  }

  public Count3(){
    this.Counter3 = this.Counter3 + 1;
  }

  public Count4(){
    this.Counter4 = this.Counter4 + 1;
  }

  public Count5(){
    this.Counter5 = this.Counter5 + 1;
  }


}
