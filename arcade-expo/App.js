import React, { useRef } from 'react';
import { StyleSheet, SafeAreaView, BackHandler, Platform } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { WebView } from 'react-native-webview';
import { ARCADE_HTML } from './arcadeHtml';

export default function App() {
  const webViewRef = useRef(null);

  // Handle hardware Android back button
  React.useEffect(() => {
    if (Platform.OS === 'android') {
      const backAction = () => {
        if (webViewRef.current) {
          // Tell the web app to navigate back to the arcade hub if inside a game
          webViewRef.current.injectJavaScript(`
            if (window.__returnToHub) {
              window.__returnToHub();
            } else {
              const backBtn = document.querySelector('#btn-back-hub');
              if (backBtn && !backBtn.classList.contains('hidden')) {
                backBtn.click();
              }
            }
            true;
          `);
          return true;
        }
        return false;
      };

      const backHandler = BackHandler.addEventListener('hardwareBackPress', backAction);
      return () => backHandler.remove();
    }
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor="#0a0d14" translucent={false} />
      <WebView
        ref={webViewRef}
        originWhitelist={['*']}
        source={{ html: ARCADE_HTML, baseUrl: 'https://cyberarcade.local' }}
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        allowsInlineMediaPlayback={true}
        mediaPlaybackRequiresUserAction={false}
        overScrollMode="never"
        bounces={false}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0d14'
  },
  webview: {
    flex: 1,
    backgroundColor: '#0a0d14'
  }
});
