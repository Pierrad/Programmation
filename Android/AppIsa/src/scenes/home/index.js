import React from 'react';
import {View, Text, StyleSheet, Alert} from 'react-native';
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema} from '../../services/RealmSchemaService';
// Parser
import StringToArray from '../../services/ParserStringService';


class HomeScreen extends React.Component{
  constructor( props ) {
    super( props );
    this.state = {
        text: null,
    }
    this.DisplayData();
  };

  DisplayData = () => {
    Realm.open({
      schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
    }).then(realm => {
      return realm.objects('Home');
    })
    .then(texte => {
      if(texte.length == 0){
        this.showAlertBdd();
      }
      else{
        this.setState({text:texte[0]["text"]});
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
        {this.state.text ? <Text> {StringToArray(this.state.text)} </Text> : null}
      </View>
    );
  };
};

// Définition des styles
const styles = StyleSheet.create({
  home: {
    flex: 1,
    backgroundColor: 'white',
  },
  image: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 200,
    width: 200
  }
});

export default HomeScreen;