#stft_sample.py
#wave形式の音声波形を読み込むためのモジュール(wave)をインポート
import wave as wave
#numpyをインポート（波形データを2byteの数値列に変換するために使用）
import numpy as np
#scipyのsignalモジュールをインポート（stft等信号処理計算用)
import scipy.signal as sp
#sounddeviceモジュールをインポート
import sounddevice as sd
#matplotlib
import matplotlib.pyplot as plt
import math

def hamming(nperseg):
    t = sp.hamming(nperseg) # 関数を使う方法
    #print(t)
    t = np.array(t)
    #print(type(t))
    """
    t = np.ones((1,nperseg))
    for i in range(len(t)):
        t[i]=0.54+0.46*math.cos(2.0*math.pi/i*t)
    print(t)
    """

    return t

# STFTを自前で実装してみる
# [INPUT]
#     sig: input signal (len x 1) 入力信号
#      fs: サンプリング周波数(wav.getframerate()で取得可能)
#   wndow: analysis window function (frlen x 1, default: hamming window) 窓関数(wid)
#  nperseg: frame length (even number, must be dividable by frsft) フレーム長(frlen)
# noverlap: frame shift  (default: frlen/2) フレームシフト(frsft)
# ex) STFT(data,fs=wav.getframerate(),window="hann",nperseg=512,noverlap=256)
# [OUTPUT]
# f : 出力されるデータの周波数軸の各インデックスの具体的な周波数〔Hz〕
# t : フレーム軸の各インデックスの具体的な時間〔sec〕
# stft_data: STFT of input signal (frlen/2+1 x nf) STFTの信号 短時間 フーリエ変換後の複素数の信号 y(l, k)

def STFT(sig,fs,frlen,frsft,wnd):
    # フレームの数を測る
    nf = int(((len(sig)-frlen)/frsft)+1) # データサイズをフレームサイズで割っている
    print("スライスの大きさ",(sig[0:frlen]).shape)
    # ハミング窓を計算するために転地する
    hamming_trans = (hamming(frlen)).T

    print("転地した後",hamming_trans.shape)
    print("nf",nf)
    stft_data = []
    for i in range(1,nf+1): # iの関係で1から215まで
        st=(i-1)*frsft # ひとつ前の場所から窓をかける
        # スライス処理と窓関数のかけ算
        #print(sig[st:st+frlen].shape,(hamming(frlen).T).shape)
        a = np.fft.fft((sig[st:st+frlen].T*hamming(frlen)))
        #print(a)
        stft_data.append(a)
        # 窓関数をかける
        # FFTを行う
    stft_data = np.array(stft_data)
    print(stft_data.shape)
    return fs,nf,stft_data



#読み込むサンプルファイル
sample_wave_file="/Users/kenta/Programing/github/yama-pyroomacoustics-learning/python_source_separation-master/section2/CMU_ARCTIC/cmu_us_axb_arctic/wav/arctic_a0001.wav"
#ファイルを読み込む
wav=wave.open(sample_wave_file)
#PCM形式の波形データを読み込み
data=wav.readframes(wav.getnframes())
#dataを2バイトの数値列に変換
data=np.frombuffer(data, dtype=np.int16)
print("元のデータの大きさ",data.shape)
#短時間フーリエ変換を行う
print(data.shape,wav.getframerate())

#print(hamming(512).shape)
#f,t,stft_data= STFT(data,wav.getframerate(),512,256,"hann")

#短時間フーリエ変換を行う
f,t,stft_data=sp.stft(data,fs=wav.getframerate(),window="hann",nperseg=512,noverlap=256)
print(f,t)
#f,t,stft_data= STFT(data,wav.getframerate(),512,256,"hann")