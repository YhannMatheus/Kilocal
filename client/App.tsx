import React, { useContext } from 'react';
import { ActivityIndicator, View, StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Contextos e Tipos
import { AuthProvider, AuthContext } from '@/context/auth.context';
import { RootStackParamList } from './src/types';
import { theme } from './src/styles/theme'; // Importe o tema para usar as cores

import { 
  LoginScreen,
  RegisterScreen,
  DashboardScreen } from '@/screens';

const Stack = createNativeStackNavigator<RootStackParamList>();

function Routes() {
  const { user, isLoading } = useContext(AuthContext);

  // 1. TELA DE CARREGAMENTO (SPLASH)
  if (isLoading) {
    return (
      <View style={{ 
        flex: 1, 
        justifyContent: 'center', 
        alignItems: 'center', 
        backgroundColor: theme.colors.background // Fundo Preto
      }}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  // 2. NAVEGAÇÃO PRINCIPAL
  return (
    <NavigationContainer>
      {/* StatusBar estilo 'light' para o texto (hora, bateria) ficar branco no fundo preto */}
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
      
      <Stack.Navigator 
        screenOptions={{ 
          headerShown: false, // Oculta o cabeçalho padrão em TODAS as telas
          contentStyle: { backgroundColor: theme.colors.background } // Garante fundo preto na transição
        }}
      >
        {user ? (
          // === FLUXO LOGADO ===
          <Stack.Screen name="Dashboard" component={DashboardScreen} />
        ) : (
          // === FLUXO GUEST (LOGIN/REGISTER) ===
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes />
    </AuthProvider>
  );
}