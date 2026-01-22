import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator, Dimensions } from 'react-native';
import { useAuth } from '@/hooks/useAuth';
import { styles } from './style';
import { theme } from '@/styles/theme';
import { Feather } from '@expo/vector-icons'; // Ícones
import { Graph } from '@/components/Graph';

// Tipos auxiliares
interface DayTracker {
    day: string;
    trained: boolean;
    isToday: boolean;
}

export default function DashboardScreen() {
    const { user, signOut } = useAuth();
    const screenWidth = Dimensions.get('window').width;
    const cardWidth = screenWidth * 0.8 - 32;
    
    // Simulação dos dias da semana (Backend enviará isso depois)
    const weekDays: DayTracker[] = [
        { day: 'D', trained: false, isToday: false },
        { day: 'S', trained: true, isToday: false },
        { day: 'T', trained: true, isToday: false },
        { day: 'Q', trained: false, isToday: true }, // Hoje
        { day: 'Q', trained: false, isToday: false },
        { day: 'S', trained: false, isToday: false },
        { day: 'S', trained: false, isToday: false },
    ];

    // Simulação dos gráficos laterais
    const otherMetrics = [
        { id: 1, title: 'Peso', value: '75 kg', color: theme.colors.primary, data: [70, 72, 75] },
        { id: 2, title: 'IMC', value: '22.4', color: '#4D91FF', data: [21, 22, 22.4] },
        { id: 3, title: 'Hidratação', value: '2.0 L', color: '#00E0FF', data: [1.5, 2.5, 2.0] },
    ];

    return (
        <View style={styles.container}>
            {/* Header com Foto e Config */}
            <View style={styles.header}>
                <View style={styles.userInfo}>
                    <View style={styles.avatarContainer}>
                        {/* Pega a primeira letra do nome */}
                        <Text style={styles.avatarText}>{user?.name?.[0] || 'U'}</Text>
                    </View>
                    <Text style={styles.userName}>{user?.name}</Text>
                </View>

                <TouchableOpacity style={styles.settingsButton} onPress={signOut}>
                    <Feather name="settings" size={24} color={theme.colors.textLight} />
                </TouchableOpacity>
            </View>

            <ScrollView showsVerticalScrollIndicator={false}>
                
                {/* 1. Rastreador Semanal (Interruptores) */}
                <View style={styles.weekTrackerContainer}>
                    <Text style={styles.weekLabel}>FREQUÊNCIA SEMANAL</Text>
                    <View style={styles.daysRow}>
                        {weekDays.map((item, index) => (
                            <View 
                                key={index} 
                                style={[
                                    styles.daySwitch, 
                                    item.trained && styles.daySwitchActive,
                                    // Se for hoje mas não treinou, coloca borda de destaque? (Opcional)
                                    item.isToday && !item.trained && { borderColor: '#FFF' } 
                                ]}
                            >
                                <Text style={[styles.dayText, item.trained && styles.dayTextActive]}>
                                    {item.day}
                                </Text>
                            </View>
                        ))}
                    </View>
                </View>

                {/* 2. Gráfico Circular de Calorias (Gigante) */}
                <View style={styles.calorieSection}>
                    <View style={styles.calorieRing}>
                        <Text style={styles.calorieValue}>1.250</Text>
                        <Text style={styles.calorieLabel}>de 2.400 kcal</Text>
                    </View>
                </View>

                {/* 3. Carrossel Horizontal de Métricas */}
                <View style={styles.metricsSection}>
                    <Text style={styles.sectionTitle}>Outras Métricas</Text>
                    
                    <ScrollView 
                        horizontal 
                        showsHorizontalScrollIndicator={false}
                        contentContainerStyle={styles.horizontalScroll}
                    >
                        {otherMetrics.map(metric => (
                            <View key={metric.id} style={styles.graphCard}>
                                <Graph 
                                    title={metric.title}
                                    value={metric.value}
                                    data={metric.data}
                                    color={metric.color}
                                    width={cardWidth}
                                    height={160}
                                />
                            </View>
                        ))}
                    </ScrollView>
                </View>

            </ScrollView>
        </View>
    );
}