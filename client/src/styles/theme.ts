// src/styles/theme.ts

export const colors = {
  background: '#121212',   // Fundo quase preto (igual da imagem)
  primary: '#0056D2',      // Azul vibrante do botão e do "CAL"
  card: '#2A2A2A',         // Cinza escuro para o fundo dos inputs
  text: '#FFFFFF',         // Texto principal branco
  textLight: '#8E8E93',    // Cinza para subtítulos e placeholders
  textHighlight: '#0056D2',// Azul para os labels (E-MAIL, SENHA)
  error: '#FF453A',
  success: '#32D74B',
  primary_opacity: 'rgba(0, 86, 210, 0.2)',
};

export const fontSizes = {
  small: 12,
  medium: 16,
  large: 24,
  xlarge: 32,
};

export const spacing = {
  small: 8,
  medium: 16,
  large: 24,
  xlarge: 40, // Espaçamento maior para o topo
};

  // ADICIONE ISSO AQUI:
export const fonts = {
  regular: 'Inter_400Regular', // Texto comum
  medium: 'Inter_600SemiBold', // Subtítulos ou botões
  bold: 'Inter_700Bold',       // Títulos grandes
}

export const theme = {
  colors,
  fontSizes,
  spacing,
  fonts,
};