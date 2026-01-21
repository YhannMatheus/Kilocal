import { View, Text, TextInput, TouchableOpacity, ScrollView, ActivityIndicator, StatusBar } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RegisterForms, RegisterErrors } from "./types";
import { AuthContext } from "@/context/auth.context";
import React, {useState, useContext} from "react";
import { globalStyles } from "@/styles/global";
import { RootStackParamList } from "@/types";
import { theme } from "@/styles/theme";
import { api } from "@/services/api";
import { styles } from "./style";

type Props = NativeStackScreenProps<RootStackParamList, 'Register'>;

export default function RegisterScreen({ navigation }: Props) {
  // Correção: signInWithToken (Sign In)
  const { signInWithToken } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  const [forms, setForms] = useState<RegisterForms>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    dayOfBirth: '',
    monthOfBirth: '',
    yearOfBirth: '',
    height: 0, // Inicia como 0
    gender: "male",
  });

  const [errors, setErrors] = useState<RegisterErrors>({});

  const handleInputChange = (field: keyof RegisterForms, value: string | number) => {
    setForms(prev => ({ ...prev, [field]: value }));

    if (errors[field as keyof RegisterErrors]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };
  
  const handleGenderSelect = (selectedGender: 'male' | 'female') => {
    setForms(prev => ({ ...prev, gender: selectedGender }));
  };

  const validateForms = (): boolean => {
    const newErrors: RegisterErrors = {};

    if (forms.name.length < 6) newErrors.name = "O nome deve ter ao menos 6 caracteres.";
    if (!forms.email.includes("@")) newErrors.email = "E-mail inválido.";
    if (forms.password.length < 6) newErrors.password = "A senha deve ter ao menos 6 caracteres.";
    if (forms.password !== forms.confirmPassword) newErrors.confirmPassword = "As senhas não coincidem.";
    
    const day = parseInt(forms.dayOfBirth);
    if (isNaN(day) || day < 1 || day > 31) newErrors.dayOfBirth = "Dia inválido.";
    
    const month = parseInt(forms.monthOfBirth);
    if (isNaN(month) || month < 1 || month > 12) newErrors.monthOfBirth = "Mês inválido.";
    
    const year = parseInt(forms.yearOfBirth);
    const currentYear = new Date().getFullYear();
    if (isNaN(year) || year < 1900 || year > currentYear) newErrors.yearOfBirth = "Ano inválido.";
    
    if (forms.height <= 0) newErrors.height = "Altura inválida.";

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async () => {
    if (!validateForms()) return;

    setLoading(true);

    try {
      const payload = {
        name: forms.name,
        email: forms.email,
        password: forms.password,
        birth_date: `${forms.yearOfBirth}-${forms.monthOfBirth.padStart(2,'0')}-${forms.dayOfBirth.padStart(2,'0')}`,
        height_cm: forms.height,
        gender: forms.gender,
        activity_level: 'moderate' 
      };

      // Correção da rota: /user/register
      const response = await api.post('/user/register', payload);
      const { access_token } = response.data;

      if (access_token) {
        await signInWithToken(access_token);
      } else {
        alert('Erro ao registrar. Tente novamente mais tarde.');
        navigation.navigate('Login');
      }

    } catch (error: any) {
      console.log("Erro Registro Completo:", error);
      console.log("Erro Message:", error.message);
      console.log("Erik Response:", error.response);
      
      const msg = error.response?.data?.detail || error.message || 'Erro ao registrar.';
      alert(msg);

    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={globalStyles.container}>
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
      
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 40 }}>
        
        <Text style={[globalStyles.title, { marginTop: 40, color: theme.colors.primary }]}>
          REGISTRATION
        </Text>

        {/* --- NOME --- */}
        <Text style={globalStyles.inputLabel}>NOME COMPLETO</Text>
        <TextInput
          style={[globalStyles.input, errors.name && styles.inputError]}
          placeholder="Seu nome"
          placeholderTextColor={theme.colors.textLight}
          value={forms.name}
          onChangeText={(t) => handleInputChange('name', t)}
        />
        {errors.name && <Text style={styles.errorText}>{errors.name}</Text>}

        {/* --- EMAIL --- */}
        <Text style={globalStyles.inputLabel}>E-MAIL</Text>
        <TextInput
          style={[globalStyles.input, errors.email && styles.inputError]}
          placeholder="exemplo@email.com"
          placeholderTextColor={theme.colors.textLight}
          value={forms.email}
          onChangeText={(t) => handleInputChange('email', t)}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}

        {/* --- DATA DE NASCIMENTO (3 Inputs) --- */}
        <Text style={globalStyles.inputLabel}>DATA DE NASCIMENTO</Text>
        <View style={styles.row}>
          {/* DIA */}
          <View style={{ width: '30%' }}>
            <TextInput
              style={[globalStyles.input, errors.dayOfBirth && styles.inputError, {textAlign: 'center'}]}
              placeholder="DD"
              placeholderTextColor={theme.colors.textLight}
              value={forms.dayOfBirth}
              onChangeText={(t) => handleInputChange('dayOfBirth', t)}
              keyboardType="numeric"
              maxLength={2}
            />
          </View>
          {/* MÊS */}
          <View style={{ width: '30%' }}>
             <TextInput
              style={[globalStyles.input, errors.monthOfBirth && styles.inputError, {textAlign: 'center'}]}
              placeholder="MM"
              placeholderTextColor={theme.colors.textLight}
              value={forms.monthOfBirth}
              onChangeText={(t) => handleInputChange('monthOfBirth', t)}
              keyboardType="numeric"
              maxLength={2}
            />
          </View>
          {/* ANO */}
          <View style={{ width: '35%' }}>
             <TextInput
              style={[globalStyles.input, errors.yearOfBirth && styles.inputError, {textAlign: 'center'}]}
              placeholder="AAAA"
              placeholderTextColor={theme.colors.textLight}
              value={forms.yearOfBirth}
              onChangeText={(t) => handleInputChange('yearOfBirth', t)}
              keyboardType="numeric"
              maxLength={4}
            />
          </View>
        </View>
        {/* Mostra erro se houver em qualquer um dos campos */}
        {(errors.dayOfBirth || errors.monthOfBirth || errors.yearOfBirth) && (
          <Text style={styles.errorText}>Data inválida (Verifique dia, mês e ano)</Text>
        )}

        {/* --- ALTURA --- */}
        <Text style={globalStyles.inputLabel}>ALTURA (CM)</Text>
        <TextInput
          style={[globalStyles.input, errors.height && styles.inputError]}
          placeholder="175"
          placeholderTextColor={theme.colors.textLight}
          // Converte o number 0 para string vazia para não aparecer "0" no input
          value={forms.height === 0 ? '' : String(forms.height)}
          onChangeText={(t) => handleInputChange('height', Number(t))}
          keyboardType="numeric"
        />
        {errors.height && <Text style={styles.errorText}>{errors.height}</Text>}

        {/* --- GÊNERO --- */}
        <Text style={globalStyles.inputLabel}>GÊNERO</Text>
        <View style={styles.row}>
          <TouchableOpacity 
            style={[
              styles.genderButton, 
              forms.gender === 'male' ? styles.genderButtonSelected : styles.genderButtonUnselected
            ]}
            onPress={() => handleGenderSelect('male')}
          >
            <Text style={[styles.genderText, forms.gender === 'male' ? {color: '#FFF'} : {color: theme.colors.textLight}]}>
              MASCULINO
            </Text>
          </TouchableOpacity>

          <TouchableOpacity 
             style={[
              styles.genderButton, 
              forms.gender === 'female' ? styles.genderButtonSelected : styles.genderButtonUnselected
            ]}
            onPress={() => handleGenderSelect('female')}
          >
            <Text style={[styles.genderText, forms.gender === 'female' ? {color: '#FFF'} : {color: theme.colors.textLight}]}>
              FEMININO
            </Text>
          </TouchableOpacity>
        </View>

        {/* --- SENHAS --- */}
        <Text style={globalStyles.inputLabel}>SENHA</Text>
        <TextInput
          style={[globalStyles.input, errors.password && styles.inputError]}
          placeholder="Mínimo 6 caracteres"
          placeholderTextColor={theme.colors.textLight}
          secureTextEntry
          value={forms.password}
          onChangeText={(t) => handleInputChange('password', t)}
        />
        {errors.password && <Text style={styles.errorText}>{errors.password}</Text>}

        <Text style={globalStyles.inputLabel}>CONFIRMAR SENHA</Text>
        <TextInput
          style={[globalStyles.input, errors.confirmPassword && styles.inputError]}
          placeholder="Repita a senha"
          placeholderTextColor={theme.colors.textLight}
          secureTextEntry
          value={forms.confirmPassword}
          onChangeText={(t) => handleInputChange('confirmPassword', t)}
        />
        {errors.confirmPassword && <Text style={styles.errorText}>{errors.confirmPassword}</Text>}

        {/* --- BOTÕES --- */}
        {loading ? (
          <ActivityIndicator size="large" color={theme.colors.primary} style={{ marginTop: 20 }} />
        ) : (
          <TouchableOpacity style={globalStyles.primaryButton} onPress={handleRegister}>
            <Text style={globalStyles.buttonText}>CADASTRAR</Text>
          </TouchableOpacity>
        )}

        <TouchableOpacity onPress={() => navigation.goBack()} style={{ marginBottom: 20 }}>
          <Text style={[globalStyles.linkText, { marginTop: 20 }]}>Voltar ao Login</Text>
        </TouchableOpacity>

      </ScrollView>
    </View>
  );
}