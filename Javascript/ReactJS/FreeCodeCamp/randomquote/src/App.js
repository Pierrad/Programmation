import React from 'react';
import './App.css';

const QUOTES = [
	{
		quote:"La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.",
		author:"Albert Einstein"
	},
	{
		quote:"Exige beaucoup de toi-même et attends peu des autres. Ainsi beaucoup d'ennuis te seront épargnés.",
		author:"Confucious"
	},
	{
		quote:"Quote 3",
		author:"Author 3"
	}
]

class RandomQuote extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentQuote:"",
			currentAuthor:""
		};
  }

  componentDidMount(){
    this.displayQuote();
  }

	displayQuote(){
		const RAND = Math.floor(Math.random() * Math.floor(3));
		this.setState({
      currentQuote: QUOTES[RAND].quote,
      currentAuthor: QUOTES[RAND].author
		})
	}
  	// Array function to bind this
	newQuote = () => {
    	this.displayQuote();
  	}
	render() {
		return (
			<>
				<div id="quote-box">
					<p id="text">{this.state.currentQuote}</p>
					<p id="author">{this.state.currentAuthor}</p>
					<button id="new-quote" onClick={this.newQuote}>New Quote</button>
					<a id="tweet-quote" href="twitter.com/intent/tweet"> <img src="https://upload.wikimedia.org/wikipedia/fr/c/c8/Twitter_Bird.svg"/></a>
				</div>
			</>
		);
	}
}

export default RandomQuote;
