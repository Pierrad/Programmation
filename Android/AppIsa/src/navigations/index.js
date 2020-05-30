import React from 'react';
import { Text, Image, StyleSheet } from 'react-native'
// Navigations
import { NavigationContainer } from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
// Icon personnalisée
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Les différentes pages de l'app
import LoginScreen from '../scenes/login';
import HomeScreen from '../scenes/home';
import RaisonScreen from '../scenes/raison';
import HistoireScreen from '../scenes/histoire';
import AmourScreen from '../scenes/amour';
import VoyageScreen from '../scenes/voyage';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

// On ajoute le Tab navigator au Stack, normalement plus besoin de toucher ça
function AllNavigator() {
    return (
        <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }}/>
                <Stack.Screen name="App" component={AppNavigator}   options={({ route }) => ({headerTitle: getHeaderTitle(route), headerTitleAlign: 'center'})}/>
            </Stack.Navigator>
        </NavigationContainer>
    );
}

// Tab Navigator, ici on pourra rajouter les pages au Tab
function AppNavigator() {
    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarIcon: ({ focused, color, size }) => {
                    let iconName;
                    // Focused veut dire si on est sur l'écran ou pas
                    if (route.name === 'Home') {
                    iconName = focused
                        ? 'home'
                        : 'home-outline';
                    } else if (route.name === 'Raison') {
                        iconName = focused ? 'upside' : 'emoticon-happy-outline';
                    } else if (route.name === 'Histoire') {
                        iconName = focused ? 'book' : 'book-outline';
                    }else if (route.name === 'Amour') {
                        iconName = focused ? 'heart' : 'heart-outline';
                    }else if (route.name === 'Voyage') {
                        iconName = focused ? 'airplane' : 'airplane-off';
                    }
                    if(iconName=='upside'){
                        return <Image style={styles.image} source={require('../assets/images/upside.png')}/>
                    }
                    else{
                        return <Icon name={iconName} size={size} color={color} />;
                    }
                },
            })}
            tabBarOptions={{
                activeTintColor: 'tomato',
                inactiveTintColor: 'gray',
            }}
        >
            <Tab.Screen name="Home" component={HomeScreen}  />
            <Tab.Screen name="Raison" component={RaisonScreen} />
            <Tab.Screen name="Histoire" component={HistoireScreen} />
            <Tab.Screen name="Amour" component={AmourScreen} />
            <Tab.Screen name="Voyage" component={VoyageScreen} />
        </Tab.Navigator>
    );
}

// Permet de changer le Head de la page selon la route prise par le navigateur
function getHeaderTitle(route) {
    // Access the tab navigator's state using `route.state`
    const routeName = route.state
      ? // Get the currently active route name in the tab navigator
        route.state.routes[route.state.index].name
      : // If state doesn't exist, we need to default to `screen` param if available, or the initial screen
        // In our case, it's "Home" as that's the first screen inside the navigator
        route.params?.screen || 'Home';

    switch (routeName) {
        case 'Home':
            return <Text> <Icon name={"gift-outline"} size={30} color={"tomato"} /> </Text>

        case 'Raison':
            return 'Raisons';
        case 'Histoire':
            return 'Histoires';
        case 'Voyage':
            return <Text> <Icon name={"airplane"} size={30} color={"tomato"} /> </Text>
        case 'Amour':
            return <Text> <Icon name={"heart-outline"} size={30} color={"tomato"} /> </Text>

    }
}

const styles = StyleSheet.create({
    image: {
      width: 20,
      height: 20
    },
  });

export default AllNavigator;