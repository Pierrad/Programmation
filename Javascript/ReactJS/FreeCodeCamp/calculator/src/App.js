import React from 'react';
import './App.css';

const NUM_STRING = ["zero","one","two","three","four","five","six","seven","eight","nine"];
const NUM = [0,1,2,3,4,5,6,7,8,9];
const OPERATORS_STRING = ["add", "subtract", "multiply", "divide"];
const OPERATORS = ["+", "-", "*", "/"];

class Calculator extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            buffer:"0",
            intermediate:"",
            finalResult:undefined
        }
    }

    // Arrow function to bind this
    clearResult = () => {
        this.setState({
            buffer:"0",
            intermediate:"",
            finalResult:undefined,
        })
    }

    // Arrow function to bind this
    addNum = (nbr) => {
        this.setState({finalResult:undefined}) // If the new calcul start with a number
        // Forbid to add multiple zero at the beginning of a number
        if(this.state.buffer.indexOf("0") === 0){
            this.setState({buffer: this.state.intermediate + nbr.toString()})
        }
        else{
            this.setState({buffer: this.state.buffer + this.state.intermediate + nbr.toString()})
        }
        this.setState({intermediate:""})
    }

    // Arrow function to bind this
    addDecimal = () => {
        this.setState({finalResult:undefined}) // If the new calcul start with a comma
        // Split at each operators and check if there is a dot in the last number to see if we can add a dot or not
        let result = this.state.buffer.split(/[\*\+\-\/]/);
        if(result[result.length-1].includes(".") === false){
            this.setState({
                buffer: this.state.buffer + "."
            })
        }
    }

    // Arrow function to bind this
    addOperators = (operators) => {
        this.setState({finalResult:undefined}); // If the new calcul start with an operator
        // We cannot add multiple following operator (except for one '-')
        let intermediate = this.state.intermediate;
        if(intermediate === "/" | intermediate === "*" | intermediate === "+" | intermediate === "-"){
            if(operators === "-" & (intermediate === "/" | intermediate === "*" | intermediate === "+")){
                this.setState({intermediate: this.state.intermediate + operators})
            }
            else{
                this.setState({intermediate:operators})
            }
        }else {
            if(this.state.buffer.indexOf("0") === 0){
                if(operators==="-"){
                    this.setState({buffer:operators})
                }
            } else {
                this.setState({intermediate:operators})
            }
        }
    }

    // Arrow function to bind this
    calculate = () => {
        this.setState({
            buffer:"0",
            finalResult: eval(this.state.buffer).toString()
        })
    }

    render(){
      return(
          <div id="calculator">
              {NUM_STRING.map((index) => {
                  return <button id={index} key={index} onClick= {() => this.addNum(NUM[NUM_STRING.indexOf(index)])}>{NUM[NUM_STRING.indexOf(index)]}</button>
              })}
              {OPERATORS_STRING.map((index)=>{
                  return <button id="index" key={index} onClick={() => this.addOperators(OPERATORS[OPERATORS_STRING.indexOf(index)])}>{OPERATORS[OPERATORS_STRING.indexOf(index)]}</button>
              })}
              <button id="decimals" onClick={this.addDecimal}>.</button>
              <button id="clear" onClick={this.clearResult}>Clear</button>
              <button id="equals" onClick={this.calculate}>=</button>
              <div id="display">
                {this.state.finalResult}
                <br/>
                {this.state.buffer}{this.state.buffer === "0" ? "" : this.state.intermediate}
              </div>
          </div>
      )
    }
}

export default Calculator;
