import React, { Component } from 'react'
import {Text, View, StyleSheet, ScrollView, Button } from 'react-native'
import { SimpleCard } from "@paraboly/react-native-card";
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema} from '../../services/RealmSchemaService';
// Modal
import Modal from 'react-native-modal';
// Custom TextInput
import MyTextInput from '../../component/TextInputComponent';
// Custom Button
import Btn from 'react-native-button';
// Parser
import StringToArray from '../../services/ParserStringService';

/*
A cause du fait que cette partie de l'app soit particulière, je ne sais pas comment réduire le code et réutiliser la même fonction pour créer
trois scénarios différents.

!TODO!
Peut être découper le code de chaque carte pour faire ressortir des petites fonctions que je pourrais réutiliser dans chaque carte
*/


export default class AmourScreen extends Component {
    constructor( props ) {
        super( props );
        this.state = {
            allElements: [],
            exist: null,
            ModalVisibilityC1: false,
            ModalVisibilityC2: false,
            ModalVisibilityC3: false,
            S1Q1: undefined,
            S1Q1I: undefined,
            S1C1: undefined,
            S1C2: undefined,
            S2C1: undefined,
            S2C2: undefined,
            S3C1: undefined,
            S3C2: undefined,
            S3Q1: undefined,
            S3Q1I: undefined,
        }
        this.DisplayData();
    };

