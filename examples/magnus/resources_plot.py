import resources
import pandas as pd
import matplotlib.pyplot as plt

X_train = resources.X_train
y_train = resources.y_train
X_test = resources.X_test
y_test = resources.y_test

# create pandas dataframe from generated dataset
df = pd.concat([pd.DataFrame(X_train, columns=['X1', 'X2']),
                pd.DataFrame(y_train, columns=['Label1'])],
               axis=1)

# Plot the generated datasets
plt.scatter(df['X1'], df['X2'], c=df['Label1'])
plt.show()