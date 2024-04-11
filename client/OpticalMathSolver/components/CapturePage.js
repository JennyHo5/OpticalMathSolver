import React, { useState, useEffect, useRef } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { Camera, CameraType } from 'expo-camera';
import Button from './Button';


const CapturePage = ({ navigation }) => {
    const [image, setImage] = useState(null);
    const [imageUri, setImageUri] = useState(null);


    const takePicture = async () => {
        try {
            await ImagePicker.requestCameraPermissionsAsync();
            let result = await ImagePicker.launchCameraAsync({
                cameraType: ImagePicker.CameraType.back,
                allowsEditing: true,
                quality: 1
            });

            if (!result.canceled) {
                setImage(result.assets[0]);
                setImageUri(result.assets[0].uri);
            }

        } catch (e) {
            console.log(e);
        }

    }

    // Pick image from the Photos library on phone
    const pickImage = async () => {
        try {
            await ImagePicker.requestMediaLibraryPermissionsAsync();
            let pickImage = await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.All,
                base64: true,
                allowsEditing: true,
                quality: 1
            });
    
            if (!pickImage.canceled) {
                setImage(pickImage.assets[0]);
                setImageUri(pickImage.assets[0].uri);
            }
        } catch (e) {
            console.log(e);
        }
    };

    const navigateToSolvePage = () => {
        navigation.navigate('SolvePage', { capturedImage: image });
    }

    return (
        <View style={styles.container}>

            {image ?
                <View style={{padding: 20}}>
                    <Image source={{ uri: imageUri, }} style={styles.image} />
                    <Button title="Confirm" onPress={navigateToSolvePage} />
                    <Button title={"Reset"} icon="retweet" onPress={() => setImage(null)} />
                </View>
                :
                <View style={styles.iconContainer}>
                    <View>
                        <Button title="Upload from Album" icon="image" onPress={pickImage} />
                    </View>
                    <View>
                        <Button title="Take a Photo" icon="camera" onPress={takePicture} />
                    </View>
                </View>
            }

        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffffff',
        justifyContent: 'center',
        paddingBottom: 40
    },
    image: {
        resizeMode: 'contain',
        width: '100%', // Fill available width
        aspectRatio: 1,
        marginBottom: 20,
    },
    camera: {
        flex: 1,
        borderRadius: 20,
    },
    iconContainer: {
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        fontSize: 18,
        marginBottom: 20,
    },
});

export default CapturePage;
