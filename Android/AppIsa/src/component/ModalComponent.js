import React, { Component } from 'react'
import { Text, View, TouchableOpacity, StyleSheet, Image, ScrollView } from 'react-native'
// Modal
import Modal from 'react-native-modal';
// Icon
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

/*
Modal Custom dont je me sers dans RaisonScreen et HistoireScreen
*/

class ModalCustom extends Component {
    changeVisibility = () => {
        this.props.changeVisibilityInParent(!this.props.visible);
    }

    render() {
        return (
            <Modal
                hardwareAccelerated = {true}
                backdropColor = "black"
                backdropOpacity = {0.80}
                swipeDirection="down"
                onSwipeComplete={() => this.changeVisibility()}
                onBackButtonPress = {() => this.changeVisibility()}
                isVisible={this.props.visible}
                >
              <View style={styles.ModalView}>
                  <Text>{this.props.texte}</Text>
                  <Image style = {styles.image} source={{uri: `data:image/jpg;base64,${this.props.image}`}}/>
                  <TouchableOpacity style={styles.touchableButtonModal} onPress= {() => this.changeVisibility()}>
                    <Icon name={"close"}  size={30} color="tomato" />
                  </TouchableOpacity>
              </View>
          </Modal>
        )
    }
}

// Définition des styles
const styles = StyleSheet.create({
    ModalView:{
      flex:1,
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'white',
      borderColor: "white",
      borderWidth:10,
      borderRadius:30,
    },
    touchableButtonModal:{
      position: "absolute", // Positionnement où on veut
      bottom: 5, // Positionnement en bas
      alignItems:'center',
      justifyContent:'center',
      width:50,
      height:50,
      borderWidth:1,
      borderColor:'rgba(0,0,0,0.2)',
      backgroundColor:'#fff',
      borderRadius:50,
    },
    image:{
        flex:1,
        width:'100%',
        height:'100%'
    }
});

export default ModalCustom;