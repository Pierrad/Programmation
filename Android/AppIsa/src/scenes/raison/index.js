import React from 'react';
import {View, StyleSheet, Button, Alert} from 'react-native';
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema} from '../../services/RealmSchemaService';
// Custom Modal
import ModalCustom from '../../component/ModalComponent';
// Custom FlatList
import FlatListCustom from '../../component/FlatListComponent';

class RaisonScreen extends React.Component{
  constructor( props ) {
    super( props );
    this.state = {
        data: null,
        text: [],
        allElements: [],
        ModalVisibility: false,
        ModalTexte: 'string',
        ModalImg: ''
    }
    this.DisplayData();
  };

  DisplayData = () => {
    Realm.open({
      schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
    }).then(realm => {
      return realm.objects('Raison');
    })
    .then(elements => {
      if(elements.length == 0){
        this.showAlertBdd();
      }
      else{
        for(let element of elements){
          this.setState({allElements: [...this.state.allElements, {
            imgPrincipal:element.imgPrincipal,
            texte: element.texte,
            imgSecondaire: element.imgSecondaire
          }]});
        }
      }
    })
    .catch(e => {
      console.log(e);
    });
  }

  showAlertBdd() {
    Alert.alert(
      "Erreur",
      "Il n'y a rien dans la base de données",
      [
        {text: "OK"}
      ],
      { cancelable: false }
    );
  }

  render() {
    return (
      <View style={styles.home}>
        {this.state.allElements ? // Dès que allElements a qqchose go render
        <FlatListCustom
          // Les données pour render la flat list
          data = {this.state.allElements}
          // on récupère le texte et image pour render le modal, on change la visibilité du modal pour trigger le state qui update la View
          // en appelant le CustomModal component et en passant le texte et image renvoyé par la flat list
          dataForModal = {(texte, image) => this.setState({ModalVisibility:!this.state.ModalVisibility, ModalTexte:texte, ModalImg:image})}
        />
        : []}
        {this.state.ModalVisibility ? // Dès que ModalVisibility est vrai go render
          <ModalCustom
            texte = {this.state.ModalTexte} // le texte pour le modal
            image = {this.state.ModalImg} // l'image pour le modal
            visible = {this.state.ModalVisibility} // le state de la visibilité du modal
            changeVisibilityInParent = {(visibility)=> this.setState({ModalVisibility:visibility})} // On récupère l'argument envoyé par le component et on change la visibilité
          />
          :null}
      </View>
    );
  };
};

// Définition des styles
const styles = StyleSheet.create({
  home: {
    flex: 1,
    backgroundColor: 'white',
  }
});

export default RaisonScreen;