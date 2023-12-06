# 여보게 추천 API v1

## 🚩 Table of Contents

- [About The Model](#-about-the-model)
- [Tech Stack](#-tech-stack)

## 💡 About The Model

### Factorization Machine

<table>
<tr>
<td>
    여보게의 추천 모델은 Factorization Machine(FM)을 기반으로 구현 되었습니다.
</td>
</tr>
</table>

> Factorization Machine(FM)은 classification, regression, ranking이 가능한 general predictor이며, 특히 추천 시스템에서 대표적인 알고리즘으로 사용되고 있다. FM은 매우 희소한 데이터에서도 정확히 모델 파라미터를 추정할 수 있으며, 선형 시간으로 학습이 가능한 장점을 지니고 있다. 이러한 특성으로 인해 FM은 현실에서 나타나는 추천 문제에서 이상적인 결과를 낼 수 있다. 기존 Matrix Factorization(MF)과 달리 사용자와 아이템에 대한 여러 메타 데이터를 포함한 feature vector를 통해 사용자과 아이템 간의 관계를 표현한다. 
> <br>References. [Towards Data Science](https://towardsdatascience.com/factorization-machines-for-item-recommendation-with-implicit-feedback-data-5655a7c749db#_edn1)

### Model Development & Train

[Google Colab](https://colab.research.google.com/drive/1IE0RJLiKQkDomUnRu3wzoR09N3o8e6OB?usp=sharing)

### API URL
https://iqan6y95ml.execute-api.ap-northeast-2.amazonaws.com/v1

|    기능     |      End Point      |                 Request Body                  |                                                설명                                                |
|:---------:|:-------------------:|:---------------------------------------------:|:------------------------------------------------------------------------------------------------:|
| 장르별 개인 추천 |    `/recommends`    |  ``` { "user_id": int, "genre_id": int } ```  |             `user_id`의 사용자가 `genre_id`를 가진 보드게임 중 모델이 예측한 10개의 추천 보드게임 id 목록을 생성합니다.             |
|   그룹 추천   | `/recommends/group` | ``` { "members": list[int], "seed": int } ``` | `members`에 해당하는 사용자들 별로 각각 선호할 것으로 예상되는 보드게임 목록을 생성한 뒤 가장 많은 인원의 목록에서 나타난 보드게임 id로 추천 목록을 구성합니다. |

## 🌟 Tech Stack

### Environment
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/gitlab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white"> <img src="https://img.shields.io/badge/google colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"> <img src="https://img.shields.io/badge/pycharm-000000?style=for-the-badge&logo=pycharm&logoColor=white">

### Development
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">

### DevOps
<img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/gitlab cicd-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white">
