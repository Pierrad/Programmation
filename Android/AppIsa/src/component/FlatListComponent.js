import React, { Component } from 'react'
import {View, StyleSheet, FlatList, TouchableHighlight, } from 'react-native'
// Chargement rapide des images
import FastImage from 'react-native-fast-image';

/*
Flat List Custom dont je me sers dans RaisonScreen et HistoireScreen
*/

export default class FlatListCustom extends Component {
    sendDataForModal = (texte, image) => {
        this.props.dataForModal(texte, image)
    }
    render() {
        return (
            <FlatList
                // number of item initially render
                initialNumToRender = {5}
                // Unrender the unmount component
                removeClippedSubviews = {true}
                // number of item render outside the visible area
                windowSize = {5}
                data={this.props.data}
                renderItem={({ item, index }) => (
                    <View style={styles.viewFlat}>
                        <TouchableHighlight style = {styles.touchableFlat} activeOpacity = {1} underlayColor={'white'} onPress={() => this.sendDataForModal(item["texte"], item["imgSecondaire"])}>
                            <FastImage style = {styles.image} source={{uri: `data:image/jpg;base64,${item["imgPrincipal"]}`, priority: FastImage.priority.high}}/>
                        </TouchableHighlight>
                    </View>
                )}
                numColumns={2}
                keyExtractor={(item, index) => index}
            />
        )
    }
}

// Définition des styles
const styles = StyleSheet.create({
    viewFlat:{
      flex: 1,
      flexDirection: 'column',
    },
    touchableFlat: {
      flex:1,
      alignItems: 'center',
      justifyContent: 'center',
    },
    image: {
      alignItems: 'center',
      justifyContent: 'center',
      borderColor:'white', // Défini la couleur de la bordure
      borderWidth: 3, // défini la largeur de la bordure d'un élément
      borderRadius: 15, // défini les coins arrondis pour la bordure d'un élément
      height: 150,
      width: 180
    }
  });