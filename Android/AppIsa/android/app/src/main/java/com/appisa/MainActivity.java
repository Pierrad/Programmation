package com.appisa;

import com.facebook.react.ReactActivity;
import org.devio.rn.splashscreen.SplashScreen; // Import this for Splash Screen
import android.os.Bundle; // Import this for Splash Screen

public class MainActivity extends ReactActivity {
  // Add this method to show the Splash Screen a bit longer
  @Override
  protected void onCreate(Bundle savedInstanceState) {
      SplashScreen.show(this);
      super.onCreate(savedInstanceState);
  }
  /**
   * Returns the name of the main component registered from JavaScript. This is used to schedule
   * rendering of the component.
   */
  @Override
  protected String getMainComponentName() {
    return "AppIsa";
  }
}
