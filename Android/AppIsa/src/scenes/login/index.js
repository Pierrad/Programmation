import React from 'react';
import {View, Alert, ImageBackground, StatusBar} from 'react-native';
// Sécurité biométrique
import TouchID from "react-native-touch-id";
// Icon personnalisée
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
// Notification locale
import NotificationService from '../../services/NotificationService';


const LoginScreen = ({navigation}) => {
  this.notification = new NotificationService(this.onNotification);
  onNotification = (notif) => {
    Alert.alert(notif.title, notif.message);
  }
  //Permissions to use notifications
  handlePerm = (perms) => {
    Alert.alert("Permissions", JSON.stringify(perms));
  }
  checkFingerPrint = () => {
    TouchID.authenticate()
      .then(success => {
        // on trigger une notif
        this.notification.scheduleNotification();
        navigation.reset({index: 0,routes: [{ name: 'App' }]})
      })
      .catch(e => {
        Alert.alert(
          'Error',
          'Not working',
          [
            {text: 'OK'},
          ]
        );
      });
  };
  return (
    <View>
      <StatusBar backgroundColor = "transparent" translucent />
      <ImageBackground source={require('../../assets/images/Wallpaper.jpg')} style={{width: '100%', height: '100%', }}>
        <View style = {{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
          <Icon name = "fingerprint" onPress={checkFingerPrint} size = {50} color = {"white"}></Icon>
        </View>
      </ImageBackground>
    </View>
  );
}

export default LoginScreen;
