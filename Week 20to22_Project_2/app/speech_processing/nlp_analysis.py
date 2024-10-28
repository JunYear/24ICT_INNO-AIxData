import spacy

# 한국어 모델 로드 (설치 필요)
# python -m spacy download ko_core_news_sm
nlp = spacy.load('ko_core_news_sm')

def analyze_text(text):
    doc = nlp(text)
    feedback = {}

    # 문장 수
    sentences = list(doc.sents)
    feedback['sentence_count'] = len(sentences)

    # 단어 수
    feedback['word_count'] = len([token for token in doc if not token.is_punct])

    # 키워드 추출 (명사)
    keywords = [token.text for token in doc if token.pos_ == 'NOUN' and not token.is_stop]
    feedback['keywords'] = list(set(keywords))

    # 감정 분석 또는 추가적인 분석 가능

    # 예시 피드백 생성
    feedback['summary'] = "전반적으로 답변이 명확하며 주요 키워드를 잘 포함하고 있습니다."

    return feedback
