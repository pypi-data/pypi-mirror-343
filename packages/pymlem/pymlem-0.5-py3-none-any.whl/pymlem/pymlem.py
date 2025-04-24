class PyMlem:
    def __init__(self):
        pass
    
    def linear_regression(self):
        return (r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "b3db0009-5416-4119-845c-4d2fdb27a353",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "d20ff5f4-c53a-4a99-bceb-2fbabf43ca8c",
   "metadata": {},
   "outputs": [],
   "source": [
    "column_names = ['Sex', 'Length', 'Diameter', 'Height', \n",
    "                'WholeWeight', 'ShuckedWeight', 'VisceraWeight', \n",
    "                'ShellWeight', 'Rings']\n",
    "\n",
    "df = pd.read_csv(r\"..\\datasets\\abalone\\abalone.data\", names=column_names)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "08f4a065-aa14-4dea-bab0-f119efa62324",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Sex</th>\n",
       "      <th>Length</th>\n",
       "      <th>Diameter</th>\n",
       "      <th>Height</th>\n",
       "      <th>WholeWeight</th>\n",
       "      <th>ShuckedWeight</th>\n",
       "      <th>VisceraWeight</th>\n",
       "      <th>ShellWeight</th>\n",
       "      <th>Rings</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>M</td>\n",
       "      <td>0.455</td>\n",
       "      <td>0.365</td>\n",
       "      <td>0.095</td>\n",
       "      <td>0.5140</td>\n",
       "      <td>0.2245</td>\n",
       "      <td>0.1010</td>\n",
       "      <td>0.150</td>\n",
       "      <td>15</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>M</td>\n",
       "      <td>0.350</td>\n",
       "      <td>0.265</td>\n",
       "      <td>0.090</td>\n",
       "      <td>0.2255</td>\n",
       "      <td>0.0995</td>\n",
       "      <td>0.0485</td>\n",
       "      <td>0.070</td>\n",
       "      <td>7</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>F</td>\n",
       "      <td>0.530</td>\n",
       "      <td>0.420</td>\n",
       "      <td>0.135</td>\n",
       "      <td>0.6770</td>\n",
       "      <td>0.2565</td>\n",
       "      <td>0.1415</td>\n",
       "      <td>0.210</td>\n",
       "      <td>9</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>M</td>\n",
       "      <td>0.440</td>\n",
       "      <td>0.365</td>\n",
       "      <td>0.125</td>\n",
       "      <td>0.5160</td>\n",
       "      <td>0.2155</td>\n",
       "      <td>0.1140</td>\n",
       "      <td>0.155</td>\n",
       "      <td>10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>I</td>\n",
       "      <td>0.330</td>\n",
       "      <td>0.255</td>\n",
       "      <td>0.080</td>\n",
       "      <td>0.2050</td>\n",
       "      <td>0.0895</td>\n",
       "      <td>0.0395</td>\n",
       "      <td>0.055</td>\n",
       "      <td>7</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Sex  Length  Diameter  Height  WholeWeight  ShuckedWeight  VisceraWeight  \\\n",
       "0   M   0.455     0.365   0.095       0.5140         0.2245         0.1010   \n",
       "1   M   0.350     0.265   0.090       0.2255         0.0995         0.0485   \n",
       "2   F   0.530     0.420   0.135       0.6770         0.2565         0.1415   \n",
       "3   M   0.440     0.365   0.125       0.5160         0.2155         0.1140   \n",
       "4   I   0.330     0.255   0.080       0.2050         0.0895         0.0395   \n",
       "\n",
       "   ShellWeight  Rings  \n",
       "0        0.150     15  \n",
       "1        0.070      7  \n",
       "2        0.210      9  \n",
       "3        0.155     10  \n",
       "4        0.055      7  "
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "4a085de4-e39b-4e9f-ba8a-c655d774ed4b",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['Sex'] = df['Sex'].map({'M': 0, 'F': 1, 'I': 2})\n",
    "df['Age'] = df['Rings'] + 1.5\n",
    "df.drop(columns='Rings', inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "ce8ae174-1e62-44c2-a3b2-769d85be4655",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Sex</th>\n",
       "      <th>Length</th>\n",
       "      <th>Diameter</th>\n",
       "      <th>Height</th>\n",
       "      <th>WholeWeight</th>\n",
       "      <th>ShuckedWeight</th>\n",
       "      <th>VisceraWeight</th>\n",
       "      <th>ShellWeight</th>\n",
       "      <th>Age</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>0.455</td>\n",
       "      <td>0.365</td>\n",
       "      <td>0.095</td>\n",
       "      <td>0.5140</td>\n",
       "      <td>0.2245</td>\n",
       "      <td>0.1010</td>\n",
       "      <td>0.1500</td>\n",
       "      <td>16.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>0.350</td>\n",
       "      <td>0.265</td>\n",
       "      <td>0.090</td>\n",
       "      <td>0.2255</td>\n",
       "      <td>0.0995</td>\n",
       "      <td>0.0485</td>\n",
       "      <td>0.0700</td>\n",
       "      <td>8.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1</td>\n",
       "      <td>0.530</td>\n",
       "      <td>0.420</td>\n",
       "      <td>0.135</td>\n",
       "      <td>0.6770</td>\n",
       "      <td>0.2565</td>\n",
       "      <td>0.1415</td>\n",
       "      <td>0.2100</td>\n",
       "      <td>10.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>0.440</td>\n",
       "      <td>0.365</td>\n",
       "      <td>0.125</td>\n",
       "      <td>0.5160</td>\n",
       "      <td>0.2155</td>\n",
       "      <td>0.1140</td>\n",
       "      <td>0.1550</td>\n",
       "      <td>11.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2</td>\n",
       "      <td>0.330</td>\n",
       "      <td>0.255</td>\n",
       "      <td>0.080</td>\n",
       "      <td>0.2050</td>\n",
       "      <td>0.0895</td>\n",
       "      <td>0.0395</td>\n",
       "      <td>0.0550</td>\n",
       "      <td>8.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4172</th>\n",
       "      <td>1</td>\n",
       "      <td>0.565</td>\n",
       "      <td>0.450</td>\n",
       "      <td>0.165</td>\n",
       "      <td>0.8870</td>\n",
       "      <td>0.3700</td>\n",
       "      <td>0.2390</td>\n",
       "      <td>0.2490</td>\n",
       "      <td>12.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4173</th>\n",
       "      <td>0</td>\n",
       "      <td>0.590</td>\n",
       "      <td>0.440</td>\n",
       "      <td>0.135</td>\n",
       "      <td>0.9660</td>\n",
       "      <td>0.4390</td>\n",
       "      <td>0.2145</td>\n",
       "      <td>0.2605</td>\n",
       "      <td>11.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4174</th>\n",
       "      <td>0</td>\n",
       "      <td>0.600</td>\n",
       "      <td>0.475</td>\n",
       "      <td>0.205</td>\n",
       "      <td>1.1760</td>\n",
       "      <td>0.5255</td>\n",
       "      <td>0.2875</td>\n",
       "      <td>0.3080</td>\n",
       "      <td>10.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4175</th>\n",
       "      <td>1</td>\n",
       "      <td>0.625</td>\n",
       "      <td>0.485</td>\n",
       "      <td>0.150</td>\n",
       "      <td>1.0945</td>\n",
       "      <td>0.5310</td>\n",
       "      <td>0.2610</td>\n",
       "      <td>0.2960</td>\n",
       "      <td>11.5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4176</th>\n",
       "      <td>0</td>\n",
       "      <td>0.710</td>\n",
       "      <td>0.555</td>\n",
       "      <td>0.195</td>\n",
       "      <td>1.9485</td>\n",
       "      <td>0.9455</td>\n",
       "      <td>0.3765</td>\n",
       "      <td>0.4950</td>\n",
       "      <td>13.5</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>4177 rows × 9 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "      Sex  Length  Diameter  Height  WholeWeight  ShuckedWeight  \\\n",
       "0       0   0.455     0.365   0.095       0.5140         0.2245   \n",
       "1       0   0.350     0.265   0.090       0.2255         0.0995   \n",
       "2       1   0.530     0.420   0.135       0.6770         0.2565   \n",
       "3       0   0.440     0.365   0.125       0.5160         0.2155   \n",
       "4       2   0.330     0.255   0.080       0.2050         0.0895   \n",
       "...   ...     ...       ...     ...          ...            ...   \n",
       "4172    1   0.565     0.450   0.165       0.8870         0.3700   \n",
       "4173    0   0.590     0.440   0.135       0.9660         0.4390   \n",
       "4174    0   0.600     0.475   0.205       1.1760         0.5255   \n",
       "4175    1   0.625     0.485   0.150       1.0945         0.5310   \n",
       "4176    0   0.710     0.555   0.195       1.9485         0.9455   \n",
       "\n",
       "      VisceraWeight  ShellWeight   Age  \n",
       "0            0.1010       0.1500  16.5  \n",
       "1            0.0485       0.0700   8.5  \n",
       "2            0.1415       0.2100  10.5  \n",
       "3            0.1140       0.1550  11.5  \n",
       "4            0.0395       0.0550   8.5  \n",
       "...             ...          ...   ...  \n",
       "4172         0.2390       0.2490  12.5  \n",
       "4173         0.2145       0.2605  11.5  \n",
       "4174         0.2875       0.3080  10.5  \n",
       "4175         0.2610       0.2960  11.5  \n",
       "4176         0.3765       0.4950  13.5  \n",
       "\n",
       "[4177 rows x 9 columns]"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "329db53d-fb9f-4264-96f9-166756248cea",
   "metadata": {},
   "outputs": [],
   "source": [
    "X = df.drop(columns='Age')\n",
    "y = df['Age']\n",
    "\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "56060c32-6f8d-4231-8baf-6d6a2d6100d3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "RMSE: 4.950310502936191\n",
      "R²: 0.5427053625654411\n"
     ]
    }
   ],
   "source": [
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.metrics import mean_squared_error, r2_score\n",
    "\n",
    "model = LinearRegression()\n",
    "model.fit(X_train, y_train)\n",
    "\n",
    "y_pred = model.predict(X_test)\n",
    "\n",
    "print(\"RMSE:\", mean_squared_error(y_test, y_pred))\n",
    "print(\"R²:\", r2_score(y_test, y_pred))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "47ba8a83-542c-4431-91a6-3406f291f14f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAq4AAAHWCAYAAAC2Zgs3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjkuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8ekN5oAAAACXBIWXMAAA9hAAAPYQGoP6dpAACcNUlEQVR4nO3dB3hb1fkG8FfTeyR24uxNEkIGI0DZYSTs3RYIpYFSyi5ljwJhllVm2aXMsv5Qwt4QdtgkIUBCyN7be2jd//Oeazme8ZWRLcl+f8/jKPfq+PpIV7Y+nfud77gsy7IgIiIiIpLk3InugIiIiIiIEwpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRSQlDRo0CCeeeGLd9gcffACXy2Vuk7WPErsJEyaYLxERUuAqIjF79NFHTZAY/UpPT8fw4cNx1llnYc2aNUglr7/+Oq666ip0BT/99FPd+SouLm7zcf7xj3/gxRdfRDIKh8Po06ePeZxvvPFGorsjInGmwFVE2uyaa67BE088gbvvvhu77ror7rvvPuyyyy6orKzs8L7sueeeqKqqMrexBq5XX301uoL//ve/6NWrl/n/888/3ykD1/fffx+rVq0yo91PPvlkorsjInGmwFVE2uzAAw/EH/7wB/z5z382o7B/+9vfsGjRIrz00kstfk9FRUW79MXtdpuRRN5KU5Zl4amnnsLkyZNx0EEHddqgjsH59ttvj3PPPdcE1+31ehORxNBfeBGJm3322cfcMngl5ndmZ2djwYIFJljKycnB8ccfb+6LRCK44447sM0225iAs6ioCKeeeio2bdrUJOC67rrr0K9fP2RmZmLvvffGDz/80ORnt5Tj+sUXX5if3a1bN2RlZWHs2LG488476/p3zz33mP/XT32IincfGwsGg+jevTtOOumkJveVlpaan3nBBRfU7fvXv/5l+sKfwcczfvx4E4w68emnn2Lx4sU49thjzddHH32E5cuXN2nHx8znZ8yYMebn9+jRAwcccAC+/vrruueJweBjjz1W93xF83h5y5HOxpiKUf95pUceecS8Xnr27Im0tDSMGjXKjNj/GhxxnzZtmnl8v//97812Sx+innvuOfMz+RhHjx5tvq+5/jt9DYhIx/B20M8R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DtSBFQxEpJOVw/rqq6+22I7lkVg6qSUsV7TDDjuYElo5OTmmTNFFF11krVy5sq5NOBy2rr76aqt3796m3YQJE6w5c+aYskVbKocV9cknn1gTJ040x2dfxo4da/3rX/+qu59ls84++2yrR48elsvlalK2KZ593BKWm+rfv7/5+dddd12T+x944AFrzz33NGWt0tLSrKFDh1oXXnihVVJS0uIxb731VnO89957r8U2jz76qGnz0ksv1T0ft9xyizVy5EhT5ovPy4EHHmh98803dd8zd+5c0xc+1sYlv95++21r9OjR5ntHjBhh/fe//222HNbLL79szkV6ero1aNAg66abbrIefvhh027RokWOy2GxX/yeK664osU2ixcvNm3OPffcun0s38bHyOeS/WV/jj76aLOvMSevARHpGC7+05GBsoiISDLiqC1H0FmKTESSk3JcRUSkS2FOMHNU6+NSwaxry9W2RCR5acRVRES6lMWLF5tJdX/4wx9Mji7znu+//35TO5ZVKOovWSwiyUWTs0REpEth2S5OMHvooYdM2TJWSeAktxtvvFFBq0iS04iriIiIiKQE5biKiIiISEpQ4CoiIiIiKaHT57iyeDaLcLNAdzzW4hYRERGR+GLmallZmZkwyQVkumzgyqC1pdVURERERCR5LFu2DP369eu6gWt0KUQ+Ebm5uYnuTkrVOXz77bfrljiUxNM5ST46J8lF5yP56Jwkn2CSnpPS0lIz0NjSEtZdJnCNpgcwaFXgGtsLOzMz0zxnyfTC7sp0TpKPzkly0flIPjonySeY5OektbROTc4SERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVERERENlu3DnjrLSQjBa4iIiIisllhIfDcc0AwiGSjwFVERESkK5s3DzjhBGDTJnvb5QIuu0yBa2P33Xcfxo4di9zcXPO1yy674I033qi7v7q6GmeeeSYKCgqQnZ2No48+GmvWrElkl0VEREQ6h1WrgFNPBbbZBvjvf4Ebb9x835AhQGYmkk1CA9d+/frhxhtvxDfffIOvv/4a++yzDw4//HD88MMP5v5zzz0Xr7zyCp577jl8+OGHWLlyJY466qhEdllEREQkpXkrK+G+8kpg2DDgwQeBcBg47DBgyhQkO28if/ihhx7aYPv66683o7Cff/65CWr/85//4KmnnjIBLT3yyCPYeuutzf2/+c1vEtRrERERkdTkvu8+7HfFFfCUlto7dtkFuPlmYPfdkQoSGrjWFw6HzchqRUWFSRngKGwwGMR+++1X12bkyJEYMGAAZsyY0WLgWlNTY76iSmtPDI/FL3Em+lzpOUseOifJR+ckueh8JB+dk+Tj+vZbpJWWIjJ8OCLXXw+LI63MaU3wOXL6Gkl44Pr999+bQJX5rMxjnTZtGkaNGoWZM2fC7/cjPz+/QfuioiKsXr26xePdcMMNuPrqq5vsf/vtt5GZhLkaye6dd95JdBekEZ2T5KNzklx0PpKPzkniFM6aherCQpT37Wu20/fcE0WZmVi6336wPB6g3tyiRKqsrEyNwHXEiBEmSC0pKcHzzz+PKVOmmHzWtrr00ktx3nnnNRhx7d+/PyZNmmQmgInzTz78QzNx4kT4fL5Ed0d0TpKSzkly0flIPjonCfTdd/Bcfjnc77yDyKGHIvy//20+JwUFSXdOolfIkz5w5ajqMCYHA9hhhx3w1Vdf4c4778QxxxyDQCCA4uLiBqOurCrQq1evFo+XlpZmvhrjyUmmE5Qq9LwlH52T5KNzklx0PpKPzkkHWrQIuOIK4Mkn7W2fD+7Bg+F2uwGOsCbpOXHal6Sr4xqJREyOKoNYPoj33nuv7r558+Zh6dKlJrVARERERGqtX89yTJwQtDlonTwZmDsXuPPOBkFrKkvoiCsv6x944IFmwlVZWZmpIPDBBx/grbfeQl5eHk4++WRz2b979+7mMv/ZZ59tglZVFBARERGp57HHgDvusP/Pie033QRsvz06m4QGrmvXrsUf//hHrFq1ygSqXIyAQSvzLuj22283Q9tceICjsPvvvz/uvffeRHZZREREJPFCIWDlSmDAAHv7zDMBzhE6+2ygNo7qjBIauLJO65akp6fjnnvuMV8iIiIiXZ5lAS+/zMvWAPNWZ82y0wDS0+39nVzS5biKiIiISDM+/RTYYw/giCOAn34CWB503jx0JQpcRURERJIZg1QGq7vvbgevGRnAZZcBCxYAo0ahK0l4OSwRERERacHs2cB227HsEkxqwJ/+BFx1FVC7oEBXo8BVREREJJlEg1QaMwbYbTege3cuDwpsvTW6MqUKiIiIiCSDmhq7pBWD0+Jie5/LBbz5JvDii10+aCUFriIiIiKJHmHlogFcPICLCPz8M/DAA5vvz8xMZO+SilIFRERERBLl7beBiy8GZs60t3v3Bq6+GjjppET3LCkpcBURERHpaOEwcPDBwFtv2du5uXYAe845QFZWonuXtBS4ioiIiHQ0LhrAygA+n73q1d//DhQWJrpXSU85riIiIiLtbf16O3917tzN+66/3l5A4PbbFbQ6pBFXERERkfZSUWFXCrj5ZqC0FFi8GJg2zb6vV69E9y7lKHAVERERibdQCHj4YXuxgFWr7H1cSOCMMxLds5SmwFVEREQknl57DTj/fDsNgAYNstMCjj1288IC0iYKXEVERETi6Ycf7KC1oAC44grgtNOAtLRE96pTUOAqIiIi8mv89BNQVgbstJO9ffbZdqoAqwXk5SW6d52KxqtFRERE2mLFCuCUU4DRo4GTT7Zrs1JGBnDZZQpa24FGXEVERERiUVIC3HSTXS2gqsreN2yYvb9790T3rlNT4CoiIiLiRE0NcO+9wHXXARs32vt23dUudbXbbonuXZegwFVERETEiXffBc47z/7/yJHAjTcChx0GuFyJ7lmXocBVREREpCXLlwP9+tn/P+gg4He/AyZNAk48EfAqjOpoesZFREREGvvmG+CSS4BvvwUWLrQnWnFk9f/+L9E969JUVUBEREQkikHq5MnA+PF2agDLXH3ySaJ7JbUUuIqIiIisWwecc46du/r00/a+44+3FxI4+OBE905qKVVAREREurbiYmD4cPuWmMPKiVfbbZfonkkjClxFRESk67GszdUA8vOBI48EZs2y67Put1+ieyctUKqAiIiIdK2Addo0YOxYOw0g6q67gK++UtCa5BS4ioiISNfASVZcKOCoo4A5c4B//GPzfdnZgFthUbJTqoCIiIh0bj/+CFx6KfDyy/Z2Zqa9kMAFFyS6ZxIjBa4iIiLSeTE4vf12IBIBPB7gz38Gpk4FevdOdM+kDRS4ioiISOfVo4cdtHLyFVMDWO5KUpYCVxEREekcamqAe+8FxozZPMnqr38F9toL+M1vEt07iQMFriIiIpLaOKL61FPA5ZcDS5bYget339mpARkZClo7EQWuIiIikrqlrd5+G7j4YrsGK/XpY6+AJZ2SAlcRERFJ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3TsRERGRuFDg2hkwOJ0zx669+qc/cd1boG/fRPdKREREJK4UuKaikhLggQfsUVXWYeXXI4/YqQFbb53o3omIiIi0CwWuqaSmBrj/frv26oYNQFYWcOaZ9n3KYxUREZFOToFrKohEWNQWuPxye+UrGjlSCweIiIhIl6KqAsnunXeA8eOB44+3g9bevYEHH7TrsR54YKJ7JyIiItJhNOKa7P75T+C774DcXODii4FzzrFTBERERES6GAWuyYajqjk5QGGhvX3jjfaEK6YJRPeJiIiIdEFKFUimWqx/+xswYgRwzTWb92+3HXDHHQpaRUREpMvTiGuiVVTYgenNNwOlpfa+BQvsCVmsyyoiIiIihiKjRAmFgH//G9hqKzsNgEErR1fffht47TUFrSIiIiKNKDpKlOuvB/7yF2DVKmDQIODJJ4GvvwYmTkx0z0RERESSkgLXjlRdvfn/p58ODB5spwnMnQtMnqxRVhEREZEtUI5rR/jpJ+DSS+3A9c037X09ewLz5wMeT6J7JyIiIpISFLi2pxUrgKuuAh5+ePNkK46uctUrUtAqIiIi4piuTbeHkhLgssvsiVcPPWQHrUccAcyZszloFREREZGYaMQ13mbNAvbZB9i40d7edVe71NVuuyW6ZyIiIiIpTYFrvHGVq27d7BxWrnp12GGAy5XoXomIiIikPAWu8eb327VYBwwAvHp6RUREROJFkVV7GDIk0T0QERER6XQ0OUtEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHAVERERkZTgTXQHROqLRCys3RRGZXUEmelu9OzmgdvtSnS3REREJAmkxIjrPffcg0GDBiE9PR0777wzvvzyy0R3SdrBklVBPP12KR55pRhPvF5ibrnN/SIiIiJJH7g+++yzOO+88zB16lR8++23GDduHPbff3+sXbs20V2TOGJw+sL0MsxfFkBulhv9irzmltvcr+BVREREkj5wve2223DKKafgpJNOwqhRo3D//fcjMzMTDz/8cKK7JnFMD/hkViVKKsIY2MuLrAw3PG6XueU29386u9K0ExERka4rqXNcA4EAvvnmG1x66aV1+9xuN/bbbz/MmDGj2e+pqakxX1GlpaXmNhgMmi9xJvpcdcRztmZjCMtXV6FnvhsuhIF68SmzW3vmW1i2qgor1/lR1D2pX7Kd5pyIMzonyUXnI/nonCSfZD0nTvvjsiwraYexVq5cib59++Kzzz7DLrvsUrf/oosuwocffogvvviiyfdcddVVuPrqq5vsf+qpp8xIrYiIiIgkl8rKSkyePBklJSXIzc1tsV2nG77i6CxzYuuPuPbv3x+TJk3a4hMhTT/5vPPOO5g4cSJ8Pl+7j7g++UYJcrLcppJAY6wwUFYRwfEH5nX5EdeOOifijM5JctH5SD46J8knmKTnJHqFvDVJHQUUFhbC4/FgzZo1DfZzu1evXs1+T1pamvlqjCcnmU5QquiI561PDy/69QqYiVgDe3ngcm0uf8ULAmuLLQwfkIE+PdJVGkuv5aSkc5JcdD6Sj85J8vEl2Tlx2peknpzl9/uxww474L333qvbF4lEzHb91AFJbQxGdx+XibwsD5asDqGiKoJw2DK33M7L9mC3sZkKWkVERLq4pB5xJV72nzJlCsaPH4+ddtoJd9xxByoqKkyVAek8Bvb24ai9c0x1gaWrg1hfYsHvdWH4AL8JWnm/iIiIdG1JH7gec8wxWLduHa688kqsXr0a2267Ld58800UFRUlumsSZwxO+xflauUsERERSc3Alc466yzzJZ0fg9ReBSnxshQREZEOltQ5riIiIiIiUQpcRURERCQlKHAVERERkZSgwFVEREREUoICVxERERFJCZq+LUklErFUDktERESapcBVksaSVcG6BQgCQQt+nwsDevnMqlpagEBEREQUuErSBK0vTC9DSUUYPfI9SE9zobrGwvxlAazdGDarail4FRER6dqU4ypJkR7AkVYGrQN7eZGV4YbH7TK33Ob+T2dXmnYiIiLSdSlwlYRjTivTAzjS6nI1zGflNvdzRJbtREREpOtS4CoJx4lYzGllekBz0v0uBEKWaSciIiJdlwJXSThWD+BELOa0Nqc6YMHvdZl2IiIi0nUpEpCEY8krVg9YVxyGZTUMXrnN/ZyYxXYiIiLSdSlwlYRjnVaWvMrL8mDJ6hAqqiIIhy1zy+28bA92G5upeq4iIiJdnAJXSQocUWXJq636+1FaEcHydSFzO3yAH0dNUCksERERUR1XSSIMTvsX5WrlLBEREWmWAldJKgxSexXoZSkiIiJNKVVARERERFKCAlcRERERSQkKXEVEREQkJShwFREREZGUoMBVRERERFKCAlcRERERSQkKXEVEREQkJShwFREREZGUoMBVRERERFKCAlcRERERSQmdfm1Ny7LMbWlpaaK7klKCwSAqKyvN8+bz+RLdHdE5SUo6J8lF5yP56Jwkn2CSnpNonBaN27ps4FpWVmZu+/fvn+iuiIiIiEgrcVteXl6L97us1kLbFBeJRLBy5Urk5OTA5XIlujspg598GOwvW7YMubm5ie6O6JwkJZ2T5KLzkXx0TpJPaZKeE4ajDFr79OkDt9vddUdc+eD79euX6G6kLL6ok+mFLTonyUjnJLnofCQfnZPkk5uE52RLI61RmpwlIiIiIilBgauIiIiIpAQFrtKstLQ0TJ061dxKctA5ST46J8lF5yP56Jwkn7QUPyedfnKWiIiIiHQOGnEVERERkZSgwFVEREREUoICVxERERFJCQpcRURERCQlKHCVBq666iqzwlj9r5EjRya6W13KRx99hEMPPdSsHsLn/8UXX2xwP+dTXnnllejduzcyMjKw3377Yf78+Qnrb1c/HyeeeGKT35kDDjggYf3tCm644QbsuOOOZkXEnj174ogjjsC8efMatKmursaZZ56JgoICZGdn4+ijj8aaNWsS1ueufj4mTJjQ5PfktNNOS1ifO7v77rsPY8eOrVtkYJdddsEbb7zRKX4/FLhKE9tssw1WrVpV9/XJJ58kuktdSkVFBcaNG4d77rmn2ftvvvlm3HXXXbj//vvxxRdfICsrC/vvv7/5QyQdfz6IgWr935mnn366Q/vY1Xz44YfmTffzzz/HO++8g2AwiEmTJplzFXXuuefilVdewXPPPWfac+nvo446KqH97srng0455ZQGvyf8Wybto1+/frjxxhvxzTff4Ouvv8Y+++yDww8/HD/88EPq/36wHJZI1NSpU61x48YluhtSi7+i06ZNq9uORCJWr169rFtuuaVuX3FxsZWWlmY9/fTTCepl1z0fNGXKFOvwww9PWJ/EstauXWvOzYcfflj3O+Hz+aznnnuurs1PP/1k2syYMSOBPe2a54P22msv65xzzklov7q6bt26WQ899FDK/35oxFWa4GVnXhYdMmQIjj/+eCxdujTRXZJaixYtwurVq016QP21nXfeeWfMmDEjoX3ryj744ANziXTEiBE4/fTTsWHDhkR3qUspKSkxt927dze3HGXiqF/93xOmPA0YMEC/Jwk4H1FPPvkkCgsLMXr0aFx66aWorKxMUA+7lnA4jGeeecaMgDNlINV/P7yJ7oAkFwZAjz76qHkD5qWcq6++GnvssQfmzJlj8pcksRi0UlFRUYP93I7eJx2LaQK8xDZ48GAsWLAAl112GQ488EDzBuDxeBLdvU4vEongb3/7G3bbbTcTEBF/F/x+P/Lz8xu01e9JYs4HTZ48GQMHDjSDIrNnz8bFF19s8mBfeOGFhPa3M/v+++9NoMo0MuaxTps2DaNGjcLMmTNT+vdDgas0wDfcKCZ2M5DlH5v/+7//w8knn5zQvokko2OPPbbu/2PGjDG/N0OHDjWjsPvuu29C+9YVMLeSH6yVi5/c5+Mvf/lLg98TTi7l7wc/7PH3ReJvxIgRJkjlCPjzzz+PKVOmmHzWVKdUAdkifiIbPnw4fvnll0R3RQD06tXL3Dae/cnt6H2SWEyx4eVQ/c60v7POOguvvvoqpk+fbiajRPF3IRAIoLi4uEF7/Z4k5nw0h4MipN+T9uP3+zFs2DDssMMOpvIDJ5neeeedKf/7ocBVtqi8vNx8IuanY0k8Xo7mH5b33nuvbl9paampLsBLQpJ4y5cvNzmu+p1pP5wnxyCJlz7ff/9983tRH9+ofT5fg98TXpZmvr5+Tzr+fDSHI4Gk35OOTeOoqalJ+d8PpQpIAxdccIGpWcn0AJbHmDp1qsnTO+644xLdtS71YaH+KAQnZPGPPCc6MHme+WPXXXcdttpqK/MGccUVV5i8MdZOlI49H/xiHjhrIPIDBT/kXXTRRWaUgyXKpP0uRz/11FN46aWXTO59NC+PExVZ25i3TG0677zzzDliHcuzzz7bvCn/5je/SXT3u9z54O8F7z/ooINM3VDmuLIc05577mlSayT+Lr30UpP6x/eMsrIy8/wzfemtt95K/d+PRJc1kORyzDHHWL1797b8fr/Vt29fs/3LL78kultdyvTp001ZksZfLLsULYl1xRVXWEVFRaYM1r777mvNmzcv0d3ukuejsrLSmjRpktWjRw9TXmbgwIHWKaecYq1evTrR3e7Umjsf/HrkkUfq2lRVVVlnnHGGKQGUmZlpHXnkkdaqVasS2u+uej6WLl1q7bnnnlb37t3N36xhw4ZZF154oVVSUpLorndaf/rTn8zfI76X8+8T3yfefvvtTvH74eI/iQ6eRURERERaoxxXEREREUkJClxFREREJCUocBURERGRlKDAVURERERSggJXEREREUkJClxFREREJCUocBURERGRlKDAVURERERSggJXEZEU53K58OKLLya6GyIi7U6Bq4iIQzNmzIDH48HBBx8c8/cOGjQId9xxB1K1/yIiyUCBq4iIQ//5z39w9tln46OPPsLKlSuRalK9/yIiClxFRBwoLy/Hs88+i9NPP92MWD766KNN2rzyyivYcccdkZ6ejsLCQhx55JFm/4QJE7BkyRKce+655rI+v+iqq67Ctttu2+AYHJXl6GzUV199hYkTJ5rj5eXlYa+99sK3337bLv1/+eWXsdVWW5n+77333njsscdMX4uLi+vafPLJJ9hjjz2QkZGB/v37469//SsqKipi7o+ISFsocBURceD//u//MHLkSIwYMQJ/+MMf8PDDD8OyrLr7X3vtNROoHnTQQfjuu+/w3nvvYaeddjL3vfDCC+jXrx+uueYarFq1ynw5VVZWhilTppiA8fPPPzeBJX8G98ez/4sWLcJvf/tbHHHEEZg1axZOPfVU/P3vf29wjAULFuCAAw7A0UcfjdmzZ5tAmP0666yzYuqLiEhbedv8nSIiXQgvszPgIwZvJSUl+PDDD81oKl1//fU49thjcfXVV9d9z7hx48xt9+7dTW5pTk4OevXqFdPP3WeffRpsP/jgg8jPzzc/+5BDDolb/x944AET1N5yyy1mm/+fM2eOeVxRN9xwA44//nj87W9/M9sMou+66y4zCnzfffeZkVoRkfakEVcRkVbMmzcPX375JY477jiz7fV6ccwxx5hgMGrmzJnYd9994/6z16xZg1NOOcUEiUwVyM3NNZf9ly5dGtf+sw3THOqLjhhHcSSWKQbZ2dl1X/vvvz8ikYgZsRURaW8acRURaQUDvFAohD59+tTt42X2tLQ03H333SagZM5nrNxud4PL9RQMBhtsM01gw4YNuPPOOzFw4EDzM3fZZRcEAoG49t8JBsxMIWBea2MDBgxw3B8RkbbSiKuIyBYw4Hv88cdx6623mlHV6BdHHxkIPv3006bd2LFjTV5rS/x+P8LhcIN9PXr0wOrVqxsErzx2fZ9++qkJFJnXus0225hgc/369XHvP1MDvv766wbfy4lh9W2//fb48ccfMWzYsCZffHwiIu1NgauIyBa8+uqr2LRpE04++WSMHj26wRcnKUUvt0+dOtUEgbz96aef8P333+Omm26qOw4rBbAM1YoVK+oCT+aXrlu3DjfffLOZ+HTPPffgjTfeaPDzmSLwxBNPmGN+8cUXJsc0ltFdp/3nSOrcuXNx8cUX4+effzaTuaKVB6JVEHjfZ599ZiZjMfidP38+XnrpJU3OEpEOo8BVRGQLGNjtt99+zV5OZ+DHUUrOsGcQ+txzz5mSUixxxUlVzCuNYkWBxYsXY+jQoWaklbbeemvce++9JmDlRC62v+CCC5r8fAaeHO084YQTzOhrz549497/wYMH4/nnnzcVEDh6zMlW0aoCHOUl7ueELga2LIm13Xbb4corr2yQgiAi0p5cVuMEKxERkdpKCffffz+WLVuW6K6IiBianCUiIgZHf1lZoKCgwOTWsjSW0gBEJJkocBUREYM5q9dddx02btxoqgScf/75uPTSSxPdLRGROkoVEBEREZGUoMlZIiIiIpISFLiKiIiISEpQ4CoiIiIiKUGBq4iIiIikBAWuIiIiIpISFLiKiIiISEpQ4CoiIiIiKUGBq4iIiIggFfw/NQYRiePAnMkAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 800x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 5))\n",
    "plt.scatter(y_test, y_pred, alpha=0.5, color='royalblue')\n",
    "plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')\n",
    "plt.xlabel(\"Actual Age\")\n",
    "plt.ylabel(\"Predicted Age\")\n",
    "plt.title(\"Predicted vs Actual Age\")\n",
    "plt.grid(True)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "176de160-ce1d-4abe-a0ab-583584b17304",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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9TS+ZsHtJCQkyLZq3LixPAYKevfdd+VxLV6biIiUSj3xj7YDQyIiIiIiov8qjikjIiIiIiLSIgZlREREREREWsSgjIiIiIiISIsYlBERERERUYV18uRJWTXXzc1NVts9cOBAie5nKarGKhQK1KhRA9u2bXuu+8igjIiIiIiIKqzk5GR5i5b169eXaHlxixhxH01x25br169j2rRp8jY0v/3223PbR1ZfJCIiIiKi/wQ9PT15T05xr8yn3fRe3Gf09u3bqnninqHifptHjhx5LvvFTBkREREREZUr6enpSEhIUHuIeWXh3Llz6NSpk9q8rl27yvnPi+Fz2zLpvMNGtbW9CzpnRc8t2t4FnZOTla3tXdA5Jhbm2t4FnZOWlKztXdA5BkZG2t4FnZKTze+SwvT09bS9CzrHwcNF27ugc/Z9VgO6SpvnkpfeH4TFixerzVu0aBE++OCDf7ztsLAwODs7q80T0yLwS01NhampKcoagzIiIiIiIipX5s2bh+nTp6vNE0U5yisGZUREREREVGp6RtrL9ioUiucWhLm4uCA8PFxtnpi2srJ6LlkygWPKiIiIiIiInmjVqhWOHTuGgv744w85/3lhUEZERERERBVWUlKSLG0vHnkl78XPAQEBqq6Qw4cPVy0/YcIEPHr0CLNnz4a3tzc2bNiAPXv24N13331u+8jui0REREREVGr6huWjWM3ly5flPcfy5I1FGzFihLwpdGhoqCpAE6pWrSpL4osgbN26dahUqRI2b94sKzA+LwzKiIiIiIiownrllVfwtFszi8BM0zrXrl3Dv4VBGRERERERlZqeEUdClRW2JBERERERkRYxKCMiIiIiItIidl8kIiIiIqIKW+ijPGCmjIiIiIiISIuYKSMiIiIiolLTM2KmrKwwU0ZERERERKRFzJQREREREVGpcUxZ2WGmjIiIiIiISIsYlBEREREREWkRuy8SEREREVGpsdBH2WGmjIiIiIiISIuYKSMiIiIiolJjoY+yw0wZERERERGRFjEoIyIiIiIi0iJ2XyQiIiIiolLTM2D3xbLCTBkREREREZEWMVNGRERERESlps9MWZlhpoyIiIiIiEiLmCkjIiIiIqJS09NnpqysMFNGRERERESkRQzKiIiIiIiItIjdF7UkMjISCxcuxOHDhxEeHg5bW1s0atRIznv55ZdRXtm1bopq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JDm+SJe61RRn909hsqrXu2M85U2Bb99PwtyP1ceLuTkrYG1Z8jap6WmOuk+qN36zTr2L85B3bsqTbl3G46So7/cHy5PDmROqq75PZi25+4++T8q77/YFwdTEALPervmkTeIxc/Gdf/YdmyW+Y23Rv5e7PAYj5HdsFLbvKR/fsfy7U9T+o3Hycz9hoBPMTfVx71GaDK4K3grDxcEIVhb5hT+sLQwwZaiz7Fouqtb6h2TIdW7cz+3RkJUFNKxthp6v2EBhrIeo2Cycu56EH34vH/dR/af0mCkrM3pKZXm7RSSVlcNGtbW9CzpnRc8t2t4FnZMjOtOTGhOL4u9p81+VllT8zYj/qwyM/jtBUUnkZPO7pDAWSSjKwcNF27ugc/Z9ll/ERddcbtdKa6/d9C/1WyqVd9ofVERERERERPQfxu6LRERERERUanr6zO+UFbYkERERERGRFjFTRkREREREpcZxkWWHmTIiIiIiIiItYlBGRERERESkRey+SEREREREpabP+5SVGWbKiIiIiIiItIiZMiIiIiIiKjUW+ig7zJQRERERERFpETNlRERERERUarx5dNlhSxIREREREWkRgzIiIiIiIiItYvdFIiIiIiIqNRb6KDvMlBEREREREWkRM2VERERERFRqvHl02WGmjIiIiIiISIsYlBEREREREWkRuy8SEREREVGpsdBH2WGmjIiIiIiISIuYKSMiIiIiolLT02d+p6ywJYmIiIiIiLSImTIiIiIiIio1jikrO8yUERERERERaRGDMiIiIiIiIi1i90UiIiIiIio1dl8sO8yUERERERERaREzZUREREREVGrMlJUdBmX/YSt6btH2LuicOT+P1vYu6BwDUybUC6vZu5q2d0HnREZEansXdI6RmZG2d0GnKHNytL0LOof3eCqq3rA3tb0LOmiqtneA/gX8NiAiIiIiItIiZsqIiIiIiKjUmO0tO2xJIiIiIiIiLWKmjIiIiIiISk3fgIU+ygozZURERERERFrETBkREREREZUaS+KXHWbKiIiIiIiItIhBGRERERERkRax+yIREREREZUaS+KXHbYkERERERGRFjFTRkREREREpcZCH2WHmTIiIiIiIqrQ1q9fD09PT5iYmKBFixa4ePHiU5dfu3YtateuDVNTU3h4eODdd99FWlrac9s/BmVERERERFRh7d69G9On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L7/8rwRkRERERET/CC8slBkGZVokxpGJLpABAQFwcHBAp06dsGbNGm3vFhERERER/YsYlGnR8OHD5YOIiIiIiP67GJQREREREVGp5VUMp3+OHUGJiIiIiIi0iJkyIiIiIiIqNVYQLTtsSSIiIiIiIi1ipoyIiIiIiEqNN48uO8yUERERERERaRGDMiIiIiIiIi1i90UiIiIiIio9FvooM2xJIiIiIiIiLWKmjIiIiIiISo2FPsoOM2VERERERERaxKCMiIiIiIhIi9h9kYiIiIiISk1Pj/mdssKWJCIiIiIi0iJmyoiIiIiIqPRY6KPMMFNGRERERESkRcyUERERERFRqenx5tFlhi1JRERERESkRQzKiIiIiIiItIjdF4mIiIiIqNT0WOijzDBTRkREREREpEXMlBERERERUenx5tFlhi1JRERERESkRQzKiIiIiIiItIjdF4mIiIiIqNRY6KPsMFNGRERERESkRcyU/YflZGVrexd0joEpr1MUlp2ao+1d0Dk52Upt7wKVA7yCXBi/XwtT5vD7tYisTG3vAZWGPj/XZYUtSUREREREpEXMlBERERERUanp6bFHQFlhpoyIiIiIiEiLGJQRERERERFpEbsvEhERERFR6bHQR5lhSxIREREREWkRM2VERERERFRqvPVH2WGmjIiIiIiISIsYlBEREREREWkRuy8SEREREVHp6TG/U1bYkkRERERERFrETBkREREREZUeC32UGWbKiIiIiIiItIiZMiIiIiIiKjU9jikrM2xJIiIiIiIiLWJQRkREREREpEXsvkhERERERKXHQh9lhpkyIiIiIiIiLWKmjIiIiIiISk1Pn/mdssKWJCIiIiIi0iIGZURERERERFrE7otERERERFR6eiz0UVaYKSMiIiIiItIiZsqIiIiIiKj0WOijzLAliYiIiIiItIhBGRERERERkRb954MyPT09HDhwQNu7QURERERU/gp9aOtRSuvXr4enpydMTEzQokULXLx48anLx8XFYdKkSXB1dYVCoUCtWrXwyy+/4HmpsGPKRo4cie3bt8ufDQ0NYWdnh4YNG2LQoEHyOf0nfWBDQ0Nha2ur5b0FPvjgAxkcXr9+HRXB6CGe6NXFBZbmhrh1LwGrNzxAUGhqidYd+oYHJoyohj0Hg/DZ5odqz9WrbYVxwzzhVdsKOTlKPHiUhOmLbiEjIwe6rPLYwag65S0YOzsg8bY37s1ahvgrtzQuq2doiGozxsF98OtQuDoj+YEffBatQdTR06plDCzMUHP+VDj37ARjRzsk3LyHe3M+QsLV2ygP7Fo3RbUZo2HduD5M3Jxwud/bCD907OnrtG0Or9VzYeFVE2mBofBdvhFBO/arLVNl4mBUmz4aChdHJNz0xp1pSxB/SXM76yLrzj1h26MfDKxtkRHgh4jtG5H+yKfY5W26vQ7rjj1g6OCI7MQEJF08jejd26DMzMzdXsdXYd2pBwwdneV0RtBjxOz/Hik3LqO8cH7jDbgNGQoje3ukPHgAvzWrkXz3rsZl9QwM4DZyJBxf7QFjR0ekBgQg4H+fI/78+fzt9e0Hp759oXBzldOpj/wQvGUz4s6dQ3ng8HpfOL85CEZ2dkh9+BCBn3+KlPv3il3esW9/OL7WB8ZOzsiKj0PsyRMI2fwFlJkZ8nl9U1O4jRoL69ZtYWRjixRfHwStX4eU+94oLxx794XzgMFP2sQXAZ99ihTvYtrEwACuQ4bDvkt3GDk6IC0wAMFfbETCpQvPvk0d5Ni7H1wGDpH7n/LQF4HrPkGyd/GfG5ehI2DftTuMHRxlmwR9sQEJF/M/NxYNX4DLoCEwq1VbLuP7/hzEnT6J8mTXhTvYfvomopJSUcvFDnN7vIQGlZw0Lnvwqg8W7v9LbZ6xoQEuLXpLNd1owVca1323a3OMbN2ojPee/qndu3dj+vTp2LRpkwzI1q5di65du+L+/ftwcip6HGRkZKBz587yuR9++AHu7u54/PgxbGxs8LxU6ExZt27dZNDl7++PX3/9Fe3bt8fUqVPRs2dPZGVlyWVcXFxk9FtRiINI24b088AbPd1lIDZu5jWkpmXjkw8bwNjo769q1Klpide6ucLXL6nIcyIgW7O4AS5dj8W4GVcxZvpV7DscAmWOErrMpW931PloDnw/Xo+zbfoh8dZ9NN33FYwd7DQuX3PBVHiMehN3Zy3D6eY9Ebh1N17c+TksG9ZVLVP/86Wwb/8Sbo6bgzOtXkf08TNodnArFK6a/8DoGgNzMyTcvI/bUxaXaHlTz0podugLRJ+4gNNNX4ff59vR4IulcOjcWrWMa//uqLtqHh4sXY/Tzfsg8aY3WhzeIoPW8sCiZVs4DBmLmH3fIXD+O0gPeAT3uUtgYGWtcXnLl16B/YBRiNn/HR7PGo+Ir9bCsmVb2L85UrVMVkwUonZ9jcD3pyBw/lSk3rkBt+kLYOxeGeWBfadOqDJ1GoK2bMatEcOR7PsAddd9BsNiLqR5TJgI59594L9mNW4MHICIfftQe8VKmNWqpVomPSIcgRvW4/aIEbg9YiQSLl9GrVWrYVq1GnSd7SsdUGnCZITu+BreE0bLYKHGik9gWMxJgm2HznAfO0Euf3fUEDxe/TFsX+kItzHjVMtUmTEXlk2a4fHyJbg3ZjgSL19CzZVrYeTggPLAtn1HVJr4DkK3b8W9cW/JAKTmyuLbxH30ODj0fB0Bn3+KOyOHIvLQAVRfshymNWo+8zZ1jdh/j0lTELJ9C+6OHYnUhw9Qc/WnMLTR/LlxGzMejr16y8Dt9ojBiDy0HzWWfgzTmvmfG31TE6T4PkDA2jUoj47ceojVv57H+PaNsWtiH9R2scfE7b8iOqn4i8UWCiMcmz1E9TgyY6Da8wWfE4/FfdrK5E0nr6r4L9HT19faozQ++eQTjB07FqNGjYKXl5cMzszMzLB161aNy4v5MTExMmHy8ssvywxbu3bt0KjR8wu4K3RQJoItEXSJ6LZx48Z47733cPDgQRmgbdu2TWP3xTlz5sj0pPhFVatWDQsWLEDmk6vOeRmtF154Qf6yKleuDAsLC7z99tvIzs7GypUr5euJqHrZsmVFUqBjxoyBo6MjrKys0KFDB9y4cUM+J/Zl8eLFclrsj3jk7d/T1iu4P5s3b0bVqlVlSlbb+r/mjh17HuP0hWg89E/G0k+9YW+nQJuWT/8jb2qij0Uz6mDl5z5ITMoNmguaMqY6fvgpGN/+EAi/gBQEBqfi+OlIZGbpdlDmOXkEArfvRfDO/Ui+/xB3pn2A7NQ0uA/rq3F5t4Gv4dGaLxH1+0mk+gchcMsuRP5+ElXfyT3Z1jdRwPn1zvBZuBqxZy8j5VEAfJevl/9XHjMI5UHkbyfhs2gtwg8eLdHyVcYNRKpfEO7NXoEk70d4vGEnwn78DVWn5gcgVaeNQuCWPQjavg9J9x7i1tuLkJ2SBo+R/VAe2Hbvg4Q/jyDh5B/ICA5ExNb/QZmeDqt2XTQub1KzLtJ87iLx7AlkRUUg5dY1JJ77CybV80+kkq9dlFmxzPAQZIYFI3rvDuSkpcGkRh2UB66DBiPi4AFE/vwzUv384Pfxx3L/nXr10ri8Q/fuCN6+DXFnzyI9JATh+35E7LmzcB08RLVM3OnT8vm0wECZEQjctBE5KSmwqF8fus7pjYGI+uUnxPz2C9Ie+yNg7SrkpKfBvltPjcub16uPpNu3EHv8D2SEhyHxyiXE/nkU5rW95PN6xsawadsOwV9uQNKtG0gPCUbojq3yf4defVAeOPcfgKjDPyH6yJM2+WQVctLSYd9dc5vYde6GsO92IOHCOWSEhiDq0AHEXzgns4/Puk1dI95L1M+HEP3rYbn/j9eslPvv8Krm/bfv0g2h326X7SDaJPLgfsSfPwuXAm2ScOE8QrZ8ibhT6tmj8uKbs7fQt2kd9G5cG9WdbDG/V2uYGBniwNX7xa4jzsUcLM1UD3sLM7XnCz4nHifuPUazqm6oZGf1L7wjKm3C4sqVK+jUqZNqnugxJ6bPFdNL4tChQ2jVqpXsvujs7Iz69evjo48+kuf7z0uFDso0EUGNiHL37dun8XlLS0sZEN29exfr1q3DV199hU8//VRtmYcPH8rA7siRI/j++++xZcsW9OjRA0FBQfjrr7+wYsUKzJ8/Hxcu5HeH6N+/PyIiIuR64sAQQWLHjh1lFD5gwADMmDED9erVk5k98RDz/m69PL6+vvjxxx/le9J290c3ZxM42ClkNitPcko27vokoH6dp39RTZ9QE2cvx+Dyjbgiz9lYG6FeHSvExmdg48oXcGhHK3y+vBEaeun2l5+ekRGsXqiH6D8LfOiVSkSfOAeb5i9oXEdfYYzstHS1eeJE1LZlk9xtGhpA39CwmGUaoyKyafkCoo6rf3FG/nEati1fULWzdeN6iDp2Nn8BpRJRx8/CpuWL0HkGhlBUrYGU2wU+v0qlnDapqTmASntwT66jqJYbhBk6usC8UVMkX7+k+TX09GU2Tk9hgjRf3e+GJbrxmtepg/iLBd6PUon4S5dg0aCB5nWMjZGTrt5bQJyMWhV3ZVNfH/adO8sufCJ40fX2EBm/xKsFup4qlXLa3KuexnWS79yW3c3Maudm2Y1d3WDdvCXiL55TdVvTMzCEslAPi5z0dFjUbwhdl9smtZFw5VKRNrGopznI1jcyQo6m99ug4TNvU+c+Nxr2X0yLIF0TfSNjzcdAg4rRBS8zKxv3QqLQspq7ap6+vh5aVnfHzcCIYtdLychEt9Xfo8uq7zB15+/wDc8/7yosOikFp3wC0Kdxbfzn6Olr7ZGeno6EhAS1h5hXWFRUlAymRHBVkJgOCwvT+LYePXokuy2K9cQ4MpGkWbNmDZYuXfrcmrLCjil7mjp16uDmzZsanxPBVB6Rqpw5cyZ27dqF2bNnq+bn5OTITJkI4EQKVHSLFH1SxS9NRN61a9eWgdmff/4p+62ePn1aDiYUwVVeV8nVq1fLDJ34hY8bN05m3MTYN5Fpy1OS9fKuAOzYsUNm07TNztZY/h8bl59dzJ3OUD2nScc2jqhV3QJjp1/V+Ly7S24G8K1Bnli/9SEe+CWjWwdnrF3aCMMnXS7xeLV/m7G9jQygMiKj1eanR0TDvJbmLg5Rx07Dc/JIVRbM/pVWcO7VWZ5ACdlJKYi9cA01Zk/EjfsP5bZc+/eQQZ5YviJSODsgPTxKbZ6YNrK2lJlDI1tr2c6iLdSXiYZ5bd3vlmZgaSV/v9nx+RczhKyEOJi5eWhcR2TI9C2t4LFolfirKE/G4o4eRuyhPWrLGXt4wuODNdAzMkZOWipCP10iM3G6TnQVE+8ps8AFKEFMm1aponEdMXbMdfBgJF6/hrSgIFg3awa79u2LdHMxrV4d9Tdvgb6xMbJTU+EzZ7bMxOkyQ2trGUBlxaq3h5g28dDcHiJDJtartW5Dbi8MQ0PZNS38u2/k8zmpqUi6cwsuQ0ciLcAfmbGxsOvQSQZ5Ilum6wytbTS2SaZok8qau+gmXL4A5/4DkXTjunyPlo2bwrZNO9W9lp5lm7pE7r/43Gg6TioX87m5dAHObw5E4o1rsk2smjSFTdtXSt09TFfFpqQhO0cJewtTtfli2i+q6EVgwdPBGot7t0VNF3skpWVg+5mbGPHVIex75w04W1sUWf7QtQcwUxijo5fnc3sfVNTy5ctlT7OCFi1aJHuR/VPiXF/0fPvyyy9hYGCAJk2aIDg4GKtWrZKv8Tz8J4MypVIp/0AVNxDws88+k9mwpKQkOfZMdBssSARrIiArGGmLX1he8ZC8eSKYEkR3Q7Ete3t7te2kpqbK1ylOSderUqXK3wZk4spB4asHOdkZ0DcoPlAqic7tnDBrUn53qdkflv5qs5ODAlPH1sC7C28iI1NzV8S839fBI6H45Vi4/FkU+WjS0AY9Orvgix26fUJVGvdmf4T6n3+INpcPy2M11S8QQTv3o9LQ/O6OYixZg/XL0N7nJHKyspBw4y5Cfzgss3L032BatwHsXnsTEV9vQNrD+zBydoXjsPHI7j0IMQe+Vy2XERKEgPcmQ9/UHBYtWsN5wgwEL51dLgKz0vL/ZA2qvfc+Gu3eI7MDacHBiPz5Jzj1VO/umPb4MW4OGwpDCwvYdeiA6gsX4e7ECTofmJWWRaMX4TJ4GAI/W4Pke3ehcKsEj0lTkTk0CmHf5hbC8l++BFVmzUODPQehzM5CygMf2cXRrGbFvOIf+Pk6VJk5B/W2fyfOBpAeHIKoI4fhUE66Jj4PgZ99iiqz5qL+N7vk50YEZqLrY3HdHf8LGlV2lo+C030+24u9l7wxuVPTIsuLbpCvNqwOhdF/8rRaa+bNmyeLdxSkqU6Eg4ODPE8PD889f8wjpgsmQwoSFReNjIzkennq1q0rM2siGWJs/M/OnzX5Tx499+7dk+OvChP9SocMGSKjblGRxdraWmbJRLqyIPFLKhwwaJonomxBBFbil3vixIkir/m0Ki4lXc/c3BzPcjXBo+YIVK49Cv/E6YvRuOuT353G2Cg3MLW1MUJ0bH53CFsbY/g+Klq8Q6hdw0Jm0basze2eJxga6KFRPWv07emODn1PqrblH5istu7joBQ4O+puoZaM6DgZNBk7qgfWCif7IpmfPJnRsbg2+B3ZjdHIzgbpoRGotXgGUvyDVMuIQO3iq8NhYGYKQ0sLpIdHotHXn6gtU5GIthLZsoLEdGZ8ouyelhEVK9tZtKv6MvZID9PczrpEVE5UZmfLqosFGVrZICtec5cZ+zeGIfH0cSSc+E1OZwT6Q19hAqfR7yDmYO7JVe7Gs5AZHip/TPf3hUm1mrDp+rocs6bLsuLioMzKktXjChLTGTHRxa7jM3uW7MYoMkSZkZGoPGky0kJC1JYT200PCoK4TJXs7Q2Lul5wGTBAjlnTVVnx8TJoMrRVbw8xnVlMe7iNGoOYP35D9C8/y+k0v0cwMDVB5XdnI2znDnmMiDFED6a/A30TE+ibmSMrJhpV5y9Geqh6m+kiUU1SU5sYyTaJKXadhwvmycyxobUVMqOi4D5uour9Pss2dYncf/G5KcVxIttk/tzcz42VNTKjIuE+/u1ykS0tCVszExjo6xUp6iGmHQqNEyuOkYE+6rjaIzAmochzV/1D4R8Vj5VvdsR/kn7pS9OXFYVCUaJifSKAEpmuY8eOoXfv3nKeOEcX05MnT9a4jiju8d1338nl8pIuPj4+8rz8eQRkQsXITZfC8ePHcevWLfTrV3Tw/9mzZ2XW6f3330fTpk1Rs2ZNWf7ynxLjwERkLbon1qhRQ+0hondB/IILDx4syXqluZoQHx+v9qhUI3/w+7NKTc1GcGia6iEKcETFpKNpo/yTSzNTA3jVssJt76JfZoIYQzZs0iWMmnJZ9bj3IAG//xUhfxaxbWh4GiKj01HZXf0L1MPNFGERRfsP6wpRmjzh+h3Yv9Iyf6aeHuzbtUTcxaeP/xNjY0RAJrqiiMIeEYeLlozPTkmVAZmhjRUcOr6scZmKIO78ddh3aKl+5avjS4g9f13VzvFX78ChQyv1dm7fCnHnr0HnZWch3c8XZvUKjOHQ04Np/ReQ9kBzaXI9hUJmUgtSPrkQJLozFktPX47B03XixFIETKILooqeHqyaNUXSradn5MX4GBGQiS6hovti7Mm/KU6gry/H1eh6e6T4+MDyxSZq7SGmk+/e0biOCNKLHCPZT46RQr1FxJhUEZAZWFjCsllzxJ3NvwWHbrfJfVg1bqreJo2bIOnO028PIm4JIAIyUSJfdNWLO3PqH29TZz43Pvdh2UR9/8X7EWMM//ZzE5X7ubFt217VJuWdkaEB6ro54MKj/CBT3FLnwqMQNPQoWcXi7JwcPAiPgYOlehdIYf/V+/Byc0BtV/WLgqRbpk+fLutEiNtlieTMxIkTkZycLKsxCsOHD5fnynnE86J+g6jaLoKxw4cPy0IfovDH81KhM2Wiu54IakSwI1KUojCHyBiJkvii8QsTQVhAQIDMjjVr1kz+AvbvV78P0rMQ1V1EBRcRnYsKjaK6Y0hIiNx+nz59ZAAoukT6+fnJQh2VKlWS3SNLst4/uZrwT7suFmfvoWCMGFAZgSGpMpgaM9QT0THpOHU+P2OxdmlDnDwXJUvai8BOBHMFpaXlICEhU23+d/sCMXqwpyyX/8AvCd07uKBKJTPM/1jzvVd0hf//tqPBpuWIv3Yb8ZdvwfPt3AxX8Le5x1aDLz5Gekg4fBbnFpSxbtoQJq7OSLh1T/5fY94k6Onpw2/dFtU2RQAm/tCKe5iZVauC2ktmyp/ztlkeSuKb18gfn2FWtRKsGtVBRky8vAdZ7aXTYeLujBuj5sjnH3+5C1XeHoI6y2chcNuPcGjfUpbAv/TaeNU2/NZ+jUZbVyDuym3EX7oJzykjYGhuisDtmov66JrYX/fDefx0pPk9QNpDH9h2ex36CgUS/vpDPi+6HWbFRsv7kAnJVy/C5tU+SPd/KLsvGju7yeyZqLgIZe6Jt/2AkUi+cVlWZ9Q3NZNl9EW3x5AVC1AehH7/nexamHTvHpLu3oHrwIEwMDGV1RiF6os+QEZkBAI3bJDTFvXqwcjRUQYvxk5OqDRmrAy4Qr7JHUMleLz9NuLOnpPVCPXNzODQtSusGjeG99Qp0HURP+xClTnvI8XHW94zy7Hfm9A3MUX0b4fl81XmzJcn1SFbvpDT8efOwOmNAUj19cntvujuDtdRY+R8ebVLFLdq2lz27BCVKMXz7uMmIT0gANFHcrep68L37obn3PeRLNrk3l04vSHaxES1/57z5iMjMgohmzfJabO6XvI+W6K8u/jfdeRb8v2Hf7+zxNvUdeF7vkfVeQuQ4u2NZO87cH5joCxpH/Vr7ufG872F8qJF8Fcb5bR5XS8Y5bWJoyPcRo6Bnr4ewr7/VrVNUQxH4V5JNa1wdZO3EchOSEBGhHqXMF007KUGWLDvL9Rzd0R9d0d8e+42UjMy0btx7vCL93/4E05W5pjapbmc3vTnVRmwVbazQmJaBradvonQuCT0baJeeEmMN/v9th9mdGuB/ypxflIeDBgwAJGRkVi4cKGMDUTlchEX5BX/EOf/BYcheXh44LfffsO7774r73MsKrmLAE1UaX9eKnRQJhpbpBlFpkncIFpUXRTjxUaMGKHW8Hlee+012fgilSkCOlFRUVRb+acDBsUXvigCIjJwIiIXB4Xow9q2bVvVwSAyd6J6oigaIsrgf/311/Im13+3ni7a+WMgTEwMMHtyLViIm0ffjccMcYPnAuPF3F1MYWNlVOpgT2Gsj3fGVIeVpZEMzsQ4tJCwNOiysH2/wtjBFjXfmyK73Ilg63K/cariH6aVXFUnSII4Ea+5YApMPT2QnZwiy+GLMWRZ8YmqZQytLFHrg3dh4uaCjNh4hB/6HQ8+XCuvkpYH1k3qo9Wx/BNlr9Xvyf8Dd+zDzdHzoHB1hKlH7s19BXFrABGAea2ZB893hiMtKAy3xs9H1B/5V/ND9/4q70lWa9GU3JtH37iHiz3HIKNQ8Q9dlXT+pCz4IQIrefPox48QvGIhshNyB6Ib2juqgi0hd9yYEvb9h8PQzh7ZCfEyIIvekztWSBD3OHOZMAMGNnbISUlGRqCfDMhSbpeD7KHoXnT0qLy3kse4cbk3j/bxgfe0qapuZArxPVjgsyO6X3lMmAATN3dZwEOUvvf9YBGyk/K7TotuXTUWLZL34RLzU3x9ZUAWf/EidF3sieOykIPryDHyfYj7lPnOFcF6boEYcYPogseIKHMuMmWuo8bKAER074w/f0aWNs9jYG4B9zHj5Um56EYbe+ovhGz9EniOZZ/LUuyfx2SbiEAi90bPD/BgjnqbFLyXpSju4vbWWCjc3GShE1EG3v+jJchOTirxNnWd3H8bW7i9JfbfXgZbD2a9q9p/hVPhz41CHgMi0Mp+0iZ+yxarfW7Ma9dB7XW5Fz8Ej8lT5f9Rvx6G/8fPrxpdWenWoDpik9Ow4dgVRCWlyKzWhuHdVWXuw+KTZUXGPImp6fjwwCm5rJWpQmbCto99TZbTL3z/M/E93L1hjX/9PVHpifP74rorahoqJBIj58/n30T9edNTFu7bQP8ZrXuVz/uNPE/z/5qg7V3QOdmp+X+8KVetN6trexd0TrSv7o/d+7cZW+h2l8h/W8HgiAp3OaY89SeVj3tL/ptM3pwJXZX2/QqtvbbJoOeXtdKGCp0pIyIiIiKiilfoo6IpHx1BiYiIiIiIKihmyoiIiIiIqPTKSaGP8oAtSUREREREpEXMlBERERERUekVuuchPTtmyoiIiIiIiLSIQRkREREREZEWsfsiERERERGVnj7zO2WFLUlERERERKRFzJQREREREVHpsSR+mWFLEhERERERaRGDMiIiIiIiIi1i90UiIiIiIio9fd6nrKwwU0ZERERERKRFzJQREREREVHpsdBHmWFLEhERERERaREzZUREREREVHp6HFNWVpgpIyIiIiIi0iIGZURERERERFrE7otERERERFR6+szvlBW2JBERERERkRYxU0ZERERERKXHQh9lhpkyIiIiIiIiLWJQRkREREREpEXsvkhERERERKWnx/xOWWFLEhERERERaREzZUREREREVHosiV9m2JJERERERERaxEwZERERERGVHkvilxkGZf9hJhbm2t4FnVOzdzVt74LOyclWansXdI7Pnofa3gWdU3dITW3vgs5RWPM7tqDs9Ext74LOyc7I0vYu6B5DI23vAZFWsPsiERERERGRFjFTRkREREREpceS+GWGLUlERERERKRFzJQR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Zs+ejfj4eNWNUQwYMACBgYG6OWmfffYZJk+ejBUrVqi1zbRzz5ycnNTtcWBQZsasbGyMfQgmx6YYxyQnC0vjlSaYKjtXR2Mfgsmx87U19iGYnOS7KcY+BJPiVv3xnMgUZk6+/CzJKdW/jLEPweQ8vllM/7/8rhdmLL169UJoaKgKtCTAklb3kgHTNv+4efOm6sio9d1336mujd27d9d7HVnn7MMPP3wsx8igjIiIiIiIirSRI0eqmyHSxCO769ev40ljUEZERERERPlmzEYfRQ0bfRARERERERkRM2VERERERFRk55QVBsyUERERERERGRGDMiIiIiIiIiNi+SIREREREeUbG30UHGbKiIiIiIiIjIiZMiIiIiIiyjc2+ig4zJQREREREREZEYMyIiIiIiIiI2L5IhERERER5VuGsQ+gCGGmjIiIiIiIyIiYKSMiIiIionxjo4+Cw0wZERERERGRETFTRkRERERE+cbFowsOM2VERERERERGxKCMiIiIiIjIiFi+SERERERE+cZGHwWHmTIiIiIiIiIjYqaMiIiIiIjyjY0+Cg4zZUREREREREbEoIyIiIiIiMiIWL5IRERERET5lqEx9hEUHcyUERERERERGREzZURERERElG9s9FFwmCkjIiIiIiIqSkGZhYUF1q1bh8epdOnSmD17doG+5rPPPou33noLj9OiRYvg5uaWr+cMGjQIXbp0eWzHRERERET0qItHG+sGcy9fDA0NxeTJk7Fx40bcvXsX7u7uqFWrltr29NNPoygYP368CizPnz+v2yZfV6lSBQMHDlTBlZZ8PWLECERFRcHBweGBr9urVy906NDhsQSpElA+7qAyP4b0LoFOz/nCqZgVTp2PxZffX8Xt4KSHem6froEY0b8UVv9xB98svG5wnxmTqqBRXXdM/PQ8dh+MgKnz7vIifHv1gY2HBxKvXMbNr2ch4fw5wztbWcG/7wB4tmkPG28vJAXdxO353yHm0IFHf00T5PXCi/Dt+dL947+CoDmzkHAh7+P3frEHvJ/vClsfX6RFRyHy3x248+N8aFJT1OOWDg4IGPwyXJs2g42bOxIuX8Stb79CwoWs32NT59i0DZxadoaVixtSb99A1K8/IfXmFYP7eo2cDLsK1XJtTzpzFOHff6a+DvzqF4PPjV6/DHHbf0dhUHxgb5R6ZRBsvb0Qd+4C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pFlR7xj7EExOUenAVZC8Kxm+2GLOLv6RtRwJZXLwLpolgI8q6rThecXmzPepwrEg9ZNUfWLujtXmzr7NYJiqbzcZ73u/3h5FCsN5I5FFsv/++2+VeZOuiNLqXko6s2fgiIiIiIhMlXFzOxYoSngJ3EikGYostN2gQQM1H0za/G/dulVvrTYiIiIiIir6mCkzEpnPJp0giYiIiIgKI06CKjjMlBERERERERkRgzIiIiIiIiIjYvkiERERERHlW7bVFej/xEwZERERERGRETFTRkRERERE+cZGHwWHmTIiIiIiIiIjYqaMiIiIiIjyLYOZsgLDTBkREREREZERMSgjIiIiIiIyIpYvEhERERFRvrHRR8FhpoyIiIiIiMiImCkjIiIiIqJ80xi104cFihJmyoiIiIiIiIyIQRkREREREZERsXyRiIiIiIjyjeuUFRxmyoiIiIiIiIyImTIiIiIiIso3tsQvOMyUERERERERGRGDMiIiIiIiIiNi+SIREREREeVbBjt9FBhmyoiIiIiIiIyImTIiIiIiIso3NvooOMyUERERERERGREzZURERERElG/MlBUcZsqIiIiIiIiMiEEZERERERGREbF80YxZWFoY+xBMjoUlr1PkpMnIMPYhmJz0lDRjH4LJsXLg705OTr6Oxj4Ek2LnYmvsQzA5d/dGGPsQTE7VoGvGPgTKhwzWLxYY/hUlIiIiIiIyImbKiIiIiIgo3zQspikwzJQREREREREZEYMyIiIiIiIiI2L5IhERERER5ZuGjT4KDDNlRERERERERsRMGRERERER5RtXzSk4zJQREREREREZETNlRERERESUb5xTVnCYKSMiIiIiIjIiBmVERERERERGxPJFIiIiIiLKtwxWLxYYZsqIiIiIiIiMiJkyIiIiIiLKNw1TZQWGmTIiIiIiIiIjYlBGRERERERkRCxfJCIiIiKifOMyZQWHmTIiIiIiIiIjYqaMiIiIiIjyLYONPgoMM2VERERERERGxEwZERERERHlm4aTygoMM2VERERERERGxKCMiIiIiIgIQEREBPr27QsXFxe4ublh6NChiIuLe+D+o0aNQqVKleDg4ICSJUvijTfeQHR0dL6+L8sXiYiIiIgo3zQZKHL69u2L4OBgbNmyBampqRg8eDCGDx+OFStWGNz/zp076vbFF1+gatWquHHjBl55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mhMhHRnNHYOQTAkJCWpdLunmqi1tlXmHsk1OKsePHw9zI2tLtW/fHk8//bRaf+ncuXNqTD799FN1gUNOws0Ju7gaxnEhMi1s1UVkQqV6K1asMPZhmKSmTZvitddeUwsCm3tAJkGILPharFgxlfGQkychQYicdJubCRMmqAYwO3bs0FtkXN4n0knNHEkgOnXqVGzZskWvm23Lli1V+29zM3r0aAwaNEgtIp79PdKhQwcVtJorjguRaTHfy6tEJkY6CX7//ffYunUratasCRsbG73HpTWvOTp06BD++ecfg81PzHFMsgch7dq10wtCPvzwQ7PLDMmabBJ8yRqH2edhSsAqJVnm6NSpUwYv8EgJo6wXaY6fIfPnz8+1XTKpUg5trjguRKaFQRmRCZWS1K5dW319+vRpvcce1La4KPvkk09UKY10wpI5DtnHwVzHhEGIvtDQUBVsGFpzyFzfI25ubggODs7VFObYsWNmOU+IXVwN47gQmRYGZUQmQrJBpE8aFEgrYimxoUwMQvRJt9KNGzeq8k2hHYMff/xRNYQxR71798a7776L1atXq/GQDPOePXswduxYDBgwAObm+eefV51tpYurkDGRsl8Zo27dusFccVyITAvnlBGZmMuXL+Ovv/5CYmKium/OvXgsLS1VswLKHYRomXsQItnU9957D6+++irS0tJUIN+mTRvVeXDatGkwRzImlStXRokSJVRznKpVq6olJJ566imVeTY3M2fOVOMgFzPkc7V58+YoX768WtfNXN8jguNCZFrYfZHIRMh6XD179lQZMznRlsnX0glryJAhcHd3V39AzY0sEXDnzh2zWY/sYTtRSme9fv36YdGiRRgxYgTOnj2LvXv3qq579erVg7mRsk1pciJz7bQdOuVqf40aNWBOkpOTdQsDC8l6SCm0jEmdOnVQoUIFmDN2cTWM40JkGhiUEZkIKSuSZhaS8ahSpYo6wZSgTLJm0iXrzJkzMDdSdtWxY0c1x0Gu9udsfvLbb7/BHDEIAT744AO0atVKza3L3mHQnEkHPcmWtmjRQnVabNSoUa7fGXNSqlQpNQ7a8ShevLixD8kkcFyITBODMiIT4efnpwKwWrVqqfIRbVB29epV1Y1RTr7NzciRI1WQKicPORt9CClRMxeGJuQb4uLiAnMgTSxu3LihC0S0J5kNGzY023XbJHMqXTnl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",
      "text/plain": [
       "<Figure size 1000x800 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(10, 8))\n",
    "corr = df.corr()\n",
    "sns.heatmap(corr, annot=True, cmap=\"coolwarm\", fmt=\".2f\")\n",
    "plt.title(\"Feature Correlation Matrix\")\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4f640be3-0083-4549-b486-87f89f6436db",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}               
''')
        
    def naive_bayes(self):
        return (r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "3544168c-73e2-413c-b38a-2a08161400c6",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.metrics import classification_report, accuracy_score, confusion_matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "08f3a0f9-3def-4471-98ea-a9c4fffa0df1",
   "metadata": {},
   "outputs": [],
   "source": [
    "data = pd.read_csv(\"../datasets/spam.csv\", encoding=\"latin-1\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "413803d8-288a-4751-8350-e8b1083716b0",
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data[['v1', 'v2']]\n",
    "data.columns = ['label', 'message']\n",
    "data.dropna(axis=0, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "cf0601c6-c569-4af9-9e2d-cadfaa847133",
   "metadata": {},
   "outputs": [],
   "source": [
    "X = data['message']\n",
    "y = data['label']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "4ea50018-cd44-40dd-bec5-cbab94445e86",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "6952a324-6d19-4775-b5f0-9c595a88168f",
   "metadata": {},
   "outputs": [],
   "source": [
    "vectorizer = CountVectorizer(stop_words='english')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "4d0c0d04-8fdb-433c-ae6d-a1f8ba6ad097",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train_vectorized = vectorizer.fit_transform(X_train)\n",
    "X_test_vectorized = vectorizer.transform(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "a58b449c-4e66-4121-b953-64334d87aaf6",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: #000;\n",
       "  --sklearn-color-text-muted: #666;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-1 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-1 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: flex;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "  align-items: start;\n",
       "  justify-content: space-between;\n",
       "  gap: 0.5em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label .caption {\n",
       "  font-size: 0.6rem;\n",
       "  font-weight: lighter;\n",
       "  color: var(--sklearn-color-text-muted);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-1 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-1 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-1 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 0.5em;\n",
       "  text-align: center;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-1 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>MultinomialNB()</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow\"><div><div>MultinomialNB</div></div><div><a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.6/modules/generated/sklearn.naive_bayes.MultinomialNB.html\">?<span>Documentation for MultinomialNB</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></div></label><div class=\"sk-toggleable__content fitted\"><pre>MultinomialNB()</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "MultinomialNB()"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = MultinomialNB()\n",
    "model.fit(X_train_vectorized, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "79d4396d-d027-4190-8f90-3fac72f7cdbe",
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred = model.predict(X_test_vectorized)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "2b908219-80d8-44aa-a0ea-30cc553478b5",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.9839\n"
     ]
    }
   ],
   "source": [
    "accuracy = accuracy_score(y_test, y_pred)\n",
    "print(f\"Accuracy: {accuracy:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "9b8ce7c4-c2ee-4af1-a63c-cd201ddd3a86",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification Report:\n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "         ham       0.99      0.99      0.99       965\n",
      "        spam       0.96      0.92      0.94       150\n",
      "\n",
      "    accuracy                           0.98      1115\n",
      "   macro avg       0.97      0.96      0.96      1115\n",
      "weighted avg       0.98      0.98      0.98      1115\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(\"Classification Report:\")\n",
    "print(classification_report(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "3551b059-a159-47ef-b64c-4b55a6fb6d96",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Confusion Matrix:\n",
      "[[959   6]\n",
      " [ 12 138]]\n"
     ]
    }
   ],
   "source": [
    "print(\"Confusion Matrix:\")\n",
    "print(confusion_matrix(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4a265f78-2ac4-4548-abbf-4a85c9c5f1c5",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
''')
        
    def random_forest(self):
        return (r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "06465798-c66a-4c6a-9b03-ad89a06bf5b5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.ensemble import RandomForestClassifier\n",
    "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "d6b99925-cd04-463c-a61f-38f955400720",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_data(data_dir):\n",
    "    texts, labels = [], []\n",
    "\n",
    "    for label in ['pos', 'neg']:\n",
    "        label_dir = os.path.join(data_dir, label)\n",
    "        for filename in os.listdir(label_dir):\n",
    "            with open(os.path.join(label_dir, filename), encoding='utf-8') as f:\n",
    "                texts.append(f.read())\n",
    "            labels.append(1 if label == 'pos' else 0)\n",
    "\n",
    "    return texts, labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "0d19c939-ea67-4381-baf0-3ea8abb5772b",
   "metadata": {},
   "outputs": [],
   "source": [
    "train_dir = \"../datasets/aclImdb/train/\"\n",
    "test_dir = \"../datasets/aclImdb/test/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "f26f57e4-2a5b-46ec-b510-1d4114728ac1",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, y_train = load_data(train_dir)\n",
    "X_test, y_test = load_data(test_dir)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "fe6f0bfb-a0d6-445a-b160-4575af56c583",
   "metadata": {},
   "outputs": [],
   "source": [
    "vectorizer = CountVectorizer(stop_words='english')\n",
    "X_train_vectorized = vectorizer.fit_transform(X_train)\n",
    "X_test_vectorized = vectorizer.transform(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "f1a7886e-1ddd-4a50-9586-9214944ffb8b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: #000;\n",
       "  --sklearn-color-text-muted: #666;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-1 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-1 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: flex;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "  align-items: start;\n",
       "  justify-content: space-between;\n",
       "  gap: 0.5em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label .caption {\n",
       "  font-size: 0.6rem;\n",
       "  font-weight: lighter;\n",
       "  color: var(--sklearn-color-text-muted);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-1 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-1 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-1 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 0.5em;\n",
       "  text-align: center;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-1 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>RandomForestClassifier(random_state=42)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow\"><div><div>RandomForestClassifier</div></div><div><a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.RandomForestClassifier.html\">?<span>Documentation for RandomForestClassifier</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></div></label><div class=\"sk-toggleable__content fitted\"><pre>RandomForestClassifier(random_state=42)</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "RandomForestClassifier(random_state=42)"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = RandomForestClassifier(n_estimators=100, random_state=42)\n",
    "model.fit(X_train_vectorized, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "be7c52a7-cfba-4f3f-b908-85c38a0d4e72",
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred = model.predict(X_test_vectorized)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "7e11ed28-174a-4104-a940-f3bf13460f0b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.8517\n"
     ]
    }
   ],
   "source": [
    "accuracy = accuracy_score(y_test, y_pred)\n",
    "print(f\"Accuracy: {accuracy:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "65fb3556-0086-4b5d-b850-80de5dd89ded",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification Report:\n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.85      0.86      0.85     12500\n",
      "           1       0.86      0.85      0.85     12500\n",
      "\n",
      "    accuracy                           0.85     25000\n",
      "   macro avg       0.85      0.85      0.85     25000\n",
      "weighted avg       0.85      0.85      0.85     25000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(\"Classification Report:\")\n",
    "print(classification_report(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "bc5054d0-2f6f-4ec1-8939-3be077b7eb63",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Confusion Matrix:\n",
      "[[10718  1782]\n",
      " [ 1926 10574]]\n"
     ]
    }
   ],
   "source": [
    "print(\"Confusion Matrix:\")\n",
    "print(confusion_matrix(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "10d6b78e-d0db-41a7-af03-c8bd6018fd94",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
''')

    def decision_tree(self):
        return (r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "7ab39eab-2b16-402b-9687-9cd383efc732",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "from sklearn.metrics import confusion_matrix, accuracy_score, classification_report\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "4f14073c-0c40-48bb-b223-9e77bbb86533",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_data(data_dir):\n",
    "    texts, labels = [], []\n",
    "\n",
    "    for label in ['pos', 'neg']:\n",
    "        label_dir = os.path.join(data_dir, label)\n",
    "        for filename in os.listdir(label_dir):\n",
    "            with open(os.path.join(label_dir, filename), encoding='utf-8') as f:\n",
    "                texts.append(f.read())\n",
    "            labels.append(1 if label == 'pos' else 0)\n",
    "\n",
    "    return texts, labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "a8bc8689-4ec0-4636-bf7f-2aafe528f649",
   "metadata": {},
   "outputs": [],
   "source": [
    "train_dir = \"../datasets/aclImdb/train/\"\n",
    "test_dir = \"../datasets/aclImdb/test/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "7a1c2043-5f9b-4767-9ca7-85252b3aab04",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, y_train = load_data(train_dir)\n",
    "X_test, y_test = load_data(test_dir)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "495fdeb6-9317-4378-a6d9-e6678c612abb",
   "metadata": {},
   "outputs": [],
   "source": [
    "vectorizer = CountVectorizer(stop_words='english')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "47d44144-5b88-43af-85b4-3c8111faba2d",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train_vectorized = vectorizer.fit_transform(X_train)\n",
    "X_test_vectorized = vectorizer.transform(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "c457a2fe-da8a-4d3b-8fc1-239e4e241641",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-2 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: #000;\n",
       "  --sklearn-color-text-muted: #666;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-2 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-2 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-2 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: flex;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "  align-items: start;\n",
       "  justify-content: space-between;\n",
       "  gap: 0.5em;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label .caption {\n",
       "  font-size: 0.6rem;\n",
       "  font-weight: lighter;\n",
       "  color: var(--sklearn-color-text-muted);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-2 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-2 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-2 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-2 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-2 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-2 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-2 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-2 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 0.5em;\n",
       "  text-align: center;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-2 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-2\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>DecisionTreeClassifier(random_state=42)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-2\" type=\"checkbox\" checked><label for=\"sk-estimator-id-2\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow\"><div><div>DecisionTreeClassifier</div></div><div><a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.6/modules/generated/sklearn.tree.DecisionTreeClassifier.html\">?<span>Documentation for DecisionTreeClassifier</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></div></label><div class=\"sk-toggleable__content fitted\"><pre>DecisionTreeClassifier(random_state=42)</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "DecisionTreeClassifier(random_state=42)"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = DecisionTreeClassifier(random_state=42)\n",
    "model.fit(X_train_vectorized, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "888331e5-3b7f-4b73-9d8d-dcf0928ab48d",
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred = model.predict(X_test_vectorized)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "f471d9a8-209e-4f9b-91c9-b8d813b28ad4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.7251\n"
     ]
    }
   ],
   "source": [
    "accuracy = accuracy_score(y_test, y_pred)\n",
    "print(f\"Accuracy: {accuracy:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "ec609ee3-2b2b-4d9a-ac16-77ddd45eb76d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification Report:\n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.72      0.73      0.73     12500\n",
      "           1       0.73      0.72      0.72     12500\n",
      "\n",
      "    accuracy                           0.73     25000\n",
      "   macro avg       0.73      0.73      0.73     25000\n",
      "weighted avg       0.73      0.73      0.73     25000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(\"Classification Report:\")\n",
    "print(classification_report(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "e938b01e-8a2b-4760-9192-d4697681637d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Confusion Matrix:\n",
      "[[9106 3394]\n",
      " [3479 9021]]\n"
     ]
    }
   ],
   "source": [
    "print(\"Confusion Matrix:\")\n",
    "print(confusion_matrix(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "05fa6398-b023-43a1-bce8-cdbe26a030bf",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}               
                ''')
        
    def multilayer_perceptron(self):
        return r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "9e073181-eca3-49ad-b845-dabf0a5569bd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import struct\n",
    "\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.neural_network import MLPClassifier\n",
    "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "7e4f8b5b-1314-4997-94a5-d5954f089eae",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_mnist_images(filename):\n",
    "    with open(filename, 'rb') as f:\n",
    "        magic, num, rows, cols = struct.unpack(\">IIII\", f.read(16))\n",
    "        print(f\"Loaded {num} images of size {rows}x{cols}\")\n",
    "\n",
    "        images = np.frombuffer(f.read(), dtype=np.uint8).reshape(num, rows*cols)\n",
    "        return images / 255.0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "6dd2b80c-8c6e-4116-9f93-494a40ebc5f0",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_mnist_labels(filename):\n",
    "     with open(filename, 'rb') as f:\n",
    "        magic, num = struct.unpack(\">II\", f.read(8))\n",
    "        labels = np.frombuffer(f.read(), dtype=np.uint8)\n",
    "        return labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "e1ff4e6f-88f2-4a2c-86b5-6d5c1213c3ce",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Loaded 60000 images of size 28x28\n",
      "Loaded 10000 images of size 28x28\n"
     ]
    }
   ],
   "source": [
    "X_train = load_mnist_images('../datasets/MNIST/train-images.idx3-ubyte')\n",
    "y_train = load_mnist_labels('../datasets/MNIST/train-labels.idx1-ubyte')\n",
    "X_test = load_mnist_images('../datasets/MNIST/t10k-images.idx3-ubyte')\n",
    "y_test = load_mnist_labels('../datasets/MNIST/t10k-labels.idx1-ubyte')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "76116044-9c38-4837-8e3f-762dc1db4b98",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "X_train shape : (60000, 784)\n",
      "y_train shape : (60000,)\n",
      "X_test shape : (10000, 784)\n",
      "y_test shape : (10000,)\n",
      "The first record of X_train : \n",
      "[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0.]\n",
      "The label of the first record : 5\n"
     ]
    }
   ],
   "source": [
    "print(f\"X_train shape : {X_train.shape}\")\n",
    "print(f\"y_train shape : {y_train.shape}\")\n",
    "print(f\"X_test shape : {X_test.shape}\")\n",
    "print(f\"y_test shape : {y_test.shape}\")\n",
    "\n",
    "print(f\"The first record of X_train : \\n{X_train[0][:100]}\")\n",
    "print(f\"The label of the first record : {y_train[0]}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "c0cf0554-7a2b-43dd-acd3-df94831ae48f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAxoAAAMsCAYAAADTY9TiAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjkuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8ekN5oAAAACXBIWXMAAA9hAAAPYQGoP6dpAABpDklEQVR4nO3dCbxN1fv48XWR+RKusUxlyiwRvkKmRCGzyFimMhQSiSKUzFSIDBEZMlaGCiWSIUpmQuZ5nrn/197/l37t82z2dqxz9j3nfN6vV6+sxzr7rLTse56z97OfqNjY2FgFAAAAABrF03kwAAAAADCQaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORMPB8uXLVVRUlO0/v/76q9fLQ4S4evWq6tatm8qUKZNKkiSJevLJJ9XSpUu9XhYiVL9+/cxzYP78+b1eCiLAhQsXVO/evVWVKlVU6tSpzb03ceJEr5eFCLJ+/Xpz/6VIkUJFR0erypUrq40bN3q9rJCQwOsFhIoOHTqoYsWKWWI5cuTwbD2ILM2aNVOzZs1SnTp1Ujlz5jR/yFatWlUtW7ZMlS5d2uvlIYIcOHBA9e/fXyVLlszrpSBCnDhxQvXp00dlyZJFFSpUyPwCEAiWDRs2mD9nM2fObCa8t27dUp988okqW7as+u2331Tu3Lm9XmKcFhUbGxvr9SLiMuOE9vTTT6uZM2eqOnXqeL0cRCDjRGZcwfjoo49Uly5dzNiVK1fMb5PTpUunVq1a5fUSEUEaNGigjh8/rm7evGl+ANy8ebPXS0IEXNE9ffq0ypAhg1q3bp35pd+ECRPML2CAQKtWrZpavXq12rlzp0qTJo0ZO3z4sMqVK5d5ZWP27NleLzFO49ape3D+/Hl148YNr5eBCGNcyYgfP75q1arVv7HEiROrli1bmie/f/75x9P1IXL89NNP5n4cNmyY10tBBEmUKJGZZABe+Pnnn1XFihX/TTIMGTNmNK9oLFy40Ly1D3dGouFS8+bNzXvzjA94xhUO41sVIBh+//1385sTY//9V/Hixc1/c58ogsG4gtG+fXv18ssvqwIFCni9HAAI2hU1ozbSV9KkSdW1a9e4quuAGg0HCRMmVLVr1zbvh4+JiVFbtmxRgwYNUk899ZR5y0qRIkW8XiLCnHGJ1vj2xNft2KFDhzxYFSLN6NGj1b59+9T333/v9VIAIGiMGgzj4T/Gly3G3QUGI8FYs2aN+euDBw96vMK4jSsaDkqVKmXeKtCiRQtVvXp19dZbb5kbznjqRffu3b1eHiLA5cuXzVsHfBlX127/PhBIJ0+eVL169VLvvPOOSps2rdfLAYCgadeundqxY4d5u7LxZbNxBaNJkybml4AGfgbfHYmGH4ynTdWoUcN84o+R4QKBZFyyNS7d+jIKwm//PhBIPXv2NB8ratw6BQCRpE2bNqpHjx7qyy+/VPny5TNvHd29e7d68803zd9Pnjy510uM00g0/GQ85sy4dHbx4kWvl4IwZ9widfubk/+6HTN6awCBYjxpZezYseYjvo3b9Pbu3Wv+YyS6169fN3996tQpr5cJAAHtHXT06FGzMPyPP/5Qa9euNR9zazBqKHFnJBp+2rNnj3nrCpksAq1w4cLmZdtz585Z4rfvDzV+HwgU4/5j4weqkWhkz57933+M/WfsS+PXRo8DAAhnqVKlMvtp3H4YhlGv9vDDD6s8efJ4vbQ4jWJwB8bz4n3vSd60aZOaP3++evbZZ1W8eORqCCyjf4vxAALjW+XbfTSMW6mM58gb/TWMq2tAoBj9WubMmWN7O5XxyO/hw4erRx991JO1AYAXvvrqK/OqhvGzmc+Bd0fDPgfly5c374E3isKN5mhGIZDxge+BBx4wexg89thjXi8REaBevXrmh73XX3/drBGaNGmS2cjvhx9+UGXKlPF6eYhA5cqVo2EfgmbUqFHqzJkz5u17n376qapVq9a/T300aodSpkzp9RIRxv2DjKu2RnM+o5eG8UAg44u+SpUqqQULFqgECfjO/m5INByMGDFCTZ06Ve3atcu8dcW4ulGhQgWzDb3xgQ8IBuN+eOOJP1OmTDE75BYsWFD17dtXPfPMM14vDRGKRAPBlC1bNvPxynb+/vtv8/eBQDAKv40nT23YsMG8imvcLtq0aVP1xhtvmC0QcHckGgAAAAC048YyAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaOe6nWFUVJT+d0dIC2YLFvYffAW7BRB7EL44B8JL7D+Ewv7jigYAAAAA7Ug0AAAAAGhHogEAAABAOxINAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABol0D/IQEEU9GiRUXstddeE7EmTZpYxpMnTxZzRo4cKWIbNmy47zUCAIDIwxUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0i4qNjY11NTEqSoW7+PHji1jKlCn9OpZdMW7SpEkt49y5c4s5r776qogNGjRIxBo2bGgZX7lyRcz54IMPROy9995TurjcOlpEwv5zo3DhwiL2448/iliKFCn8Ov7Zs2dFLE2aNCouCub+M7AHvVOhQgURmzp1qmVctmxZMWf79u0BXRfnwNDWs2dPVz8j48WT38mWK1fOMl6xYoUKNvYfvOR2/3FFAwAAAIB2JBoAAAAAtCPRAAAAAKBdyDfsy5Ili4glTJjQMi5VqpSYU7p0aRF78MEHRax27doqUA4cOCBiI0aMELEXXnhBxM6fP28Zb9q0Sczx4p5R6FW8eHHLePbs2a7qiOzunfTdM9euXXNVj1GiRAnHJn52x8KdlSlTxvHPfs6cOUFcUdxWrFgxEVu7dq0na0HoatasmWXcrVs3MefWrVtxskYMCFVc0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAILKLwd02K/O3yV6g+RaZ2TULunDhgmNjKsPhw4ct49OnTwe9WRX859u80fD444+L2JQpUyzjjBkz+v2eO3futIwHDhwo5kyfPl3EfvnlFxHz3bsDBgzwe12RyLfZlyFnzpyWcaQWg9s1R8uePbuIZc2a1TKmoRic+O6ZxIkTe7YWxD1PPvmkiDVu3NixMWi+fPlcHb9Lly6W8aFDh1w9qMj3c4BhzZo1KlRwRQMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAgMguBt+/f7+InTx5MqjF4HYFOGfOnBGxp59+WsR8uyd/8cUXmleHUDFmzBgRa9iwYUDf07fYPHny5K66ydsVLhcsWFDz6iJLkyZNRGz16tWerCWusXvgwSuvvOJYILlt27aArguhpWLFiiLWvn17x9fZ7aPnnntOxI4ePXofq4PX6tevL2LDhw8XsZiYGMeHTixfvlzE0qZNK2IfffSR47rsjm93rAYNGqhQwRUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAAiuxj81KlTIta1a1fHwq3ff/9dzBkxYoSr99y4caNlXKlSJTHn4sWLrjpFduzY0dV7IrwULVpUxKpVqyZibjob2xVrL1iwQMQGDRokYr5dSO3+Xth1mC9fvrxfa8W9db/G/zdu3Di/Ot0jctl1U54wYYJfD4qxK9jdt2/ffawOwZYggfWj7RNPPCHmfPbZZyKWNGlSEfvpp58s4759+4o5K1euFLFEiRKJ2IwZMyzjypUrKzfWrVunQhk/7QAAAABoR6IBAAAAQDsSDQAAAACRXaNhZ+7cuSL2448/Wsbnz58XcwoVKiRiLVu2dLzX3a4ew85ff/0lYq1atXL1WoS2woULW8ZLly4Vc1KkSCFisbGxIvbdd985NvUrW7asiPXs2dPx3vfjx4+LOZs2bRKxW7duOdaY+DYDNGzYsEHEIpFdc8P06dN7spZQ4Lbhqt3fK0Smpk2bilimTJkcX2fXaG3y5Mna1gVvNG7c2K+6L7tzim9jv3PnzvndELCyi5qMAwcOiNikSZNUKOOKBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2oV8MbgdN8U6Z8+edXWsV155xTL+6quvXBXLIjLkypXLsYmkXXHriRMnROzw4cOORWAXLlwQc7755htXMZ2SJEliGXfu3FnMadSoUUDXECqqVq3q+OcXqeyK4rNnz+7qtQcPHgzAihDXxcTEiFiLFi1c/Vw+c+aMZfz+++9rXh2Cza6BXo8ePRwftPLJJ5+4eoiK2+JvX2+//bZfr+vQoYOI2T24JZRwRQMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO3CshjcjXfffVfEihYt6th1uWLFimLOkiVLNK8OcVGiRIkcO8fbFf/adaZv0qSJiK1bty5ki4azZMni9RLirNy5c7ua99dff6lIY/f3x65AfMeOHSJm9/cK4SdbtmyW8ezZs/0+1siRIy3jZcuW+X0sBF+vXr0cC78N165ds4wXL14s5nTr1k3ELl++7LiGxIkTu+r4bfczMSoqyvFhBPPmzVPhhisaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoF7HF4BcvXnTsAm7YsGGDZfzZZ5+JOXYFZXaFvR9//LFjt0rEXUWKFHHV9dlXjRo1RGzFihXa1oXwsHbtWhWqUqRIIWJVqlQRscaNGzsWUbrt/uvb5RnhyXcfFSxY0NXrfvjhBxEbPny4tnUhsB588EERa9eunYjZfY7yLf6uWbOm3+vIkSOHZTx16lRXDxKyM2vWLMt44MCBKhJwRQMAAACAdiQaAAAAALQj0QAAAACgXcTWaNjZvXu3iDVr1swynjBhgpjz0ksvuYolS5bMMp48ebKYc/jwYdfrRXANGTLEsQGPXf1FqNdjxIsnv4+4deuWJ2sJZ6lTp9Z2rEKFCjnuU7vmow8//LCIJUyY0DJu1KiRqz1i1/xqzZo1lvHVq1fFnAQJ5I+l9evXixjCj9299B988IHj61auXCliTZs2FbGzZ8/ex+oQTL7nHUNMTIyr13bo0MEyTpcunZjTvHlzEatevbqI5c+f3zJOnjy5qzoRu9iUKVMca4XDEVc0AAAAAGhHogEAAABAOxINAAAAANqRaAAAAADQjmJwB3PmzLGMd+7c6apIuEKFCiLWv39/yzhr1qxiTr9+/UTs4MGDrtcLPZ577jkRK1y4sKuCr/nz56twYlf47fvfvXHjxiCuKLTYFUXb7ZvRo0dbxj169PD7PX2bmtkVg9+4cUPELl26JGJbtmyxjD///HNXDUrtHoJw9OhRy/jAgQNiTpIkSURs27ZtIobQli1bNhGbPXu2X8fas2eP415DaLl27ZqIHT9+XMTSpk0rYn///be25siHDh2yjM+dOyfmZMyYUcROnDghYgsWLFCRiCsaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoRzH4Pdq8ebOI1atXT8Sef/55EfPtKt66dWsxJ2fOnCJWqVIlP1aK+2FXkGrXqfTYsWMi9tVXX6lQkChRIhF79913Xb32xx9/tIy7d++ubV3hpl27diK2b98+EStVqpS299y/f79lPHfuXDFn69atIvbrr7+qQGrVqpVjIaddYS/CT7du3Vw9eMINN93DEVrOnDnjqnP8woULRSx16tSW8e7du8WcefPmidjEiRNF7NSpU5bx9OnTXRWD282LVFzRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAABAO4rBA1S09MUXX4jYuHHjLOMECeQff5kyZUSsXLlyIrZ8+XI/Vgrdrl69KmKHDx9WoVD83bNnTzGna9euImbXvXnw4MGW8YULF7SsMVJ8+OGHKhJVqFDBcY6/3aERdxUuXFjEKleu7Nex7Ip4t2/f7texEFrWrFkjYnYPlNDJ9zNZ2bJlXT3EgIda/B+uaAAAAADQjkQDAAAAgHYkGgAAAAC0o0bjHhUsWFDE6tSpI2LFihUTMbuaDF9btmwRsZ9++ume1ojgmT9/vgqVe6J96y/q16/v6v7n2rVra14dcGdz5szxegnQbMmSJSKWKlUqV6/1bSLZrFkzbesC7rV5r109RmxsrIjRsO//cEUDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtKAb/j9y5c4vYa6+9ZhnXqlVLzMmQIYNf73fz5k1Xzd7sio8QWFFRUa5iNWvWFLGOHTuqYHr99ddF7J133hGxlClTWsZTp04Vc5o0aaJ5dQAiXZo0afz+ufbJJ59YxjQHRTAtXrzY6yWEPK5oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgXUQUg9sVazds2NCx8NuQLVs2betYt26dZdyvX7+Q6TQdaew6fdrF7PbWiBEjLOPPP/9czDl58qSIlShRQsReeukly7hQoUJizsMPPyxi+/fvdyxq8y2yBILN7gELuXLlcuwOjbhtwoQJlnG8eP5/p7lq1SoNKwL888wzz3i9hJDHFQ0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQL+WLw9OnTi1jevHkt41GjRok5efLk0baGNWvWiNhHH30kYvPmzbOM6fgd+uLHjy9i7dq1s4xr164t5pw7d07EcubMqa1YctmyZSLWq1cvv44PBIrdAxbup3AYwVe4cGERq1ixouPPumvXronYxx9/LGJHjx697zUC/nrkkUe8XkLI44wOAAAAQDsSDQAAAADakWgAAAAAiJwajdSpU4vYmDFjXN0fqvOeOt/73wcPHuzYCM1w+fJlbWtA8K1evVrE1q5dK2LFihVzPJZdUz+72iI7vo39pk+fLuZ07NjR1bGAUFCyZEkRmzhxoidrgbMHH3zQ1TnP18GDB0WsS5cu2tYF6PDzzz871pBRb3t3XNEAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAACA8isGffPJJEevatatlXLx4cTHnoYce0raGS5cuidiIESNErH///pbxxYsXta0BcdeBAwdErFatWiLWunVrEevZs6df7zl8+HAR+/TTTy3jXbt2+XVsIC6KioryegkAcEebN2+2jHfu3OnqAUSPPvqoiB0/flxFIq5oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAAAQHsXgL7zwgquYG1u2bBGxhQsXWsY3btwQc+w6fJ85c8avNSAyHD58WMTeffddVzEASn333XeWcd26dT1bC/TYtm2biK1atcoyLl26dBBXBASO7wOCDOPGjROxfv36iVj79u0dP7+GI65oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgXVRsbGysq4l0cIUPl1tHC/YfvNx/BvYgfHEOhJfYf8GXIkUKEZsxY4aIVaxYUcS+/vpry7h58+ZizsWLF1W47T+uaAAAAADQjkQDAAAAgHYkGgAAAAC0o0YDfuP+UHiJGg14jXMgvMT+i7t1G3YN+9q2bWsZFyxYUMwJpSZ+1GgAAAAA8AyJBgAAAADtSDQAAAAAaEeiAQAAAEA7isHhNwrR4CWKweE1zoHwEvsPXqIYHAAAAIBnSDQAAAAAaEeiAQAAAEA7Eg0AAAAA3hWDAwAAAIBbXNEAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0Ha9euVa+99prKly+fSpYsmcqSJYuqV6+e2rFjh9dLQ4S4cOGC6t27t6pSpYpKnTq12aF14sSJXi8LEeKvv/5SdevWVY888ohKmjSpiomJUWXKlFELFizwemmIEJwDEZf069fP3IP58+f3eikhgUTDwYcffqhmz56tKlSooIYPH65atWqlfvrpJ/X444+rzZs3e708RIATJ06oPn36qK1bt6pChQp5vRxEmH379qnz58+rpk2bmufAd955x4xXr15djR071uvlIQJwDkRcceDAAdW/f3/zi2e4w+NtHaxatUo98cQTKmHChP/Gdu7cqQoUKKDq1KmjpkyZ4un6EP6uXr2qTp8+rTJkyKDWrVunihUrpiZMmKCaNWvm9dIQoW7evKmKFi2qrly5orZt2+b1chDmOAcirmjQoIE6fvy4eQ40EmC+cHbGFQ0HpUqVsiQZhpw5c5q3UhnfrgCBlihRIvMHLBBXxI8fX2XOnFmdOXPG66UgAnAORFxg3M0ya9YsNWzYMK+XElISeL2AUGRcBDp69KiZbABAJLh48aK6fPmyOnv2rJo/f7767rvvVP369b1eFgAEnHEFo3379urll18272iBeyQafpg6dao6ePCgec8oAESCzp07qzFjxpi/jhcvnqpVq5YaNWqU18sCgIAbPXq0Wa/2/fffe72UkEOicY+M+5FfffVVVbJkSbM4EgAiQadOncy6tEOHDqkZM2aY3/Bdu3bN62UBQECdPHlS9erVy3wQRtq0ab1eTsihRuMeHDlyRFWrVk2lTJnSvE/PuE8ZACJBnjx5VMWKFVWTJk3UwoULzUeOPv/88+atpAAQrnr27Gk+Vtm4dQr3jkTDJeO+5GeffdYsfly0aJHKlCmT10sCAM8YVzeMPkP0FAIQroynjBqP8e7QoYN5NXfv3r3mP8YT965fv27++tSpU14vM04j0XDB2FDGN3fGD1Tjm7y8efN6vSQA8JRRGH77SxgACEdGPe6tW7fMRCN79uz//rNmzRrzM6Hxa+p1744aDQfGfcjGk1VWr16t5s2bZ9ZmAECkOHbsmEqXLp0lZnyTN3nyZJUkSRK+eAEQtozu33PmzLG9ncpoZGo0MX300Uc9WVuoINFw8aQV41GOxhUN4/KYb4O+xo0be7Y2RA7j6T7GbXvGpVvDggULzA6lBuO+UaNuCAiE1q1bq3PnzqkyZcqohx56yKxVM568ZzwYY/DgwSp58uReLxERgHMgvBATE6Nq1qwp4rd7adj9HqzoDO6gXLlyasWKFXf8ff74EAzZsmUzH61n5++//zZ/HwiE6dOnq/Hjx6s///zTfPpKdHS02RXc+HBXvXp1r5eHCME5EHHtsyGdwd0h0QAAAACgHcXgAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA8K4zeFRUlP53R0gLZgsW9h98BbsFEHsQvjgHwkvsP4TC/uOKBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAGiXQP8hAfhj+PDhItahQwfLePPmzWLOc889J2L79u3TvDoAABAX/fDDDyIWFRUlYuXLl1fBxhUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0oxhcg+joaBFLnjy5iFWrVs0yTps2rZgzZMgQEbt69ep9rxFxS7Zs2USscePGInbr1i3L+LHHHhNz8uTJI2IUg8NJrly5ROyBBx4QsTJlyljGn3zyieM+1W3evHki1qBBA8v42rVrAV0DAs9u/5UqVcoy7t+/v5jzv//9L6DrAuKaoUOH3vXviWHy5MkqLuCKBgAAAADtSDQAAAAAaEeiAQAAAEA7ajTu8V76bt26iTklS5YUsfz58/v1fhkzZnRs2obQd/z4cRH76aefRKx69epBWhHCSb58+SzjZs2aiTl169YVsXjx5HdPmTJlcqzHiI2NVYFk9/dg9OjRlnGnTp3EnHPnzgV0XdArZcqUIrZs2TLL+MiRI2JOhgwZRMxuHhCKPvjgAxFr06aNZXz9+nVXTfy8wBUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0i9hicLsmZ3bFhI0aNbKMkyRJIuZERUWJ2D///CNi58+fd2y+Vq9ePRGza5C1bds2EUPouHjxoojRZA+6DBgwwDKuWrWqCjdNmjSxjMePHy/m/PLLL0FcEYLBrvCbYnCEsxIlSjg2t1y5cqWYM2PGDBUXcEUDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtEkRCd9EPP/xQzKlfv76IRUdH+/V+O3fuFLFnnnnGsXjHrqA7JibGVQyh7cEHHxSxQoUKebIWhJ+lS5f6VQx+7NgxEfMtsrbrHm7XLdxOqVKlLOOyZcu6eh1wt4evADqUKVNGxN5++23LuGHDhmLOqVOntK2hoc3x8+fPL2K7d++2jLt06aLiKq5oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgXVgWg7/wwguW8csvv6zt2L4FOIZKlSq56gyeI0cObetAaEuaNKmIZcmSxa9jFStWTMTsHjRA5/HI8emnn1rGc+fOdfW669evB7TDcooUKSzjzZs3izmZMmVydSzf/6Z169bd5+oQCmJjY0UsceLEnqwF4WXs2LEiljNnTss4b968Yo5dV25/9ejRQ8TSpEkjYq+88oplvGnTJhVXcUUDAAAAgHYkGgAAAAC0I9EAAAAAoF1Y1mjUrVvXr9ft3btXxNauXWsZd+vWzVU9hp3HHnvMr3Uh/Bw6dEjEJk6cKGLvvvuu47Hs5pw5c0bERo0adU9rROi6ceOGX+eoQPNtZJoqVSq/j3XgwAHL+OrVq34fC6HtiSeeELFff/3Vk7UgdF26dMmxJkhnPVDhwoVFLGvWrK4aooZSXRJXNAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0C4si8F9G5m0atVKzFmyZImI7dq1S8SOHTumbV3p06fXdiyEn759+/pVDA7ERQ0aNHA8NydJksTv4/fq1cvv1yI0HmJgOHv2rGWcMmVKMefRRx8N6LoQGT9vCxQoIGJbt27V1hgvWbJkjg8Xsmvma/dgg1mzZqlQwRUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0SxAJXZfjSkFtyZIlvV4CQky8ePEcO4QCwdSoUSMRe+utt0QsR44cIvbAAw/49Z4bN24UsevXr/t1LMRdZ86cEbGff/7ZMn7uueeCuCKEg8yZMzs+mOJODyN47bXXLOPjx4/7vY4hQ4ZYxnXr1nX8/Gr43//+p0IZVzQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANAuLIvBderQocNdOzveC7uuk75WrVolYqtXr/b7PRHafIu/Y2NjPVsLQke2bNks45deeknMqVixol/HLl26tIj5uy/PnTvnqrD822+/FbHLly/79Z4Awlv+/Pkt4zlz5og5MTExIjZy5EgRW7FihV9r6NKli4g1a9bM8XX9+vVT4YYrGgAAAAC0I9EAAAAAoB2JBgAAAADtIqJGI2nSpCKWN29eEevdu7eIVa1a9Z6bqrltrGbXmKV58+YidvPmTcdjAYhMvvcjG+bPn28ZZ8mSRcVFvs3YDGPHjvVkLQhdadKk8XoJCIIECeRH1saNG4vY+PHj/fqMZtdUuXv37ndtumdInTq1iNk144uKirKMJ0+eLOaMGTNGhRuuaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoF3IF4M/8MADIlakSBHLePbs2WJOxowZXTWA8i3YtmueV6VKFVcF6G4Km2rVqiViw4cPF7Fr1645Hh9AZPItOvQd3w9/H35h57nnnhOxZ599VsS+++47v46PyFC9enWvl4AgaNCggYiNGzfOsYGo3flp165dIvbEE084xmrUqCHmPPTQQ64+Yx4/ftwybtGihYoEXNEAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAACCyi8ETJkzoqhD766+/djzWe++9J2I//vijiP3yyy+OHSDtXmfXrddX2rRpRWzAgAEitn//fhGbO3euZXz16lXH90Po8S28dVt0W6ZMGREbNWqUtnUh7ti8ebOIlStXzrF77uLFi0XsypUr2tbVsmVLEWvfvr224yMyLFu2zPEBAgg/9evXF7EJEyaI2PXr10XszJkzlvGLL74o5pw+fVrEBg8eLGJly5Z1LBi3e9iGb0G6ISYmRv3XP//8o5zO3Ybdu3erUMYVDQAAAADakWgAAAAA0I5EAwAAAIB2JBoAAAAAtIuKtatYsZuosbOsvx2/+/TpI2Jdu3Z1PJZdV9mXXnrJsYDIrmD722+/FXMef/xxV527Bw4c6Fgwbtd10s73339vGX/44Yeuip3sbNy4UfnD5dbRItj7L664efOmtj/zggULWsZbtmxRoSyY+y+S96C/UqZMKWInT550fN3zzz8fMp3BOQcGXu3atS3jmTNnijmXL18Wsbx584rYvn37VDgJ5/1n95CdrFmzitj777/vqmjcDbs9M2bMGMu4ZMmSfheD+/ryyy9FrEmTJirc9h9XNAAAAABoR6IBAAAAQDsSDQAAAADh27Avfvz4lnHfvn3FnC5duojYxYsXReytt96yjKdPn+6qHsOuEYtvk7MiRYqIOTt37hSxtm3bOjYeSpEihZhTqlQpEWvUqJGIVa9e3TJeunSpcsOuQUz27NldvRbBN3r0aMu4devWfh+rVatWlnGnTp38Phbg5JlnnvF6CQgDN27ccJxjd498okSJArQiBMO8efNcNWO2+0zjL9+Gem6bLzds2NBVI1VfBw4cUJGAKxoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAIRvMbhvoapd4felS5dEzK44dsmSJZZxiRIlxJzmzZuL2LPPPitiSZIkcWwaaNccxk2B0rlz50Rs0aJFrmK+xUcvvviicuP11193NQ9xw7Zt27xeAjxi17S0cuXKrhpb2TUwCyS78+nw4cODugZERlGw3TkxT548Imb3sIt27dppXh0CJdDnD7uGonXr1hUx34f27N69W8yZMWOG5tWFF65oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgXVRsbGysq4k2nTd1Onz4sGWcNm1aMefq1asiZlcYlixZMss4R44cfq/r3XfftYwHDBgg5ty8eVNFIpdbR4tA779QsWPHDhF79NFHXb02Xrx4jn8v7Ard4qpg7r9g7MHSpUtbxm+//baYU6lSJRHLnj17QLvlpk6d2jKuWrWqmDNy5EgRi46Odjy2XdF69erVRWzZsmUqLuIcGHzDhg1z9TCC9OnTi9iVK1dUOGH/+a979+4i1rdvXxE7fvy4ZVysWLGI7fDt7/7jigYAAAAA7Ug0AAAAAGhHogEAAABAOxINAAAAAOHbGfzIkSOOxeCJEiUSsUKFCjke+9tvvxWxn376ScTmzp0rYnv37rWMI7XwG3HDX3/9JWKPPPKIq9feunUrACuCLqNGjbKM8+fP7+p1b775poidP39e27p8C9Aff/xxv4sCly9fbhl/+umnIVP4jbjLbv9du3bNk7Ug7smaNauIvfzyy6720dixYy3jSC38vh9c0QAAAACgHYkGAAAAAO1INAAAAACEb41GmTJlLOOaNWuKOXb3Bh87dkzEPv/8c8v49OnTYg73byIU+d4vanj++ec9WQvihrZt23q9BNvz8IIFC0SsY8eOYd1ADd5IkSKFiNWoUUPE5syZE6QVIS5ZunSpq7qNKVOmiFjv3r0Dtq5IwRUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0i4p12WkpKipK/7sjpLlt0qUD++/OBWwLFy4Usccee8zxzzBXrlxizu7du1WoCOb+C8YeLFy4sGXcvn17Madp06YBXYPd//9Lly5Zxj///LOrhxRs3rxZhTvOgcF36NAhEUuVKpWIFSlSRMS2bdumwgn7z53u3buLWN++fUWsbt26IsYDBO5//3FFAwAAAIB2JBoAAAAAtCPRAAAAAKAdiQYAAAAA7SgGh98oRIOXwq0Y3FeiRIlErFmzZiL2/vvvOxbHzp0711W33Hnz5onYkSNHXK03EnEODL7p06e7evhF9erVRWzfvn0qnLD/4CWKwQEAAAB4hkQDAAAAgHYkGgAAAAC0I9EAAAAAoB3F4PAbhWjwUrgXgyPu4xwIL7H/4CWKwQEAAAB4hkQDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO2iYmNjY/UfFgAAAEAk44oGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0I5Ew8Fff/2l6tatqx555BGVNGlSFRMTo8qUKaMWLFjg9dIQIZYvX66ioqJs//n111+9Xh7CHOdAxAUbNmxQ1atXV6lTpzb3Yf78+dWIESO8XhYiwIULF1Tv3r1VlSpVzP1n/OydOHGi18sKGQm8XkBct2/fPnX+/HnVtGlTlSlTJnXp0iU1e/Zs84Q3ZswY1apVK6+XiAjRoUMHVaxYMUssR44cnq0HkYFzILy2ZMkS9fzzz6siRYqod955RyVPnlzt3r1bHThwwOulIQKcOHFC9enTR2XJkkUVKlTI/PIP7tFHww83b95URYsWVVeuXFHbtm3zejkIc8ZJ7emnn1YzZ85UderU8Xo5AOdABM25c+dUrly5VKlSpdSsWbNUvHjciIHgunr1qjp9+rTKkCGDWrdunfmF34QJE1SzZs28XlpI4G+sH+LHj68yZ86szpw54/VSEGGMb5Zv3Ljh9TIQ4TgHIli+/PJLdfToUdWvXz8zybh48aK6deuW18tCBEmUKJGZZMA/JBouGSc34/KZcbl26NCh6rvvvlMVKlTwelmIIM2bN1cpUqRQiRMnNq9wGN+sAMHCORBe+P77783z3sGDB1Xu3LnN26aMcdu2bc0ragDiNmo0XOrcubN5P7LB+FalVq1aatSoUV4vCxEgYcKEqnbt2qpq1apmIe6WLVvUoEGD1FNPPaVWrVpl3rcMBBrnQHhh586d5lXcGjVqqJYtW6oBAwaYt5OOHDnSvKI2bdo0r5cI4C6o0XDJuA/ZKDw7dOiQmjFjhvnh79NPP1Xp06f3emmIQLt27VIFCxY0n/6zaNEir5eDCMA5EF549NFH1Z49e1SbNm3M/XabMTYS3x07dqicOXN6ukZEDmo07h23TrmUJ08eVbFiRdWkSRO1cOFC83FnxlMwyNPgBeNpU8Y3fMuWLTMLc4FA4xwILyRJksT8d8OGDS3xF1980fz36tWrPVkXAHdINPxkPP1n7dq15rcpgBeMYtxr166Z984DwcY5EMFgPFLZ4HvlLF26dOa/jacBAYi7SDT8dPnyZfPfZ8+e9XopiFDG7QRGYbhRHAkEG+dABIPxGGWDUQz+X8YtfIa0adN6si4A7pBoODh27JiIXb9+XU2ePNm8pJs3b15P1oXIcfz4cRHbtGmTmj9/vqpcuTLPlUdAcQ6El+rVq2f+e/z48Zb4uHHjVIIECVS5cuU8WhkAN3jqlIPWrVubDYOMotuHHnpIHTlyRE2dOtUsjBw8eDDfJiPg6tevb36gMxpWGbcLGE+dGjt2rEqaNKn64IMPvF4ewhznQHjJeKpeixYt1Oeff24+faps2bLmU6eMBqbdu3f/99YqIJCMJ+wZTzm7fSVtwYIF/3amb9++vUqZMqXHK4y7eOqUg+nTp5vfpPz555/q5MmTKjo62ryUa2ys6tWre708RIARI0aYH+yMJ00ZH/iMWwWM/gW9e/c2i8KBQOIcCK8ZV9D69+9vPunH+KCXNWtW9eqrr6pOnTp5vTREiGzZsql9+/bZ/t7ff/9t/j7skWgAAAAA0I6buwEAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAAOBdZ/CoqCj9746QFswWLOw/+Ap2CyD2IHxxDoSX2H8Ihf3HFQ0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAAB410cDAAAgFOTKlUvEFi1aZBnHjx9fzMmaNWtA1wVEGq5oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHcXgAAAgZI0cOVLE6tevL2KpU6e2jBcuXBjQdQHgigYAAACAACDRAAAAAKAdiQYAAAAA7Ug0AAAAAGgXFRsbG+tqYlSUCid58+YVseeee07EWrVqZRmvXbtWzPn9999dveewYcMs42vXrqlQ5nLraBFu+w+htf8M7EH44hwYeOnTp7eMv/76azGnRIkSrv7fbN682TKuUKGCmHPy5EkVKth/CIX9xxUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAC0i4hi8NatW4vYoEGDRCx58uQBXUf58uUt42XLlqlQRiEavBQqxeB25xW7rsVXrlyxjIsWLSrmREdHi1ijRo1EbPny5ZbxwYMHlS5HjhwRsXnz5onYunXrVLjjHKhXrly5HH9WV61a1dWfzVtvveW4J/kZHLn7z+6/Z9q0aSLmu9/sHiR04MABFYliKQYHAAAA4BUSDQAAAADakWgAAAAA0C4iajRSp04tYlu3bhWxdOnSBXQdZ86ccbxPe8mSJSpUcH8ovBQqNRoDBw4UsS5duqhwcuvWLRHbsmWL4z3QdvdE7927V4UKzoF62TXeW7lypV9/No0bNxYxu/0Wyth//kuaNKmIbd++XcQeeuihuzZxNowbN05FolhqNAAAAAB4hUQDAAAAgHYkGgAAAAC0I9EAAAAAoF0CFQFOnTolYr179xaxwYMHOxYM7d+/X8zJkiWLq3U8+OCDlnGVKlVCuhgckSFr1qwiliRJEsu4YcOGYk7btm1dHf+bb76xjJs3b67CSa1atbQd6+TJkyL2xx9/aDu+XTFk7ty573oeMxQpUkTE8ufPL2L9+vVzXHsoFYNDb3O+L7/80q8iZLu/Y3ZNJIHbLl26JGI7d+50LAZPmzZtQNcVjriiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdhFRDG5n9OjRItamTRsRK1SokGV87tw5bWsYNWqUtmMB96pixYquiirtCr1TpkyprUOtXTfgcPLMM8+4KoTdsWOHXwWMhw8fVsEUHR0tYn/++adfD8moXr2648MBEJ5eeuklV3vm22+/dfw5ffDgQc2rQyT6+OOPRaxcuXKW8WOPPRbEFYUHrmgAAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAAKBdVKzLKk433TlDXZ06dUTs7bfftowLFy6s7f3sioq2bdumQsX9FADfq0jYfzqNGzdOxAoUKGAZFytWzO/jnz9/3jKeOnWqmLN27VoRmzZtmohduXIlzu8/A3vwzg8HsPv/b+fq1auW8VNPPSXmrFu3ToUKzoHurFq1SsTsfpYeOnRIxKpUqWIZ79q1S/PqQhf7T6/MmTOL2L59+yzja9euiTnZs2f3/CEdcXn/cUUDAAAAgHYkGgAAAAC0I9EAAAAAoF3ENuyzM2vWLBFbuXKlZbxkyRLHe9/dev/9913ViQC3pUmTRsQGDBggYi1atBCxU6dOWcbr168Xcz744AMR27x5s4hdvnzZMt6/f/9dVo1QkTBhQhEbMWKEZdykSRO/j1+yZEnLeOPGjX4fC3FXjRo1LOMnn3zS1f3dM2fO1FbDBQSiNsXuHGnXeHTMmDEBXVco4YoGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADaUQz+H40aNRKxQoUKWcb58+fX9n6+heaAk3feeUfEWrZsKWIjR450bD554cIFzatDKHn66adF7KWXXhKxZs2aOR7r+vXrItahQ4eQbkgKdx588EERs2vE6Mbp06dF7MCBA0qXjh07OjZos9OlSxdta0D4NaWzKxDH/+GKBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2kVEMXiePHlEbM6cOSKWI0cOEUuQIHB/RPPnzw/YsRG3JU2aVMS6devmWJzbqVMnMWfZsmUitnjxYhGjw27kKl68uIgtWbJExOLHj6+tYNKuW/zNmzf9Oj7iLrv/p0WLFrWM48WT32neunVLxH766Se/1vD666+7mte+fXvLOGvWrK5e17lzZxF7+OGHLeODBw+6OhYQabiiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdhFRDP7YY4+JWPbs2YNa+O22gM23WA3hqWfPnq6KwWfMmOFYwEuRN5zUq1dPW+G3286433zzjYitW7fOMl6wYIGrB3Vs3rz5vteIwChbtqxjZ3C7wm+7hwWcOHHC8f0KFy7s+H6G6tWrOx7r4sWLrjqR586dW8RmzZplGTdo0EDM2bdvn+MagHDHFQ0AAAAA2pFoAAAAANCORAMAAACAdhFRo2F3z++bb74pYh9++KGIJU6cOGDrypgxY8COjbite/furpqeTZs2zTKmHgP++Prrr13VrhUrVkzEYmJitK3jiSeeuOvY0Lt3bxEbNmyYiA0cONAyPnbsmJY14s6io6Nd1Tv6OnTokIh98cUXIrZr1y4Ry5Url2XctWtXMadGjRqu6j18a9wGDx4s5qRMmVLEfvzxR1fzEH6ioqIcf07j7riiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdhFRDG5nxIgRIrZz504Re/DBBx2PZdfob9SoUSKWIkWKe1ojwtdvv/0mYnaFsb776PLly2LO0qVLNa8O4WbVqlUiVq1aNRHLkiWLYzF4+vTpxZxatWqJWIsWLRwLK+3Eiye//3rjjTdErGjRopZxhQoVxBy7RnHwX+nSpUVs6NChjq/77LPPRKxPnz4iZre3Bg0aZBlXrVpVzDl//rxjs1NDly5dLOOcOXOKOaNHj3Z1/B9++MEypjlfeKL4+/5xRQMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO2iYl1Wurgp4otUdn827777roj16tXLMt69e7eYY1fQGFeLzIJZJBVX99+TTz4pYr///rtlfO3aNTEnderUItahQwcRe+eddyzjCxcuuFrDtm3bVLgLdpFeXN2DcVWjRo1ErH379pZx8eLFtb3fW2+95dg9XLdIOwd269ZNxPr16+fXA1Ps/PLLL67Ob25+bq5YsULESpQoYRmvXLnS1brsOtP7FpZ7IdL2X6BlzpzZr89fTz/9tKv9F27c7j+uaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoF3EdgbXKWHChI6F33auX78uYjdv3tS2LvgvY8aMIrZw4UJXnZRff/11y3jKlClizqlTp1x1k/ctBk+ePLmrwnLAa1OnThWxr776yjL+/vvvxZwyZcr49X45cuTw63Vw78EHH3RVJDxv3jzHYxUuXFjEsmXL5nj8zp07uyq8zZUrl4h9+eWXdz32nY5vVwwO3O3BPvg/XNEAAAAAoB2JBgAAAADtSDQAAAAAaEeNhgbvv/++X68bP368iB04cEDDinC/NmzYIGIpUqRw1cDKribDjY4dOzrOsbunffPmzX69HxBsN27csIzXr1+vrUZjx44dfq8Lept2+dtI7tatW47HKliwoJizf/9+EUucOLGI/f3335bxU089JeacPXvW9XoBOOOKBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2kXFuqzasmtsE0hp0qQRsQkTJojYtGnTXMUC2cht27ZtrgqHfT366KMitmfPHhUq/C3480ew91/37t1FrGfPniKWJEkSv46/c+dOEcuZM6eI7du3zzKuXbu2q8L1SBDM/efFHryfc9Irr7zieI6aMWOGCrb48eNbxosXLxZzypcv71dhud3rVq5cqQIpnM+BdkqUKOHXn3Hp0qVdNez74IMPRMyuSambP5sTJ06IWLNmzSzj7777ToWySNt/gZY5c2bHn8F27H52R0ITv1iX+48rGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAARE5n8BEjRojY888/L2K5cuUSsUOHDlnGBw8eFHN27dolYkWLFnU8/ptvvulX4bdh8ODBd10n4o4BAwaI2PXr10WsSJEiIlaxYkXH46dKlUrEvvnmGxHr0qWL475F5MiQIYOILVq0SMQKFCjguN8CLX369CL2xhtv+FX4bWfr1q1BLfyG/Tnw0qVLIpY0aVLL+JdffgloIfP58+ddPewg1Iu/ETdVrVpVxEaOHOnJWuIirmgAAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAABA5ncHtOpAOGTJExEqWLOl4rL1794rYli1bROypp54SsejoaMfj2/0R2nXiLVasmGV88eJFFcroSgovRWJn8OnTp4tYvXr1HF/3+OOPi9j27dtF7PLly47HSpIkiYjZPSTDt/Db7fnU7s/ZrtjX9+EgK1asUMHGOVCpatWqOf6/L1eunN9/dpMmTbKM//zzTzHn999/FzEv9kOwsf/0SpgwoYitX7/eMs6XL5+Y07Fjx4gsBo+lMzgAAAAAr5BoAAAAANCORAMAAABA5NRouGl4d6cGZp988okKplOnTolYmjRpVLjj/lB4KRJrNF555RURGzNmjF/Hsruv/ezZs46vS5kypavGlf66cOGCiL3wwgsi9sMPPyivcQ6El9h/gbd27VrHxs4LFy4UserVq6twF0uNBgAAAACvkGgAAAAA0I5EAwAAAIB2JBoAAAAAtEugQkjnzp1FLFGiRCKWPHlyx2PZFS82bNjQ8XV2xZKVKlVyfB0A3K+lS5e6auLXoEEDx2PpLOB268aNG5bxsGHDxJzZs2eL2Jo1awK6LgCws3HjRsdicDefOSMZVzQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAAIjszuCIW+hKCi9FYmdwO3YPxPDtpF2+fHkxZ8eOHX51s922bZurdf3444+Or/UttAw1nAPhJfZf4GXLls0ynjZtmpgzadIkERs9erQKd7F0BgcAAADgFRINAAAAANqRaAAAAADQjkQDAAAAgHYUg8NvFKLBSxSDw2ucA+El9h+8RDE4AAAAAM+QaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgXVRsbGys/sMCAAAAiGRc0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWi40KxZMxUVFXXHfw4ePOj1EhHG1q5dq1577TWVL18+lSxZMpUlSxZVr149tWPHDq+Xhgixc+dO1aBBA/Xwww+rpEmTqjx58qg+ffqoS5cueb00RIgNGzao6tWrq9SpU5t7MH/+/GrEiBFeLwsRYv369apKlSoqRYoUKjo6WlWuXFlt3LjR62WFBB5v68Lq1avV7t27LTHjj61NmzYqW7Zs6q+//vJsbQh/derUUb/88ouqW7euKliwoDpy5IgaNWqUunDhgvr111/NH7hAoPzzzz/mvkuZMqV5zjM+6BnnxIkTJ5of/ObNm+f1EhHmlixZop5//nlVpEgRVb9+fZU8eXLzZ/KtW7fUwIEDvV4eIiDJ/d///qcyZ86sWrdube67Tz75RJ06dUr99ttvKnfu3F4vMU4j0fDTypUr1VNPPaX69eunevTo4fVyEMZWrVqlnnjiCZUwYULLN8wFChQwk5ApU6Z4uj6Et/79+6u3335bbd682byqdlvTpk3V5MmTzR+2qVKl8nSNCF/nzp1TuXLlUqVKlVKzZs1S8eJxIwaCq1q1auaXK8bP3TRp0pixw4cPm/vSuLIxe/Zsr5cYp/E31k9ffvmledvUiy++6PVSEOaMH7D/TTIMOXPmND/0bd261bN1IXI+6BnSp09viWfMmNH80Oe7NwHdP2uPHj1qfqln7LeLFy+a3ygDwfLzzz+rihUr/ptk3D7/lS1bVi1cuNC8uwB3RqLhh+vXr6sZM2aYHwCNW6eAYDMuRBo/fGNiYrxeCsJcuXLlzH+3bNnSvCfZuJXqq6++Up9++qnq0KGDWTcEBMr3339v3hdv1EIat6gYt00Z47Zt26orV654vTxEgKtXr6okSZKIuFErdO3aNfNqL+6MRMMPixcvVidPnlSNGjXyeimIUFOnTjV/8Br3KwOBZBRA9u3bVy1dutS8R954GIFRGN6+fXs1dOhQr5eHMGfcrnLjxg1Vo0YN9cwzz5i3qbRo0UKNHj1aNW/e3OvlIQIYCa5RD3nz5s1/Y0aCsWbNGvPXPBDo7hI4/D7ucCn3gQceMJ/8AwTbtm3b1KuvvqpKlixp3icPBJpx5bZMmTKqdu3a5u0D33zzjVm7kSFDBvOJaECgGLelGE83Mx5EcPspU7Vq1TI/6I0ZM8Z8+plxKykQKO3atTOvoBlXdd98803z1r3333/frNMwXL582eslxmkkGn6c9IynrBjfrPz3fj0gGIwnThmFacYTgIzCyPjx43u9JIS56dOnq1atWpmPUzYeb3v7g57xw7Zbt26qYcOGnAsRMLdvWTH22X8Z9ZFGomEU6ZJoIJCMJNe4ZfSjjz5SkyZNMmPGA1qMpMOoHTJu58OdcevUPZo7d6757Qq3TSHYzp49q5599ll15swZtWjRIpUpUyavl4QIYDzG0bhl6naScZvxaFvjXPj77797tjaEv9vnOd+HEaRLl8789+nTpz1ZFyKLkVAYdZFGYfgff/xh9re6/VAC4+lTuDMSDT/ujTeyV+OHLBAsRtGj8Rx541tl4ykXefPm9XpJiBDGD9f/3pv834diGIz754FAKVq0qO198IcOHTL/nTZtWk/WhchjPMa7dOnS5qPlbz+owPgCxmhgijsj0bgHx48fNzfWCy+8YD5tAAgG40OeUfRt3CIwc+ZMszYDCBbj2zrjqoVvJ/pp06aZjxs1mvkBgXK7FnL8+PGW+Lhx41SCBAn+fSoaEEzGk/eMqxqdOnWit4sDajTucWMZ395x2xSCqXPnzmr+/PnmFQ2jOZpvg77GjRt7tjaEv65du6rvvvvObFBqFH4b9RjGVTUj9vLLL3MLHwLKuG3PeMrU559/bv78NXoXLF++3PzSpXv37uw/BNxPP/1kPnTAaM5nnP+MJ1BNmDDBfCJfx44dvV5enEdn8HtgfJO8Z88e85ItRbgIFuMbuxUrVtzx9/krjED77bff1Lvvvmte2TAe7Z09e3bziWdGMaTxrTIQSMZtesZTzowPd8bP36xZs5pP3jO+TQYCbffu3eaTpzZs2KDOnz//7/nvjTfeoGGpCyQaAAAAALTjxjIAAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABo57rTUlRUlP53R0gLZgsW9h98BbsFEHsQvjgHwkvsP4TC/uOKBgAAAADtSDQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0C6B/kMCAAB455FHHhGxAQMGWMYvvPCCmFOwYEER27Ztm+bVAZGDKxoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHMTgAAAhZpUqVErFFixaJ2PHjxy3jjz/+WMw5evSo5tUBkY0rGgAAAAC0I9EAAAAAoB2JBgAAAADtSDQAAAAAaEcxOOCBl156ScQqV64sYoULF7aMc+fO7er4v/76q4g9//zzlvHZs2ddHQsIpmTJkonY8uXLRSxTpkyW8f/+9z8xZ+/evZpXB69Vq1ZNxGbNmiVio0ePFrG3337bMr506ZLm1QHwxRUNAAAAANqRaAAAAADQjkQDAAAAgHZRsbGxsa4mRkXpf3eENJdbR4tQ2n8xMTGW8bhx4xzrJQxnzpwRsVWrVjm+X7ly5Vzd575t2zbLOG/evCqUBXP/hdoeDDbfeglD2rRpHV93+vRpEXv66adFbMKECSK2fft2y7h48eJizvnz51UgcQ4MvBw5cljGmzZtEnN+/vlnEatataqI3bp1S4UT9h9CYf9xRQMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1o2KdB586dRSxhwoQi9thjj1nGjRo1cnV83yJeQ758+e5pjQieRYsWWcbZsmUTcwYOHChiH330kYidOnXK8f3y5MkjYr/99puI5cqVyzLu1auXmNOnTx/H90N4yJ8/v4h16NBBxLJmzep4LN+9ZciSJYvj6z744AMRs3tIgV0h6sGDBx3PuQgtiRMnFjHfh2n8+eefYk69evXCvvAb3kidOrVlXL9+fTGnR48erh6Q4atnz54iNmDAABVuuKIBAAAAQDsSDQAAAADakWgAAAAA0I5EAwAAAIB2dAb/j7JlyzoWTNrNeeGFFwL652VX1LZr1y7PuzzTlVSpSpUqORaDz5gxQ8xp2LBhQNdlV9TtW3i2b98+MSd79uwqVNAZ/P7YFX4PHTrUr2NdvXpVxGbOnCli5cuXv+eCyTv92Tdp0sQynjJligo2zoF62T0Q47XXXrOMc+bMKeYcOHBARSL2n14lSpRwPCcWL148oP8fvvjiCxFr3ry5iovoDA4AAADAMyQaAAAAALQj0QAAAACgHYkGAAAAAO1CvjN4xowZRWzatGmW8SOPPOLqWClTphSxZMmSORZErV+/XsQef/xxpUu8ePEc1wVvJEiQwLFQf/r06SrYZs2a5VgMbteFN0WKFCJ27tw5zatDsL377rsi1rVrV1evnTRpkmV8/PhxMWfQoEEiZjevcOHClvHixYvFnJiYGFfHstvjCB2JEiUSscaNG4vY8uXLLeNILfyGXnbnmc8++0zEHnvsMcdz0dy5c0Vs3rx5jg+wqFu3rquC9IQJE4rYtWvXVKjgigYAAAAA7Ug0AAAAAGhHogEAAAAgsms0Klas6OqeusyZMwdsDXaN8U6cOOHq/j/f5lQTJkwQcx5++GFX69iyZYureQisZcuWiViRIkUs40uXLqlgs2ug5it9+vQi9uKLL4rY6NGjta0L3rCr6UqSJImI2TVxfPvtty3jw4cPu3rPHDlyiFiPHj0s47Rp04o5Fy9edFVjcuXKFVfrQNz05ptviljy5Mkd9x+gg10NhW89hmHJkiWWcdWqVf1+z507dzp+prX7DGi3rk2bNqlQwRUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAAiuxjcrnjM38Jvu2LZbt26idivv/5qGW/fvt3V8U+ePCliHTt29Kvwe+/evSL20ksvuXotAiuuFqTu2bNHxP766y/LOF++fGJOzpw5A7oueMOuuV2VKlVcPezigw8+sIzbtWvnqtnpkCFDRKxatWqW8alTp8Scfv36idinn34qYghtlStXFrFffvlFxDZs2BCkFSGSXL582e+i8UA6Z9Mg1+6BQ6GEKxoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAEROMbhdoViJEiX8Otb+/ftdFVPbFaLp5Lb4200xUqgXByGwrl+/LmI3btzwZC3w3saNGx0fdHGnYvDy5ctbxpUqVRJzhg4dKmJZsmRxXNd7770nYiNHjnR8HUJL6dKlXf08L1CggLb3LFeunIgdP378rg/IQOSIiopyFTt9+rRlnDhxYjHn0UcfFbFmzZqJWNGiRS3jI0eOiDkNGzYUsYMHD6pQxhUNAAAAANqRaAAAAADQjkQDAAAAgHYkGgAAAAAipxi8c+fOIpY0aVJXr121apVjwaHOwu9UqVK56rpbpkyZe1674dtvv72P1SESJUqUSMTsith8nT9/PkArgpeuXr3qqgOtnUyZMlnGs2fPdlVEGRsbK2Ljx4+3jOfOnetqDQhtjRs3FrGtW7eK2N9//+14LLsi28GDB7v6uez796BLly5izscff+y4BoS+fPnyuTpnvfHGG46fTX2LvO+kQYMGlvGsWbNUJOCKBgAAAADtSDQAAAAAaEeiAQAAACByajTGjh0rYjExMSJ29uxZEXvxxRcdm6Lo1KZNGxHr27ev4+vsmgXVq1dPxAK9foSfbNmyiVju3LkdX7do0SK/3s/u72ahQoVErGTJkiI2c+ZMy3j79u1+rQH3Zt++fQE9vl1t2aBBgyzjf/75J6BrQNzQokULx5/Td6olSpgwoWXcu3dvMad169YitnjxYhGrWrWqZTxhwgQxZ/fu3drOi4i7Tp48KWLR0dEi9sQTT/hVj3bp0iUR27Jli4pEXNEAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAACByisHtmkLZxYLt+eefF7FevXq5eu2NGzcs49GjR4s5FH7jXhvxPfzwwyJWqlQpv45vtyfXr18vYo8//rhlnDp1ajEnc+bMrhoC5siRw7EhF+5P/PjxReypp54SMbtCRze++eYbV+dKRGYztAQJEjj+PLwT33ONXWG228ZnX331lWVcunRpMad79+4iRjF4ZDTsK1GihOPPV989dCdff/21iG2hGBwAAAAA9CDRAAAAAKAdiQYAAAAA7Ug0AAAAAGgXFWvX0tBuop9FguHm5s2bIubyj1C1a9fOsft5KHH7361DXN1/SZIkEbF06dLdtZjxTkVn5cuXd3y/xIkTuypq07m/Dxw44Pi6iRMnuioQPnHihIjt3btXxfX9F5f3oBu+3dcNtWrV0nZ8u//X1atXV+GOc6C9ChUqWMZLly4Vc/LmzSti27Ztc+zW7Nsp/E5dnt2wW8Off/7p6mEKcQH7L/Dy589vGW/atMnV/we7vbVjxw4VTtzuP65oAAAAANCORAMAAACAdiQaAAAAALQj0QAAAAAQOZ3B44r+/ftbxvHiydzs1q1bro61YsUKbetC8Iu83333XVfdj/PkyaNtHefOnXPsrG3XYdeuE6+vcePGueoMvmHDBhcrhVcyZcokYs2bN7eMa9eu7aqQz+7/tW/xo++x7R6AADg5ePCgq3l25zxd3DzoApGtQIEC2j4DRiquaAAAAADQjkQDAAAAgHYkGgAAAAC0o0bDoRFQkSJFHO/Fs7vXuWPHjiK2c+fO+14jgmPu3LkiVqlSJRG7evWqY/Oyv//+W8yZN2+eq2P5NrOzu6fYrslVrly5RGzPnj2W8RtvvCHmXLhwQcQQWs3RDH369HF8Xc+ePUVs1KhRIlazZk3HGo0tW7a4WCkihW9zt7ja7K1s2bJBrQlB6Ll8+bLjZ8Dly5eL2LVr1wK6rlDCFQ0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALSL2GLwpEmTiljjxo1dFQD7mjZtmohNnTpVxGjqEjoqV64sYnZF3bVq1RKxjRs3aluHb+O9Dz/8UMx56KGHROzYsWMiVq9ePcuYwu/QU65cOREbMWKE4+uqV68uYt9//72IZciQQcR69erleHzfhxYgsvk+IMXugSleeOCBByzjNm3aiDlffPFFEFeEuMSu2W7Lli0t4+PHj4s5n376qYhxTvw/XNEAAAAAoB2JBgAAAADtSDQAAAAAaEeiAQAAAEC7iCgGj46OFrHPPvtMxOrUqeN4rNdff91VN10Kv0ObXfHimTNnRGzz5s3a3jNx4sQiNnPmTMu4WrVqrjqKN2jQQMQ2bNhw32uEt+weTpEyZUoRW7FihWW8cOFCx8JYw3PPPed4fLsuz3YFkohcvp3iDx8+7OrhK3ZFtf6y29++x8+WLZuY07RpU21rQNxld95cvHix48NWunXrJubMmjVL8+rCC1c0AAAAAGhHogEAAABAOxINAAAAANqRaAAAAADQLiKKwe06J7sp/Dbs3r37nrvwIvTt2LFDxAoXLixiY8eOFbE0adJYxps2bRJz9uzZI2Jdu3YVsdy5c1vGa9asEXPatm0b0O7kiDvsHjJh9+AC35hdYWzNmjVFbPjw4SJ2+vRpy3jcuHEBLeJF6PMt/u7fv7+YM3jwYFfHmjp1qmX8yCOPiDmFChUSsR49eojYlStXLOPKlSuLOSdOnHC1LoS2gQMHuvqsOG3aNL/2Lf4PVzQAAAAAaEeiAQAAAEA7Eg0AAAAA2oVljUaePHks486dO/t9X/6zzz6rbV0I3T1k6Nu3r4h16dJFxOLFs+bvVapUcfWe8+fPFzHfvbto0SJXx0J4Spcunat5vg30li5dKuY89dRTro7VvHlzy3jBggWuXgfc9vHHH7uaZ3f/u11DXF/nz58XMbt6yvfff98yvnbtmqt1IbRVrFjRVcPIy5cvixjN+O4fVzQAAAAAaEeiAQAAAEA7Eg0AAAAA2pFoAAAAANAuKtau25PdxKgoFSp8G/zUr1/f1evat28vYjSiujOXW0eLUNp/CL/9F1f2YKdOnUTMTQMpu7WfOnXKVdHuBx984FgwGak4B8JL7D972bJls4zXr18v5iROnNhVgficOXM0ry7y9h9XNAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0C7kO4Pny5dPxFKkSOH4urFjx4rYjz/+qG1dAKDbpEmTRCxhwoQi9s4771jG69atc9WJfujQofe9RgAIliRJkohY586dLeOUKVOKObNnzxYxCr8DgysaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoF/KdwT/88EPHQqB9+/aJOVWrVhWx7du3a15deKMrKbwUiZ3BEbdwDoSX2H9KtW3bVsRGjRplGa9atUrMqVixoohdvXpV8+rCG53BAQAAAHiGRAMAAACAdiQaAAAAALQL+RqNChUqiNjixYst49q1a4s58+bNC+i6IgH3h8JL1GjAa5wD4aVI23/Fixd31Xjv888/t4w/++wzMefAgQOaVxd5YqnRAAAAAOAVEg0AAAAA2pFoAAAAANCORAMAAACAdiFfDA7vRFohGuIWisHhNc6B8BL7D16iGBwAAACAZ0g0AAAAAGhHogEAAABAOxINAAAAAN4VgwMAAACAW1zRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAABAOxINP/Tr18/skpk/f36vl4IIcfXqVdWtWzeVKVMmlSRJEvXkk0+qpUuXer0sRIj169erKlWqqBQpUqjo6GhVuXJltXHjRq+XhQhx4cIF1bt3b3MPpk6d2vz5O3HiRK+XhQjB/rs/JBr36MCBA6p///4qWbJkXi8FEaRZs2ZqyJAhqlGjRmr48OEqfvz4qmrVqmrlypVeLw1hbsOGDap06dJqz5495g/bXr16qZ07d6qyZcuq7du3e708RIATJ06oPn36qK1bt6pChQp5vRxEGPbf/eHxtveoQYMG6vjx4+rmzZvm5tu8ebPXS0KY++2338wrGB999JHq0qWLGbty5Yp5RS1dunRq1apVXi8RYaxatWpq9erVZnKRJk0aM3b48GGVK1cu88rG7NmzvV4iIuCK7unTp1WGDBnUunXrVLFixdSECRPML2CAQGP/3R+uaNyDn376Sc2aNUsNGzbM66Ugghh7zriC0apVq39jiRMnVi1btjQ/AP7zzz+erg/h7eeff1YVK1b8N8kwZMyY0byisXDhQvO2AiCQEiVKZH7IA7zA/rs/JBouGVcw2rdvr15++WVVoEABr5eDCPL777+b3x4b98f/V/Hixc1/c688Av1tnlEX5Ctp0qTq2rVrXNUFANxRgjv/Fv5r9OjRat++fer777/3eimIMMZtKsY3yL5uxw4dOuTBqhApcufOrX799VfzyxbjyprBSDDWrFlj/vrgwYMerxAAEFdxRcOFkydPmgWQ77zzjkqbNq3Xy0GEuXz5snnp1pdx+9Tt3wcCpV27dmrHjh3mrXpbtmwxr2A0adLETIAN7D8AwJ2QaLjQs2dP85Fmxq1TQLAZt60Yt6/4MgrCb/8+ECht2rRRPXr0UF9++aXKly+feevo7t271Ztvvmn+fvLkyb1eIgAgjiLRcGA8aWXs2LGqQ4cO5i0qe/fuNf8xPuRdv37d/PWpU6e8XibCmHGL1O1vj//rdszorQEEunfQ0aNHzcLwP/74Q61du1bdunXL/D2jfggAADskGg6M+4+NH6hGopE9e/Z//zHuTzZuJzB+bTxfGQiUwoULm3vt3Llzlvjte+SN3wcCLVWqVGY/jdsPwzDq1R5++GGVJ08er5cGAIijKAZ3YPQqmDNnju3tVOfPnzebpz366KOerA2RoU6dOmrQoEHmlbXbfTSMW6mM53gb/TUyZ87s9RIRYb766ivzqoaxL+PF4/sqAIA9Eg0HMTExqmbNmiJ+u5eG3e8BOhnJRN26dVX37t3VsWPHVI4cOdSkSZPM2/bGjx/v9fIQAf2DjKu2RnM+o5eG8QQqI8mtUqWK6tixo9fLQ4QYNWqUOnPmzL9P2VuwYIE6cOCA+WujfjJlypQerxDhjP3nPzqD+6lcuXJ0BkfQGDVBxlPPpkyZYnYoLViwoOrbt6965plnvF4awpxR+G08eWrDhg3mVVzjdtGmTZuqN954QyVMmNDr5SFCZMuWzXzEvJ2///7b/H0gUNh//iPRAAAAAKAdN9cCAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAADAu87gUVFR+t8dIS2YLVjYf/AV7BZA7EH44hwIL7H/EAr7jysaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0I5EAwAAAIB2JBoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAABAuwT6DwkAAACEv2nTpolYiRIlRKxBgwaW8Zo1a1Qk4IoGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAADaUQweRLly5bKMR48eLeY0atRIxA4fPhzQdSEylCtXzjL+4YcfxJx48eI5vs6wYsUKzasDACD0ZM2aVcSyZcsmYlOmTLGM8+bNK+Zcv35dhRuuaAAAAADQjkQDAAAAgHYkGgAAAAC0I9EAAAAAEHrF4NHR0SKWPHlyETt79qxlfOnSJRVuqlatahmXKVNGzHn55ZdFbMCAASJ248YNzatDOGnWrJmItW/f3jK+deuWq2MNGTJExCZPnmwZf/zxx2IOexRAXNa9e3cR69evn4gNHDhQxN56662ArQtxV+bMmUXsiSeecPXaHDlyWMYJEsiP4BSDAwAAAIALJBoAAAAAtCPRAAAAAKBdVGxsbKyriVFRfr1B3759Xd0X2bVrV8t46NChKtyULl3aMl6+fLmr1+XJk0fEdu3apbzmcuto4e/+i9R6jJdeeknE7GqC3DTsc1PL4XvvqWHfvn0qXPafgT14bw2rXn/9dRFr166d4z3K06dPF7EXX3xRxUWcA0OLb83o9u3bxZz06dO7um/+1VdftYzHjx+vgo39F3z58+cXsT///NPVa+fOnWsZ165dW8xxWzsZF7jdf1zRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAAAg9Br2udW7d2/LeM+ePWLOvHnzVCjLkCGD10tAHPbggw+KWOHChS3jCRMmiDkxMTEiljhxYsf327Ztm6ti8Fy5cjkeC5GjefPmIjZs2DAR27lzp4i1bt3asfmV788CQ58+fVztX+BuDxpo27atY+G3naNHj4rY6tWr72N1CNV9ZPcwI7e+/PLLkC38vh9c0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAIHyLwZMnT+5Y9Fq5cmURW7dunYqLfP97DG+88YZfx6pbt66IDRgwwK9jIW6oWbOmiL3yyiuOe97fzt12PvroIxGzO/5nn33m1/ERehImTChinTt3tox79eol5gwZMsTV/jpz5oxl/Pjjj7sqBj9//vxdVg1IJUqU0PZzs02bNiK2ZcsWv46F0DJ06FDL+MUXX/RsLaGKKxoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAIReMfjevXv9el2KFClE7L333hOxxo0bi9jp06eV13LkyCFixYsX92Qt8JbdHp00aZJfx7Ir1vZXVFRU0N8Todf1+/3337eMO3XqJOaMHDnSr/eze8DHsWPHROzgwYN+HR+RIVu2bCI2YsQIv471ww8/iNjy5cv9OhZCi90DWVq2bOnJWsIJnyAAAAAAaEeiAQAAAEA7Eg0AAAAAoVejMXHiRBHLlCmTqyZNvp555hkRq127toiNGzdOec3uPuM9e/ZYxo888oirY82cOVPbuhD8moxhw4a5arJ35coVETt69KhlHB0dLeakTp3a1bp8j3/u3DkxJ2XKlK7WitBnt2/69u0rYrNmzbKMP/30U7/fM2vWrJbxyy+/7PexgNsWLFggYnnz5nV8nd050K7R5OXLl+9jdQiVerRRo0Y5NjHdsGGDmGPXeBT/hysaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAACEXjH4zZs3XTXSadSokWPDOzuvvvqqiM2ZM8cyPnnypAq2dOnSiZjb4m+Ejpo1azo243NbTL1mzRoRq1ixomXcrFkzMeezzz5zdfwePXrc9e/JnY6P0JcggTzV//LLL44PHzC0bdvWMr5x44bf65gyZYrjOXHw4MF+Hx+RKV++fCIWGxvr+LpPPvlExJYuXaptXfBf8uTJRaxQoUIilitXLhF78sknLeN69eqJOalSpXK1jg4dOljG3377rZiza9cuV8eKVFzRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAAAg9IrB7Zw9e9axMNFtMXiBAgVELHPmzNqKwX27QrZu3drV6+rWrev3eyJusiuUtuv67abjt13ht2/RmVubNm1yLEh329HZtwu04ZVXXhGx4sWL39Ma4a06deq4KqIsX768iJ06dcqv92zYsKGIlShRwjK+cOGCmDNo0CC/3g+RYciQISIWFRXlqhj8hx9+sIz79u2reXXQ5eGHHxaxzz//3NV5zM1nTruHqAwcOFDE9u7d67gu3B1XNAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAACI9icDurV6+2jJs2ber3sUqWLGkZb9y4UcwpVaqUq5hvd8qePXuqQNq6dauInT59OqDvCXfeeecdEUuWLJnj6/r37y9iAwYM8GsNK1euFLHvvvvOVYdnN+yKc69everXsRB32J1Pt2/fLmKrVq3y6/gZMmRw9aCEePGs322NHDlS295FePr4448t45o1a7oq/P7jjz9ErFGjRo4P6kDcsG3bNhErWLCgiOXMmdPxWOfOnROx/fv3q2BL5uLzQjjiigYAAAAA7Ug0AAAAAGhHogEAAAAgfGs0xo0bZxmXLVtWzHnxxRddHWvUqFF3Hd8L33uKb926pQIpb968ImZ3T+r48eMDuo5IV7hwYRGLjo523B+G+PHjB2xdu3btUsFm1wzL7r8bcdczzzwjYr169RKx69evOx4rRYoUIjZ79mwRi4mJEbHRo0dbxh9++KHj+yFy2DUC9f35Z1cPZGfs2LEidvz48ftYHbxmVy+4efPmoK7h/PnzInbkyBERs9unNWrUsIwnTpyoIgGfFgAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAACN9icF+DBw8WsYYNGwZ9Hb7F33aNgQKtRIkSIkYxuF758+d3LG5NlSqViAX64QDB5tug0pAwYcKw/+8ONxUqVHCcM3fuXL8KyceMGSPmZMmSxdWDC3r06OHYSAuRq0WLFiKWMWNGvxrdzps3T9u6gNtOnjwpYn///berYvBly5apSMQVDQAAAADakWgAAAAA0I5EAwAAAIB2JBoAAAAAIqcYPK7wLWi0Kwb/5ptvROzs2bOuOvEibhgxYoRjcWskqFOnjqtuvYjbjh49ahlfuXJFzJkxY4aIRUdHi1jatGkdu/PadY//+OOPXZ0XEZk6deokYi1bthQxNw9gqVSpkogdOnToPlYH6Hf48GEVibiiAQAAAEA7Eg0AAAAA2pFoAAAAANCORAMAAACAdhFRDH7q1CkR279/v6tu5NOmTfPrPQsXLixiFIOHnzfffFOFqjx58ojYwIEDXb127969jsXG8M7mzZst4zZt2rgqvN20aZPjOXDUqFFizrp160TMroM4IlPmzJld7b948eR3nzdv3rSMP/vsMzGHwm/ENXYPMTh27JiKRFzRAAAAAKAdiQYAAAAA7Ug0AAAAAEROjcaePXtEbPLkySL2yCOPiNjWrVsdG0f53sMcl1WuXFnEUqVKZRmfPn06iCvCbSdPnlShWpMxb948MSdNmjSu7iv1bezn2yAOcYvdudMuZtd4b9iwYZZx+vTpxZxatWqJGHU7kStHjhyW8fz588Wc3LlzuzrW0KFDLeNu3brd5+oQ6fvRkDp1alevvXTpkmPN75AhQ1zVO6b1aX7qOzYkTZpUxN5//30RmzlzpuPfsbiCKxoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAEROMfi5c+dErEWLFioSPfTQQyKWMGFCT9YSrnyLYO0aR9mZMGGCqyLbQEqePLmrNdSoUcOvhzA899xzIrZ9+/Z7WiNCQ9myZUXstddes4z79evnqmEfIpdvobfbwm87cbnIFcFl97nH7oFArVq1soxbt27tqujazrVr1yzjCxcu+F1YPtOngPv48eOu/htTpkwpYkeOHAmZvydc0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAIHKKwUPdmTNnROzw4cOWccaMGf0+fv/+/R2LnW7cuOH38SONb+fNr776ylVBlp1ly5ZZxrGxsWKOXVduuwLrN99807Fzs13xWPHixR07nPruIcPXX3/tal0IT19++aWIHTp0yLHjLeBPcayv5cuXi9iWLVs0rAihJn369CI2fPhwEatfv7629/T9jGb38/uvv/4SczZt2qSCbdKkSSpUcEUDAAAAgHYkGgAAAAC0I9EAAAAAoB2JBgAAAADtomLtKlXtJtoUoeLePPnkk46Ft3YFUG7YFSpfvHhRBZLLraNFsPefXYfk2bNnu/pz9+0qfuvWLW3rsutYbnf8FStWOHYLD3YH81Def+F4DnziiSdEbNWqVSLWoUMHy3j06NEBXVcoCedz4P3Yu3evZZw5c2ZXr7Mr7J01a5a2dYWbcN5/r7/+uogNGTLEr2MtXLhQxAYPHixiv/zyi4hdv37dr/eMBLEu9x9XNAAAAABoR6IBAAAAQDsSDQAAAADaUaMRx+6RtruXMCYmxvFYFSpUcHWfvk7hfH+onYceekjEWrVqJWI9e/YMWI3GsWPHROznn38WMbsGjmfPnlXhhBoN9xInTixidvUYqVKlErH8+fMHtfYrlETaOdBOvnz5HBvv2TXwe++990Ssb9++nv89DyXhvP+yZcsmYvPnz3dsKGrXcHfChAmaVwcDNRoAAAAAPEOiAQAAAEA7Eg0AAAAA2pFoAAAAANAugf5Dwq1169a5alLTtWtXEfvmm28cjwW9Dh48KGK9e/cWsT179ljGXbp0EXPy5MkjYtu2bROxjz76yDLevXu3qyZDwH81b95cxAoVKuQqRvE37qZEiRIiFh0d7fi6q1evihiF37hT00dDwYIFPVkL7g9XNAAAAABoR6IBAAAAQDsSDQAAAADakWgAAAAA0I7O4PBbOHclRdxHZ3D3tmzZ4qoYt1ixYiJ248aNgK0r1HEOtLdv3z7LOGnSpGJOpUqVRGzjxo0BXVe4Yf/BS3QGBwAAAOAZEg0AAAAA2pFoAAAAANCORAMAAACAdnQGB4Awlzp1ahF77733RIzCb+iQNWtWr5cAII7gigYAAAAA7Ug0AAAAAGhHogEAAABAOxr2wW80C4KXaNgHr3EOhJfYf/ASDfsAAAAAeIZEAwAAAIB2JBoAAAAAtCPRAAAAAKAdiQYAAAAA7Ug0AAAAAGhHogEAAABAOxINAAAAANqRaAAAAADwrjM4AAAAALjFFQ0AAAAA2pFoAAAAANCORAMAAACAdiQaAAAAALQj0QAAAACgHYkGAAAAAO1INAAAAABoR6IBAAAAQDsSDQAAAABKt/8HosYei/bsGrkAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 1000x1000 with 25 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(10, 10))\n",
    "for i in range(25):\n",
    "    plt.subplot(5, 5, i + 1)\n",
    "    plt.imshow(X_train[i].reshape(28, 28), cmap=\"gray\")\n",
    "    plt.title(str(y_train[i]))\n",
    "    plt.axis(\"off\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "9ed7e48a-c420-4b7e-a201-38e9d0cb63b0",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "F:\\College\\PRML\\prmlvenv\\lib\\site-packages\\sklearn\\neural_network\\_multilayer_perceptron.py:691: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (10) reached and the optimization hasn't converged yet.\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-2 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: #000;\n",
       "  --sklearn-color-text-muted: #666;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-2 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-2 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-2 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: flex;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "  align-items: start;\n",
       "  justify-content: space-between;\n",
       "  gap: 0.5em;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label .caption {\n",
       "  font-size: 0.6rem;\n",
       "  font-weight: lighter;\n",
       "  color: var(--sklearn-color-text-muted);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-2 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-2 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-2 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-2 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-2 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-2 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-2 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-2 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-2 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 0.5em;\n",
       "  text-align: center;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-2 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-2 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-2\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>MLPClassifier(max_iter=10, random_state=42)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-2\" type=\"checkbox\" checked><label for=\"sk-estimator-id-2\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow\"><div><div>MLPClassifier</div></div><div><a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.6/modules/generated/sklearn.neural_network.MLPClassifier.html\">?<span>Documentation for MLPClassifier</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></div></label><div class=\"sk-toggleable__content fitted\"><pre>MLPClassifier(max_iter=10, random_state=42)</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "MLPClassifier(max_iter=10, random_state=42)"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = MLPClassifier(hidden_layer_sizes=(64,), max_iter=10, random_state=42)\n",
    "model.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "ef8b10dd-3062-4b19-b038-436ea060fc95",
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred = model.predict(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "ad72619a-f76b-4164-87a2-1d19d026c372",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy : 0.9736\n",
      "Classification Report: \n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.98      0.99      0.98       980\n",
      "           1       0.99      0.99      0.99      1135\n",
      "           2       0.98      0.97      0.97      1032\n",
      "           3       0.97      0.97      0.97      1010\n",
      "           4       0.98      0.97      0.97       982\n",
      "           5       0.99      0.95      0.97       892\n",
      "           6       0.97      0.98      0.97       958\n",
      "           7       0.97      0.97      0.97      1028\n",
      "           8       0.96      0.97      0.97       974\n",
      "           9       0.96      0.97      0.96      1009\n",
      "\n",
      "    accuracy                           0.97     10000\n",
      "   macro avg       0.97      0.97      0.97     10000\n",
      "weighted avg       0.97      0.97      0.97     10000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(f\"Accuracy : {accuracy_score(y_test, y_pred)}\")\n",
    "print(f\"Classification Report: \\n{classification_report(y_test, y_pred)}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "7d437451-4e6e-4e46-b496-861fcbfa4ee4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAxUAAAIjCAYAAAB1STYOAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjkuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8ekN5oAAAACXBIWXMAAA9hAAAPYQGoP6dpAACReElEQVR4nO3dB1gUVxcG4E+QIqgINrBXwC527L1Gxd41aozGEks0BhuxYos19t4Va+wldmPvDXtXBFRAkSaw/3OvP5tdNInr0nbme/NMYArDDDvuzplz7r2pNBqNBkRERERERF/J7Gt/kIiIiIiISGBQQURERERERmFQQURERERERmFQQURERERERmFQQURERERERmFQQURERERERmFQQURERERERmFQQURERERERmFQQURERERERmFQQUT0GXfv3kXdunVhZ2eHVKlSYdu2bQm6/0ePHsn9Ll++PEH3a8qqV68uJyIiMj0MKogoxbp//z569uyJfPnywdraGunTp0elSpUwc+ZMhIeHJ+rv7tKlC65du4bx48dj1apVKFOmDJTi22+/lQGN+Ht+7u8oAiqxXkxTp041eP8vXrzAr7/+isuXLyfQERMRUUqXOrkPgIjoc3bt2oVWrVrBysoKnTt3RtGiRREVFYUTJ05gyJAhuHHjBhYuXJgov1vcaJ86dQrDhw9H3759E+V35M6dW/4eCwsLJIfUqVMjLCwMO3bsQOvWrfXWrVmzRgZxERERX7VvEVSMHj0aefLkQcmSJb/45/bv3/9Vv4+IiJIfgwoiSnEePnyItm3byhvvQ4cOwcnJSbuuT58+uHfvngw6EktgYKD8miFDhkT7HSILIG7ck4sI1kTWZ926dZ8EFWvXrkWjRo2wefPmJDkWEdzY2NjA0tIySX4fERElPJY/EVGKM3nyZISGhmLJkiV6AUWcAgUKoH///tr56OhojB07Fvnz55c3y+IJ+bBhwxAZGan3c2L5N998I7Md5cqVkzf1orRq5cqV2m1E2Y4IZgSRERE3/+Ln4sqG4r7XJX5GbKfrwIEDqFy5sgxM0qZNCxcXF3lM/9WmQgRRVapUga2trfzZpk2bwtfX97O/TwRX4pjEdqLtR9euXeUN+pdq37499uzZg+DgYO2yc+fOyfInsS6+N2/eYPDgwShWrJg8J1E+1aBBA1y5ckW7zZEjR1C2bFn5vTie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qC0aVIvGyD/++COePXsmt+nfvz8mTpyIbdu24datW/IG/N/GmBDjQnTp0gXdunWTPxO3Tx8fH7le9Ewlen0SpVqBgYHySb/IEIiMwcCBA7FixQp5Y3/x4kXMnj1bzguix6W7d+9iyJAhspH32rVrZQPyL/H8+XNZlqU7BQUFyUbVosH3vn37cOfOHYwcORLnzp375OdFKZPoJermzZuyByovLy/07dsXZmZmX3TsRESkPAwqiIj+T7QTED0V5cqVS/asJLIB4uZZtKmIy1yIHpY6deokA4W4EqFmzZr9635FCVbLli1lAOLq6ooePXrg/fv3cp0oERLds/7yyy/ImjWrvDkXxOB54qZe9KQkjkP0QCVKikQ3rYI4RtFzlAhURBsH0dPShAkTvug8p06dKts36E5i3z179pTn3aZNG9leQ/SUpZu1iFOrVi0ZgIhsjdi2SZMmem1V/uvYiYhIeVKJ1trJfRBERERERGS6mKkgIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiKjMKggIiIiIiIY4392+zZp2RclvgAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 1000x600 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "cm = confusion_matrix(y_test, y_pred)\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\")\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.xlabel(\"Predicted Label\")\n",
    "plt.ylabel(\"True Label\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6169b99a-67f7-4f5d-8ede-b1f98217d5e9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}    
    '''
    
    def dnn(self):
        return r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fbc505a2-585d-4832-a086-1f5272eb7bbf",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "import pickle\n",
    "\n",
    "from sklearn.metrics import confusion_matrix\n",
    "import tensorflow as tf\n",
    "from tensorflow import keras\n",
    "from tensorflow.keras import layers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "2fe62058-5982-41a9-8994-0702d32b5802",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_cifar10_batch(filename):\n",
    "    with open(filename, 'rb') as f:\n",
    "        batch = pickle.load(f, encoding='bytes')\n",
    "        data = batch[b'data']\n",
    "        labels = np.array(batch[b'labels'])\n",
    "        return data, labels\n",
    "\n",
    "def load_cifar10_data():\n",
    "    x_train, y_train = [], []\n",
    "    for i in range(1, 6):\n",
    "        data, labels = load_cifar10_batch(f'../datasets/cifar-10-python/cifar-10-batches-py/data_batch_{i}')\n",
    "        x_train.append(data)\n",
    "        y_train.append(labels)\n",
    "\n",
    "    x_train = np.concatenate(x_train)\n",
    "    y_train = np.concatenate(y_train)\n",
    "\n",
    "    x_test, y_test = load_cifar10_batch(f'../datasets/cifar-10-python/cifar-10-batches-py/test_batch')\n",
    "\n",
    "    return x_train, y_train, x_test, y_test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "d63dd40e-9fae-40ff-9b36-d4711397415f",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, y_train, X_test, y_test = load_cifar10_data()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "c7c45223-e4bb-4297-93b9-884aa8ec9c0b",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train = X_train.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)\n",
    "X_test = X_test.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "c9194805-302e-461f-beeb-ed2cabe68b71",
   "metadata": {},
   "outputs": [],
   "source": [
    "y_train = keras.utils.to_categorical(y_train, 10)\n",
    "y_test = keras.utils.to_categorical(y_test, 10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "af39e5ba-2faf-4611-9424-e6019e7b2217",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1000x1000 with 25 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(10,10))\n",
    "for i in range(25):\n",
    "    plt.subplot(5,5,i+1)\n",
    "    plt.xticks([])\n",
    "    plt.yticks([])\n",
    "    plt.imshow(X_train[i])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "9c595cba-7f9d-4f98-a612-a099214af2f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "model = keras.Sequential([\n",
    "    layers.Conv2D(32, (3,3), input_shape=(32, 32, 3), activation=\"relu\"),\n",
    "    layers.MaxPooling2D((2,2)),\n",
    "    layers.Conv2D(64, (3,3), activation=\"relu\"),\n",
    "    layers.MaxPooling2D((2,2)),\n",
    "    layers.Conv2D(64, (3,3), activation=\"relu\"),\n",
    "    layers.Flatten(),\n",
    "    layers.Dense(64, activation=\"relu\"),\n",
    "    layers.Dense(10, activation=\"softmax\"),\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "027f062e-70e5-4fd4-9be6-65abda5650b4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m15s\u001b[0m 17ms/step - accuracy: 0.2691 - loss: 3.1106 - val_accuracy: 0.4212 - val_loss: 1.6742\n",
      "Epoch 2/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 17ms/step - accuracy: 0.4908 - loss: 1.4145 - val_accuracy: 0.5403 - val_loss: 1.2965\n",
      "Epoch 3/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 16ms/step - accuracy: 0.5650 - loss: 1.2241 - val_accuracy: 0.5810 - val_loss: 1.1730\n",
      "Epoch 4/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 16ms/step - accuracy: 0.6164 - loss: 1.0888 - val_accuracy: 0.5991 - val_loss: 1.1395\n",
      "Epoch 5/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 16ms/step - accuracy: 0.6570 - loss: 0.9798 - val_accuracy: 0.6289 - val_loss: 1.0797\n",
      "Epoch 6/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 16ms/step - accuracy: 0.6814 - loss: 0.9150 - val_accuracy: 0.6303 - val_loss: 1.0723\n",
      "Epoch 7/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 17ms/step - accuracy: 0.7110 - loss: 0.8285 - val_accuracy: 0.6489 - val_loss: 1.0383\n",
      "Epoch 8/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 17ms/step - accuracy: 0.7336 - loss: 0.7710 - val_accuracy: 0.6603 - val_loss: 1.0724\n",
      "Epoch 9/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 17ms/step - accuracy: 0.7489 - loss: 0.7235 - val_accuracy: 0.6612 - val_loss: 1.0238\n",
      "Epoch 10/10\n",
      "\u001b[1m782/782\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m13s\u001b[0m 16ms/step - accuracy: 0.7623 - loss: 0.6744 - val_accuracy: 0.6552 - val_loss: 1.0774\n"
     ]
    }
   ],
   "source": [
    "model.compile(optimizer=\"adam\",\n",
    "              loss=\"categorical_crossentropy\",\n",
    "              metrics=[\"accuracy\"])\n",
    "\n",
    "history = model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "69993be0-0694-4c5d-8436-e66d6121875f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m313/313\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m1s\u001b[0m 4ms/step\n"
     ]
    },
    {
     "data": {
      "image/png": "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xGratGnIkyePDEDEvB2i5KpZs2ZymwIFCqB+/fro3r27HDo3PDwc/fr1k1mThI5QJTDgICIiIiJSJkaESuOWLFkiA4g+ffrIsigRIPTs2VNO9BdjxIgRCAoKkvNqiExG5cqV5TC46dOnV2wj+oGIIKNWrVoyY9KyZUs5d0dipItSnm5QQ+QZfhza6N70etBGn4LCoY3MjLXzekE6pN66WnWKgsYdqhNENxGz6mqSfysetM57vxBoI+sMBtBG1qap93vMqPZMpFYhp0chrUn74RsREREREaVaqTe0JCIiIiJKCal4lKq0iBkOIiIiIiJSGwYcRERERESkNiypIiIiIiLSsFGqUhP+NYmIiIiISG0YcBARERERkdqwpIqIiIiISBlHqUpSzHAQEREREZHaMOAgIiIiIiK1YUkVEREREZEyjlKVpPjXJCIiIiIitWHAQUREREREasOSKiIiIiIiZRylKkkxw0FERERERGrDgIOIiIiIiNSGJVVERERERMo4SlWS4l+TiIiIiIjUhgEHERERERGpDUuqiIiIiIiUcZSqJMUMBxERERERqY1GZjhuT60LbWTdajW0ke/O7tBKWnrxRUdLrzpFRqX0HlBy0tXRzs+5pak+tFFAcDi0kbWpRp6GUjz4ThMRERERKeMoVUmKf00iIiIiIlIbBhxERERERKQ2LKkiIiIiIlLGkqokxb8mERERERGpDQMOIiIiIiJSG5ZUEREREREp09Ih2NWFGQ4iIiIiIlIbBhxERERERKQ2LKkiIiIiIlLGUaqSFP+aRERERESkNgw4iIiIiIhIbVhSRURERESkjKNUJSlmOIiIiIiISG0YcBARERERkdqwpIqIiIiISBlHqUpS/GsSEREREZHaMOAgIiIiIiK1YUkVEREREZEyjlKVpJjhICIiIiIitWHAQUREREREasOSKiIiIiIiJelYUpWkmOEgIiIiIiK1YcBBRERERERqw5IqIiIiIiIlLKlKWsxwEBERERGR2jDgICIiIiIitWFJFRERERGRMlZUJSlmOIiIiIiISG0YcBARERERkdqwpIqIiIiISAlHqUpazHAQEREREZHaMMORSOvXOuPcmVN4+/oVDA3To2jxEug3aChy5HBUbOPj443F8+fg+rWrCA4KQvYcOdCley/UrF032fbzqXMbZM+U4bv2lUcfY7Dz5e/a29fM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AgVQvnz0DKa9e/fG06dPsWpV5I3t74rLkqq4pK/1hqJ1Vh+9ehv35SdxIVVy3cme/Qn3bpuhj+7O1L1+E7/jTUjcDQ0cl5Kbx34fzPggAvp535LEOP7et4zcfxfx1eAymlUKCUGcZjiGDh36y+0TJ06MtWMhIiIiIiIdLKkiIiIiIopPEuoEewl+pnEiIiIiIqI/xYCDiIiIiIgUw5IqIiIiIiI1BmBNlTYxw0FERERERIphwEFERERERIphSRURERERkRqOUqVdzHAQEREREZFiGHAQEREREZFiWFJFRERERKSGJVXaxQwHEREREREphgEHEREREREphiVVRERERERqDAxYU6VNzHAQEREREZFiGHAQEREREZFiWFJFRERERKSGo1RpFzMcRERERESkGAYcRERERESkGJZUERERERGp4SBV2sUMBxERERERKYYBBxERERERKYYlVUREREREagxZU6VVzHAQEREREZFiGHAQEREREZFiWFJFRERERKSGE/9pFzMcRERERESkGAYcRERERESkGJZUERERERGp4SBV2sUMBxERERERKYYBBxERERERKYYlVUREREREagzBmiptYoaDiIiIiIgUo5sZjgjopXA9PfHQz+HQR1++6ud5h+np631xYlXoo2Lj/4E+OtynBPRRhJ5ex/T1tEl/6GbAQURERET0lzhKlXaxpIqIiIiIiBTDgIOIiIiIiBTDkioiIiIiIjWGLKnSKmY4iIiIiIhIMQw4iIiIiIhIMSypIiIiIiJSY8hhqrSKGQ4iIiIiIlIMAw4iIiIiIlIMS6qIiIiIiNSwokq7mOEgIiIiIiLFMOAgIiIiIiLFsKSKiIiIiEgNR6nSLmY4iIiIiIhIMQw4iIiIiIhIMSypIiIiIiJSw4oq7WKGg4iIiIiIFMOAg4iIiIiIFMOSKiIiIiIiNWyR1y7+exIRERERkWIYcBARERERkWJYUkVEREREpMaAw1RpFTMcRERERESkGAYcRERERESkGJZUERERERGpYUGVdjHDQUREREREimHAQUREREREimFJFRERERGRGkOOUqVVzHAQEREREZFiGHAQEREREZFiWFJFRERERKSGBVXaxQwHEREREREphhmOv3Du7BksXbwA169fQ8CrV5gybRZKli6j2n5g/16sX7saN65fQ3BwMFav2wQ390zQifNepHbe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ChUqoHXr1nLo3M+fP6NTp05yBKvfHaFKYMBBRERERKSDzp49i5IlS6qWo/p+eHp6yqFv+/TpI+fqEPNqiExGkSJF5LC3pqbRQ++uWLFCBhmlS5eWo1PVrl1bzt3xJzgPhw7hPBz6RU+nZeA8HHqG83DoF87DoV/i8zwcT4L+fJjZ2JLGOn53EI+Jnt6hEhERERFRbGDAQUREREREimEfDiIiIiKiBDIsbkLEDAcRERERESmGAQcRERERESmGJVVERERERBpYU6VNOjks7rvQcOij0C/6ed7mJvF3WD0l6d5f7u8x0tNhUr/q67C4elpI/eWrfn6eh+npdSxN9QnQRx8PDEB89fT1J8RXqZMnRkLDkioiIiIiIlIMS6qIiIiIiNToaXJVMcxwEBERERGRYhhwEBERERGRYlhSRURERESkhhVV2sUMBxERERERKYYBBxERERERKYYlVUREREREajhKlXYxw0FERERERIphwEFERERERIphSRURERERkRoDjlOlVcxwEBERERGRYhhwEBERERGRYlhSRURERESkjhVVWsUMBxERERERKYYBBxERERERKYYlVUREREREalhRpV3McBARERERkWIYcBARERERkWJYUkVEREREpMaANVVaxQwHEREREREphgEHEREREREphiVVRERERERqDDhOlVYxw0FERERERIphwEFERERERIphSRURERERkTpWVGkVMxxERERERKQYBhxERERERKQYllQREREREalhRZV2McNBRERERESKYcBBRERERESKYUkVEREREZEaA9ZUaRUDjj+0aME8HDqwDw8f3IeJiSmye+RE5249kTati8Z+ly9dwOyZ03H1ymUYGRkio5s7Zs6ZD1NTUyRUC+Z6Y9G82RrrnJxdsHLjdvl9pzbNcfHcGY3t1WvXQ+8BQ6FLvn79Cp/Zs7Bz+1YEBgTAxsYWVWvUROu27WGgQ59Q586ewdLFC3Dj+jUEvHqFydNmoWTpMjHuO3rEUGxYtwY9+/RH46ae0CULfOfiwL69eCD+5k1N4eGRE9169EJal3TQJb/zet+/fw8zpk7C+bNn8OXrV6RLlx4Tp86Ag0Mq6BJ/f39MnzIRx47+i9DQj0jj5IzhI8cgS9Zs0AX6fh1bGMN1bNW369iWjWuxb/dO3Lp5HR9CQrD7nxOwsEiG+MDQ0ACDmhVFwzJZ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GPAKgYEBqozHvbt35PDX9vYOSGZpFafHvvPEXfRtXAhPXgbLYXE9XO3QpU5+LN19SW6/+zQIq/Zfxfy+VdHP5wAu3n0BG8skKJErLa7ef6ka3epPzFh/Gr59q+LcbT+cFcPi1s6HJKbGWPpt1CoRbGwf3xBmpsZoMWY9kiUxkQ/hVfCHHwIk0l8GEaKpIw68f/8eXl5e2LhxoyzFKFiwoOzH4eISOeze3r17ERwcjLp16/7xz1Yyw5EnR6YY1w8dMQZV1cppxFwN69aslOeQ0c0NXbr1gkeu3FBS6BdlW9iH9u+Fi+fP4m3wG1glt0Z2j1xo06GLLJfyf+GHkYP74f69O3JkKls7exQrWRqeXu3keP1KMjcxQmwKCXmP2TNn4OCB/XgdFChbAkV5VZv2HWRLcGxR+i/37JlTaNPyx0n8qlargeGjx/2wvnL5UmjUxFPxif/EUIuxKUeWmANmMWxq9ZqR9e2xQekRX37n9d68aYMsHXzp/wLOaV3kfBwlSpVW9LgM46CQ+sg/hzBjeuSgF46OqdHEswVq14nuoxYblCxJic/XsTCFr2NDfnIdS/2t7DemiQGFAUNHoXI15bK3aapP+M99RNnS0BbFUK2IG2ysksi+G2sPXseYZf/KbIQgMhz9mhRG47LZkCqlBQKDP+D0jecYueSILMH603k4hHZi4r/6BWCX3ByX7/mj56x9ck4OoWgOJ+yd0iTG57k18pZD9/7KxwMDEF+9/hB/MzXJk8TufU+CDjjUJ9kRpVRi0jRtUTLgiM+UDjjiq9gOOOKLuP3LjTuxHXDEF/o6xGRcBBzxgb7WwCsdcMRXvxNw6CIGHPoTcMT5xH+6VJJARERERAmfnrZ16ObEf0REREREpNsYcBARERERke6WVBERERERxScGYE2VNjHDQUREREREimHAQUREREREimFJFRERERGRGo5SpV3McBARERERkWIYcBARERERkWJYUkVEREREpIYVVdrFDAcRERERESmGAQcRERERESmGJVVEREREROpYU6VVzHAQEREREZFiGHAQEREREZFiWFJFRERERKTGgDVVWsUMBxERERERKYYBBxERERERKYYlVUREREREagxYUaVVzHAQEREREZFiGHAQEREREZFiWFJFRERERKSGFVXaxQwHEREREREphgEHEREREREphiVVRERERETqWFOl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",
      "text/plain": [
       "<Figure size 1000x1000 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "y_pred = model.predict(X_test)\n",
    "y_pred_labels = np.argmax(y_pred, axis=1)\n",
    "y_true_labels = np.argmax(y_test, axis=1)\n",
    "\n",
    "cmatrix = confusion_matrix(y_true_labels, y_pred_labels)\n",
    "\n",
    "plt.figure(figsize=(10,10))\n",
    "sns.heatmap(cmatrix, annot=True, cmap=\"Blues\")\n",
    "plt.xlabel(\"Predicted Label\")\n",
    "plt.ylabel(\"True Label\")\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "62414ed0-7bea-413b-ac59-357cc1b8935f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1200x600 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Extract training and validation accuracy/loss\n",
    "train_accuracy = history.history[\"accuracy\"]\n",
    "val_accuracy = history.history[\"val_accuracy\"]\n",
    "train_loss = history.history[\"loss\"]\n",
    "val_loss = history.history[\"val_loss\"]\n",
    "\n",
    "# Set the epoch range\n",
    "epochs = range(1, len(train_accuracy) + 1)\n",
    "\n",
    "# Plot Accuracy\n",
    "plt.figure(figsize=(12, 6))\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.plot(epochs, train_accuracy, 'r', label=\"Training Accuracy\")\n",
    "plt.plot(epochs, val_accuracy, 'b', label=\"Validation Accuracy\")\n",
    "plt.title('Training and Validation Accuracy')\n",
    "plt.xlabel('Epochs')\n",
    "plt.ylabel('Accuracy')\n",
    "plt.legend()\n",
    "\n",
    "# Plot Loss\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.plot(epochs, train_loss, 'r', label=\"Training Loss\")\n",
    "plt.plot(epochs, val_loss, 'b', label=\"Validation Loss\")\n",
    "plt.title('Training and Validation Loss')\n",
    "plt.xlabel('Epochs')\n",
    "plt.ylabel('Loss')\n",
    "plt.legend()\n",
    "\n",
    "# Show the plots\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
    
    '''
    
    def ensemble(self):
        return r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "8223ae8f-a7ab-440e-98c1-daa4e8940e9b",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "import os\n",
    "\n",
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.ensemble import VotingClassifier\n",
    "from sklearn.ensemble import BaggingClassifier\n",
    "from sklearn.ensemble import AdaBoostClassifier\n",
    "from sklearn.ensemble import StackingClassifier\n",
    "\n",
    "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "27f5b884-e90f-4f4d-be09-d3ff23040ea0",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_data(data_dir):\n",
    "    texts, labels = [], []\n",
    "\n",
    "    for label in ['pos', 'neg']:\n",
    "        label_dir = os.path.join(data_dir, label)\n",
    "        for filename in os.listdir(label_dir):\n",
    "            with open(os.path.join(label_dir, filename), encoding='utf-8') as f:\n",
    "                texts.append(f.read())\n",
    "            labels.append(1 if label == 'pos' else 0)\n",
    "\n",
    "    return texts, labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "21582387-3eb9-4211-9c76-0434ac6b2454",
   "metadata": {},
   "outputs": [],
   "source": [
    "train_dir = \"../datasets/aclImdb/train/\"\n",
    "test_dir = \"../datasets/aclImdb/test/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "9687075e-abb9-464a-9ede-a1783baf15ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, y_train = load_data(train_dir)\n",
    "X_test, y_test = load_data(test_dir)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "a3625811-bb6f-4bf0-ba5d-b8ac7190e934",
   "metadata": {},
   "outputs": [],
   "source": [
    "vectorizer = CountVectorizer(stop_words='english')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "63ebfd4b-69f7-4182-b9ba-547a8a690e17",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train_vectorized = vectorizer.fit_transform(X_train)\n",
    "X_test_vectorized = vectorizer.transform(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "51f3ec0d-cc44-4107-9c82-c41fac09f993",
   "metadata": {},
   "outputs": [],
   "source": [
    "voting_clf = VotingClassifier(estimators=[\n",
    "    ('lr', LogisticRegression(max_iter=1000)),\n",
    "    ('nb', MultinomialNB()),\n",
    "    ('dt', DecisionTreeClassifier())\n",
    "], voting='hard')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "450c76a7-b0d7-4045-a0d0-66e78f41e600",
   "metadata": {},
   "outputs": [],
   "source": [
    "bagging_clf = BaggingClassifier(\n",
    "    estimator=DecisionTreeClassifier(),\n",
    "    n_estimators=50,\n",
    "    random_state=42\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "df8aaf43-b655-4a69-bdbb-a3fcb0843c4a",
   "metadata": {},
   "outputs": [],
   "source": [
    "boosting_clf = AdaBoostClassifier(\n",
    "    estimator=DecisionTreeClassifier(max_depth=1),\n",
    "    n_estimators=50,\n",
    "    learning_rate=1.0,\n",
    "    random_state=42\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "c76238c4-cf2c-4a6e-975d-5ebffa28d33d",
   "metadata": {},
   "outputs": [],
   "source": [
    "stacking_clf = StackingClassifier(\n",
    "    estimators=[\n",
    "        ('lr', LogisticRegression(max_iter=1000)),\n",
    "        ('nb', MultinomialNB()),\n",
    "        ('dt', DecisionTreeClassifier())\n",
    "    ],\n",
    "    final_estimator=LogisticRegression(),\n",
    "    cv=5\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "42c30429-9055-4da0-b5e7-b30f7e5800bc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model Accuracy: 0.85612\n",
      "\n",
      "Classification Report: \n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.84      0.88      0.86     12500\n",
      "           1       0.87      0.83      0.85     12500\n",
      "\n",
      "    accuracy                           0.86     25000\n",
      "   macro avg       0.86      0.86      0.86     25000\n",
      "weighted avg       0.86      0.86      0.86     25000\n",
      "\n"
     ]
    },
    {
     "data": {
      "image/png": "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bNy4UfLkySO1atUy650Bjfrss8/k9OnTrsfu9DVTpkwp8+fPd627f/++zJs3T5o1a2YeHzp0SGrWrCmNGjWSP//802zT19QvGcAXPyfx48eXzZs3y4QJE2TcuHHyySefmG2vv/66/P7777Jo0SLZsGGDCWT037gGEapDhw6mvLlmzRrZuXOn+XmJKHtYrlw5E5ToHwf6s6BLz549H9pP/80vXrzYlE2dli1bJrdu3TKBv9JgRYOXadOmye7du6Vbt27y2muvya+//mrhpwREM+1hQexQuXJlR4UKFTzWPf30044+ffo4fvvtN0fy5Mkdd+7c8dieK1cux0cffWTuly5d2tGhQweP7eXLl3cULVr0ka95//59R7JkyRyLFy92rdN/dgsWLPDYb9CgQR7H6dKli+O5555zPV62bJkjKCjIcfnyZfO4devWjnbt2nkcQ99D3LhxHbdv347U5wE86uekQIECjrCwMNc6/RnRdQcOHDD/ftetW+faduHCBUdwcLDj66+/No+LFCniGDx4cITHXr16tXm+89/xZ5995kiRIsVD++XIkcMxfvx4cz80NNSRNm1ax6xZs1zbX331Vccrr7xi7uvPbOLEiR3r16/3OIb+jOh+QKAgwxLLPPXUUx6PM2XKZLIqWvrRv+C06dXZT6LLkSNHTDZD7d+/X5555hmP54d/fPbsWWnbtq3JrGg6Xf961OMeP348Suepf1Vqyvzvv/92ZXdq165tMi9Kz1cbFt3PtUaNGiY1rucMeKNMmTKmRONUtmxZU/bZs2ePybyULl3atU1/ZvLlyyd79+41j7U0qaXT8uXLm+n3NQPoDX29l19+2fwMKC17fv/9965s419//WWyLVqKdf950IyL82cXCAQ03cYyCRIk8Hisv5T1S16DCg1eNEgIzxkkRIaWgy5evGjS6Dly5DDXStFf9jo6IiqefvppyZUrl3z11VfSvn17M6pIAxQnPd8333zTfDmEp6UqwF+0t0uD5x9++MH0Y2m5ZuzYsdKpU6f/fEwNTrQfTP+40BKu9qloSVQ5S0X6elmyZPF4HtcqQiAhYIGh/Spnzpwxf805G2HD078itedEGw6dwvegrFu3TqZMmWJq+urEiRNy4cKFh4Im7UmJzC9p/asya9asEjduXJNhcT9f/Ws3d+7cUX6vwL/RHi93zn6sggULyr1798x2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",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "voting_clf.fit(X_train_vectorized, y_train)\n",
    "y_pred = voting_clf.predict(X_test_vectorized)\n",
    "\n",
    "print(f\"Model Accuracy: {accuracy_score(y_test, y_pred)}\")\n",
    "print(f\"\\nClassification Report: \\n{classification_report(y_test, y_pred)}\")\n",
    "\n",
    "cm = confusion_matrix(y_test, y_pred)\n",
    "\n",
    "\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\", xticklabels=[\"negative\", \"positive\"], yticklabels=[\"neutral\", \"positive\"])\n",
    "plt.xlabel('Predicted')\n",
    "plt.ylabel('Actual')\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "069e2a6d-e68b-49ea-ac50-eb6ac5d0baae",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model Accuracy: 0.7942\n",
      "\n",
      "Classification Report: \n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.79      0.80      0.80     12500\n",
      "           1       0.80      0.79      0.79     12500\n",
      "\n",
      "    accuracy                           0.79     25000\n",
      "   macro avg       0.79      0.79      0.79     25000\n",
      "weighted avg       0.79      0.79      0.79     25000\n",
      "\n"
     ]
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "bagging_clf.fit(X_train_vectorized, y_train)\n",
    "y_pred = bagging_clf.predict(X_test_vectorized)\n",
    "\n",
    "print(f\"Model Accuracy: {accuracy_score(y_test, y_pred)}\")\n",
    "print(f\"\\nClassification Report: \\n{classification_report(y_test, y_pred)}\")\n",
    "\n",
    "cm = confusion_matrix(y_test, y_pred)\n",
    "\n",
    "\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\", xticklabels=[\"negative\", \"positive\"], yticklabels=[\"neutral\", \"positive\"])\n",
    "plt.xlabel('Predicted')\n",
    "plt.ylabel('Actual')\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "b39a5e08-787e-4ea9-815e-86dfc22b2cbe",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model Accuracy: 0.75704\n",
      "\n",
      "Classification Report: \n",
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.80      0.68      0.74     12500\n",
      "           1       0.72      0.83      0.77     12500\n",
      "\n",
      "    accuracy                           0.76     25000\n",
      "   macro avg       0.76      0.76      0.76     25000\n",
      "weighted avg       0.76      0.76      0.76     25000\n",
      "\n"
     ]
    },
    {
     "data": {
      "image/png": "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JCgoSAoVKuS0jI72mvTv318yZsxojletWlUOHDjgdI6LFy9Ks2bNJDg4WFKmTCmtW7eW69evO7XZvn27lC9fXhInTixZs2aVoUOHitcDloYNG8onn3xy3369uJdfftld1wUAAFxw6dIlKVeunCRMmFB+//132b17twwfPtwp6aDf3VqjqiUd69evl6RJk0r16tUlLCzM3kaDlV27dsnixYtl7ty5pma1Xbt29uNXr16VatWqSfbs2WXz5s0ybNgwMwXK+PHj3fp+4tkeNOznAXSSuGXLlpkozdGOHTtMZHbmzBnxtrA73r4CwDcxcRzgnYnjes/b55bzDK2V95HbvvPOO7JmzRr5448/oj2uX/+ZMmWSHj16SM+ePc2+K1euSPr06WXixInSuHFj2bNnjxQoUEA2btwoJUqUMG0WLFggNWvWlBMnTpjnjx07Vt59910z6701Wlhfe9asWbJ3717xWoZF00DRDV/WCE6jLAAAcP9qze7YwsPDzXet46b7ovPbb7+ZIEN7P0JCQszSOl9//bVTbaoGGZpssKRIkUJKlSol69atM4/1VruBrGBFaXud5V4zMlabChUqOMUGmqXZt2+fyfK47TOM6RM0szJt2rT79v/0008mCgMAAPd/2bpjGzJkiAkqHDfdF53Dhw+b7EeePHlk4cKF0qFDB+ncubNMmjTJHNdgRWlGxZE+to7prQY7jhIkSGAWO3ZsE905HF/DKxPHvffee9KgQQM5dOiQVK5c2exbunSpTJ061azYDAAAPKNv377SvXt3p32BgYHRto2MjDSZkcGDB5vHmmHZuXOnqVdp2bKlxDYxDlhq165t+qX0A9AARauKixQpYupaNOICAADO3DWqOTAw8IEBSlQ68idqz0f+/PllxowZ5n6GDBnMrdaealuLPi5atKi9TdTleO7cuWNGDlnP19uo9avWY6uN1xaQrFWrlinkuXHjhkk5vfLKK6ZgRwMXAADgmRqWmNARQlpH4mj//v1mNI/KmTOnCSi0l8SiNTFam1KmTBnzWG8vX75sRv9YNEGh2RutdbHa6MihiIgIexsdUZQ3b163ToPy2Cte68VpSkkrhHWYlHYP/fnnn267MAAA8Pi6detmvpe1R+TgwYOmdEOHGnfs2NE+mV3Xrl1l0KBBpkBXR/u2aNHCfK/Xq1fPnpF58cUXpW3btrJhwwaT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",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "boosting_clf.fit(X_train_vectorized, y_train)\n",
    "y_pred = boosting_clf.predict(X_test_vectorized)\n",
    "\n",
    "print(f\"Model Accuracy: {accuracy_score(y_test, y_pred)}\")\n",
    "print(f\"\\nClassification Report: \\n{classification_report(y_test, y_pred)}\")\n",
    "\n",
    "cm = confusion_matrix(y_test, y_pred)\n",
    "\n",
    "\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\", xticklabels=[\"negative\", \"positive\"], yticklabels=[\"neutral\", \"positive\"])\n",
    "plt.xlabel('Predicted')\n",
    "plt.ylabel('Actual')\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3dfeb755-185d-46f3-86db-fd965ffac03f",
   "metadata": {},
   "outputs": [],
   "source": [
    "stacking_clf.fit(X_train_vectorized, y_train)\n",
    "y_pred = stacking_clf.predict(X_test_vectorized)\n",
    "\n",
    "print(f\"Model Accuracy: {accuracy_score(y_test, y_pred)}\")\n",
    "print(f\"\\nClassification Report: \\n{classification_report(y_test, y_pred)}\")\n",
    "\n",
    "cm = confusion_matrix(y_test, y_pred)\n",
    "\n",
    "\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\", xticklabels=[\"negative\", \"positive\"], yticklabels=[\"neutral\", \"positive\"])\n",
    "plt.xlabel('Predicted')\n",
    "plt.ylabel('Actual')\n",
    "plt.title(\"Confusion Matrix\")\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}    
    '''
    
    def knn(self):
        return r'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "9e073181-eca3-49ad-b845-dabf0a5569bd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import struct\n",
    "\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.metrics import confusion_matrix, accuracy_score\n",
    "from scipy.stats import mode"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "7e4f8b5b-1314-4997-94a5-d5954f089eae",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_mnist_images(filename):\n",
    "    with open(filename, 'rb') as f:\n",
    "        magic, num, rows, cols = struct.unpack(\">IIII\", f.read(16))\n",
    "        print(f\"Loaded {num} images of size {rows}x{cols}\")\n",
    "\n",
    "        images = np.frombuffer(f.read(), dtype=np.uint8).reshape(num, rows*cols)\n",
    "        return images / 255.0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "6dd2b80c-8c6e-4116-9f93-494a40ebc5f0",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_mnist_labels(filename):\n",
    "     with open(filename, 'rb') as f:\n",
    "        magic, num = struct.unpack(\">II\", f.read(8))\n",
    "        labels = np.frombuffer(f.read(), dtype=np.uint8)\n",
    "        return labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "e1ff4e6f-88f2-4a2c-86b5-6d5c1213c3ce",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Loaded 60000 images of size 28x28\n",
      "Loaded 10000 images of size 28x28\n"
     ]
    }
   ],
   "source": [
    "X_train = load_mnist_images('../datasets/MNIST/train-images.idx3-ubyte')\n",
    "y_train = load_mnist_labels('../datasets/MNIST/train-labels.idx1-ubyte')\n",
    "X_test = load_mnist_images('../datasets/MNIST/t10k-images.idx3-ubyte')\n",
    "y_test = load_mnist_labels('../datasets/MNIST/t10k-labels.idx1-ubyte')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "76116044-9c38-4837-8e3f-762dc1db4b98",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "X_train shape : (60000, 784)\n",
      "y_train shape : (60000,)\n",
      "X_test shape : (10000, 784)\n",
      "y_test shape : (10000,)\n",
      "The first record of X_train : \n",
      "[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n",
      " 0. 0. 0. 0.]\n",
      "The label of the first record : 5\n"
     ]
    }
   ],
   "source": [
    "print(f\"X_train shape : {X_train.shape}\")\n",
    "print(f\"y_train shape : {y_train.shape}\")\n",
    "print(f\"X_test shape : {X_test.shape}\")\n",
    "print(f\"y_test shape : {y_test.shape}\")\n",
    "\n",
    "print(f\"The first record of X_train : \\n{X_train[0][:100]}\")\n",
    "print(f\"The label of the first record : {y_train[0]}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "c0cf0554-7a2b-43dd-acd3-df94831ae48f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1000x1000 with 25 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(10, 10))\n",
    "for i in range(25):\n",
    "    plt.subplot(5, 5, i + 1)\n",
    "    plt.imshow(X_train[i].reshape(28, 28), cmap=\"gray\")\n",
    "    plt.title(str(y_train[i]))\n",
    "    plt.axis(\"off\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "5b451166-32c9-4d5f-9fbb-24157b241db3",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_combined = np.vstack([X_train, X_test])\n",
    "y_combined = np.hstack([y_train, y_test])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "9ed7e48a-c420-4b7e-a201-38e9d0cb63b0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: #000;\n",
       "  --sklearn-color-text-muted: #666;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-1 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-1 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: flex;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "  align-items: start;\n",
       "  justify-content: space-between;\n",
       "  gap: 0.5em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label .caption {\n",
       "  font-size: 0.6rem;\n",
       "  font-weight: lighter;\n",
       "  color: var(--sklearn-color-text-muted);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-1 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-1 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-1 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 0.5em;\n",
       "  text-align: center;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-1 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>KMeans(n_clusters=10, random_state=42)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow\"><div><div>KMeans</div></div><div><a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.6/modules/generated/sklearn.cluster.KMeans.html\">?<span>Documentation for KMeans</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></div></label><div class=\"sk-toggleable__content fitted\"><pre>KMeans(n_clusters=10, random_state=42)</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "KMeans(n_clusters=10, random_state=42)"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "kmeans = KMeans(n_clusters=10, random_state=42)\n",
    "kmeans.fit(X_combined)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "ef8b10dd-3062-4b19-b038-436ea060fc95",
   "metadata": {},
   "outputs": [],
   "source": [
    "cluster_labels = kmeans.predict(X_combined)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "ad72619a-f76b-4164-87a2-1d19d026c372",
   "metadata": {},
   "outputs": [],
   "source": [
    "def map_clusters_to_labels(clusters, true_labels):\n",
    "    labels = np.zeros(10)\n",
    "    for i in range(10):\n",
    "        mask = (clusters == i)\n",
    "        labels[i] = mode(true_labels[mask])[0]\n",
    "    return labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "7d437451-4e6e-4e46-b496-861fcbfa4ee4",
   "metadata": {},
   "outputs": [],
   "source": [
    "mapped_labels = map_clusters_to_labels(cluster_labels, y_combined)\n",
    "predicted_labels = mapped_labels[cluster_labels.astype(int)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "6169b99a-67f7-4f5d-8ede-b1f98217d5e9",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "KMeans Clustering Accuracy (after label matching): 0.5815\n"
     ]
    },
    {
     "data": {
      "image/png": "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5PTtwikiIiIioj+GNRXGGVQQERERERkMM005jQiGYUREREREFCEcqSAiIiIi0sX0p3DjO0ZERERERBHCkQoiIiIiIl2sqQg3jlQQEREREVGEcKSCiIiIiEgXayrCje8YERERERFFCEcqiIiIiIh0saYi3BhUEBERERHpYvpTuPEdIyIiIiKiCOFIBRERERGRLqY/hRtHKoiIiIiIKEI4UkFEREREpIs1FeHGd4yIiIiIyAAlT54cUaJECXVr166dWv/x40f1c5w4cRAtWjTUqFEDz54903sMLy8vVKhQAfb29ogfPz569OiBL1++6G1z4MAB5MiRA7a2tkiVKhUWLlwY7ufKoIKIiIiIKGRNRWTdwuHUqVN48uSJ9rZ79261vFatWur/Ll26YPPmzVizZg0OHjyIx48fo3r16trf//r1qwooPn/+jKNHj2LRokUqYBg4cKB2m7t376ptihUrhvPnz6Nz585o3rw5du7cGZ6niiiBgYGBMDEf9YMvs+GYuz3M0atT0/72UyAiIqJwimrASfh2FaZE2mP7be34y78rDf4tW7bg5s2bePPmDeLFi4fly5ejZs2aav21a9eQPn16HDt2DK6urti+fTsqVqyogo0ECRKobWbOnIlevXrB29sbNjY26uetW7fi0qVL2r9Tp04d+Pr6YseOHT/93DhSQUREREQUsqYikm6fPn1SAYHuTZb9iIw2LF26FM2aNVMpUGfOnIG/vz9Kliyp3SZdunRwdnZWQYWQ/zNnzqwNKESZMmXU37x8+bJ2G93H0GyjeYyfxaCCiIiIiOgPBRXu7u6IGTOm3k2W/cjGjRvV6EGTJk3U/adPn6qRhlixYultJwGErNNsoxtQaNZr1n1vGwk8/Pz8fvotM+CBJyIiIiIi09KnTx907dpVb5kUSP/IvHnzUK5cOSRKlAiGiEEFEREREdEfuvidra3tTwURuu7fv489e/Zg/fr12mUJEyZUKVEyeqE7WiGzP8k6zTYnT57UeyzN7FC624ScMUrux4gRA3Z2dj/9HJn+RERERERkwBYsWKCmg5VZmjRy5swJa2tr7N27V7vs+vXragrZfPnyqfvyv6enJ54/f67dRmaQkoAhQ4YM2m10H0OzjeYxfhZHKoiIiIiIDPTidwEBASqoaNy4MaysgpvuUovh5uamUqlix46tAoUOHTqoYEBmfhKl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",
      "text/plain": [
       "<Figure size 1000x600 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "accuracy = accuracy_score(y_combined, predicted_labels)\n",
    "print(f\"KMeans Clustering Accuracy (after label matching): {accuracy:.4f}\")\n",
    "\n",
    "# Confusion matrix\n",
    "cm = confusion_matrix(y_combined, predicted_labels)\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.heatmap(cm, annot=True, cmap=\"Blues\", fmt=\"d\")\n",
    "plt.title(\"Confusion Matrix (KMeans Clustering)\")\n",
    "plt.xlabel(\"Predicted Label\")\n",
    "plt.ylabel(\"True Label\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b614d737-5f65-461a-b920-971d71ed5238",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}    
    '''
    
class IOT:
    def __init__(self):
        ...
        
    def temperature_sensor(self):
        return r'''
float temp;
int temppin = 0;
void setup() {
Serial.begin(9600);
}
void loop() {
int sensorvalue = analogRead(temppin);
float voltage = sensorvalue * (5.0 / 1023.0);
temp = voltage / 0.1;
Serial.print(“TEMPERATURE = ”);
Serial.print(temp);
Serial.print(“oC”);
Serial.println();
delay(1000);
}
    '''
    
    def soil_moisture_sensor(self):
        return r'''
    const int sensor_pin = A0;
void setup() {
Serial.begin(9600);
}
void loop() {
float moisture_percentage;
int sensor_analog;
sensor_analog = analogRead(sensor_pin);
moisture_percentage = (100 - ((sensor_analog / 1023.00) * 100));
Serial.print(“Moisture Percentage”);
Serial.print(moisture_percentage);
Serial.print(“% \n \n”);
delay(1000);
}
    '''
    
    def raindrop_sensor(self):
        return r'''
    # define POWER_PIN D7
# define AO_PIN A0
void setup() {
Serial.begin(9600);
pinMode(POWER_PIN, OUTPUT); }
void loop() {
digitalWrite(POWER_PIN, HIGH);
delay(10);
int rainValue = analogRead(AO_PIN);
digitalWrite(POWER_PIN, LOW);
Serial.println(rainValue);
delay(1000); }
    '''

    def pir_sensor(self):
        return r'''
    int sensor = 4;
void setup(){
 pinMode(sensor, INPUT);
 Serial.begin(9600);
}
void loop(){
 int state = digitalRead(sensor);
 if (state == HIGH){
 Serial.println("Motion detected");
 delay(1000);
 }
 else{
 Serial.println("Motion absent");
 delay(1000);
 }
}
    '''

    def ultrasonic_sensor(self):
        return r'''
    const int trigPin = 12;
const int echoPin = 14;
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701
long duration;
float distanceCm;
float distanceInch;
void setup() {
 Serial.begin(115200);
 pinMode(trigPin, OUTPUT);
 pinMode(echoPin, INPUT);
}
void loop() {
 digitalWrite(trigPin, LOW);
 delayMicroseconds(2);
 digitalWrite(trigPin, HIGH);
 delayMicroseconds(10);
 digitalWrite(trigPin, LOW);
 duration = pulseIn(echoPin, HIGH);
 distanceCm = duration * SOUND_VELOCITY/2;
 distanceInch = distanceCm * CM_TO_INCH;
 Serial.print("Distance (cm): ");
 Serial.println(distanceCm);
 Serial.print("Distance (inch): ");
 Serial.println(distanceInch);
 delay(1000);
}

    '''

    def ultrasonic_sensor_rp(self):
        return r'''
    import RPi.GPIO as GPIO
import time

# Pin configuration
TRIG = 11  # GPIO pin for Trigger
ECHO = 12  # GPIO pin for Echo

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s, divide by 2
    distance = round(distance, 2)

    return distance

try:
    while True:
        dist = measure_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()

    '''
    
    def raindrop_sensor_rp(self):
        return r'''
    import RPi.GPIO as GPIO
import time

# GPIO setup
RAIN_SENSOR_PIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(RAIN_SENSOR_PIN) == 0:
            print("Rain detected!")
        else:
            print("No rain.")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

    '''
    
    def soil_moisture_sensor_rp(self):
        return r'''
    import RPi.GPIO as GPIO
import time

# GPIO setup
MOISTURE_SENSOR_PIN = 11  

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(MOISTURE_SENSOR_PIN) == 0:
            print("Soil is wet")
        else:
            print("Soil is dry")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

    '''
    
    def pir_sensor_rp(self):
        return r'''
    import RPi.GPIO as GPIO
import time

PIR_PIN = 11  

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)

print("Waiting for PIR to stabilize...")
time.sleep(2)  # Allow PIR to stabilize
print("Ready! Monitoring for motion...")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
        else:
            print("No Motion")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

    '''
    
    def temperature_sensor_rp(self):
        return r'''
    import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.D0) # pin  7

try:
    while True:
        temp = dht.temperature
        humidity = dht.humidity
        print(f"Temp: {temp}°C | Humidity: {humidity}%")
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped")

    '''
    
    def single_led_rp(self):
        return r'''
    import RPi.GPIO as gp
from time import sleep
gp.setwarnings(False)
gp.setmode ( gp.BOARD)
gp.setup(11, gp.out,initial=gp.Low)
While True:
gp.output(11,gp.HIGH)
Sleep(1)
gp.output(11,gp.LOW)
Sleep(1)

    '''
    
    def multi_led_rp(self):
        return r'''
    import RPi.GPIO as gp
from time import sleep
gp.setwarnings(False)
gp.setmode (gp.BOARD)
gp.setup(11, gp.out,initial=gp.LOW)
gp.setup(12, gp.out,initial=gp.LOW)
While True:
gp.output(11,gp.HIGH)
gp.output(12,gp.LOW)
Sleep(1)
gp.output(11,gp.LOW)
gp.output(12,gp.HIGH)
Sleep(1)
    '''
    
    def buzzer_rp(self):
        return r'''
    import RPI GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buzzer = 11
GPIO.setup(buzzer,GPIO.OUT)
while True:
GPIO.output(buzzer,GPIO.HIGH)
print(“Beep”)
sleep(0.5)
GPIO.output(buzzer,GPIO.LOW)
print(“No Beep”)
Sleep(0.5)
    '''