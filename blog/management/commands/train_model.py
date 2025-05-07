# blog/management/commands/train_model.py

from django.core.management.base import BaseCommand
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import LSTM, Embedding, Dense, SpatialDropout1D, Dropout, Bidirectional
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

class Command(BaseCommand):
    help = 'Train a classification model'

    def handle(self, *args, **kwargs):
        # Path ke dataset dalam aplikasi Django
        dataset_path = os.path.join('blog', 'datasets', 'dataset1.csv')
        
        # Membaca dataset
        try:
            df = pd.read_csv(dataset_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(dataset_path, encoding='latin1')
            except UnicodeDecodeError:
                df = pd.read_csv(dataset_path, encoding='ISO-8859-1')

        # Preprocessing data
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.preprocessing.sequence import pad_sequences

        tokenizer = Tokenizer(num_words=5000, lower=True, oov_token='<UNK>')
        tokenizer.fit_on_texts(df['Text'].values)
        sequences = tokenizer.texts_to_sequences(df['Text'].values)
        word_index = tokenizer.word_index

        X = pad_sequences(sequences, maxlen=100)

        # Mengubah label menjadi format numerik
        label_encoder = LabelEncoder()
        df['Label'] = label_encoder.fit_transform(df['Label'])

        # One-hot encoding untuk dua label
        y = pd.get_dummies(df['Label']).values

        # Membagi data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Membangun model untuk dua kelas
        model = Sequential()
        model.add(Embedding(input_dim=len(word_index) + 1, output_dim=128))
        model.add(SpatialDropout1D(0.2))
        model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))  # Dua neuron untuk output dua kelas

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Callbacks untuk early stopping dan model checkpoint
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss', mode='min')

        # Pelatihan model
        history = model.fit(X_train, y_train, epochs=20, batch_size=64, validation_split=0.1, callbacks=[early_stopping, model_checkpoint])

        # Evaluasi model
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1)

        print(classification_report(y_test_classes, y_pred_classes))

        # Plotting confusion matrix
        conf_matrix = confusion_matrix(y_test_classes, y_pred_classes)
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title('Confusion Matrix')
        plt.savefig('confusion_matrix.png')

        # Simpan tokenizer
        with open('tokenizer.json', 'w') as f:
            f.write(tokenizer.to_json())

        self.stdout.write(self.style.SUCCESS('Model training complete and saved.'))
