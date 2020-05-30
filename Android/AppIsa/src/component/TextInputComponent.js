import * as React from "react";
import { StyleSheet, TextInput } from "react-native";

/*
TextInput Custom dont je me sers dans AmourScreen
*/

const BLUE = "#428AF8";
const TOMATO = "tomato";

class MyTextInput extends React.Component {
    constructor( props ) {
        super( props );
        this.state = {
            isFocused:false,
            InputValue:''
        }
    };

    componentDidMount(){
        this.setState({InputValue:this.props.initialValue});
    }

  handleFocus = event => {
    this.setState({ isFocused: true });
    if (this.props.onFocus) {
      this.props.onFocus(event);
    }
  };

  handleBlur = event => {
    this.setState({ isFocused: false });
    if (this.props.onBlur) {
      this.props.onBlur(event);
    }
  };
  handleKeyDown = () => {
    this.props.response(this.state.InputValue.nativeEvent.text)
  }

  render() {
    return (
      <TextInput
        selectionColor={BLUE}
        underlineColorAndroid={
          this.state.isFocused ? TOMATO : BLUE
        }
        onFocus={this.handleFocus}
        onBlur={this.handleBlur}
        style={styles.textInput}
        value = {this.state.InputValue}
        onChange = {text => this.setState({InputValue:text})}
        onSubmitEditing = {this.handleKeyDown}
      />
    );
  }
}

const styles = StyleSheet.create({
  textInput: {
    height: 40,
    paddingLeft: 6
  }
});

export default MyTextInput;