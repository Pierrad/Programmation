package com.Pierrad.AppMum;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;
import android.annotation.SuppressLint;

import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.StrictMode;
import android.widget.TextView;

import android.widget.EditText;

import androidx.core.widget.ListPopupWindowCompat;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.translate.Translate;
import com.google.cloud.translate.TranslateOptions;
import com.google.cloud.translate.Translation;

import java.io.IOException;
import java.io.InputStream;

import java.util.List;
import java.util.Random;

public class ClickIntentService extends IntentService {

    private EditText inputToTranslate;
    private TextView translatedTv;
    private String translatedText;
    private boolean connected;
    Translate translate;

    @SuppressLint("SetTextI18n")



    public ClickIntentService() {
        super("ClickIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {


    }

        /*
        AppWidgetManager appWidgetManager = AppWidgetManager.getInstance(this);
        int[] widgetIds = appWidgetManager.getAppWidgetIds(new ComponentName(this, Widget.class));
        for (int appWidgetId : widgetIds) {
            Widget.updateAppWidget(getApplicationContext(), appWidgetManager, appWidgetId);
        }
        */

    public void getTranslateService() {

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try (InputStream is = getResources().openRawResource(R.raw.identifiant)) {

            //Get credentials:
            final GoogleCredentials myCredentials = GoogleCredentials.fromStream(is);

            //Set credentials and get translate service:
            TranslateOptions translateOptions = TranslateOptions.newBuilder().setCredentials(myCredentials).build();
            translate = translateOptions.getService();

        } catch (IOException ioe) {
            ioe.printStackTrace();

        }
    }

    public String translate(String word) {
            getTranslateService();
            Translation translation = translate.translate(word, Translate.TranslateOption.targetLanguage("fr"), Translate.TranslateOption.model("base"));
            translatedText = translation.getTranslatedText();

            return translatedText;
        }

    public boolean checkInternetConnection() {

        //Check internet connection:
        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);

        //Means that we are connected to a network (mobile or wi-fi)
        connected = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).getState() == NetworkInfo.State.CONNECTED ||
                connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState() == NetworkInfo.State.CONNECTED;

        return connected;
    }

    public String getStart(List<String> array) {

        Random rand = new Random();
        int listSize = array.size();
        int n = rand.nextInt(listSize);
        MainActivity intent = new MainActivity();
        String word = intent.translateW(array.get(n));
        return word;
    }

    public String test(String mot){
        MainActivity intent = new MainActivity();
        String word = intent.translateW2(mot);
        return word;
    }


}