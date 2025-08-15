import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Link } from 'expo-router';

export default function Index() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>ChessVision</Text>
        <Text style={styles.subtitle}>Analyze Your Chess Games</Text>
      </View>
      
      <View style={styles.buttonsContainer}>
        <Link href="/(tabs)/camera" asChild>
          <TouchableOpacity style={styles.button}>
            <View style={styles.buttonContent}>
              <Text style={styles.buttonText}>New Game</Text>
              <Text style={styles.buttonIcon}>📸</Text>
            </View>
          </TouchableOpacity>
        </Link>

        <Link href="/(tabs)/Details" asChild>
          <TouchableOpacity style={styles.button}>
            <View style={styles.buttonContent}>
              <Text style={styles.buttonText}>Analyze Position</Text>
              <Text style={styles.buttonIcon}>🔍</Text>
            </View>
          </TouchableOpacity>
        </Link>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
    padding: 20,
  },
  header: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 60,
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#AAAAAA',
    textAlign: 'center',
    marginBottom: 40,
  },
  buttonsContainer: {
    paddingBottom: 60,
    gap: 16,
  },
  button: {
    backgroundColor: '#222222',
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderColor: '#333333',
  },
  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
  buttonIcon: {
    fontSize: 24,
  },
});
