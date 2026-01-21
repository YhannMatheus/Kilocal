import React from "react";
import { View, Text, Dimensions, StyleSheet } from "react-native";
import { LineChart, ProgressChart } from "react-native-chart-kit";
import { theme } from "@/styles/theme";

// Tipagem correta dos tipos
type ChartType = "line" | "progress";

interface ChartProps {
  title: string;
  type: ChartType;
  data: number[];
  labels?: string[];
  height?: number;
  unity?: string;
}

// Estilos mantidos
const styles = StyleSheet.create({
  container: { marginBottom: 20 },
  title: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    marginLeft: 5
  },
  chartStyle: { marginVertical: 8, borderRadius: 16 },
  progressContainer: {
    backgroundColor: theme.colors.card,
    borderRadius: 16,
    padding: 10,
    alignItems: 'center',
    justifyContent: 'center'
  },
  emptyText: {
    position: 'absolute',
    alignSelf: 'center',
    top: '50%', // Ajustei para centralizar melhor
    color: theme.colors.textLight,
    fontSize: 14,
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 5,
    borderRadius: 5,
    zIndex: 10
  }
});

export const Graph = ({
  title,
  type,
  data,
  labels = [],
  height = 220,
  unity = ""
}: ChartProps) => {
  const screenWidth = Dimensions.get("window").width;
  const isEmpty = !data || data.length === 0;

  const chartConfig = {
    backgroundGradientFrom: theme.colors.card,
    backgroundGradientTo: theme.colors.card,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
    decimalPlaces: 2,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    propsForDots: { 
      r: "4",
      strokeWidth: "2",
      stroke: "#fff"
    }
  };

  if (type === "line") {
    const displayData = isEmpty ? [0, 0, 0, 0, 0] : data;
    const displayLabels = isEmpty ? ["-", "-", "-", "-", "-"] : labels;
    
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{title} {unity ? `(${unity})` : ''}</Text>
        <View>
            <LineChart
            data={{
                labels: displayLabels,
                datasets: [{ data: displayData }]
            }}
            width={screenWidth - 40}
            height={height}
            chartConfig={chartConfig}
            style={styles.chartStyle}
            withDots={!isEmpty}
            />
            
            {isEmpty && (
                <Text style={styles.emptyText}>Nenhum registro encontrado</Text>
            )}
        </View>
      </View>
    );
  }

  if (type === "progress") {
    const displayData = isEmpty ? [0, 0, 0] : data;
    const displayLabels = labels.length ? labels : ["Meta 1", "Meta 2", "Meta 3"];

    return (
      <View style={styles.container}>
        <Text style={styles.title}>{title}</Text>
        <View style={styles.progressContainer}>
          <ProgressChart
            data={{ 
              labels: displayLabels, 
              data: displayData 
            }}
            width={screenWidth - 40}
            height={height}
            strokeWidth={16}
            radius={32}
            hideLegend={false}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1, index) => {
                const colors = ['#0056D2', '#32D74B', '#FF453A'];
                
                const safeIndex = index ?? 0;
                
                const color = colors[safeIndex] || theme.colors.primary;
                return isEmpty ? `rgba(100,100,100, ${opacity * 0.2})` : color; 
              }
            }} 
          />
          {isEmpty && (
            <Text style={styles.emptyText}>Sem dados</Text>
          )}
        </View>
      </View>
    );
  }

  return null;
};