import React, { useRef, useState } from 'react';
import {
  View, Text, StyleSheet, Button, Image, ActivityIndicator,
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as FileSystem from 'expo-file-system';

const SERVER_URL = 'http://172.18.239.123:5000/piece-detect';   // Updated IP address

export default function PieceDetectScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  const [loading, setLoading]   = useState(false);
  const [result, setResult]     = useState<string | null>(null); // base64 annotated jpeg
  const [squares, setSquares]   = useState<any[]>([]);

  if (!permission?.granted) {
    return (
      <View style={styles.container}>
        <Text>No camera permission</Text>
        <Button title="Grant" onPress={requestPermission} />
      </View>
    );
  }

  const captureAndSend = async () => {
    setLoading(true);
    try {
      const photo = await cameraRef.current?.takePictureAsync({ quality: 0.8 });
      if (!photo?.uri) throw new Error('Capture failed');

      // Build FormData
      const form = new FormData();
      form.append('image', {
        uri: photo.uri,
        name: 'board.jpg',
        type: 'image/jpeg',
      } as any);
      form.append('side', 'right_w');   // or expose a toggle

      // POST
      const res = await fetch(SERVER_URL, {
        method: 'POST',
        body: form,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Decide what to do with the response
      const contentType = res.headers.get('content-type') ?? '';
      if (!res.ok) {
        const errorText = await res.text();
        console.error('Server error details:', errorText);
        throw new Error(`Server error: ${res.status} - ${errorText}`);
      }

      const json = await res.json();
      console.log('Received response:', json);
      
      if (json.fen) {
        console.log('FEN string received:', json.fen);
      }
      
      if (json.image) {
        setResult(json.image);
      }
      
      if (json.squares && json.pieces) {
        const formattedSquares = json.squares.map((s: { square: string; center: [number, number] }) => ({
          name: s.square,
          center: s.center
        }));
        setSquares(formattedSquares);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      {!result && !squares.length && (
        <CameraView style={styles.camera} ref={cameraRef} facing="back" mode="picture" />
      )}

      {result && (
        <Image source={{ uri: result }} style={styles.resultImage} resizeMode="contain" />
      )}

      {squares.length > 0 && (
        <View style={styles.list}>
          {squares.map((s) => (
            <Text key={s.name}>{s.name} : [{s.center.join(', ')}]</Text>
          ))}
        </View>
      )}

      <View style={styles.buttonBar}>
        {!loading && !result && !squares.length && (
          <Button title="📸 Capture & Detect" onPress={captureAndSend} />
        )}
        {(result || squares.length > 0) && (
          <Button title="Retake" onPress={() => { setResult(null); setSquares([]); }} />
        )}
      </View>

      {loading && <ActivityIndicator size="large" color="#fff" style={styles.overlay} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  resultImage: { flex: 1 },
  list: { padding: 10 },
  buttonBar: { position: 'absolute', bottom: 40, alignSelf: 'center' },
  overlay: { position: 'absolute', top: '50%', left: '50%', marginLeft: -20 },
});