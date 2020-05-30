import React, { Component } from 'react'
import {View,Text, StyleSheet, Button, Alert,TouchableOpacity, Image, ScrollView} from 'react-native';
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema} from '../../services/RealmSchemaService';
// Modal
import Modal from 'react-native-modal';
// Swiper, pour swiper de page en page
import Swiper from 'react-native-swiper'
// Custom Touchable
import TouchableCustom from '../../component/TouchableComponent';
// Parser
import StringToArray from "../../services/ParserStringService";

/*
Similairement à AmourScreen, il faudrait pouvoir créer une fonction qui puisse render toutes nos cartes (sauf la carte 1 car elle est différente)

!TODO!
Faire une fonction de render utilisable pour toutes les cartes, pour cela il faudrait pouvoir gérer les states dont on se sert dans chaque fonction
*/

export default class VoyageScreen extends Component {
  constructor(props){
    super(props);
    this.state = {
      exist: false,
      allElements: [],
      ModalVisibility:null,
      ModalVisibility_:null,
      ModalVisibility__:null,
      ModalVisibility1:null,
      ModalVisibility2:null,
      ModalVisibility3:null,
      ModalVisibility4:null,
      ModalVisibility5:null,
      ModalVisibility6:null
    }
    this.DisplayData();
  }

  DisplayData = () => {
    Realm.open({
      schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
    }).then(realm => {
      return realm.objects('Voyage');
    })
    .then(elements => {
      if(elements.length == 0){
        this.showAlertBdd();
      }
      else{
        for(let element of elements){
            this.setState({allElements: [...this.state.allElements, {
              imgPrincipal:element.imgPrincipal,
              titrePrincipal : element.titrePrincipal,
              imgSecondaire: element.imgSecondaire,
              titreSecondaire: element.titreSecondaire,
              imgTertiaire: element.imgTertiaire,
              titreTertiaire: element.titreTertiaire,
              imgArray1: element.imgArray1,
              texteArray1: element.texteArray1,
              imgArray2: element.imgArray2,
              texteArray2: element.texteArray2,
            }]});
        }
        this.setState({exist:[]})
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

  renderCard1 = () => {

    let allCard1 = [];
    for(let i = 0;i<this.state.allElements[0].imgArray1.length; i++){
      allCard1.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[0].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[0].texteArray1[i])}</Text>
        </View>
      )
    }
    let allCard2 = [];
    for(let i = 0;i<this.state.allElements[0].imgArray2.length; i++){
      allCard2.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[0].imgArray2[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[0].texteArray2[i])}</Text>
        </View>
      )
    }

