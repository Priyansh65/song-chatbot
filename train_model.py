import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -------------------------
# SAMPLE DATASET
# -------------------------
texts = [
    "I am very happy", "I feel amazing", "so excited today",
    "I am sad", "feeling depressed", "very lonely",
    "I am angry", "so frustrated", "hate this",
    "I love you", "feeling romantic", "miss you",
    "I am okay", "normal day", "nothing special"
]

labels = [
    "happy", "happy", "happy",
    "sad", "sad", "sad",
    "angry", "angry", "angry",
    "romantic", "romantic", "romantic",
    "chill", "chill", "chill"
]

# -------------------------
# TEXT PROCESSING
# -------------------------
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences, maxlen=10)

# -------------------------
# LABEL ENCODING
# -------------------------
encoder = LabelEncoder()
encoded_labels = encoder.fit_transform(labels)

# -------------------------
# MODEL
# -------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(1000, 16, input_length=10),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation="relu"),
    tf.keras.layers.Dense(5, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

model.fit(padded, encoded_labels, epochs=50, verbose=1)

# -------------------------
# SAVE MODEL
# -------------------------
model.save("emotion_model.h5")

import pickle
pickle.dump(tokenizer, open("tokenizer.pkl", "wb"))
pickle.dump(encoder, open("encoder.pkl", "wb"))

print("Model trained and saved")