import pandas as pd
import numpy as np
from game import Board
from montecarlo import MCTS
from aux_funcs import board_to_flat, board_to_tensor
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import SparseCategoricalCrossentropy

TITLE_ROW = [
    'move', 'score', 't0_0', 't1_0', 't2_0', 't3_0', 't4_0', 't5_0', 't6_0', 't7_0', 't8_0', 't9_0', 't10_0', 't11_0',
    't12_0', 't13_0', 't14_0', 't15_0', 't0_2', 't1_2', 't2_2', 't3_2', 't4_2', 't5_2', 't6_2', 't7_2', 't8_2', 't9_2',
    't10_2', 't11_2', 't12_2', 't13_2', 't14_2', 't15_2', 't0_4', 't1_4', 't2_4', 't3_4', 't4_4', 't5_4', 't6_4',
    't7_4', 't8_4', 't9_4', 't10_4', 't11_4', 't12_4', 't13_4', 't14_4', 't15_4', 't0_8', 't1_8', 't2_8', 't3_8',
    't4_8', 't5_8', 't6_8', 't7_8', 't8_8', 't9_8', 't10_8', 't11_8', 't12_8', 't13_8', 't14_8', 't15_8', 't0_16',
    't1_16', 't2_16', 't3_16', 't4_16', 't5_16', 't6_16', 't7_16', 't8_16', 't9_16', 't10_16', 't11_16', 't12_16',
    't13_16', 't14_16', 't15_16', 't0_32', 't1_32', 't2_32', 't3_32', 't4_32', 't5_32', 't6_32', 't7_32', 't8_32',
    't9_32', 't10_32', 't11_32', 't12_32', 't13_32', 't14_32', 't15_32', 't0_64', 't1_64', 't2_64', 't3_64', 't4_64',
    't5_64', 't6_64', 't7_64', 't8_64', 't9_64', 't10_64', 't11_64', 't12_64', 't13_64', 't14_64', 't15_64', 't0_128',
    't1_128', 't2_128', 't3_128', 't4_128', 't5_128', 't6_128', 't7_128', 't8_128', 't9_128', 't10_128', 't11_128',
    't12_128', 't13_128', 't14_128', 't15_128', 't0_256', 't1_256', 't2_256', 't3_256', 't4_256', 't5_256', 't6_256',
    't7_256', 't8_256', 't9_256', 't10_256', 't11_256', 't12_256', 't13_256', 't14_256', 't15_256', 't0_512', 't1_512',
    't2_512', 't3_512', 't4_512', 't5_512', 't6_512', 't7_512', 't8_512', 't9_512', 't10_512', 't11_512', 't12_512',
    't13_512', 't14_512', 't15_512', 't0_1024', 't1_1024', 't2_1024', 't3_1024', 't4_1024', 't5_1024', 't6_1024',
    't7_1024', 't8_1024', 't9_1024', 't10_1024', 't11_1024', 't12_1024', 't13_1024', 't14_1024', 't15_1024', 't0_2048',
    't1_2048', 't2_2048', 't3_2048', 't4_2048', 't5_2048', 't6_2048', 't7_2048', 't8_2048', 't9_2048', 't10_2048',
    't11_2048', 't12_2048', 't13_2048', 't14_2048', 't15_2048', 't0_4096', 't1_4096', 't2_4096', 't3_4096', 't4_4096',
    't5_4096', 't6_4096', 't7_4096', 't8_4096', 't9_4096', 't10_4096', 't11_4096', 't12_4096', 't13_4096', 't14_4096',
    't15_4096', 't0_8192', 't1_8192', 't2_8192', 't3_8192', 't4_8192', 't5_8192', 't6_8192', 't7_8192', 't8_8192',
    't9_8192', 't10_8192', 't11_8192', 't12_8192', 't13_8192', 't14_8192', 't15_8192', 't0_16384', 't1_16384',
    't2_16384', 't3_16384', 't4_16384', 't5_16384', 't6_16384', 't7_16384', 't8_16384', 't9_16384', 't10_16384',
    't11_16384', 't12_16384', 't13_16384', 't14_16384', 't15_16384', 't0_32768', 't1_32768', 't2_32768', 't3_32768',
    't4_32768', 't5_32768', 't6_32768', 't7_32768', 't8_32768', 't9_32768', 't10_32768', 't11_32768', 't12_32768',
    't13_32768', 't14_32768', 't15_32768']

# MCTS
N_SIMS = 10
# RL Model
N_RUNS = 30
N_TOP_RUNS = 10
MODEL_PATH = './cnn_model.keras'

while True:
    df = pd.DataFrame(columns=TITLE_ROW)

    model = load_model(MODEL_PATH)

    for i in range(N_RUNS):
        prev_boards = []
        prev_moves = []
        board = Board()
        while not board.game_over:
            move = MCTS(board, heuristic=model).best_move(N_SIMS)
            prev_boards.append(board.get_board())
            prev_moves.append(move)
            board.make_move(move)
        for idx, b in enumerate(prev_boards):
            b = board_to_flat(b)
            df.loc[len(df)] = np.insert(b, 0, [prev_moves[idx], board.get_score()])
        print(f'{i} done, score: {board.get_score()}')

    # take best runs
    df.sort_values(['score'], ascending=False, inplace=True)
    train_df = df[df['score'].isin(df['score'].unique()[:N_TOP_RUNS])].astype(float)
    train_df['score'] = train_df['score'] / (train_df['score'].abs().max() + 1)

    # Train and Test Split
    X_train, X_test, y_train, y_test = train_test_split(train_df.iloc[:, 2:],
                                                        train_df['move'],
                                                        random_state=42,
                                                        test_size=0.1,
                                                        shuffle=True)

    # Define CNN
    cnn = Sequential()
    cnn.add(layers.Reshape((16, 4, 4), input_shape=(256,)))
    cnn.add(layers.Conv2D(256, 2, padding='same', activation='relu'))
    cnn.add(layers.Conv2D(256, 2, padding='same', activation='relu'))
    cnn.add(layers.Conv2D(256, 2, padding='same', activation='relu'))
    cnn.add(layers.Flatten())
    cnn.add(layers.Dense(256, activation='relu'))
    cnn.add(layers.Dense(4, activation='softmax'))

    cnn.compile(optimizer='adam',
                loss=SparseCategoricalCrossentropy(),
                metrics=['accuracy'])

    cnn.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test))

    if cnn.evaluate(X_test,  y_train) > model.evaluate(X_test,  y_train):
        cnn.save(MODEL_PATH)
        print('model updated')