    return(
      <>
        <TouchableCustom
          imgPrincipal={this.state.allElements[0].imgPrincipal}
          titrePrincipal={this.state.allElements[0].titrePrincipal}
          style = {{borderWidth: 15, borderColor:'transparent'}}
          changeVisibility = {()=>this.setState({ModalVisibility:true})}
        />
        <Modal
          backdropColor = "white" backdropOpacity = {1}
          onBackButtonPress = {() => this.setState({ModalVisibility:false})}
          isVisible={this.state.ModalVisibility}
          style={styles.modal}
        >
          <TouchableCustom
            imgPrincipal={this.state.allElements[0].imgSecondaire}
            titrePrincipal={this.state.allElements[0].titreSecondaire}
            style = {{borderBottomWidth: 5, borderColor:'transparent', width:330, height:200}}
            changeVisibility = {()=>this.setState({ModalVisibility_:true})}
          />
          <TouchableCustom
            imgPrincipal={this.state.allElements[0].imgTertiaire}
            titrePrincipal={this.state.allElements[0].titreTertiaire}
            style = {{borderBottomWidth: 5, borderColor:'transparent', width:330, height:200}}
            changeVisibility = {()=>this.setState({ModalVisibility__:true})}
          />
        </Modal>
        <Modal
          backdropColor = "white" backdropOpacity = {1}
          onBackButtonPress = {() => this.setState({ModalVisibility_:false})}
          isVisible={this.state.ModalVisibility_}
          style={styles.modal}
        >
          <Swiper style={{}} showsButtons={false}>
            {allCard1}
          </Swiper>
        </Modal>
        <Modal
          backdropColor = "white" backdropOpacity = {1}
          onBackButtonPress = {() => this.setState({ModalVisibility__:false})}
          isVisible={this.state.ModalVisibility__}
          style={styles.modal}
        >
          <Swiper style={{}} showsButtons={false}>
            {allCard2}
          </Swiper>
        </Modal>
      </>
    )
  }

  renderCard2 = () => {
    let allCard = [];
    for(let i = 0;i<this.state.allElements[1].imgArray1.length; i++){
      allCard.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[1].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[1].texteArray1[i])}</Text>
        </View>
      )
    }
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[1].imgPrincipal}
            titrePrincipal={this.state.allElements[1].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility1:true})}
          />
          <Modal
            backdropColor = "white" backdropOpacity = {1}
            onBackButtonPress = {() => this.setState({ModalVisibility1:false})}
            isVisible={this.state.ModalVisibility1}
            style={styles.modal}
          >
            <Swiper style={{}} showsButtons={false}>
              {allCard}
            </Swiper>
          </Modal>
      </>
    )
  }

  renderCard3 = () => {
    let allCard = [];
    for(let i = 0;i<this.state.allElements[2].imgArray1.length; i++){
      allCard.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[2].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[2].texteArray1[i])}</Text>
        </View>
      )
    }
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[2].imgPrincipal}
            titrePrincipal={this.state.allElements[2].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility2:true})}
          />
          <Modal
            backdropColor = "white" backdropOpacity = {1}
            onBackButtonPress = {() => this.setState({ModalVisibility2:false})}
            isVisible={this.state.ModalVisibility2}
            style={styles.modal}
          >
            <Swiper style={{}} showsButtons={false}>
              {allCard}
            </Swiper>
          </Modal>
      </>
    )
  }

  renderCard4 = () => {
    let allCard = [];
    for(let i = 0;i<this.state.allElements[3].imgArray1.length; i++){
      allCard.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[3].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[3].texteArray1[i])}</Text>
        </View>
      )
    }
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[3].imgPrincipal}
            titrePrincipal={this.state.allElements[3].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility3:true})}
          />
          <Modal
            backdropColor = "white" backdropOpacity = {1}
            onBackButtonPress = {() => this.setState({ModalVisibility3:false})}
            isVisible={this.state.ModalVisibility3}
            style={styles.modal}
          >
            <Swiper style={{}} showsButtons={false}>
              {allCard}
            </Swiper>
          </Modal>
      </>
    )
  }

  renderCard5 = () => {
    let allCard = [];
    for(let i = 0;i<this.state.allElements[4].imgArray1.length; i++){
      allCard.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[4].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[4].texteArray1[i])}</Text>
        </View>
      )
    }
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[4].imgPrincipal}
            titrePrincipal={this.state.allElements[4].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility4:true})}
          />
          <Modal
            backdropColor = "white" backdropOpacity = {1}
            onBackButtonPress = {() => this.setState({ModalVisibility4:false})}
            isVisible={this.state.ModalVisibility4}
            style={styles.modal}
          >
            <Swiper style={{}} showsButtons={false}>
              {allCard}
            </Swiper>
          </Modal>
      </>
    )
  }

  renderCard6 = () => {
    let allCard = [];
    for(let i = 0;i<this.state.allElements[5].imgArray1.length; i++){
      allCard.push(
        <View style={styles.slide}>
          <Image style={{width:300,height:300, borderRadius:20}} source={{ uri: `data:image/jpg;base64,${this.state.allElements[5].imgArray1[i]}` }}></Image>
          <Text style={styles.text}>{StringToArray(this.state.allElements[5].texteArray1[i])}</Text>
        </View>
      )
    }
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[5].imgPrincipal}
            titrePrincipal={this.state.allElements[5].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility5:true})}
          />
          <Modal
            backdropColor = "white" backdropOpacity = {1}
            onBackButtonPress = {() => this.setState({ModalVisibility5:false})}
            isVisible={this.state.ModalVisibility5}
            style={styles.modal}
          >
            <Swiper style={{}} showsButtons={false}>
              {allCard}
            </Swiper>
          </Modal>
      </>
    )
  }

  renderCard7 = () => {
    return(
      <>
          <TouchableCustom
            imgPrincipal={this.state.allElements[6].imgPrincipal}
            titrePrincipal={this.state.allElements[6].titrePrincipal}
            style = {{borderWidth: 15, borderColor:'transparent'}}
            changeVisibility = {()=>this.setState({ModalVisibility6:true})}
          />
      </>
    )
  }

  render() {
      return (
          <View style={{flex:1}}>
              <ScrollView>
                {this.state.exist ? this.renderCard1(): null}
                {this.state.exist ? this.renderCard2(): null}
                {this.state.exist ? this.renderCard3(): null}
                {this.state.exist ? this.renderCard4(): null}
                {this.state.exist ? this.renderCard5(): null}
                {this.state.exist ? this.renderCard6(): null}
                {this.state.exist ? this.renderCard7(): null}
              </ScrollView>
          </View>
      )
  }
}

const styles = StyleSheet.create({
  modal:{
    flex:1,
  },
  slide: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: 'black',
    fontSize: 15,
  }
})
