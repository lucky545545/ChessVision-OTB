import React, { useRef, useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from './types';
import {  Button,Image,StyleSheet,View,ActivityIndicator,Text,Linking,} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as FileSystem from 'expo-file-system';


const SERVER_URL = 'http://192.168.11.123:5000/detect'; // <-- change IP



type DetailsScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'details'>;

export default function Details() {
  const navigation = useNavigation<DetailsScreenNavigationProp>();
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  const [loading, setLoading] = useState(false);
  const [processedUri, setProcessedUri] = useState<string | null>(null);

  if (!permission) return <View />;

  // If not granted, show improved request UI:
  if (!permission.granted) {
    const handlePress = async () => {
      if (permission.canAskAgain) {
        await requestPermission(); // await so state updates before re-render
      } else {
        // Permanently denied; guide user to settings
        Linking.openSettings();
      }
    };

    return (
      <View style={styles.container}>
        <Text style={styles.message}>
          We need camera permission to proceed.
        </Text>
        <Button
          title={
            permission.canAskAgain
              ? 'Grant Camera Permission'
              : 'Open Settings to Enable'
          }
          onPress={handlePress}
        />
      </View>
    );
  }

  const captureAndRunYOLO = async () => {
    setLoading(true);
    try {
      // 1. capture
      const pic = await cameraRef.current!.takePictureAsync?.({ quality: 0.8 });
      if (!pic?.uri) throw new Error('Failed to capture image');

      // 2. copy to DocumentDirectory
      const fileName = pic.uri.split('/').pop() ?? `${Date.now()}.jpg`;
      const localPath = `${FileSystem.documentDirectory}${fileName}`;
      await FileSystem.copyAsync({ from: pic.uri, to: localPath });

      // 3. upload
      const form = new FormData();
      form.append('image', {
        uri: localPath,
        name: 'board.jpg',
        type: 'image/jpeg',
      } as any);
      form.append('side', 'right_w');

      console.log('Sending image to server for square detection...');
      
      // Add a timeout to the fetch request
      const fetchWithTimeout = (url: string, options: any, timeout = 20000): Promise<Response> => {
        return Promise.race([
          fetch(url, options),
          new Promise<never>((_, reject) =>
            setTimeout(() => reject(new Error('Request timed out')), timeout)
          ),
        ]);
      };

      const res = await fetchWithTimeout(SERVER_URL, {
        method: 'POST',
        body: form,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server error: ${res.status} - ${errorText}`);
      }
      
      console.log('Received response from server.');

      // 4. save returned image
      const blob = await res.blob();
      const processedPath = `${FileSystem.documentDirectory}processed_${Date.now()}.jpg`;
      await FileSystem.writeAsStringAsync(
        processedPath,
        await new Promise<string>((resolve, reject) => {
          const fr = new FileReader();
          fr.onload = () => resolve((fr.result as string).split(',')[1]);
          fr.onerror = (e) => reject(e);
          fr.readAsDataURL(blob);
        }),
        { encoding: FileSystem.EncodingType.Base64 }
      );

      setProcessedUri(processedPath);
    } catch (e) {
      console.error('Error during square detection:', e);
      // You could add an alert here to notify the user
      // Alert.alert('Error', 'Could not detect squares. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
  <View style={styles.container}>
    {processedUri ? (
      <View style={styles.fullscreenContainer}>
        <Image
          source={{ uri: processedUri }}
          style={styles.fullscreenImage}
          resizeMode="contain"
        />
        <View style={styles.previewControls}>
  <Button title="Retake" onPress={() => setProcessedUri(null)} />
  <View style={{ marginTop: 8 }} />
  <Button
    title="Detect Pieces"
    onPress={() => {
      if (processedUri) {
        navigation.navigate('piece_dtct', { processedUri });
      }
    }}
  />
</View>
        
      </View>
    ) : (
      <CameraView style={styles.camera} ref={cameraRef} facing="back" mode="picture">
        <View style={styles.buttonContainer}>
          <Button title="📸 Detect Squares" onPress={captureAndRunYOLO} />
        </View>
      </CameraView>
    )}

    {loading && (
      <ActivityIndicator
        size="large"
        color="#fff"
        style={styles.overlay}
      />
    )}
  </View>
);

}

const styles = StyleSheet.create({
  fullscreenContainer: {
  flex: 1,
  backgroundColor: 'black',
  justifyContent: 'center',
  alignItems: 'center',
},
fullscreenImage: {
  width: '100%',
  height: '100%',
},
previewControls: {
  position: 'absolute',
  top: 40,
  right: 20,
},

  container: { flex: 1 },
  camera: { flex: 1 },
  buttonContainer: { flex: 1, justifyContent: 'flex-end', margin: 32 },
  overlay: { position: 'absolute', top: '50%', left: '50%', marginLeft: -20 },
  preview: { width: 200, height: 200, alignSelf: 'center', marginTop: 20 },
  message: { textAlign: 'center', marginBottom: 12, fontSize: 16 },
});
