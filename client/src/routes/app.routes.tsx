import React from "react";
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { RootStackParamList } from "@/types";

import { DashboardScreen } from "@/screens";
const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppRoutes(){
    return(
        <Stack.Navigator screenOptions={{headerShown: false}}>
            <Stack.Screen name="Dashboard" component={DashboardScreen}/>
        </Stack.Navigator>
    )
}