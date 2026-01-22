import React, { useCallback } from 'react';
import { StatusBar, View, ActivityIndicator } from 'react-native';
import { AuthProvider } from '@/context/auth.context';
import { Routes } from '@/routes';
import { theme } from '@/styles/theme';

// 1. Importar as fontes que você quer usar
import { 
  useFonts, 
  Inter_400Regular, 
  Inter_600SemiBold, 
  Inter_700Bold 
} from '@expo-google-fonts/inter';
import * as SplashScreen from 'expo-splash-screen';

// (Opcional) Impede a Splash Screen de sumir até carregarmos tudo
SplashScreen.preventAutoHideAsync();

export default function App() {
  // 2. Carregar as fontes na memória
  const [fontsLoaded] = useFonts({
    Inter_400Regular,
    Inter_600SemiBold,
    Inter_700Bold,
  });

  // 3. Callback para esconder a Splash Screen quando a fonte carregar
  const onLayoutRootView = useCallback(async () => {
    if (fontsLoaded) {
      await SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  // Se a fonte não carregou, não mostra nada (ou retorna null)
  if (!fontsLoaded) {
    return null; 
  }

  // 4. Aplica o onLayout na View principal
  return (
    <View style={{ flex: 1 }} onLayout={onLayoutRootView}>
      <AuthProvider>
        <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
        <Routes />
      </AuthProvider>
    </View>
  );
}