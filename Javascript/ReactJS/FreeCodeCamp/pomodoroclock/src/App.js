import React from 'react';
import './App.css';

let interval;
let beep;

class PomodoroClock extends React.Component{
  constructor(props){
    super(props);
    this.state={
      timeSessionLeft:"", // Time left for the session
      timeBreakLeft:"", // Time left for the break
      startStop:true, // state to display "Start" or "Stop" depending on the play/pause
      sessionBreak:true, // state to display "Session" or "Break"
      break:false, // state to know if we have click the button to pause or play
      breakLenght:5, // State that describe the Break Lenght
      sessionLenght:25, // State that describe the Session Lenght
      counter:false // Allow to not start multiple setInterval
    }
  }

  componentDidMount(){
    this.setTiming();
  }

  // Arrow function to bind this
  reset = () => {
    clearInterval(interval);
    this.setState({
      timeSessionLeft:"", // Time left for the session
      timeBreakLeft:"", // Time left for the break
      startStop:true, // state to display "Start" or "Stop" depending on the play/pause
      sessionBreak:true, // state to display "Session" or "Break"
      break:false, // state to know if we have click the button to pause or play
      breakLenght:5, // State that describe the Break Lenght
      sessionLenght:25, // State that describe the Session Lenght
      counter:false // Allow to not start multiple setInterval
    })
    this.setTiming();
  }

  // Arrow function to bind this
  setTiming = () => {
    // Assure that the state is correctly updated by returning a function besides an object
    if(this.state.breakLenght >= 0 & this.state.breakLenght <= 10){
      this.setState((state)=>{
        return {
          timeSessionLeft: state.sessionLenght.toString() + ":00",
          timeBreakLeft: "0" + state.breakLenght.toString() + ":00"
        }
      });
    } else {
      this.setState((state)=> {
        return {
          timeSessionLeft: state.sessionLenght.toString() + ":00",
          timeBreakLeft: state.breakLenght.toString() + ":00"
        }
      })
    }
    if(this.state.sessionLenght >= 0 & this.state.sessionLenght <= 10){
      this.setState((state)=>{
        return {
          timeSessionLeft: "0" + state.sessionLenght.toString() + ":00",
          timeBreakLeft: state.breakLenght.toString() + ":00"
        }
      });
    } else {
      this.setState((state)=> {
        return {
          timeSessionLeft: state.sessionLenght.toString() + ":00",
          timeBreakLeft: state.breakLenght.toString() + ":00"
        }
      })
    }
  }

  // Arrow function to bind this
  breakIncrement = () => {
    if(this.state.breakLenght + 1 !== 61){
      this.setState({breakLenght:this.state.breakLenght + 1})
    }
    this.setTiming();
  }

  // Arrow function to bind this
  breakDecrement = () => {
    if(this.state.breakLenght - 1 !== 0){
      this.setState({breakLenght:this.state.breakLenght - 1})
    }
    this.setTiming();
  }

  // Arrow function to bind this
  sessionIncrement = () => {
    if(this.state.sessionLenght + 1 !== 61){
      this.setState({sessionLenght:this.state.sessionLenght + 1})
    }
    this.setTiming();
  }

  // Arrow function to bind this
  sessionDecrement = () => {
    if(this.state.sessionLenght - 1 !== 0){
      this.setState({sessionLenght:this.state.sessionLenght - 1})
    }
    this.setTiming();
  }

  playSound(){
    beep = new Audio("http://soundbible.com/grab.php?id=2210&type=mp3");
    beep.setAttribute("id", "beep");
    beep.play()
  }


  // Arrow function to bind this
  playPause = () => {
    this.setState((state) => {return {break: !state.break, startStop: !state.startStop, counter: true}});
    // Not launch multiple setInterval
    if(!this.state.counter){
      this.startStopSession();
    }
  }

  // TODO : A way to group the two function below ?

