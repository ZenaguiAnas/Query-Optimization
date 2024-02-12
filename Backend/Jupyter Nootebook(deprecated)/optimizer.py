import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

df = pd.read_csv('queries_dataset.csv')

df = df.dropna()

df['input_query'] = df['input_query'].astype(str)
df['optimized_query'] = df['optimized_query'].astype(str)

queries = df['input_query'].tolist()
optimized_queries = df['optimized_query'].tolist()

all_texts = queries + optimized_queries

# Tokenization
tokenizer = Tokenizer(filters='')
tokenizer.fit_on_texts(all_texts)

# Vocabulary size
vocab_size = len(tokenizer.word_index) + 1

tokenized_queries = tokenizer.texts_to_sequences(queries)
tokenized_optimized_queries = tokenizer.texts_to_sequences(optimized_queries)

max_len = max(max(len(seq) for seq in tokenized_queries), max(len(seq) for seq in tokenized_optimized_queries))
padded_queries = pad_sequences(tokenized_queries, padding='post', maxlen=max_len)
padded_optimized_queries = pad_sequences(tokenized_optimized_queries, padding='post', maxlen=max_len)

input_data = tf.convert_to_tensor(padded_queries)
output_data = tf.convert_to_tensor(padded_optimized_queries)

print("Tokenized Queries:\n", tokenized_queries)
print("\nTokenized Optimized Queries:\n", tokenized_optimized_queries)
print("\nPadded Queries:\n", padded_queries)
print("\nPadded Optimized Queries:\n", padded_optimized_queries)
print("\nVocabulary Size:", vocab_size)
print("\nMax Sequence Length:", max_len)


def build_sequence_to_sequence_model(vocab_size, max_len):
    encoder_inputs = Input(shape=(max_len,))
    encoder_embedding = Embedding(vocab_size, 128, input_length=max_len, mask_zero=True)(encoder_inputs)
    encoder_lstm, state_h, state_c = LSTM(128, return_state=True)(encoder_embedding)
    encoder_states = [state_h, state_c]

    decoder_inputs = Input(shape=(max_len,))
    decoder_embedding = Embedding(vocab_size, 128, input_length=max_len, mask_zero=True)(decoder_inputs)
    decoder_lstm = LSTM(128, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
    decoder_dense = Dense(vocab_size, activation='softmax')
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    return model

model = build_sequence_to_sequence_model(vocab_size, max_len)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()

input_train_np, input_test_np, output_train_np, output_test_np = train_test_split(
    input_data.numpy(), output_data.numpy(), test_size=0.2, random_state=42
)

input_train = tf.convert_to_tensor(input_train_np)
input_test = tf.convert_to_tensor(input_test_np)
output_train = tf.convert_to_tensor(output_train_np)
output_test = tf.convert_to_tensor(output_test_np)

model.fit([input_train, input_train], output_train, epochs=50, batch_size=1, validation_data=([input_test, input_test], output_test))

evaluation_result = model.evaluate([input_test, input_test], output_test, batch_size=1)
print("Evaluation Loss:", evaluation_result[0])
print("Evaluation Accuracy:", evaluation_result[1])

# Make predictions on the testing set
predictions = model.predict([input_test, input_test], batch_size=1)

for i in range(min(3, len(predictions))):
    print("\nExample", i + 1)
    print("Predicted Sequence:", predictions[i])
    print("Actual Output:", output_test[i])

def predict_optimized_query(new_query, tokenizer, model, max_len):
    tokenized_new_query = tokenizer.texts_to_sequences([new_query])
    padded_new_query = pad_sequences(tokenized_new_query, padding='post', maxlen=max_len)

    prediction = model.predict([padded_new_query, padded_new_query], batch_size=1)

    predicted_sequence = np.argmax(prediction, axis=-1)[0]
    predicted_query = " ".join(tokenizer.index_word[idx] for idx in predicted_sequence if idx != 0)

    return predicted_query

# Example usage:
new_query = 'SELECT name, age FROM users WHERE country = "France";'
predicted_optimized_query = predict_optimized_query(new_query, tokenizer, model, max_len)

print("Input Query:", new_query)
print("Predicted Optimized Query:", predicted_optimized_query)