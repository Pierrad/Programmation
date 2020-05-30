import React, {useState} from 'react';
import {View, Text, StyleSheet, Image, Button} from 'react-native';
import firebase from 'react-native-firebase';
import RNFetchBlob from 'rn-fetch-blob';

getBase64 = async (url) => {
  const fs = RNFetchBlob.fs;
  let imagePath = null;
  let base64 = 64;

  await RNFetchBlob
    .config({
      fileCache: true
    })
    .fetch("GET", url)
    // the image is now dowloaded to device's storage
    .then(resp => {
      // the image path you can use it directly with Image component
      imagePath = resp.path();
      return resp.readFile("base64");
    })
    .then(base64Data => {
      // here's base64 encoded image
      base64 = base64Data.toString();
      // remove the file from storage
      return fs.unlink(imagePath);
    });
  return base64;
}

// async function
getUrl = async (ref) => {
  return url = await ref.getDownloadURL();
}

const HomeScreen = () => {
  const [imgSource, setUrl] = useState(undefined);
  const [imgBase64, setBase] = useState("rien");
  const reference = firebase.storage().ref('Test/MajJapan.jpg');
  let url = new String("ok");
  let base64 = new String("ko");

  base64 = getUrl(reference)
  .then(newUrl => {
    url = newUrl;
    return getBase64(newUrl)
  })
  .then(base => {
    if (base !== null){
      return base;
    }
  });

  return (
    <View style={styles.home}>
      <Text>Home</Text>
      <Button onPress={() => {setUrl(`data:image/jpg;base64,${base64["_55"]}`);}} title='rekt'/>
      <Image style = {styles.image} source={{uri: imgSource}}/>
    </View>
  );
};

// Définition des styles
const styles = StyleSheet.create({
  home: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white'
  },
  image: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 100,
    width: 100
  }
});

export default HomeScreen;