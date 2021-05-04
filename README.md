# protocol-analyzer

## 설명
> Ethernet Frame Raw Data (HEX data)를 입력으로 받아 계층별 프로토콜 분석을 수행하는 프로그램이다. 4계층에 대한 프로토콜 정보는 PROTOCOLS_IP.txt 파일에서 읽어오고, Well-Known 포트에 대한 정보는 SERVICES.txt 파일에서 읽어온다.

## 프로그램 구현 도구
Base: Python3  
GUI: PyQt5 (QT)

## 프로그램 구동 시스템 요구사항 및 구동 방법
O/S: Independent ( Python3 및 PyQt5 설치 가능하여야 함. )  
Python3 Interpreter  
PyQt5 Python3 library. ( Using pip command: pip install pyqt5 )  
  
* Execute this command  
	> python3 start.py  
* Only for Windows OS users, can run start.exe alternatively.  

## 프로그램 구조 및 UI
![P_01](https://user-images.githubusercontent.com/8454866/116965782-97426380-ace9-11eb-9380-2fed7f557365.png)
![P_02](https://user-images.githubusercontent.com/8454866/116965783-97dafa00-ace9-11eb-9a43-0192470bc408.png)
![P_03](https://user-images.githubusercontent.com/8454866/116965828-b50fc880-ace9-11eb-8fd5-3b7d8745bae6.png)
