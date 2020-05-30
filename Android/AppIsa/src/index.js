import React, { Fragment } from 'react';
// Interface de navigation
import Navigator from './navigations';
// SplashScreen
import SplashScreen from 'react-native-splash-screen'
// Firebase for accessing to Storage
import firebase from 'react-native-firebase';
// Local database
import Realm from 'realm';
// Import Schemas for Realm
import {RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema} from './services/RealmSchemaService';
// Some Useful tools
import _ from 'underscore';

/*
!TODO!
Permettre à l'application de vérifier le contenu de la BDD locale et serveur pour vérifier qu'ils possèdent la même chose et si ce n'est pas
le cas, alors il faudrait téléchargement, seulement ce qui est nécéssaire et pas tout retélécharger (bien que les données ne soient pas lourdes)
*/

class App extends React.Component{
    constructor( props ) {
        super( props );
        this.state = {
            empty: false,
            text: 'string',
            allElements: []
        }
        // Si pas de bdd alors on download le contenu sinon on passe
        Realm.open({
            schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
        }).then(realm => {
            if(_.isEmpty(realm.objects('Exist')) == true){
                // On ajoute un objet qui va permettre de prouver l'existence de la bdd aux prochaines ouvertures
                Realm.open({
                    schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
                }).then(realm => {
                    realm.write(() => {
                        realm.create('Exist', {value: 'true'});
                    });
                })
                .catch(e => {
                    console.log(e);
                });
                // On télécharge et ajoute les données a la bdd
                this.AddDataHome();
            }
            else{
                SplashScreen.hide();
            }
        });
    };

    AddDataHome = () => {
        let ref = firebase.firestore().collection("Home");
        ref.get()
        .then(querySnapshot => {
          querySnapshot.forEach(doc => {
            let data = doc.data()
            this.setState({text: data.intro});
          })
        })
        .then(() => {
            Realm.open({
                schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
            }).then(realm => {
                realm.write(() => {
                    realm.create('Home', {text: this.state.text});
                });
                // On continu à télécharger
                this.AddDataRaison();
            })
            .catch(e => {
                console.log(e);
            })
        })
        .catch(e => {
            console.log(e);
        });
    }

    AddDataRaison = () => {
        let ref = firebase.firestore().collection("Raison");
        ref.get()
        .then(querySnapshot => {
          querySnapshot.forEach(doc => {
            let data = doc.data()
            this.setState({allElements: [...this.state.allElements, {imgPrincipal:data.base64, texte: data.texte, imgSecondaire: data.image}]});
          })
        })
        .then(() => {
            Realm.open({
                schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
            }).then(realm => {
                realm.write(() => {
                    for(let i of Array(this.state.allElements.length).keys()){
                        realm.create('Raison',
                        {
                            imgPrincipal: this.state.allElements[i].imgPrincipal,
                            texte: this.state.allElements[i].texte,
                            imgSecondaire: this.state.allElements[i].imgSecondaire
                        });
                    }
                });
                // On continu à télécharger
                this.AddDataHistoire();
            })
            .catch(e => {
                console.log(e);
            })
        })
        .catch(e => {
            console.log(e);
        });
    }

