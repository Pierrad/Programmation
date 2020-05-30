/*
Service de Notification locale qui est appelé à chaque ouverture de l'application pour trigger une notif qui se lancera chaque jour
*/

// Notification locale
import PushNotification from 'react-native-push-notification';

export default class NotificationService {
    // onNotificaitn is a function passed in that is to be called when a
    // notification is to be emitted.
    constructor(onNotification) {
        this.configure(onNotification);
        this.lastId = 0;
    }

    configure(onNotification) {
        PushNotification.configure({
            onNotification: onNotification,

            // IOS ONLY (optional): default: all - Permissions to register.
            permissions: {
            alert: true,
            badge: true,
            sound: true
            },

            popInitialNotification: true,
        });
    }
    // On s'en sert pas
    //Appears right away
    localNotification() {
        this.lastId++;
        PushNotification.localNotification({
            title: "Local Notification",
            message: "My Notification Message",
            playSound: false,
            actions: '["Yes", "No"]'
        });
    }

    //Appears after a specified time. App does not have to be open.
    scheduleNotification() {
        // On cancel toutes les anciennes notifs pour pas rajouter une notif à chaque fois que l'on ouvre l'app
        this.cancelAll();
        this.lastId++;
        PushNotification.localNotificationSchedule({
            smallIcon: "icon",
            date: new Date(Date.now() + (30 * 1000)), //30 seconds
            title: "Envie d'un câlin ?",
            message: "Il te reste peut-être des choses à lire...",
            playSound: false,
            repeatType: 'day'
        });
    }

    checkPermission(cbk) {
        return PushNotification.checkPermissions(cbk);
    }

    cancelNotif() {
        PushNotification.cancelLocalNotifications({id: ''+this.lastId});
    }

    cancelAll() {
        PushNotification.cancelAllLocalNotifications();
    }
}