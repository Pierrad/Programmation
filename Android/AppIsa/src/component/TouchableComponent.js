import React, { Component } from 'react'
import { TouchableOpacity } from 'react-native'
// Image avec texte au dessus
import ImageOverlay from "react-native-image-overlay";
// Parser
import StringToArray from "../services/ParserStringService";

/*
TouchableOpacity Custom dont je me sers dans VoyageScreen
*/

export default class TouchableCustom extends Component {
    render() {
        return (
            <TouchableOpacity style={{ alignSelf: 'flex-start'}} activeOpacity = {1} onPress={() => this.props.changeVisibility()}>
            <ImageOverlay
                containerStyle={this.props.style}
                height = {250}
                source={{ uri: `data:image/jpg;base64,${this.props.imgPrincipal}` }}
                rounded = {30}
                title={StringToArray(this.props.titrePrincipal)}
                titleStyle={{ color: 'white', fontSize : 20,fontWeight: 'bold' }}
                contentPosition="center"
                overlayAlpha={0.1}
            />
        </TouchableOpacity>
        )
    }
}