    DisplayData = () => {
        Realm.open({
          schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
        }).then(realm => {
          return realm.objects('Amour');
        })
        .then(elements => {
          if(elements.length == 0){
            this.showAlertBdd();
          }
          else{
            for(let element of elements){
                this.setState({allElements: [...this.state.allElements, {
                    titre: element.titre,
                    texte1: element.texte1,
                    texte2: element.texte2,
                    texte3: element.texte3,
                    texte4: element.texte4,
                    question: element.question,
                    reponse1: element.reponse1,
                    indice1: element.indice1,
                    choix1: element.choix1,
                    choix2: element.choix2
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

    checkIfEqual = (value1, value2, card) => {
        if(card == "card1"){
            if(value1==value2){
                this.setState({S1Q1:true, S1Q1I: false})
            }else {
                this.setState({S1Q1I:true, S1Q1:false})
            }
        }
        if(card == "card3"){
            if(value1==value2){
                this.setState({S3Q1:true, S3Q1I: false})
            }else {
                this.setState({S3Q1I:true, S3Q1:false})
            }
        }
    }
    // Render Card 1
    card1 = () => {
        return (
            <View style={styles.viewInside}>
                <SimpleCard
                    title = {this.state.allElements[0].texte1.substring(0,223)+"......"}
                    onPress = {() => this.setState({ModalVisibilityC1:true})}
                />
                <Modal
                    hardwareAccelerated = {true}
                    backdropColor = "white"
                    backdropOpacity = {1}
                    onBackButtonPress = {() => this.setState({ModalVisibilityC1:false})}
                    isVisible={this.state.ModalVisibilityC1}
                    style={styles.modal}
                >
                    <ScrollView>
                        <Text>{StringToArray(this.state.allElements[0].texte1)}</Text>
                        <MyTextInput
                            initialValue={this.state.allElements[0].question}
                            response = {(value) => this.checkIfEqual(value, this.state.allElements[0].reponse1, "card1")}
                        />
                        {this.state.S1Q1 ?
                            <View>
                                <Text>{StringToArray(this.state.allElements[0].texte2)}</Text>
                                <Btn style={styles.Btn} onPress = {() => this.setState({S1C1:true, S1C2:false})}> {this.state.allElements[0].choix1}</Btn>
                                <Btn style={styles.Btn} onPress = {() => this.setState({S1C1:false, S1C2:true})}> {this.state.allElements[0].choix2}</Btn>
                                {this.state.S1C1 ?
                                    <Text>{StringToArray(this.state.allElements[0].texte3)}</Text>
                                : null}
                                {this.state.S1C2 ?
                                    <Text>{StringToArray(this.state.allElements[0].texte4)}</Text>
                                : null}
                            </View>
                        : null}
                        {this.state.S1Q1I ?
                            <Text>{this.state.allElements[0].indice1}</Text>
                        : null}

                    </ScrollView>
                </Modal>
            </View>
        )
    }
    // Render Card 2
    card2 = () => {
        return (
            <View style={styles.viewInside}>
                <SimpleCard
                    title = {this.state.allElements[1].texte1.substring(0,204)}
                    onPress = {() => this.setState({ModalVisibilityC2:true})}
                />
                <Modal
                    hardwareAccelerated = {true}
                    backdropColor = "white"
                    backdropOpacity = {1}
                    onBackButtonPress = {() => this.setState({ModalVisibilityC2:false})}
                    isVisible={this.state.ModalVisibilityC2}
                    style={styles.modal}
                >
                    <ScrollView>
                        <Text>{StringToArray(this.state.allElements[1].texte1)}</Text>
                        <Btn style={styles.Btn} onPress = {() => this.setState({S2C1:true, S2C2:false})}> {this.state.allElements[1].choix1}</Btn>
                        <Btn style={styles.Btn} onPress = {() => this.setState({S2C1:false, S2C2:true})}> {this.state.allElements[1].choix2}</Btn>
                        {this.state.S2C1 ?
                            <View>
                                <Text>{StringToArray(this.state.allElements[1].texte2)}</Text>
                                <Text>{StringToArray(this.state.allElements[1].texte3)}</Text>
                            </View>
                        : null}
                        {this.state.S2C2 ?
                            <Text>{this.state.allElements[1].texte4}</Text>
                        : null}
                    </ScrollView>
                </Modal>
            </View>
        )
    }
    // Render Card 2
    card3 = () => {
        return (
            <View style={styles.viewInside}>
                <SimpleCard
                    title = {this.state.allElements[2].texte1.substring(0,190)}
                    onPress = {() => this.setState({ModalVisibilityC3:true})}
                />
                <Modal
                    hardwareAccelerated = {true}
                    backdropColor = "white"
                    backdropOpacity = {1}
                    onBackButtonPress = {() => this.setState({ModalVisibilityC3:false})}
                    isVisible={this.state.ModalVisibilityC3}
                    style={styles.modal}
                >
                    <ScrollView>
                        <Text>{StringToArray(this.state.allElements[2].texte1)}</Text>
                        <Btn style={styles.Btn} onPress = {() => this.setState({S3C1:true, S3C2:false, S3Q1I:undefined})}> {this.state.allElements[2].choix1}</Btn>
                        <Btn style={styles.Btn} onPress = {() => this.setState({S3C1:false, S3C2:true, S3Q1I:undefined})}> {this.state.allElements[2].choix2}</Btn>
                        {this.state.S3C1 ?
                            <View>
                                <Text>{StringToArray(this.state.allElements[2].texte2)}</Text>
                                {this.card3_()}
                            </View>
                        : null}
                        {this.state.S3C2 ?
                            <View>
                                <Text>{StringToArray(this.state.allElements[2].texte3)}</Text>
                                {this.card3_()}
                            </View>
                        : null}
                    </ScrollView>
                </Modal>
            </View>
        )
    }
    // Render Card 3, une sous partie
    card3_ = () => {
        return (
            <View>
                <MyTextInput
                    initialValue={this.state.allElements[2].question}
                    response = {(value) => this.checkIfEqual(value, this.state.allElements[2].reponse1, "card3")}
                />
                {this.state.S3Q1 ?
                        <Text>{StringToArray(this.state.allElements[2].texte4)}</Text>
                : null}
                {this.state.S3Q1I ?
                    <Text>{this.state.allElements[2].indice1}</Text>
                : null}
            </View>
        )
    }

    render() {
        return (
            <View style={styles.view}>
                {this.state.exist ? this.card1(): null}
                {this.state.exist ? this.card2(): null}
                {this.state.exist ? this.card3(): null}
            </View>

        )
    }
}

// Définition des styles
const styles = StyleSheet.create({
    view: {
        flex:1
    },
    viewInside:{
        borderColor:'transparent',
        borderWidth:1
    },
    modal:{
        flex:1,
        alignContent:"center",
        justifyContent:"center"
    },
    Btn:{
        fontSize: 20,
        color: 'tomato',
        borderWidth: 5,
        borderColor:'transparent'
    }
  });