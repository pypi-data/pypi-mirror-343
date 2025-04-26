from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
from tensorflow.keras.optimizers import Adam
import numpy as np

class GenerativeFeedbackNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize generator
        self.generator = Sequential([
            Dense(hidden_size, input_dim=input_size),
            LeakyReLU(alpha=0.2),
            Dense(output_size, activation='linear')
        ])

        # Initialize discriminator
        self.discriminator = Sequential([
            Dense(hidden_size, input_dim=output_size),
            LeakyReLU(alpha=0.2),
            Dense(1, activation='sigmoid')
        ])

        self.discriminator.compile(
            loss='binary_crossentropy',
            optimizer=Adam(learning_rate=0.0002),
            metrics=['accuracy']
        )

    def train(self, real_data, epochs=1000, batch_size=32):
        # Generate noise and fake data
        noise = np.random.normal(0, 1, (batch_size, self.generator.input_shape[1]))
        generated_data = self.generator.predict(noise)
        
        # Labels for real and fake data
        real_labels = np.ones((batch_size, 1))
        fake_labels = np.zeros((batch_size, 1))
        
        # Train discriminator on real data
        self.discriminator.trainable = True
        d_loss_real = self.discriminator.train_on_batch(real_data, real_labels)
        
        # Train discriminator on fake data
        d_loss_fake = self.discriminator.train_on_batch(generated_data, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # Train generator to fool discriminator
        self.discriminator.trainable = False
        self.generator.compile(
            loss='binary_crossentropy',
            optimizer=Adam(learning_rate=0.0002)
        )
        g_loss = self.generator.train_on_batch(noise, real_labels)
        
        return d_loss, g_loss

    def predict(self, input_data):
        return self.generator.predict(input_data)