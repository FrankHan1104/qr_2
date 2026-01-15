# QR 코드 생성기 (PyQt5)

간단한 데스크톱 GUI 프로그램으로, 여러 QR 코드를 동시에 생성하고 PNG로 저장할 수 있습니다.

필요한 패키지:

- PyQt5
- qrcode
- Pillow

설치 (Windows, PowerShell):

```powershell
python -m pip install -r requirements.txt
```

실행:

```powershell
python qrcode_app.py
```

또는 빌드된 exe 파일:

```powershell
./dist/qrcode_app.exe
```

사용법:

1. 각 섹션에 URL 또는 텍스트 입력 후 "생성" 버튼 클릭 (미리보기 표시)
2. "저장" 버튼으로 PNG 파일로 저장
