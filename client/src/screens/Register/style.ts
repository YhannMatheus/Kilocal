import { StyleSheet } from "react-native";
import { theme } from "@/styles/theme";

export const styles = StyleSheet.create({
    row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10
  },
  inputError: {
    borderColor: theme.colors.error,
    borderWidth: 1
  },
  errorText: {
    color: theme.colors.error,
    fontSize: 12,
    marginTop: -10,
    marginBottom: 10,
    marginLeft: 5
  },
  genderButton: {
    width: '48%',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  genderButtonSelected: {
    backgroundColor: theme.colors.primary,
  },
  genderButtonUnselected: {
    backgroundColor: theme.colors.card,
  },
  genderText: {
    fontWeight: 'bold',
    fontSize: 14,
  }
})