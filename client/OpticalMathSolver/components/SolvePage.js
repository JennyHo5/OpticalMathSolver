import MathView from 'react-native-math-view';
import React, { useState, useEffect } from 'react';
import { ActivityIndicator, Image, SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import * as FS from 'expo-file-system';

const SolvePage = ({ route, navigation }) => {
    const { capturedImage } = route.params;
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const solveImage = async () => {
        await this.toServer({
            type: capturedImage.type,
            base64: capturedImage.base64,
            uri: capturedImage.uri
        });
    };

    useEffect(() => {
        solveImage(); // Call solveImage when component mounts
    }, []);

    toServer = async (mediaFile) => {
        let schema = "http://";
        let host = process.env.EXPO_PUBLIC_HOST; // Copy only the host value from metro bundler -> run `flask run -h [host]` to start the backend
        let route = "/solve";
        let port = "5000";
        let url = "";
        let content_type = "";

        url = schema + host + ":" + port + route;

        try {
            let response = await FS.uploadAsync(url, mediaFile.uri, {
                headers: {
                    "content-type": content_type,
                },
                httpMethod: "POST",
                uploadType: FS.FileSystemUploadType.BINARY_CONTENT,
            });

            console.log("response.headers", response.headers);
            console.log("response.body", response.body);
            if (response.body.includes('error') || response.body.includes('Error')) {
                console.log("error");
                setError('Failed to process the image. Please try again.');
            } else {
                let responseObj = JSON.parse(response.body);
                setResult(responseObj);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.imageContainer}>
                <Image source={{ uri: capturedImage.uri }} style={styles.image} />
            </View>
            {error ? (
                <Text style={styles.text}>{error}</Text>
            ) : result ? (
                <ScrollView>
                {result.map((item, index) => (
                        <View key={index} style={styles.resultContainer}>
                            <Text style={styles.text}>Question {index + 1}: </Text>
                            <MathView
                                math={item.question}
                                style={{marginTop: 5, marginBottom: 5}}
                            />

                            <Text style={styles.text}>Answer: </Text>
                            <MathView
                                math={item.answer}
                                style={{marginTop: 5, marginBottom: 5}}
                            />
                        </View>
                    ))}
                </ScrollView>
            ) : (
                <ActivityIndicator size="large" />
            )}
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        // alignItems: 'center',
        // justifyContent: 'center',
    },
    imageContainer: {
        padding: 20,
        alignItems: 'center'
    },
    image: {
        resizeMode: 'contain',
        width: '100%',
        height: 200,
        aspectRatio: 1,
        marginBottom: 10,
    },
    text: {
        fontSize: 18,
        marginTop: 10,
        marginBottom: 10,
    },
    resultsContainer: {
        width: '100%',
        flexGrow: 1,
    },
    resultContainer: {
        backgroundColor: '#f0f0f0',
        borderRadius: 10,
        padding: 10,
        marginBottom: 10,
        marginHorizontal: 20
    },
});

export default SolvePage;