import React from 'react';
import './App.css';

const ID = ["Q","W","E","A","S","D","Z","X","C"];
const CLIP = ["https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/606%20Basic/25[kb]606-snare1.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/32[kb]ha64-hho1.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/10[kb]ha64-sd1.1.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/8[kb]ha64-sd2.2.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/21[kb]ha64-sha4.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/4[kb]ha64-tom-a2.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Hammond%20Auto%20Vari%2064%201974/45[kb]ha64-bd-2.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Roland%20SH09/69[kb]909bass3.wav.mp3",
              "https://sampleswap.org/samples-ghost/DRUMS%20(FULL%20KITS)/DRUM%20MACHINES/Roland%20SH09/69[kb]anabdrm5.wav.mp3"];

class DrumMachine extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            currentSound:""
        }
    }

    componentDidMount(){
        document.addEventListener("keydown", this.keyDown, false);
    }
      componentWillUnmount(){
        document.removeEventListener("keydown", this.keyDown, false);
    }

    keyDown = (event) => {
        if(event.keyCode === 81) this.playSound("Q");
        if(event.keyCode === 87) this.playSound("W");
        if(event.keyCode === 69) this.playSound("E");
        if(event.keyCode === 65) this.playSound("A");
        if(event.keyCode === 83) this.playSound("S");
        if(event.keyCode === 68) this.playSound("D");
        if(event.keyCode === 90) this.playSound("Z");
        if(event.keyCode === 88) this.playSound("X");
        if(event.keyCode === 67) this.playSound("C");
    }

    // Array function to bind this
    playSound = (key) =>{
        this.setState({
            currentSound:key
        })
        let audio = new Audio(CLIP[ID.indexOf(key)]);
        audio.classList.add("clip");
        audio.setAttribute("id", key);
        audio.play();
    }

    render(){
        return(
            <div id="drum-machine">
                <div id="display">
                    {ID.map((id, key) => {
                        return(
                            <button className="drum-pad" id={id} key={key} onClick={() => this.playSound(id)}>{id}</button>
                        )
                    })}
                    <p id="display-text">{this.state.currentSound}</p>
                </div>
            </div>
        );
    }
}

export default DrumMachine;
