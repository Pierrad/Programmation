package com.Pierrad.AppMum;
import android.annotation.SuppressLint;
import android.content.Context;

import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.StrictMode;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.InterstitialAd;
import com.google.android.gms.ads.MobileAds;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.translate.Translate;
import com.google.cloud.translate.TranslateOptions;
import com.google.cloud.translate.Translation;

import java.io.BufferedReader;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    public static List<String> myList = new ArrayList<>();

    private EditText inputToTranslate;
    private TextView translatedTv;
    private String originalText;
    private String translatedText;
    private boolean connected;
    public static Translate translate;

    private AdView mAdView;
    private InterstitialAd mInterstitialAd;


    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Test : ca-app-pub-3940256099942544~3347511713
        // Deploy : ca-app-pub-3871891744391537~7935908223
        MobileAds.initialize(this,
                "ca-app-pub-3871891744391537~7935908223");

        mAdView = findViewById(R.id.adView);
        AdRequest adRequest = new AdRequest.Builder().build();
        mAdView.loadAd(adRequest);

        mInterstitialAd = new InterstitialAd(this);
        // Test : ca-app-pub-3940256099942544/1033173712
        // Deploy : ca-app-pub-3871891744391537/2533206603
        mInterstitialAd.setAdUnitId("ca-app-pub-3871891744391537/2533206603");
        mInterstitialAd.loadAd(new AdRequest.Builder().build());
        mInterstitialAd.setAdListener(new AdListener() {
            public void onAdLoaded() {
                // Call displayInterstitial() function
                displayInterstitial();
            }
        });

        getTranslateService();

        inputToTranslate = findViewById(R.id.inputToTranslate);
        translatedTv = findViewById(R.id.translatedTv);
        Button translateButton = findViewById(R.id.translateButton);

        InputStream is = null;
        try {
            is = getAssets().open("wordlist.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
        BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8 ));
        String str;
        try {
            while ((str = br.readLine()) != null) {
                myList.add(str + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
            translatedTv.setText("fail");
        }

        int listSize = myList.size();
        /*
        Random rand = new Random();
        int n = rand.nextInt(listSize);
        translatedTv.setText(myList.get(n));
        translatedTv.setText(String.valueOf(listSize));
        */
        List<String> subList1 = new ArrayList<>(myList.subList(0, listSize));


        Intent intent = new Intent(this, Widget.class);
        intent.setAction(Widget.ACTION_TEXT_CHANGED);
        intent.putStringArrayListExtra("NewString", (ArrayList<String>) subList1);
        getApplicationContext().sendBroadcast(intent);

        translateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (checkInternetConnection()) {

                    //If there is internet connection, get translate service and start translation:
                    getTranslateService();
                    translate();

                } else {

                    //If not, display "no connection" warning:
                    translatedTv.setText(getResources().getString(R.string.no_connection));
                }
            }
        });

    }

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


    public void translate() {

        //Get input text to be translated:
        originalText = inputToTranslate.getText().toString();
        Translation translation = translate.translate(originalText, Translate.TranslateOption.targetLanguage("it"), Translate.TranslateOption.model("base"));
        translatedText = translation.getTranslatedText();
        //Translated text and original text are set to TextViews:
        translatedTv.setText(translatedText);

    }

    public boolean checkInternetConnection() {

        //Check internet connection:
        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);

        //Means that we are connected to a network (mobile or wi-fi)
        connected = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).getState() == NetworkInfo.State.CONNECTED ||
                connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState() == NetworkInfo.State.CONNECTED;

        return connected;
    }

    public String translateW(String mot){
        Translation translation = translate.translate(mot, Translate.TranslateOption.targetLanguage("it"), Translate.TranslateOption.model("base"));
        translatedText = translation.getTranslatedText();
        return translatedText;
    }
    public String translateW2(String mot){
        Translation translation = translate.translate(mot, Translate.TranslateOption.targetLanguage("fr"), Translate.TranslateOption.model("base"));
        translatedText = translation.getTranslatedText();
        return translatedText;
    }

    public void displayInterstitial() {
        // If Ads are loaded, show Interstitial else show nothing.
        if (mInterstitialAd.isLoaded()) {
            mInterstitialAd.show();
        }
    }

}