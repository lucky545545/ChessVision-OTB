import React, { useRef, useState } from 'react';
import { Button, Image, StyleSheet, View } from 'react-native';
import { CameraView, useCameraPermissions, CameraCapturedPicture } from 'expo-camera';

export default function CameraScreen() {
  /* 1️⃣ Permission hook */
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  /* 2️⃣ Where we’ll store the shot */
  const [photo, setPhoto] = useState<CameraCapturedPicture | null>(null);

  /* Wait until permission info is loaded */
  if (!permission) return <View />;
  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Button title="Grant camera permission" onPress={requestPermission} />
      </View>
    );
  }

  /* 3️⃣ The actual capture function */
  const takePicture = async () => {
    if (cameraRef.current) {
      const pic = await cameraRef.current.takePictureAsync({
        quality: 0.8,           // 0–1, optional
        base64: false,          // set true if you need base64
        skipProcessing: false,  // keep false for auto-rotation
      });
      setPhoto(pic);            // pic.uri is your local file
    }
  };
  

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef} facing="back" mode="picture">
        <View style={styles.buttonContainer}>
          <Button title="📸 Take Photo" onPress={takePicture} />
        </View>
      </CameraView>

      {photo && (
        <Image source={{ uri: photo.uri }} style={styles.preview} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  buttonContainer: { flex: 1, justifyContent: 'flex-end', margin: 32 },
  preview: { width: 200, height: 200, alignSelf: 'center', marginTop: 20 },
});