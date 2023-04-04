import numpy as np
import matplotlib.pyplot as mp


# begin 11/2 covid data
NonSymptonList = [2791, 3288, 3180, 4022, 5074, 6801, 6989, 7820, 9520, 10446, 13167, 14409]
SymptonList = [531, 704, 596, 526, 535, 843, 1294, 1133, 1150, 1452, 1675, 1747]
TotalList = [NonSymptonList[i] + SymptonList[i] for i in range(len(NonSymptonList))]
XList = list(range(len(TotalList)))

def do_fit(data_list):
	z1 = np.polyfit(XList, data_list, 3)  # 曲线拟合，返回值为多项式的各项系数
	yn = np.poly1d(z1)

	xn = np.linspace(0,len(data_list),100)
	mp.plot(xn, yn(xn), XList, data_list, 'o')
	mp.show()
	print(z1)

if __name__ == '__main__':
	do_fit(SymptonList)
	print('ok')
