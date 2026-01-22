// src/styles/global.ts
import { StyleSheet } from 'react-native';
import { theme } from './theme';

export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    padding: theme.spacing.large,
    justifyContent: 'center',
  },
  
  // LOGO (O "KILOCAL")
  logoContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: theme.spacing.small,
  },

  logoTextWhite: {
    fontSize: 40, // Letra bem grande
    fontWeight: '900', // Extra bold
    color: theme.colors.text,
  },
  logoTextBlue: {
    fontSize: 40,
    fontWeight: '900',
    color: theme.colors.primary,
  },
  
  // Subtítulo ("Sua performance...")
  title:{
    fontSize: theme.fontSizes.large,
    color: theme.colors.text,
    textAlign: 'center',
    marginBottom: 20,
  },

  subtitle: {
    fontSize: theme.fontSizes.medium,
    color: theme.colors.textLight,
    textAlign: 'center',
    marginBottom: 60, // Bastante espaço até os inputs
  },

  // Labels (E-MAIL, SENHA)
  inputLabel: {
    color: theme.colors.primary,
    fontSize: theme.fontSizes.small,
    fontWeight: 'bold',
    marginBottom: 8, // Espaço entre o label e o input
    marginTop: 10,
    textTransform: 'uppercase', // Força ficar maiúsculo
  },

  // O Input em si (Caixa cinza)
  input: {
    backgroundColor: theme.colors.card,
    borderRadius: 12, // Bordas bem arredondadas
    paddingVertical: 18, // Altura maior como na imagem
    paddingHorizontal: 20,
    fontSize: theme.fontSizes.medium,
    color: theme.colors.text,
    marginBottom: theme.spacing.medium,
  },

  // Botão Azul
  primaryButton: {
    backgroundColor: theme.colors.primary,
    paddingVertical: 18,
    borderRadius: 12, // Combina com o input
    alignItems: 'center',
    marginTop: 30,
    shadowColor: theme.colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5, // Sombra no Android
  },

  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 1, // Espaçamento entre letras (ENTRAR)
    textTransform: 'uppercase',
  },

  // Link inferior (Esqueceu a senha?)
  linkText: {
    color: theme.colors.textLight,
    textAlign: 'center',
    marginTop: theme.spacing.large,
    fontSize: theme.fontSizes.medium,
    textDecorationLine: 'underline',
  },
  
  //Check box styles
  checkBoxContainer:{
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.medium,
    marginTop: theme.spacing.medium,
  },

  checkbox :{
    marginRight: theme.spacing.small,
    borderRadius: 4,
    borderColor: theme.colors.textLight
  },

  checkBoxLabel:{
    color: theme.colors.text,
    fontSize: theme.fontSizes.medium,
  },
  greeting: {
    fontSize: 14,
    color: theme.colors.textLight,
    fontFamily: theme.fonts.regular, // <--- Agora isso existe e carrega a Inter!
},
userName: {
    fontSize: 24,
    color: theme.colors.text,
    fontFamily: theme.fonts.bold, // <--- Fica em negrito bonito
},


});