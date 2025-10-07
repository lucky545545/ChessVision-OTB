import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ImageBackground } from 'react-native';
import { Link } from 'expo-router';

// A free-to-use, dark chess background image
// Go up two levels from (tabs) to reach the project root, then into 'assets'
const backgroundImage = require('../../assets/images/wp3269708-chess-wallpaper-black-and-white.jpg');

export default function Index() {
  return (
    <ImageBackground 
      source={backgroundImage} 
      resizeMode="cover" 
      style={styles.backgroundImageContainer}
    >
      {/* This overlay view darkens the background image to make text more readable */}
      <View style={styles.overlay}>
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
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  backgroundImageContainer: {
    flex: 1, // This makes the background image cover the entire screen
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)', // Semi-transparent black overlay
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
    color: '#DDDDDD', // Slightly brighter for better contrast on the overlay
    textAlign: 'center',
    marginBottom: 40,
  },
  buttonsContainer: {
    paddingBottom: 60,
    gap: 16,
  },
  button: {
    backgroundColor: 'rgba(34, 34, 34, 0.8)', // Made button slightly transparent
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderColor: '#444444', // Slightly lighter border
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
