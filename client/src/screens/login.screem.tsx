import { View, Text, TextInput, ActivityIndicator, TouchableOpacity, StatusBar } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { AuthContext } from '@/context/auth.context';
import React, { useState, useContext } from 'react';
import { RootStackParamList } from '@/types';
import { globalStyles } from '@/styles/global';
import { theme } from '@/styles/theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Login'>;

export const LoginScreen = ({ navigation }: Props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signIn } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!email || !password) return;
    
    setLoading(true);
    try {
      await signIn(email, password);
    } catch (error) {
      alert('Erro ao logar. Verifique credenciais.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={globalStyles.container}>
      {/* Garante que a barra de status (bateria, hora) fique branca */}
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />

      {/* LOGO: KILO (Branco) + CAL (Azul) */}
      <View style={globalStyles.logoContainer}>
        <Text style={globalStyles.logoTextWhite}>KILO</Text>
        <Text style={globalStyles.logoTextBlue}>CAL</Text> 
        {/* Na imagem parece KILOCALL com dois Ls, mas o nome do seu projeto é KiloCal. 
            Ajuste aqui se quiser adicionar o 'L' extra */}
      </View>

      <Text style={globalStyles.subtitle}>Sua performance em tempo real</Text>
      
      {/* Label e Input de Email */}
      <Text style={globalStyles.inputLabel}>E-MAIL</Text>
      <TextInput 
        placeholder="atleta@exemplo.com" 
        placeholderTextColor={theme.colors.textLight} 
        style={globalStyles.input} 
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      
      {/* Label e Input de Senha */}
      <Text style={globalStyles.inputLabel}>SENHA</Text>
      <TextInput 
        placeholder="••••••••" 
        placeholderTextColor={theme.colors.textLight}
        style={globalStyles.input} 
        secureTextEntry 
        value={password}
        onChangeText={setPassword}
      />
      
      {loading ? (
        <ActivityIndicator size="large" color={theme.colors.primary} style={{ marginTop: 30 }} />
      ) : (
        <TouchableOpacity style={globalStyles.primaryButton} onPress={handleLogin}>
          <Text style={globalStyles.buttonText}>ENTRAR</Text>
        </TouchableOpacity>
      )}
      
      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={globalStyles.linkText}>Esqueceu a senha?</Text>
      </TouchableOpacity>
      
      {/* Botão temporário para ir ao registro */}
      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={[globalStyles.linkText, { color: theme.colors.primary, marginTop: 10, textDecorationLine: 'none' }]}>
          Não tem conta? Cadastre-se
        </Text>
      </TouchableOpacity>
    </View>
  );
}