    AddDataHistoire = () => {
        // On remet allElements à zero sinon on aura tous les items de 'Raison' dans 'Histoire'
        this.setState({allElements: []})
        let ref = firebase.firestore().collection("Histoire");
        ref.get()
        .then(querySnapshot => {
          querySnapshot.forEach(doc => {
            let data = doc.data()
            this.setState({allElements: [...this.state.allElements, {imgPrincipal:data.base64, texte: data.texte, imgSecondaire: data.image}]});
          })
        })
        .then(() => {
            Realm.open({
                schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
            }).then(realm => {
                realm.write(() => {
                    for(let i of Array(this.state.allElements.length).keys()){
                        realm.create('Histoire',
                        {
                            imgPrincipal: this.state.allElements[i].imgPrincipal,
                            texte: this.state.allElements[i].texte,
                            imgSecondaire: this.state.allElements[i].imgSecondaire
                        });
                    }
                });
                // On continu à télécharger
                this.AddDataAmour();
            })
            .catch(e => {
                console.log(e);
            })
        })
        .catch(e => {
            console.log(e);
        });
    }
    AddDataAmour = () => {
        // On remet allElements à zero sinon on aura tous les items de 'Raison' dans 'Histoire'
        this.setState({allElements: []})
        let ref = firebase.firestore().collection("Amour");
        ref.get()
        .then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = doc.data()
                this.setState({allElements: [...this.state.allElements, {
                    titre: data.titre,
                    texte1: data.texte1,
                    texte2: data.texte2,
                    texte3: data.texte3,
                    texte4: data.texte4,
                    question: data.question,
                    reponse1: data.reponse1,
                    indice1: data.indice1,
                    choix1: data.choix1,
                    choix2: data.choix2
                }]});
            })
        })
        .then(() => {
            Realm.open({
                schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
            }).then(realm => {
                realm.write(() => {
                    for(let i of Array(this.state.allElements.length).keys()){
                        realm.create('Amour',
                        {
                            titre: this.state.allElements[i].titre,
                            texte1: this.state.allElements[i].texte1,
                            texte2: this.state.allElements[i].texte2,
                            texte3: this.state.allElements[i].texte3,
                            texte4: this.state.allElements[i].texte4,
                            question: this.state.allElements[i].question,
                            reponse1: this.state.allElements[i].reponse1,
                            indice1: this.state.allElements[i].indice1,
                            choix1: this.state.allElements[i].choix1,
                            choix2: this.state.allElements[i].choix2
                        });
                    }
                });
                // On continu à télécharger
                this.AddDataVoyage();
            })
            .catch(e => {
                console.log(e);
            })
        })
        .catch(e => {
            console.log(e);
        });
    }

    AddDataVoyage = () => {
        // On remet allElements à zero sinon on aura tous les items de 'Raison' dans 'Histoire'
        this.setState({allElements: []})
        let ref = firebase.firestore().collection("Voyage");
        ref.get()
        .then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = doc.data()
                this.setState({allElements: [...this.state.allElements, {
                    imgPrincipal:data.imgPrincipal,
                    titrePrincipal : data.titrePrincipal,
                    imgSecondaire: data.imgSecondaire,
                    titreSecondaire: data.titreSecondaire,
                    imgTertiaire: data.imgTertiaire,
                    titreTertiaire: data.titreTertiaire,
                    imgArray1: data.imgArray1,
                    texteArray1: data.texteArray1,
                    imgArray2: data.imgArray2,
                    texteArray2: data.texteArray2,
                  }]});
            })
        })
        .then(() => {
            Realm.open({
                schema:[RaisonSchema, ExistSchema, HomeSchema, HistoireSchema, VoyageSchema, AmourSchema]
            }).then(realm => {
                realm.write(() => {
                    for(let i of Array(this.state.allElements.length).keys()){
                        realm.create('Voyage',
                        {
                            imgPrincipal: this.state.allElements[i].imgPrincipal,
                            titrePrincipal : this.state.allElements[i].titrePrincipal,
                            imgSecondaire: this.state.allElements[i].imgSecondaire,
                            titreSecondaire: this.state.allElements[i].titreSecondaire,
                            imgTertiaire: this.state.allElements[i].imgTertiaire,
                            titreTertiaire: this.state.allElements[i].titreTertiaire,
                            imgArray1: this.state.allElements[i].imgArray1,
                            texteArray1: this.state.allElements[i].texteArray1,
                            imgArray2: this.state.allElements[i].imgArray2,
                            texteArray2: this.state.allElements[i].texteArray2
                        });
                    }
                });
                // On peut maintenant cacher le splashscreen et laisser l'utilisateur interagir avec l'app
                SplashScreen.hide();
            })
            .catch(e => {
                console.log(e);
            })
        })
        .catch(e => {
            console.log(e);
        });
    }

    render() {
        return (
            <Fragment>
                <Navigator/>
            </Fragment>
        )
    }
}

export default App;
