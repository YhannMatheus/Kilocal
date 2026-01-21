import React, {useState, useEffect, useContext} from "react";
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '@/types';
import { AuthContext } from '@/context/auth.context';

type Props = NativeStackScreenProps<RootStackParamList, 'Dashboard'>;

export default function DashboardScreen({navigation}: Props) {
    const { user, signOut } = useContext(AuthContext);
    const [loading, setLoading] = useState(false);

}