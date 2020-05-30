/*
Les différents schémas d'objets présent dans la Database Realm
*/

export const ExistSchema = {
  name: "Exist",
  properties: {
    value: 'string'
  }
}

export const RaisonSchema = {
  name: 'Raison',
  properties: {
    imgPrincipal : 'string',
    texte : 'string',
    imgSecondaire: 'string'
  }
}

export const HomeSchema = {
  name: 'Home',
  properties: {
    text: 'string'
  }
}

export const HistoireSchema = {
  name: 'Histoire',
  properties: {
    imgPrincipal : 'string',
    texte : 'string',
    imgSecondaire: 'string'
  }
}
// BDD longue mais pour un seul type de donnée qui diffère je préfère ajouter plutôt que changer la manière de faire derrière
export const VoyageSchema = {
  name: 'Voyage',
  properties: {
    imgPrincipal : 'string',
    titrePrincipal : 'string',
    imgSecondaire: 'string',
    titreSecondaire: 'string',
    imgTertiaire: 'string',
    titreTertiaire: 'string',
    imgArray1: {type:'string[]'},
    texteArray1: {type:'string[]'},
    imgArray2: {type:'string[]'},
    texteArray2: {type:'string[]'}
  }
}
// 3 cartes différentes, avec des logiques et des évènements différents, je ne pense pas pouvoir faire différemment pour l'instant
export const AmourSchema = {
  name: 'Amour',
  properties: {
    titre: 'string',
    texte1: 'string',
    texte2: 'string',
    texte3: 'string',
    texte4: 'string',
    question: 'string',
    reponse1: 'string',
    indice1: 'string',
    choix1: 'string',
    choix2: 'string'
  }
}