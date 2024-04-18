# Batch Processing

## 배경
임베딩(Embedding) 작업을 처리하는데, 아래와 같이 인자로 여러 문장을 받을 수 있다.
```
embedded_result = embedding_model(sentences: list[str])
```
하지만 현재 로직은 한 문장만 임베딩 모델에게 보내는데, 요청이 많아질 수록 임베딩 처리를 개별적으로 하는 것은 큰 오버헤드가 될 수 있다.</br>
게다가, 임베딩 모델 자체는 원래 여러 문장을 한 번에 처리하도록 설계 돼있어서, 실제로 여러 문장을 한 번에 처리하는 것이 성능 상 더 좋다고 한다.</br></br>

따라서 `batch_size`와 `latency_time`을 정하여 일정 개수의 데이터가 쌓이거나, 또는 일정 시간마다 임베딩 부분 일괄 처리를 할 수 있도록 설계하였다.</br></br>

현재는 `batch_size = 10`, `latency_time = 0.1`로 설정했지만, 실제 운영 시에는 트래픽과 임베딩 처리 시간을 고려하여 적절하게 설정해야 응답 시간, 성능 등 여러 측면에서 좋은 결과를 낼 수 있을 것으로 예측한다.

## 실행
```
python main.py
```

## 모델링 

임베딩 작업을 비슷하게 모델링하여 문자열의 길이르 두 배로 하여 반환하는 함수로 변경하였다.
함수 내 `time.sleep(1)`을 추가로 넣어 임베딩이 처리되는 시간을 고려하였다.</br></br>

30개의 요청을, 0.04초 간격으로 보냈다.

## 결과 
아래 결과에서 알 수 있듯이, 0.1초 간격의 배치 처리와 0.04초의 요청 간격을 고려했을 때, 한 배치 크기가 2~3으로 예상과 같이 처리되었음을 확인할 수 있다.
```
Batch: 0 1 2
Batch: 3 4 5
Batch: 6 7
Batch: 8 9 10
Batch: 11 12 13
Batch: 14 15
Batch: 16 17 18
Batch: 19 20 21
Batch: 22 23
Batch: 24 25 26
(Request: 0) Result: ABCED0ABCED0
(Request: 1) Result: ABCED1ABCED1
(Request: 2) Result: ABCED2ABCED2
Batch: 27 28 29
(Request: 3) Result: ABCED3ABCED3
(Request: 4) Result: ABCED4ABCED4
(Request: 5) Result: ABCED5ABCED5
(Request: 6) Result: ABCED6ABCED6
(Request: 7) Result: ABCED7ABCED7
(Request: 8) Result: ABCED8ABCED8
(Request: 9) Result: ABCED9ABCED9
(Request: 10) Result: ABCED10ABCED10
(Request: 11) Result: ABCED11ABCED11
(Request: 12) Result: ABCED12ABCED12
(Request: 13) Result: ABCED13ABCED13
(Request: 14) Result: ABCED14ABCED14
(Request: 15) Result: ABCED15ABCED15
(Request: 16) Result: ABCED16ABCED16
(Request: 17) Result: ABCED17ABCED17
(Request: 18) Result: ABCED18ABCED18
(Request: 19) Result: ABCED19ABCED19
(Request: 20) Result: ABCED20ABCED20
(Request: 21) Result: ABCED21ABCED21
(Request: 22) Result: ABCED22ABCED22
(Request: 23) Result: ABCED23ABCED23
(Request: 24) Result: ABCED24ABCED24
(Request: 25) Result: ABCED25ABCED25
(Request: 26) Result: ABCED26ABCED26
(Request: 27) Result: ABCED27ABCED27
(Request: 28) Result: ABCED28ABCED28
(Request: 29) Result: ABCED29ABCED29
```