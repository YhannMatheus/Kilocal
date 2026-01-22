import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';

import { useAuth } from '@/hooks/useAuth';
import { AuthRoutes } from './auth.routes';
import { AppRoutes } from './app.routes';
import { theme } from '@/styles/theme';

export function Routes() {
  const { user, isLoading } = useAuth();

  // 1. Tela de Carregamento (Enquanto verifica se tem token salvo)
  if (isLoading) {
    return (
      <View style={{ 
        flex: 1, 
        justifyContent: 'center', 
        alignItems: 'center', 
        backgroundColor: theme.colors.background 
      }}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  // 2. Decisão de qual navegador mostrar
  return (
    <NavigationContainer>
      {user ? <AppRoutes /> : <AuthRoutes />}
    </NavigationContainer>
  );
}
