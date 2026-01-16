import React, { useContext } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { AuthContext } from '@/context/auth.context';
import { globalStyles } from '@/styles/global';

export default function DashboardScreen() {
  const { user, signOut } = useContext(AuthContext);

  return (
    <View style={globalStyles.container}>
      <Text style={[globalStyles.title, { color: '#FFF' }]}>Dashboard</Text>
      
      <Text style={{ color: '#FFF', textAlign: 'center', marginBottom: 20 }}>
        Bem-vindo, {user?.name || 'Atleta'}!
      </Text>

      <Button title="Sair (Logout)" onPress={signOut} color="red" />
    </View>
  );
}