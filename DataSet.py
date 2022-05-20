from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

import sys
sys.path.append('..')
import Functions as fn

X, Y = [], []
for i, etiket in enumerate(fn.etiketler):
    etiket_klasoru = fn.resimlerDiziniOnIslenmis + '/' + etiket
    for resim_adi in fn.listdir(etiket_klasoru):
        resim = fn.resmi_al(etiket_klasoru + '/' + resim_adi, fn.renkliDeger)
        X.append(resim)
        Y.append(i)

if(fn.renkliDeger=="gri"):
    X = fn.np.array(X).astype('float32')/255.
elif(fn.renkliDeger=="renkli"):
    X = fn.np.array(X).astype('float32')
X = X.reshape(X.shape[0], fn.en, fn.boy, fn.kanal)
Y = fn.np.array(Y).astype('float32')
Y = to_categorical(Y, fn.etiketSayisi)

x, x_test, y, y_test = train_test_split(X, Y, test_size=0.1, random_state=1, stratify=Y)
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.1111, random_state=1, stratify=y)
fn.np.save('VeriSetleri/x_train.npy', x_train)
fn.np.save('VeriSetleri/x_test.npy', x_test)
fn.np.save('VeriSetleri/x_val.npy', x_val)
fn.np.save('VeriSetleri/y_train.npy', y_train)
fn.np.save('VeriSetleri/y_test.npy', y_test)
fn.np.save('VeriSetleri/y_val.npy', y_val)
