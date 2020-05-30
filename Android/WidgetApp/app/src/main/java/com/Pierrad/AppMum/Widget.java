package com.Pierrad.AppMum;

import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;

import android.os.Bundle;
import android.widget.RemoteViews;

import java.util.List;

public class Widget extends AppWidgetProvider {

    public static final String ACTION_TEXT_CHANGED = "com.Pierrad.AppMum.TEXT_CHANGED";
    public static List<String> test;
    //public static String mot = "okkk";

    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);
        if (intent.getAction() != null && intent.getAction().equals(ACTION_TEXT_CHANGED)) {
            // handle intent here
            //mot = "dab";
            test = intent.getStringArrayListExtra("NewString");
        }

    }


    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager,
                                int appWidgetId) {

            // Construct the RemoteViews object
            RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget);

            ClickIntentService intent = new ClickIntentService();
            // Passe de mot anglais a italien
            String word = intent.getStart(test);
            // Passe de mot italien a Francais
            String mot = intent.test(word);

            views.setTextViewText(R.id.textView, word);
            views.setTextViewText(R.id.textView2, mot);

            // Instruct the widget manager to update the widget
            appWidgetManager.updateAppWidget(appWidgetId, views);
        }

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        // There may be multiple widgets active, so update all of them
        for (int appWidgetId : appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId);
        }
    }

    @Override
    public void onEnabled(Context context) {
        // Enter relevant functionality for when the first widget is created
    }

    @Override
    public void onDisabled(Context context) {
        // Enter relevant functionality for when the last widget is disabled
    }

    @Override
    public void onAppWidgetOptionsChanged(Context context, AppWidgetManager appWidgetManager, int appWidgetId, Bundle newOptions) {
        super.onAppWidgetOptionsChanged(context, appWidgetManager, appWidgetId, newOptions);
        updateAppWidget(context, appWidgetManager, appWidgetId);
    }

}