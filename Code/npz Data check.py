import numpy as np
import glob
import sys
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

x_train = np.empty((0, 120, 320))
y_train = np.empty((0, 4))
training_data = glob.glob('./training_data/*.npz')

for single_npz in training_data:
    with np.load(single_npz) as data:
        x = data['train']
        y = data['train_labels']
    x_train = np.vstack((x_train, x))
    y_train = np.vstack((y_train, y))

x_train = x_train.reshape(-1,120,320,1)

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3)


print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
'''
#get_ipython().run_line_magic('matplotlib', 'inline')

plt_row = 3
plt_col = 3

plt.rcParams["figure.figsize"] = (10,10)
f, axarr = plt.subplots(plt_row, plt_col, figsize=[10,10])

for i in range(plt_row*plt_col):
        sub_plt = axarr[i//plt_row, i%plt_col]
        sub_plt.axis('off')
        sub_plt.imshow((x_train[i].reshape(120, 320)))
        sub_plt_title = 'R: ' + str(np.argmax(y_train[i]))
        sub_plt.set_title(sub_plt_title)

plt.show()
'''
fig = plt.figure()
for i in range(10):
    # 2x5 그리드에 i+1번째 subplot을 추가하고 얻어옴
    subplot = fig.add_subplot(2, 5, i + 1)
 
    # x, y 축의 지점 표시를 안함
    subplot.set_xticks([])
    subplot.set_yticks([])
 
    # subplot의 제목을 i번째 결과에 해당하는 숫자로 설정
    subplot.set_title('%d' % np.argmax(y_train[i]))
 
    # 입력으로 사용한 i번째 테스트 이미지를 28x28로 재배열하고
    # 이 2차원 배열을 그레이스케일 이미지로 출력
    subplot.imshow(x_train[i].reshape((120, 320)))
 
plt.show()
