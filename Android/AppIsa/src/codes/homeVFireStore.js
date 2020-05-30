import React from 'react';
import {View, Text, StyleSheet, Image, Button, FlatList, Alert} from 'react-native';
// Firebase for accessing to Storage
import firebase from 'react-native-firebase';
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {ImageSchema, ExistSchema} from '../../services/RealmSchemaService';
// Loading UI
import * as Progress from 'react-native-progress';
// Chargement rapide des images
import FastImage from 'react-native-fast-image';
// Some Useful tools
import _ from 'underscore';


class Home extends React.Component{
  constructor( props ) {
    super( props );
    this.state = {
        empty: false,
        data: null,
        disableButton: false,
        loading: false,
        base64 : 'string',
        image: [],
        allBase: []
    }
    // Exist or not
    Realm.open({
      schema:[ImageSchema, ExistSchema]
    }).then(realm => {
      if(_.isEmpty(realm.objects('Exist')) == true){
        this.setState({ empty : true });
      }
    });
  };

  GetDataFromFS = () => {
    this.setState({loading:true});
    let ref = firebase.firestore().collection('images');
    ref.get()
    .then(querySnapshot => {
      querySnapshot.forEach(doc => {
        let data = doc.data()
        this.setState({allBase: [...this.state.allBase, {id:data.id, src: data.base64}]});
      })
    })
    .then(() => {
      this.setState({loading:false, disableButton:true});
    })
    .catch(function(error) {
      console.log("Error getting documents: ", error);
    });
  }

  AddData = () => {
    Realm.open({
      schema:[ImageSchema, ExistSchema]
    }).then(realm => {
      console.log(_.isEmpty(realm.objects('Exist')))
      if(_.isEmpty(realm.objects('Exist')) == true){
        realm.write(() => {
          realm.create('Exist', {value: 'true'});
          for(let i of Array(this.state.allBase.length).keys()){
            realm.create('Image', {id: this.state.allBase[i].id, base64: this.state.allBase[i].src});
          }
        });
        this.setState({ data : realm });
      }
      else {
        console.log("already exist")
      }
    });
  }


  DisplayData = () => {
    let image = null;
    Realm.open({
      schema:[ImageSchema, ExistSchema]
    }).then(realm => {
      return image = realm.objects('Image');
    })
    .then(imgs => {
      if(imgs.length == 0){
        this.showAlertBdd();
      }
      else{
        for(let img of imgs){
          this.setState({image:[...this.state.image, img.base64]});
        }
      }
    })
    .catch(e => {
      console.log(e);
    });
  }

  DeleteData = () => {
    Realm.open({
      schema:[ImageSchema, ExistSchema]
    }).then(realm => {
      realm.write(() => {
        let allImage = realm.objects('Image');
        realm.delete(allImage);
        let Exist = realm.objects('Exist');
        realm.delete(Exist);
      });
      this.setState({ data : realm });
    });
  }

  showAlertBdd = () => {
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
        <Text>Home</Text>
        {this.state.empty ? this.state.disableButton ? null : <Button title="Get Data from FireStore" onPress={this.GetDataFromFS}></Button> : null}
        {this.state.loading ? <Progress.Circle size={30} indeterminate={true} /> : null}
        {this.state.empty ? this.state.disableButton ? <Button title="Add Data" onPress={this.AddData}></Button> : <Button disabled={true} title="Add Data" onPress={this.AddData.bind(this, this.state.base64)}></Button>: null}
        <Button title="Display Data" onPress={this.DisplayData}></Button>
        <Button title="Delete Data" onPress={this.DeleteData}></Button>
        <Text> {this.state.data ? 'Number of image in this Realm: ' + this.state.data.objects('Image').length : null} </Text>
        {this.state.image ?
        <FlatList
          data={this.state.image}
          renderItem={({ item }) => (
            <View style={{ flex: 1, flexDirection: 'column'}}>
              <FastImage style = {styles.image} source={{uri: `data:image/jpg;base64,${item}`, priority: FastImage.priority.normal}}/>
            </View>
          )}
          numColumns={2}
          keyExtractor={(item, index) => index}
        /> : []}
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

export default Home;