import {
  AdMob,

  BannerAdPosition,
  BannerAdSize,
  AdmobConsentStatus
} from '@capacitor-community/admob';
import { Capacitor } from '@capacitor/core';

// Google AdMob Configuration 
export const ADMOB_CONFIG = {
  // Production IDs 
  BANNER_ID: 'ca-app-pub-7426288615924368/5799892988',
  INTERSTITIAL_ID: 'ca-app-pub-7426288615924368/3139563918',

  // Google Official Test IDs (for fallback/development testing) 
  TEST_BANNER_ID: 'ca-app-pub-3940256099942544/6300978111',
  TEST_INTERSTITIAL_ID: 'ca-app-pub-3940256099942544/1033173712',
  REWARDED_ID: 'ca-app-pub-3940256099942544/5224354917',

  // Set to false for release APK / production, true during local development/debugging 
  IS_TESTING: true,

};
class AdService {
  constructor() {
    this.isInitialized = false;
    this.isBannerShowing = false;
    this.interstitialLoaded = false;
    this.rewardedLoaded = false;
  }

  isNativePlatform() {

    try {
      return typeof Capacitor !== 'undefined' && typeof Capacitor.isNativePlatform === 'function' && Capacitor.isNativePlatform();
    } catch (e) {
      return false;
    }
  }

  async init() {
    if (!this.isNativePlatform()) {

      console.log('[AdService] Non-native platform, skipping native AdMob initialization.');
      return;
    }

    try {
      if (typeof AdMob !== 'undefined' && AdMob.initialize) {
        await AdMob.initialize({
          initializeForTesting: ADMOB_CONFIG.IS_TESTING,
        });
        this.isInitialized = true;
        console.log('[AdService] AdMob initialized successfully');

        // Preload ads
        this.preloadInterstitial();
        this.preloadRewarded();
      }
    } catch (err) {
      console.warn('[AdService] AdMob initialization failed:', err);
    }
  }

  // --- BANNER AD ---
  async showBanner(position = BannerAdPosition.BOTTOM_CENTER) {
    if (!this.isNativePlatform() || !this.isInitialized) return;

    try {
      if (typeof AdMob !== 'undefined' && AdMob.showBanner) {
        await AdMob.showBanner({
          adId: ADMOB_CONFIG.BANNER_ID,
          adSize: BannerAdSize.BANNER,
          position: position,
          margin: 0,
          isTesting: ADMOB_CONFIG.IS_TESTING
        });
        this.isBannerShowing = true;
        console.log('[AdService] Banner shown');
      }
    } catch (err) {
      console.warn('[AdService] Failed to show banner:', err);
    }
  }

  async hideBanner() {
    if (!this.isNativePlatform() || !this.isBannerShowing) return;

    try {
      if (typeof AdMob !== 'undefined' && AdMob.hideBanner) {
        await AdMob.hideBanner();
        this.isBannerShowing = false;
      }
    } catch (err) {
      console.warn('[AdService] Failed to hide banner:', err);
    }
  }

  async resumeBanner() {
    if (!this.isNativePlatform()) return;
    try {
      if (typeof AdMob !== 'undefined' && AdMob.resumeBanner) {
        await AdMob.resumeBanner();
        this.isBannerShowing = true;
      }
    } catch (err) {
      console.warn('[AdService] Failed to resume banner:', err);
    }
  }

  // --- INTERSTITIAL AD ---
  async preloadInterstitial() {
    if (!this.isNativePlatform() || !this.isInitialized) return;

    try {
      if (typeof AdMob !== 'undefined' && AdMob.prepareInterstitial) {
        await AdMob.prepareInterstitial({
          adId: ADMOB_CONFIG.INTERSTITIAL_ID,
          isTesting: ADMOB_CONFIG.IS_TESTING,
        });
        this.interstitialLoaded = true;
        console.log('[AdService] Interstitial preloaded');
      }
    } catch (err) {
      this.interstitialLoaded = false;
      console.warn('[AdService] Failed to preload interstitial:', err);
    }
  }

  async showInterstitial() {
    if (!this.isNativePlatform() || !this.isInitialized) return;

    try {
      if (typeof AdMob !== 'undefined' && AdMob.showInterstitial) {
        await AdMob.showInterstitial();
        this.interstitialLoaded = false;
        this.preloadInterstitial();
      }
    } catch (err) {
      console.warn('[AdService] Failed to show interstitial. Attempting re-prep:', err);
      this.preloadInterstitial();
    }
  }

  // --- REWARDED VIDEO AD ---
  async preloadRewarded() {
    if (!this.isNativePlatform() || !this.isInitialized) return;

    try {
      if (typeof AdMob !== 'undefined' && AdMob.prepareRewardVideoAd) {
        await AdMob.prepareRewardVideoAd({
          adId: ADMOB_CONFIG.REWARDED_ID,
          isTesting: ADMOB_CONFIG.IS_TESTING,
        });
        this.rewardedLoaded = true;
        console.log('[AdService] Rewarded video preloaded');
      }
    } catch (err) {
      this.rewardedLoaded = false;
      console.warn('[AdService] Failed to preload rewarded video:', err);
    }
  }

  async showRewarded(onRewardCallback) {
    if (!this.isNativePlatform() || !this.isInitialized) {
      console.log('[AdService] Non-native or AdMob not ready; granting mock reward for testing/web.');
      if (typeof onRewardCallback === 'function') {
        onRewardCallback({ type: 'coins', amount: 100 });
      }
      return;
    }

    try {
      if (typeof AdMob !== 'undefined' && AdMob.showRewardVideoAd) {
        const rewardItem = await AdMob.showRewardVideoAd();
        console.log('[AdService] User earned reward:', rewardItem);
        if (typeof onRewardCallback === 'function') {
          onRewardCallback(rewardItem);
        }
        this.preloadRewarded();
      }
    } catch (err) {
      console.warn('[AdService] Failed to show rewarded video:', err);
      this.preloadRewarded();
    }
  }
}

export const adService = new AdService();
