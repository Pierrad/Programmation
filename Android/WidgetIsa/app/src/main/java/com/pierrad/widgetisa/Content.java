package com.pierrad.widgetisa;

import android.os.AsyncTask;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import java.io.IOException;


public class Content extends AsyncTask<String, Integer, String> {
    String title = "start";
    String[] titleOut = new String[2];


    protected String doInBackground(String... strings) {

        String url = "";
        try {
            //Connect to the website
            Document document = Jsoup.connect(url).get();
            //Get the title of the website
            title = document.title();
            titleOut = title.split("-");

        } catch (IOException e) {
            title = "fail";

        }
        return titleOut[0];
    }



    protected void onProgressUpdate(Integer... progress) {

    }

    protected void onPostExecute(Long result) {
    }
}

