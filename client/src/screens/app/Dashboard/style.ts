import { StyleSheet, Dimensions } from 'react-native';
import { theme } from '@/styles/theme';

const { width } = Dimensions.get('window');

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
        paddingTop: 60,
    },
    
    // --- 1. HEADER (Foto + Config) ---
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 24,
        marginBottom: 24,
    },
    userInfo: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12, // Espaço entre foto e nome
    },
    avatarContainer: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: theme.colors.primary,
        justifyContent: 'center',
        alignItems: 'center',
    },
    avatarText: {
        color: '#FFF',
        fontSize: 18,
        fontFamily: theme.fonts.bold,
    },
    userName: {
        fontSize: 18,
        color: theme.colors.text,
        fontFamily: theme.fonts.bold,
    },
    settingsButton: {
        padding: 8,
        backgroundColor: '#2A2A2E',
        borderRadius: 12,
    },

    // --- 2. RASTREADOR SEMANAL (Interruptores) ---
    weekTrackerContainer: {
        paddingHorizontal: 24,
        marginBottom: 32,
    },
    weekLabel: {
        color: theme.colors.textLight,
        fontSize: 12,
        marginBottom: 10,
        fontFamily: theme.fonts.medium,
    },
    daysRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    daySwitch: {
        width: 40,
        height: 40, // Alterar para 60 se quiser estilo "cápsula"
        borderRadius: 20,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#2A2A2E',
    },
    daySwitchActive: {
        backgroundColor: theme.colors.primary,
        borderColor: theme.colors.primary,
    },
    dayText: {
        color: theme.colors.textLight,
        fontFamily: theme.fonts.medium,
        fontSize: 12,
    },
    dayTextActive: {
        color: '#FFF',
        fontFamily: theme.fonts.bold,
    },

    // --- 3. GRÁFICO CIRCULAR (Calorias) ---
    calorieSection: {
        alignItems: 'center',
        marginBottom: 40,
    },
    calorieRing: {
        width: 200,
        height: 200,
        borderRadius: 100,
        borderWidth: 15,
        borderColor: '#2A2A2E', // Fundo do anel
        justifyContent: 'center',
        alignItems: 'center',
        borderTopColor: theme.colors.primary, // Simula progresso (truque simples)
        borderRightColor: theme.colors.primary,
    },
    calorieValue: {
        fontSize: 32,
        fontFamily: theme.fonts.bold,
        color: theme.colors.text,
    },
    calorieLabel: {
        fontSize: 14,
        color: theme.colors.textLight,
        fontFamily: theme.fonts.regular,
    },

    // --- 4. CARROSSEL DE GRÁFICOS ---
    metricsSection: {
        marginBottom: 40,
    },
    sectionTitle: {
        paddingHorizontal: 24,
        fontSize: 18,
        color: theme.colors.text,
        marginBottom: 16,
        fontFamily: theme.fonts.medium,
    },
    horizontalScroll: {
        paddingLeft: 24, // Espaço inicial
    },
    graphCard: {
        width: width * 0.8, // Ocupa 80% da tela para mostrar que tem mais ao lado
        marginRight: 16,
        backgroundColor: '#1E1E22', // Cartão mais escuro
        borderRadius: 16,
        padding: 16,
    }
});