  // Arrow function to bind this
  startStopSession = () => {
    interval = setInterval(()=>{
      if(this.state.break){
        let minutes = parseInt(this.state.timeSessionLeft.split(":")[0], 10)
        let seconds = parseInt(this.state.timeSessionLeft.split(":")[1], 10)
        if(seconds === 0){
          seconds = 60;
          minutes = minutes - 1;
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeSessionLeft: "0" + minutes.toString() + ":" + seconds.toString()})
          }else{
            this.setState({timeSessionLeft: minutes.toString() + ":" + seconds.toString()});
          }
        }
        if(seconds > 0 & seconds <= 10){
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeSessionLeft: "0" + minutes.toString() + ":0" + (seconds - 1).toString()})
          }else{
            this.setState({timeSessionLeft: minutes.toString() + ":0" + (seconds - 1).toString()})
          }
        }else{
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeSessionLeft: "0" + minutes.toString() + ":" + (seconds - 1).toString()})
          }else{
            this.setState({timeSessionLeft: minutes.toString() + ":" + (seconds - 1).toString()})
          }
        }
        if(this.state.timeSessionLeft === "00:00"){
          clearInterval(interval);
          this.playSound();
          this.setTiming();
          this.setState({sessionBreak:!this.state.sessionBreak});
          this.startStopBreak();
        }
      }
    }, 1000)
  }

  // Arrow function to bind this
  startStopBreak = () => {
    interval = setInterval(() => {
      if(this.state.break){
        let minutes = parseInt(this.state.timeBreakLeft.split(":")[0], 10)
        let seconds = parseInt(this.state.timeBreakLeft.split(":")[1], 10)
        if(seconds === 0){
          seconds = 60;
          minutes = minutes - 1;
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeBreakLeft: "0" + minutes.toString() + ":" + seconds.toString()})
          }else{
            this.setState({timeBreakLeft: minutes.toString() + ":" + seconds.toString()});
          }
        }
        if(seconds > 0 & seconds <= 10){
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeBreakLeft: "0" + minutes.toString() + ":0" + (seconds - 1).toString()})
          }else{
            this.setState({timeBreakLeft: minutes.toString() + ":0" + (seconds - 1).toString()})
          }
        }else{
          if(minutes >= 0 & minutes <= 10){
            this.setState({timeBreakLeft: "0" + minutes.toString() + ":" + (seconds - 1).toString()})
          }else{
            this.setState({timeBreakLeft: minutes.toString() + ":" + (seconds - 1).toString()})
          }
        }
        if(this.state.timeBreakLeft === "00:00"){
          clearInterval(interval);
          this.playSound();
          this.setTiming();
          this.setState({sessionBreak:!this.state.sessionBreak});
          this.startStopSession();
        }
      }
    }, 1000)
  }

  render(){
    return(
      <div id="Container">
        <p id="break-label">{this.state.breakLenght}</p>
        <button id="break-increment" onClick={this.breakIncrement}></button>
        <button id="break-decrement" onClick={this.breakDecrement}></button>
        <p id="session-label">{this.state.sessionLenght}</p>
        <button id="session-increment" onClick={this.sessionIncrement}></button>
        <button id="session-decrement" onClick={this.sessionDecrement}></button>
        <p id="timer-label">{this.state.sessionBreak ? "Session" : "Break"}</p>
        <p id="time-left">{this.state.sessionBreak ? this.state.timeSessionLeft : this.state.timeBreakLeft}</p>
        {this.state.startStop ?
          <button id="start_stop" onClick={this.playPause} style={{backgroundImage:'url("https://cdn.onlinewebfonts.com/svg/img_217916.png")'}}></button>
        :
          <button id="start_stop" onClick={this.playPause} style={{backgroundImage:'url("https://image.flaticon.com/icons/png/512/16/16427.png")'}}></button>
        }
        <button id="reset" onClick={this.reset}></button>
      </div>
    )
  }
}

export default PomodoroClock;
